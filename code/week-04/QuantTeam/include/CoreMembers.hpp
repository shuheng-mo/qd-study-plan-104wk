#pragma once

#include <string>
#include <iostream>
#include <memory>
#include "Employee.hpp"
#include "WorkStrategy.hpp"

// 1. 量化研究员 (QR)
class QuantResearcher : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    QuantResearcher(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void propose_strategy() const;
    void conduct_backtest() const;

protected:
    void execute_main_task() const override;
};

// 2. 量化开发员 (QD)
class QuantDeveloper : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    QuantDeveloper(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void review_code() const;
    void optimize_system() const;

protected:
    void execute_main_task() const override;
};

// 3. 交易员 (Trader)
class Trader : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    Trader(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void execute_orders() const;
    void monitor_positions() const;

protected:
    void execute_main_task() const override;
};

// 4. 风险管理员
class RiskManager : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    RiskManager(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void calculate_var() const;
    void check_limits() const;
    void generate_risk_report() const;

protected:
    void execute_main_task() const override;
};

// 5. 投资组合管理员
class PortfolioManager : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    PortfolioManager(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void rebalance_portfolio() const;
    void optimize_allocation() const;

protected:
    void execute_main_task() const override;
};

// 6. 数据科学家
class DataScientist : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    DataScientist(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void clean_data() const;
    void build_models() const;

protected:
    void execute_main_task() const override;
};

// 7. 合规官
class ComplianceOfficer : public Employee
{
private:
    std::unique_ptr<WorkStrategy> work_strategy;

public:
    ComplianceOfficer(const std::string &n, double s, EmployeeLevel lvl = EmployeeLevel::SENIOR);

    void do_work() const override;
    std::string get_skills() const override;
    void review_trades() const;
    void check_regulations() const;

protected:
    void execute_main_task() const override;
};