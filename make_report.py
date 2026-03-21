#!/usr/bin/env python3
"""
Generates a static HTML benchmark report using staticdash.Dashboard and Plotly.
Scans output/*.csv and matching .json for metadata, separates sections by platform/CPU.
"""

import os
import glob
import json
import re
from pathlib import Path
import datetime
import pandas as pd
from plotly import graph_objs as go
from staticdash import Dashboard, Page

OUTPUT_DIR = Path("output")
REPORT_DIR = Path("docs")
REPORT_DIR.mkdir(exist_ok=True)


class Benchmark:
    def __init__(self, meta, df):
        self.meta = meta
        self.df = df

        min_param = None
        max_param = None

        for line in self.df["command"]:
            param = int(line.split()[-1])

            if min_param is None or param < min_param:
                min_param = param

            if max_param is None or param > max_param:
                max_param = param

        self.param_range = (min_param, max_param)

        # Ensure parameter_size column is present
        if "parameter_size" not in self.df.columns and "command" in self.df.columns:

            def extract_param(cmd):
                ms = re.findall(r"\b(\d+)\b", str(cmd))
                return int(ms[-1]) if ms else None

            self.df["parameter_size"] = self.df["command"].apply(extract_param)
        if "impl" not in self.df:
            self.df["impl"] = self.df["command"].apply(lambda x: x.split()[1])

    @property
    def platform(self):
        return self.meta.get("platform", "Unknown")

    @property
    def cpu(self):
        return self.meta.get("cpu_model", "Unknown")

    @property
    def timestamp(self):
        iso_str = self.meta.get("timestamp")
        dt = datetime.datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M")


def load_benchmarks(output_dir=OUTPUT_DIR):
    benchmarks = []

    for csv_path in glob.glob(str(output_dir / "*.csv")):
        base = os.path.splitext(csv_path)[0]
        json_path = base + ".json"

        if not Path(json_path).exists():
            continue

        with open(json_path) as f:
            meta = json.load(f)

        df = pd.read_csv(csv_path)
        benchmarks.append(Benchmark(meta, df))
    return benchmarks


def generate_plotly_figure_for_benchmark(benchmark):
    fig = go.Figure()
    for impl in sorted(benchmark.df["impl"].unique()):
        sub = benchmark.df[benchmark.df["impl"] == impl]
        fig.add_trace(
            go.Scatter(
                x=sub["parameter_size"],
                y=sub["mean"],
                mode="lines+markers",
                error_y=dict(array=sub["stddev"], visible=True),
                name=impl.capitalize(),
            )
        )
    fig.update_layout(
        xaxis_title="List Size",
        yaxis_title="Mean Time (s)",
        legend_title="Implementation",
        hovermode="x unified",
    )
    return fig


def group_benchmarks(benchmarks):
    # cpu_type => list of benchmarks
    group = {}

    for benchmark in benchmarks:
        cpu_type = (benchmark.platform, benchmark.cpu)
        if cpu_type not in group:
            group[cpu_type] = {}

        param_range = benchmark.param_range

        if param_range not in group[cpu_type]:
            group[cpu_type][param_range] = []

        group[cpu_type][param_range].append(benchmark)

    for cpu_type in group:
        for param_range in group[cpu_type]:
            group[cpu_type][param_range].sort(key=lambda b: b.timestamp)

    return group


def main():
    benchmarks = load_benchmarks()
    range_groups = group_benchmarks(benchmarks)

    db = Dashboard(title="Benchamrk Results")

    for cpu_type, range_group in range_groups.items():
        page_title = f"{cpu_type[0]}: {cpu_type[1]}"
        page_slug = f"param_{cpu_type}"

        page = Page(page_slug, page_title)

        for rng, benchmarks in range_group.items():
            for bench in benchmarks:
                bench_title = f"**Parameter Range**: {rng[0]}–{rng[1]}"
                bench_title += f", **Timestamp:** {bench.timestamp}"

                page.add_text(bench_title)
                fig = generate_plotly_figure_for_benchmark(bench)
                page.add_plot(fig, height=400, width=800)

        db.add_page(page)
    db.publish(output_dir=REPORT_DIR)


if __name__ == "__main__":
    main()
