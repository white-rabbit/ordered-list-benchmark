#pragma once

#include <vector>

#include "sorted_list_base.h"

class SortedListNaive : public SortedListBase<SortedListNaive> {
public:
    SortedListNaive(int size) : maxSize_(size), curSize_(0), data_(size, -1) {}
    friend class SortedListBase<SortedListNaive>;

private:
    void add_impl(int n) {
        int insert_pos = -1;

        for (int i = 0; i < maxSize_; ++i) {
            if (data_[i] == -1 || data_[i] <= n) {
                insert_pos = i;
                break;
            }
        }

        if (insert_pos == -1 || data_[insert_pos] == n) {
            return;
        }

        shift_forward(insert_pos);

        data_[insert_pos] = n;
        ++curSize_;
    }

    void remove_impl(int n) {
        int pos = -1;

        for (int i = 0; i < maxSize_; ++i) {
            if (data_[i] <= n) {
                pos = (data_[i] == n) ? i : -1;
                break;
            }
        }

        if (pos == -1) {
            return;
        }

        --curSize_;
        shift_backward(pos);
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
