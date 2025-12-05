#pragma once

#include <memory>
#include <string>

// 策略模式 - 工作策略接口
class WorkStrategy
{
public:
    virtual ~WorkStrategy() = default;
    virtual void execute(const std::string &employee_name) const = 0;
    virtual std::string get_strategy_name() const = 0;
};

// 具体策略实现
class ResearchStrategy : public WorkStrategy
{
public:
    void execute(const std::string &employee_name) const override;
    std::string get_strategy_name() const override { return "Research Strategy"; }
};

class DevelopmentStrategy : public WorkStrategy
{
public:
    void execute(const std::string &employee_name) const override;
    std::string get_strategy_name() const override { return "Development Strategy"; }
};

class TradingStrategy : public WorkStrategy
{
public:
    void execute(const std::string &employee_name) const override;
    std::string get_strategy_name() const override { return "Trading Strategy"; }
};

class RiskManagementStrategy : public WorkStrategy
{
public:
    void execute(const std::string &employee_name) const override;
    std::string get_strategy_name() const override { return "Risk Management Strategy"; }
};

class DataAnalysisStrategy : public WorkStrategy
{
public:
    void execute(const std::string &employee_name) const override;
    std::string get_strategy_name() const override { return "Data Analysis Strategy"; }
};

class ComplianceStrategy : public WorkStrategy
{
public:
    void execute(const std::string &employee_name) const override;
    std::string get_strategy_name() const override { return "Compliance Strategy"; }
};