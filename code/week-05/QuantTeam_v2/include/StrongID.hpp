#pragma once

#include <cstdint>
#include <functional>

/**
 * 强类型 ID 模板 - 类型安全的 ID 系统
 * 使用 Tag 类型区分不同的 ID 类型，防止混淆
 */
template<typename Tag, typename ValueType = uint64_t>
class StrongID {
private:
    ValueType value;

public:
    // 只能显式构造
    constexpr explicit StrongID(ValueType val = 0) noexcept : value(val) {}

    constexpr ValueType get() const noexcept { return value; }
    constexpr bool is_valid() const noexcept { return value != 0; }

    // 比较运算符 (C++20)
    constexpr bool operator==(const StrongID& other) const noexcept = default;
    constexpr bool operator!=(const StrongID& other) const noexcept = default;
    constexpr bool operator<(const StrongID& other) const noexcept {
        return value < other.value;
    }

    // 支持哈希，可用于 unordered_map
    struct Hash {
        size_t operator()(const StrongID& id) const noexcept {
            return std::hash<ValueType>{}(id.value);
        }
    };
};

// 定义不同类型的 ID Tag
struct EmployeeTag {};
struct OrderTag {};
struct StrategyTag {};

// 具体的 ID 类型
using EmployeeID = StrongID<EmployeeTag>;
using OrderID = StrongID<OrderTag>;
using StrategyID = StrongID<StrategyTag>;
