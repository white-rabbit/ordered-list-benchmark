#!/usr/bin/env python3
"""
Benchmarking script for sorted list implementations.

- Detects platform and CPU information
- Runs hyperfine benchmarks for all three implementations (array, binary, set)
- Creates metadata JSON file with platform information

Usage:
    python3 benchmark.py --min 10 --max 100
"""

import argparse
import platform
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime


# Configuration
BINARY_NAME = "sortedlist"
BUILD_DIR = Path("build")
IMPLEMENTATIONS = ["array", "binary", "set"]
DEFAULT_RUNS = 40
DEFAULT_WARMUP = 5


def get_platform_data():
    system = platform.system()  # 'Darwin', 'Linux', 'Windows'
    processor = platform.processor()

    # Get CPU model
    cpu_model = get_cpu_model(system)

    return {
        "platform": system,
        "processor": processor,
        "cpu_model": cpu_model,
        "platform_release": platform.release(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat(),
    }


def get_cpu_model(system):
    """Get CPU model for the current system"""
    try:
        if system == "Darwin":  # macOS
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout.strip()

        elif system == "Linux":
            # Try lscpu first (more reliable)
            try:
                result = subprocess.run(
                    ["lscpu"], capture_output=True, text=True, timeout=5
                )
                for line in result.stdout.split("\n"):
                    if line.startswith("Model name:"):
                        return line.split(":", 1)[1].strip()
            except FileNotFoundError:
                pass

            # Fallback to /proc/cpuinfo
            result = subprocess.run(
                ["cat", "/proc/cpuinfo"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "model name" in line:
                    return line.split(":", 1)[1].strip()

        elif system == "Windows":
            try:
                result = subprocess.run(
                    ["wmic", "cpu", "get", "name"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    return lines[1].strip()
            except FileNotFoundError:
                pass

    except Exception as e:
        print(f"Warning: Could not get CPU model: {e}", file=sys.stderr)

    return platform.processor() or "Unknown"


def sanitize_filename(text):
    # Remove/replace problematic characters
    replacements = {
        " ": "_",
        ".": "_",
        "(": "",
        ")": "",
        "/": "_",
        "\\": "_",
        ":": "",
        "*": "",
        "?": "",
        '"': "",
        "<": "",
        ">": "",
        "|": "",
        "@": "",
    }
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    return result


def generate_filename(platform_data, output_dir="output/"):
    system = platform_data["platform"]
    cpu = sanitize_filename(platform_data["cpu_model"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"benchmark_{system}_{cpu}_{timestamp}"
    filepath = Path(output_dir) / filename

    return filepath


def build_benchmark_commands(parameter_sizes):
    """Build list of hyperfine commands for all implementations and parameter sizes"""
    commands = []

    for impl in IMPLEMENTATIONS:
        for param_size in parameter_sizes:
            binary_path = BUILD_DIR / BINARY_NAME
            cmd = f"{binary_path} {impl} {param_size}"
            commands.append(cmd)

    return commands


def main():
    parser = argparse.ArgumentParser(
        description="Run benchmarks for sorted list implementations."
    )
    parser.add_argument("--min", type=int, required=True, help="Minimum parameter size")
    parser.add_argument("--max", type=int, required=True, help="Maximum parameter size")
    parser.add_argument(
        "--count",
        type=int,
        required=False,
        default=10,
        help="Data points count between min and max",
    )
    args = parser.parse_args()

    min_size = args.min
    max_size = args.max

    if min_size >= max_size:
        print("Error: min must be less than max")
        sys.exit(1)

    count = args.count
    if count < 2:
        print("Error: count must be at least 2")
        sys.exit(1)

    step = (max_size - min_size) // (count - 1)
    parameter_sizes = [min_size + step * i for i in range(count - 1)] + [max_size]

    # Get platform data
    print("Detecting platform information...")
    platform_data = get_platform_data()

    print(f"  Platform: {platform_data['platform']}")
    print(f"  CPU Model: {platform_data['cpu_model']}")
    print(f"  Release: {platform_data['platform_release']}")

    # Verify binary exists
    binary_path = BUILD_DIR / BINARY_NAME
    if not binary_path.exists():
        print(f"\n✗ Error: Binary not found at {binary_path}")
        print("  Please build the project first:")
        print("  cd build && cmake .. && make")
        sys.exit(1)

    # Generate filename
    base_filepath = generate_filename(platform_data)
    csv_file = base_filepath.with_suffix(".csv")
    json_file = base_filepath.with_suffix(".json")

    # Save metadata
    print("\nSaving platform metadata...")
    with open(json_file, "w") as f:
        json.dump(platform_data, f, indent=2)
    print(f"  Metadata: {json_file}")
    print(f"  CSV output: {csv_file}")

    # Build benchmark commands
    benchmark_commands = build_benchmark_commands(parameter_sizes)

    print(
        f"\nBenchmarking {len(IMPLEMENTATIONS)} implementations × {len(parameter_sizes)} parameter sizes"
    )
    print(f"  Implementations: {', '.join(IMPLEMENTATIONS)}")
    print(f"  Parameter sizes: {parameter_sizes[0]}...{parameter_sizes[-1]}")
    print(f"  Runs per command: {DEFAULT_RUNS}")
    print(f"  Warmup: {DEFAULT_WARMUP}")

    # Build hyperfine command
    hyperfine_cmd = [
        "hyperfine",
        f"--runs={DEFAULT_RUNS}",
        f"--warmup={DEFAULT_WARMUP}",
        "--export-csv",
        str(csv_file),
    ] + benchmark_commands

    # Run hyperfine
    print("\nRunning benchmarks...")
    print(f"Total commands to run: {len(benchmark_commands)}")
    print()

    try:
        result = subprocess.run(hyperfine_cmd)

        if result.returncode == 0:
            print(f"\n{'=' * 60}")
            print("✓ Benchmark completed successfully!")
            print(f"  Data: {csv_file}")
            print(f"  Metadata: {json_file}")
            print(f"{'=' * 60}")
        else:
            print(f"\n✗ Hyperfine failed with return code: {result.returncode}")
            sys.exit(result.returncode)

    except FileNotFoundError:
        print("✗ Error: hyperfine not found. Please install it first.")
        print("  Installation: https://github.com/sharkdp/hyperfine#installation")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
