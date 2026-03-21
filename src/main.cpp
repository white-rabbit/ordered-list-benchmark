#include <cassert>
#include <print>

#include "sorted_list_arr_bin.h"
#include "sorted_list_arr_naive.h"
#include "sorted_list_set.h"

template <typename T> void assert_sorted(const T &list) {
    auto it = list.cbegin();
    auto prev = *it;

    for (++it; it != list.cend(); ++it) {
        assert(prev >= *it);
        prev = *it;
    }
}

template <typename T> void print_list(const T &list) {
    for (const auto &item : list) {
        std::print("{} ", item);
    }
    std::println("");
}

template <typename T>
void simulate(T &list, int size, int updateCount, int maxValue) {
    // randomize
    std::srand(clock());

    for (int i = 0; i < updateCount; ++i) {
        auto number = std::rand() % maxValue;
        list.add(number);

        if (i > size) {
            auto to_remove = std::rand() % maxValue;
            list.remove(to_remove);
        }
    }

    assert_sorted(list);

    print_list(list);
}

int main(int argc, char **argv) {
    if (argc != 3) {
        std::println("Please provide the struct type (array, or set) and its "
                     "size(integer).");
        return 1;
    }

    int size = -1;
    int updateCount = 1'000'000;

    std::string structType = argv[1];
    size = std::atoi(argv[2]);

    if (structType != "array" && structType != "set" &&
        structType != "binary" && structType != "all") {
        std::println("Invalid struct type. Please choose 'array' or 'set'.");
        return 1;
    }

    // simply use maxValue equal to size
    // so deletion from the array happens
    // regularly
    int maxValue = size;

    if (structType == "array") {
        auto naive = SortedListNaive(size);
        simulate(naive, size, updateCount, maxValue);
    } else if (structType == "binary") {
        auto binary = SortedListBinarySearch(size);
        simulate(binary, size, updateCount, maxValue);
    } else if (structType == "set") {
        auto tree = SortedListSet(size);
        simulate(tree, size, updateCount, maxValue);
    } else {
        assert(false);
    }

    return 0;
}
