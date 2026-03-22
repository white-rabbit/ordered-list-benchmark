# Sorted List Performance

This is a small test to compare three different approaches
for maintaining a sorted list of integers. The main feature
is the dynamic nature of the list, as constant elements
addition and removal is expected.


## Three Implementations Compared

1. **Array-based (Naive)**: Linear search with manual element shifting using `std::vector`
   - Operations: O(n) insertion and deletion
   - Simple implementation, efficient for small lists

2. **Binary Search**: Binary search for insertion point with `std::vector` and `std::lower_bound`
   - Operations: O(n) due to shifting, but faster search phase
   - Better than naive for larger lists

3. **Tree-based (std::set)**: Self-balancing BST using `std::set`
   - Operations: O(log n) insertion and deletion
   - Higher overhead per operation, but best scaling for large lists

## Building the Project

### Requirements
- C++23 compatible compiler (clang, g++, or MSVC)
- CMake 3.15+
- Python 3 (for visualization)

### Build Steps

```bash
# Create and enter build directory
mkdir -p build
cd build

# Configure with CMake
cmake ..

# Compile (Linux/Mac)
make

# Compile (Windows)
cmake --build .

# The executable 'sortedlist' will be created in the build directory
```

### Python Scripts and Environment

Python scripts are used for running and visualizing benchmarks and generating
summary reports. It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows:
```bash
python3 -m venv venv
venv\Scripts\activate
python3 -m pip install -r requirements.txt
```


Additionally, the `hyperfine` tool is required for benchmarking.

```bash
brew install hyperfine
```

on Windows can be installed with ```scoop``` or any other package manager:

```bash
scoop install hyperfine
```


## Running Benchmarks

**Python script**: Use `benchmark.py` to customize parameter ranges.:
    ```bash
    python benchmark.py --min 10 --max 1000
    ```
    This will run all implementations over a set of 10 datapoints across your specified parameter range.

The benchmarking system will store output in timestamped files in the `output/` directory, so previous results are preserved.

## Report Generation

After running benchmarks, generate interactive HTML reports using the `make_report.py`. Reports group and visualize benchmark results by platform/CPU, parameter range, and implementation. The staticdash report uses Plotly for interactive visualization and organizes results by size range, date, and machine.

All reports are generated in the `docs/` directory for review and sharing.
