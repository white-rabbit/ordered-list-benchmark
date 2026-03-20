#pragma once

#include <vector>

#include "sorted_list_base.h"

class SortedListBinarySearch : public SortedListBase<SortedListBinarySearch> {
public:
    SortedListBinarySearch(int size) : maxSize_(size), curSize_(0), data_(size, -1) {}
    friend class SortedListBase<SortedListBinarySearch>;

private:
    void add_impl(int n) {
        auto it = std::lower_bound(data_.begin(), data_.end(), n,
                                   std::greater<int>());

        if (it == data_.end()) {
            return;
        }

        int insert_pos = std::distance(data_.begin(), it);

        if (data_[insert_pos] == n) {
            return;
        }

        shift_forward(insert_pos);

        data_[insert_pos] = n;

        ++curSize_;
    }

    void remove_impl(int n) {
        auto it = std::lower_bound(data_.begin(), data_.end(), n,
                                   std::greater<int>());

        if (n != *it) {
            return;
        }

        int pos = std::distance(data_.begin(), it);

        shift_backward(pos);

        --curSize_;
    }

    inline void shift_forward(int pos) {
        std::memmove(&data_[pos + 1], &data_[pos],
                     (maxSize_ - pos - 1) * sizeof(int));
    }

    inline void shift_backward(int pos) {
        std::memmove(&data_[pos], &data_[pos + 1],
                     (maxSize_ - pos - 1) * sizeof(int));
        data_[maxSize_ - 1] = -1;
    }

    // Iterator support - delegates to derived class implementations
    auto begin_impl() { return data_.begin(); }
    auto end_impl() { return data_.begin() + curSize_; }

    auto cbegin_impl() const { return data_.cbegin(); }
    auto cend_impl() const { return data_.cbegin() + curSize_; }

    auto begin_impl() const { return data_.begin(); }
    auto end_impl() const { return data_.begin() + curSize_; }

    // Data
    size_t maxSize_;
    size_t curSize_;

    std::vector<int> data_;
};
