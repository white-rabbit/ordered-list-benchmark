#pragma once

#include <set>

#include "sorted_list_base.h"

class SortedListSet : public SortedListBase<SortedListSet> {
public:
    SortedListSet(size_t size) : maxSize_(size) {}
    friend class SortedListBase<SortedListSet>;

private:
    void add_impl(int n) {
        data_.insert(n);
        if (data_.size() > maxSize_) {
            data_.erase(data_.begin());
        }
    }

    void remove_impl(int n) {
        auto it = data_.find(n);
        if (it != data_.end()) {
            data_.erase(it);
        }
    }

    // Iterator support - delegates to derived class implementations
    auto begin_impl() { return data_.rbegin(); }
    auto end_impl() { return data_.rend(); }

    auto cbegin_impl() const { return data_.crbegin(); }
    auto cend_impl() const { return data_.crend(); }

    auto begin_impl() const { return data_.rbegin(); }
    auto end_impl() const { return data_.rend(); }

    // Data
    std::set<int> data_;
    size_t maxSize_;
};
