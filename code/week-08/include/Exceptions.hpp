#pragma once

#include <exception>
#include <string>
#include <format>
#include <source_location>

/**
 * Week 8 - 异常层次结构
 *
 * 本文件演示了如何构建完善的异常层次结构：
 * 1. 基础异常类 QuantTeamException
 * 2. 数据相关异常 DataException
 * 3. 业务逻辑异常 BusinessException
 * 4. 系统异常 SystemException
 * 5. 使用 std::source_location 记录异常位置
 */

// ============================================================================
// 基础异常类 - 所有自定义异常的基类
// ============================================================================

class QuantTeamException : public std::exception {
protected:
    std::string message;
    std::source_location location;
    mutable std::string full_message;  // mutable 允许在 const 函数中修改

    void build_message() const {
        full_message = std::format(
            "[{}:{}:{}] {}: {}",
            location.file_name(),
            location.line(),
            location.column(),
            get_exception_type(),
            message
        );
    }

    virtual std::string get_exception_type() const {
        return "QuantTeamException";
    }

public:
    explicit QuantTeamException(
        std::string msg,
        std::source_location loc = std::source_location::current())
        : message(std::move(msg))
        , location(loc) {
        build_message();
    }

    const char* what() const noexcept override {
        return full_message.c_str();
    }

    const std::source_location& where() const noexcept {
        return location;
    }

    const std::string& get_message() const noexcept {
        return message;
    }
};

// ============================================================================
// 数据异常 - 文件IO、序列化等数据操作相关异常
// ============================================================================

class DataException : public QuantTeamException {
protected:
    std::string get_exception_type() const override {
        return "DataException";
    }

public:
    using QuantTeamException::QuantTeamException;
};

// 文件未找到异常
class FileNotFoundException : public DataException {
protected:
    std::string get_exception_type() const override {
        return "FileNotFoundException";
    }

public:
    using DataException::DataException;
};

// 序列化异常
class SerializationException : public DataException {
protected:
    std::string get_exception_type() const override {
        return "SerializationException";
    }

public:
    using DataException::DataException;
};

// 反序列化异常
class DeserializationException : public DataException {
protected:
    std::string get_exception_type() const override {
        return "DeserializationException";
    }

public:
    using DataException::DataException;
};

// 文件格式错误异常
class InvalidFormatException : public DataException {
protected:
    std::string get_exception_type() const override {
        return "InvalidFormatException";
    }

public:
    using DataException::DataException;
};

// ============================================================================
// 业务逻辑异常 - 业务规则违反相关异常
// ============================================================================

class BusinessException : public QuantTeamException {
protected:
    std::string get_exception_type() const override {
        return "BusinessException";
    }

public:
    using QuantTeamException::QuantTeamException;
};

// 无效员工异常
class InvalidEmployeeException : public BusinessException {
protected:
    std::string get_exception_type() const override {
        return "InvalidEmployeeException";
    }

public:
    using BusinessException::BusinessException;
};

// 资金不足异常
class InsufficientFundsException : public BusinessException {
protected:
    std::string get_exception_type() const override {
        return "InsufficientFundsException";
    }

public:
    using BusinessException::BusinessException;
};

// 重复员工异常
class DuplicateEmployeeException : public BusinessException {
protected:
    std::string get_exception_type() const override {
        return "DuplicateEmployeeException";
    }

public:
    using BusinessException::BusinessException;
};

// 策略执行失败异常
class StrategyExecutionException : public BusinessException {
protected:
    std::string get_exception_type() const override {
        return "StrategyExecutionException";
    }

public:
    using BusinessException::BusinessException;
};

// 无效交易异常
class InvalidTradeException : public BusinessException {
protected:
    std::string get_exception_type() const override {
        return "InvalidTradeException";
    }

public:
    using BusinessException::BusinessException;
};

// ============================================================================
// 系统异常 - 系统级错误
// ============================================================================

class SystemException : public QuantTeamException {
protected:
    std::string get_exception_type() const override {
        return "SystemException";
    }

public:
    using QuantTeamException::QuantTeamException;
};

// 配置错误异常
class ConfigurationException : public SystemException {
protected:
    std::string get_exception_type() const override {
        return "ConfigurationException";
    }

public:
    using SystemException::SystemException;
};

// 资源耗尽异常
class ResourceExhaustedException : public SystemException {
protected:
    std::string get_exception_type() const override {
        return "ResourceExhaustedException";
    }

public:
    using SystemException::SystemException;
};

// 网络异常
class NetworkException : public SystemException {
protected:
    std::string get_exception_type() const override {
        return "NetworkException";
    }

public:
    using SystemException::SystemException;
};

// ============================================================================
// 异常处理工具函数
// ============================================================================

namespace ExceptionUtils {
    // 递归打印嵌套异常
    inline void print_exception(const std::exception& e, int level = 0) {
        std::string indent(level * 2, ' ');
        std::cerr << indent << "Exception: " << e.what() << '\n';

        try {
            std::rethrow_if_nested(e);
        } catch (const std::exception& nested) {
            print_exception(nested, level + 1);
        } catch (...) {
            std::cerr << indent << "  Unknown nested exception\n";
        }
    }

    // 获取异常的简短描述
    inline std::string get_short_description(const std::exception& e) {
        if (const auto* qte = dynamic_cast<const QuantTeamException*>(&e)) {
            return qte->get_message();
        }
        return e.what();
    }
}
