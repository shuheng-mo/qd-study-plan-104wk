#pragma once

#include <stdexcept>
#include <string>

// 自定义异常类层次结构
class QuantTeamException : public std::exception
{
protected:
    std::string message;

public:
    explicit QuantTeamException(const std::string &msg) : message(msg) {}
    const char *what() const noexcept override { return message.c_str(); }
};

class InsufficientFundsException : public QuantTeamException
{
public:
    explicit InsufficientFundsException(const std::string &msg)
        : QuantTeamException("资金不足: " + msg) {}
};

class RiskLimitExceededException : public QuantTeamException
{
public:
    explicit RiskLimitExceededException(const std::string &msg)
        : QuantTeamException("风险限制超出: " + msg) {}
};

class ComplianceViolationException : public QuantTeamException
{
public:
    explicit ComplianceViolationException(const std::string &msg)
        : QuantTeamException("合规违规: " + msg) {}
};

class SystemOverloadException : public QuantTeamException
{
public:
    explicit SystemOverloadException(const std::string &msg)
        : QuantTeamException("系统过载: " + msg) {}
};