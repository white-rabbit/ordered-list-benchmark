#pragma once

template <typename Derived> class SortedListBase {
public:
    void add(int n) { static_cast<Derived *>(this)->add_impl(n); }

    void remove(int n) { static_cast<Derived *>(this)->remove_impl(n); }

    // Iterator support - delegates to derived class implementations
    auto begin() { return static_cast<Derived *>(this)->begin_impl(); }
    auto end() { return static_cast<Derived *>(this)->end_impl(); }

    auto cbegin() const {
        return static_cast<const Derived *>(this)->cbegin_impl();
    }
    auto cend() const {
        return static_cast<const Derived *>(this)->cend_impl();
    }

    auto begin() const {
        return static_cast<const Derived *>(this)->cbegin_impl();
    }
    auto end() const { return static_cast<const Derived *>(this)->cend_impl(); }
};
