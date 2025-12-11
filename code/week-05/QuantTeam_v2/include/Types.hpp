#pragma once

#include <string>

// 员工等级枚举
enum class EmployeeLevel {
    JUNIOR,
    SENIOR,
    PRINCIPAL,
    DIRECTOR
};

// 员工类型枚举
enum class EmployeeType {
    QUANT_RESEARCHER,
    QUANT_DEVELOPER,
    TRADER,
    RISK_MANAGER
};

// 辅助函数
inline std::string level_to_string(EmployeeLevel level) {
    switch (level) {
        case EmployeeLevel::JUNIOR: return "Junior";
        case EmployeeLevel::SENIOR: return "Senior";
        case EmployeeLevel::PRINCIPAL: return "Principal";
        case EmployeeLevel::DIRECTOR: return "Director";
    }
    return "Unknown";
}
