#pragma once

#include <string>
#include <cstdint>

// 员工级别
enum class EmployeeLevel
{
    JUNIOR,
    SENIOR,
    LEAD,
    PRINCIPAL
};

// 市场数据（用于策略测试）
struct MarketData
{
    std::string symbol;
    double price;
    double volume;
    uint64_t timestamp;

    MarketData(std::string sym, double p, double v = 0.0, uint64_t ts = 0)
        : symbol(std::move(sym)), price(p), volume(v), timestamp(ts) {}
};

// 辅助函数 - 级别转字符串
inline std::string level_to_string(EmployeeLevel level)
{
    switch (level)
    {
    case EmployeeLevel::JUNIOR:
        return "Junior";
    case EmployeeLevel::SENIOR:
        return "Senior";
    case EmployeeLevel::LEAD:
        return "Lead";
    case EmployeeLevel::PRINCIPAL:
        return "Principal";
    default:
        return "Unknown";
    }
}
