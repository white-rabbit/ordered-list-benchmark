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

# Compile
make

# The executable 'sortedlist' will be created in the build directory
```

## Running Benchmarks

```bash
# Test with specific implementation and parameter size
./sortedlist array 100      # Test naive array approach with 100 elements
./sortedlist binary 100     # Test binary search approach with 100 elements
./sortedlist set 100        # Test std::set approach with 100 elements
```
