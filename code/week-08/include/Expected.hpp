#pragma once

#include <variant>
#include <stdexcept>
#include <type_traits>
#include <utility>
#include <functional>

/**
 * Week 8 - Expected<T, E> - 函数式错误处理
 *
 * 这是一个简化版的 std::expected (C++23)
 * 提供零开销的错误处理，替代异常
 *
 * 特点：
 * 1. 要么包含值 (T)，要么包含错误 (E)
 * 2. 显式的错误处理，编译期检查
 * 3. 支持函数式操作：and_then, or_else, transform
 * 4. 零开销（相比异常）
 */

// ============================================================================
// Unexpected - 表示错误值
// ============================================================================

template<typename E>
class Unexpected {
private:
    E error;

public:
    explicit Unexpected(E err) : error(std::move(err)) {}

    const E& value() const& { return error; }
    E& value() & { return error; }
    E&& value() && { return std::move(error); }
};

// 辅助函数 - 创建 Unexpected
template<typename E>
Unexpected<E> make_unexpected(E error) {
    return Unexpected<E>(std::move(error));
}

// ============================================================================
// Expected<T, E> - 主模板
// ============================================================================

template<typename T, typename E>
class Expected {
private:
    std::variant<T, E> data;

public:
    // 构造函数 - 从值构造
    Expected(const T& value) : data(value) {}
    Expected(T&& value) : data(std::move(value)) {}

    // 构造函数 - 从错误构造
    Expected(const Unexpected<E>& unex) : data(unex.value()) {}
    Expected(Unexpected<E>&& unex) : data(std::move(unex.value())) {}

    // 检查是否包含值
    bool has_value() const noexcept {
        return std::holds_alternative<T>(data);
    }

    explicit operator bool() const noexcept {
        return has_value();
    }

    // 访问值（如果包含错误则抛异常）
    T& value() & {
        if (!has_value()) {
            throw std::runtime_error("Expected contains error, not value");
        }
        return std::get<T>(data);
    }

    const T& value() const& {
        if (!has_value()) {
            throw std::runtime_error("Expected contains error, not value");
        }
        return std::get<T>(data);
    }

    T&& value() && {
        if (!has_value()) {
            throw std::runtime_error("Expected contains error, not value");
        }
        return std::move(std::get<T>(data));
    }

    // 访问错误
    E& error() & {
        if (has_value()) {
            throw std::runtime_error("Expected contains value, not error");
        }
        return std::get<E>(data);
    }

    const E& error() const& {
        if (has_value()) {
            throw std::runtime_error("Expected contains value, not error");
        }
        return std::get<E>(data);
    }

    E&& error() && {
        if (has_value()) {
            throw std::runtime_error("Expected contains value, not error");
        }
        return std::move(std::get<E>(data));
    }

    // 访问值（使用 * 和 ->）
    T& operator*() & {
        return std::get<T>(data);
    }

    const T& operator*() const& {
        return std::get<T>(data);
    }

    T&& operator*() && {
        return std::move(std::get<T>(data));
    }

    T* operator->() {
        return &std::get<T>(data);
    }

    const T* operator->() const {
        return &std::get<T>(data);
    }

    // value_or - 如果有错误则返回默认值
    template<typename U>
    T value_or(U&& default_value) const& {
        return has_value() ? std::get<T>(data) : static_cast<T>(std::forward<U>(default_value));
    }

    template<typename U>
    T value_or(U&& default_value) && {
        return has_value() ? std::move(std::get<T>(data)) : static_cast<T>(std::forward<U>(default_value));
    }

    // and_then - 如果包含值，则应用函数并返回新的 Expected
    template<typename Func>
    auto and_then(Func&& func) & -> decltype(func(std::declval<T&>())) {
        using Result = decltype(func(std::declval<T&>()));
        if (has_value()) {
            return func(std::get<T>(data));
        } else {
            return Result(Unexpected<E>(std::get<E>(data)));
        }
    }

    template<typename Func>
    auto and_then(Func&& func) const& -> decltype(func(std::declval<const T&>())) {
        using Result = decltype(func(std::declval<const T&>()));
        if (has_value()) {
            return func(std::get<T>(data));
        } else {
            return Result(Unexpected<E>(std::get<E>(data)));
        }
    }

    template<typename Func>
    auto and_then(Func&& func) && -> decltype(func(std::declval<T&&>())) {
        using Result = decltype(func(std::declval<T&&>()));
        if (has_value()) {
            return func(std::move(std::get<T>(data)));
        } else {
            return Result(Unexpected<E>(std::move(std::get<E>(data))));
        }
    }

    // or_else - 如果包含错误，则应用函数
    template<typename Func>
    auto or_else(Func&& func) & -> Expected<T, E> {
        if (has_value()) {
            return *this;
        } else {
            func(std::get<E>(data));
            return *this;
        }
    }

    template<typename Func>
    auto or_else(Func&& func) const& -> Expected<T, E> {
        if (has_value()) {
            return *this;
        } else {
            func(std::get<E>(data));
            return *this;
        }
    }

    // transform - 如果包含值，则转换值
    template<typename Func>
    auto transform(Func&& func) & -> Expected<decltype(func(std::declval<T&>())), E> {
        using U = decltype(func(std::declval<T&>()));
        if (has_value()) {
            return Expected<U, E>(func(std::get<T>(data)));
        } else {
            return Expected<U, E>(Unexpected<E>(std::get<E>(data)));
        }
    }

    template<typename Func>
    auto transform(Func&& func) const& -> Expected<decltype(func(std::declval<const T&>())), E> {
        using U = decltype(func(std::declval<const T&>()));
        if (has_value()) {
            return Expected<U, E>(func(std::get<T>(data)));
        } else {
            return Expected<U, E>(Unexpected<E>(std::get<E>(data)));
        }
    }
};

// ============================================================================
// Expected<void, E> - void 特化
// ============================================================================

template<typename E>
class Expected<void, E> {
private:
    std::variant<std::monostate, E> data;

public:
    // 构造函数 - 成功（无值）
    Expected() : data(std::monostate{}) {}

    // 构造函数 - 从错误构造
    Expected(const Unexpected<E>& unex) : data(unex.value()) {}
    Expected(Unexpected<E>&& unex) : data(std::move(unex.value())) {}

    // 检查是否成功
    bool has_value() const noexcept {
        return std::holds_alternative<std::monostate>(data);
    }

    explicit operator bool() const noexcept {
        return has_value();
    }

    // 访问错误
    E& error() & {
        if (has_value()) {
            throw std::runtime_error("Expected contains value, not error");
        }
        return std::get<E>(data);
    }

    const E& error() const& {
        if (has_value()) {
            throw std::runtime_error("Expected contains value, not error");
        }
        return std::get<E>(data);
    }

    // or_else - 如果包含错误，则应用函数
    template<typename Func>
    auto or_else(Func&& func) & -> Expected<void, E> {
        if (!has_value()) {
            func(std::get<E>(data));
        }
        return *this;
    }
};

// ============================================================================
// 辅助函数和工具
// ============================================================================

namespace ExpectedUtils {
    // 创建成功的 Expected
    template<typename T, typename E>
    Expected<T, E> make_expected(T value) {
        return Expected<T, E>(std::move(value));
    }

    // 创建失败的 Expected
    template<typename T, typename E>
    Expected<T, E> make_expected_error(E error) {
        return Expected<T, E>(Unexpected<E>(std::move(error)));
    }
}
