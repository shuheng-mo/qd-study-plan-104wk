#pragma once

#include <system_error>
#include <string>

/**
 * Week 8 - std::error_code 系统
 *
 * 本文件演示了如何使用 std::error_code 和自定义错误类别
 * 这是一种轻量级的错误处理机制，适合系统级错误
 *
 * 特点：
 * 1. 与标准库错误处理机制集成
 * 2. 可以与系统错误码混合使用
 * 3. 零开销（相比异常）
 * 4. 明确的错误语义
 */

// ============================================================================
// QuantTeam 错误码枚举
// ============================================================================

enum class QuantTeamError {
    SUCCESS = 0,                    // 成功（错误码为0表示成功）
    INVALID_EMPLOYEE_ID = 1,        // 无效的员工ID
    DUPLICATE_EMPLOYEE = 2,         // 重复的员工
    INSUFFICIENT_FUNDS = 3,         // 资金不足
    STRATEGY_FAILED = 4,            // 策略执行失败
    DATA_CORRUPTION = 5,            // 数据损坏
    INVALID_CONFIGURATION = 6,      // 无效配置
    NETWORK_ERROR = 7,              // 网络错误
    AUTHENTICATION_FAILED = 8,      // 认证失败
    PERMISSION_DENIED = 9,          // 权限拒绝
    RESOURCE_EXHAUSTED = 10         // 资源耗尽
};

// ============================================================================
// QuantTeam 错误类别
// ============================================================================

/**
 * 错误类别定义了错误码的语义和描述
 * 必须继承自 std::error_category
 */
class QuantTeamErrorCategory : public std::error_category {
public:
    // 类别名称
    const char* name() const noexcept override {
        return "QuantTeam";
    }

    // 错误消息
    std::string message(int ev) const override {
        switch (static_cast<QuantTeamError>(ev)) {
            case QuantTeamError::SUCCESS:
                return "Success";
            case QuantTeamError::INVALID_EMPLOYEE_ID:
                return "Invalid employee ID";
            case QuantTeamError::DUPLICATE_EMPLOYEE:
                return "Employee already exists";
            case QuantTeamError::INSUFFICIENT_FUNDS:
                return "Insufficient funds for operation";
            case QuantTeamError::STRATEGY_FAILED:
                return "Strategy execution failed";
            case QuantTeamError::DATA_CORRUPTION:
                return "Data corruption detected";
            case QuantTeamError::INVALID_CONFIGURATION:
                return "Invalid system configuration";
            case QuantTeamError::NETWORK_ERROR:
                return "Network communication error";
            case QuantTeamError::AUTHENTICATION_FAILED:
                return "Authentication failed";
            case QuantTeamError::PERMISSION_DENIED:
                return "Permission denied";
            case QuantTeamError::RESOURCE_EXHAUSTED:
                return "System resources exhausted";
            default:
                return "Unknown QuantTeam error";
        }
    }

    // 错误条件（可选，用于错误码的分类）
    std::error_condition default_error_condition(int ev) const noexcept override {
        switch (static_cast<QuantTeamError>(ev)) {
            case QuantTeamError::NETWORK_ERROR:
                return std::errc::network_unreachable;
            case QuantTeamError::PERMISSION_DENIED:
                return std::errc::permission_denied;
            case QuantTeamError::RESOURCE_EXHAUSTED:
                return std::errc::not_enough_memory;
            default:
                return std::error_condition(ev, *this);
        }
    }
};

// 全局错误类别实例
inline const QuantTeamErrorCategory& quant_team_category() {
    static QuantTeamErrorCategory instance;
    return instance;
}

// ============================================================================
// 创建 error_code 的辅助函数
// ============================================================================

inline std::error_code make_error_code(QuantTeamError e) {
    return {static_cast<int>(e), quant_team_category()};
}

// 将 QuantTeamError 注册为 error_code 枚举
namespace std {
    template<>
    struct is_error_code_enum<QuantTeamError> : true_type {};
}

// ============================================================================
// 数据加载错误枚举（另一个错误域的示例）
// ============================================================================

enum class LoadError {
    SUCCESS = 0,
    FILE_NOT_FOUND = 1,
    INVALID_FORMAT = 2,
    PERMISSION_DENIED = 3,
    CORRUPTED_DATA = 4,
    VERSION_MISMATCH = 5
};

class LoadErrorCategory : public std::error_category {
public:
    const char* name() const noexcept override {
        return "DataLoad";
    }

    std::string message(int ev) const override {
        switch (static_cast<LoadError>(ev)) {
            case LoadError::SUCCESS:
                return "Success";
            case LoadError::FILE_NOT_FOUND:
                return "File not found";
            case LoadError::INVALID_FORMAT:
                return "Invalid file format";
            case LoadError::PERMISSION_DENIED:
                return "Permission denied";
            case LoadError::CORRUPTED_DATA:
                return "Data corrupted";
            case LoadError::VERSION_MISMATCH:
                return "Version mismatch";
            default:
                return "Unknown load error";
        }
    }
};

inline const LoadErrorCategory& load_error_category() {
    static LoadErrorCategory instance;
    return instance;
}

inline std::error_code make_error_code(LoadError e) {
    return {static_cast<int>(e), load_error_category()};
}

namespace std {
    template<>
    struct is_error_code_enum<LoadError> : true_type {};
}

// ============================================================================
// 错误码工具函数
// ============================================================================

namespace ErrorCodeUtils {
    // 检查错误码是否表示成功
    inline bool is_success(const std::error_code& ec) {
        return !ec;  // error_code 为 0 表示成功
    }

    // 检查错误码是否表示失败
    inline bool is_failure(const std::error_code& ec) {
        return static_cast<bool>(ec);
    }

    // 格式化错误信息
    inline std::string format_error(const std::error_code& ec) {
        if (!ec) {
            return "Success";
        }
        return std::string(ec.category().name()) + ": " + ec.message();
    }

    // 比较两个错误码
    inline bool is_same_error(const std::error_code& ec1, const std::error_code& ec2) {
        return ec1 == ec2;
    }

    // 检查是否是特定类别的错误
    inline bool is_quant_team_error(const std::error_code& ec) {
        return ec.category() == quant_team_category();
    }

    inline bool is_load_error(const std::error_code& ec) {
        return ec.category() == load_error_category();
    }

    // 检查是否是系统错误
    inline bool is_system_error(const std::error_code& ec) {
        return ec.category() == std::system_category() ||
               ec.category() == std::generic_category();
    }
}

// ============================================================================
// 结果类型 - 结合 error_code 和返回值
// ============================================================================

/**
 * Result<T> 包装返回值和错误码
 * 类似于 Expected，但专门用于 error_code
 */
template<typename T>
struct Result {
    T value;
    std::error_code error;

    // 构造函数 - 成功
    explicit Result(T val) : value(std::move(val)), error() {}

    // 构造函数 - 失败
    explicit Result(std::error_code ec) : value{}, error(ec) {}

    // 检查是否成功
    bool is_success() const {
        return !error;
    }

    bool is_failure() const {
        return static_cast<bool>(error);
    }

    explicit operator bool() const {
        return is_success();
    }

    // 访问值（如果失败则抛异常）
    T& get() {
        if (is_failure()) {
            throw std::system_error(error);
        }
        return value;
    }

    const T& get() const {
        if (is_failure()) {
            throw std::system_error(error);
        }
        return value;
    }

    // 获取值或默认值
    T value_or(T default_value) const {
        return is_success() ? value : default_value;
    }
};

// void 特化
template<>
struct Result<void> {
    std::error_code error;

    Result() : error() {}
    explicit Result(std::error_code ec) : error(ec) {}

    bool is_success() const {
        return !error;
    }

    bool is_failure() const {
        return static_cast<bool>(error);
    }

    explicit operator bool() const {
        return is_success();
    }
};
