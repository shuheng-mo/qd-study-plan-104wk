#pragma once

#include "Types.hpp"
#include <variant>
#include <string>
#include <iostream>

// ============================================================================
// Week 6 优化 6.1: std::variant 多态 - 值语义多态
// ============================================================================
// 核心思想：使用 std::variant 实现无继承的多态，提供值语义
// 优势：可拷贝、无虚函数、内存紧凑、类型安全
// ============================================================================

// 量化研究员（无继承关系）
struct QuantResearcher
{
    std::string name;
    double salary;
    EmployeeLevel level;
    int publications = 0;

    QuantResearcher(std::string n, double s, EmployeeLevel lvl, int pubs = 0)
        : name(std::move(n)), salary(s), level(lvl), publications(pubs) {}

    void do_work() const
    {
        std::cout << name << " (Researcher) is analyzing market data and backtesting strategies...\n";
    }

    std::string get_skills() const
    {
        return "Statistics, Machine Learning, Backtesting";
    }

    double calculate_bonus() const
    {
        double base_bonus = salary * 0.2;
        // 基于发表论文数量的奖励
        return base_bonus * (1.0 + publications * 0.1);
    }
};

// 量化开发员（无继承关系）
struct QuantDeveloper
{
    std::string name;
    double salary;
    EmployeeLevel level;
    int code_commits = 0;

    QuantDeveloper(std::string n, double s, EmployeeLevel lvl, int commits = 0)
        : name(std::move(n)), salary(s), level(lvl), code_commits(commits) {}

    void do_work() const
    {
        std::cout << name << " (Developer) is optimizing trading system and writing C++ code...\n";
    }

    std::string get_skills() const
    {
        return "C++, Python, Low-latency Systems, Performance Optimization";
    }

    double calculate_bonus() const
    {
        double base_bonus = salary * 0.18;
        // 基于代码提交数量的奖励
        return base_bonus * (1.0 + code_commits * 0.001);
    }
};

// 交易员（无继承关系）
struct Trader
{
    std::string name;
    double salary;
    EmployeeLevel level;
    double pnl = 0.0; // Profit and Loss

    Trader(std::string n, double s, EmployeeLevel lvl, double profit = 0.0)
        : name(std::move(n)), salary(s), level(lvl), pnl(profit) {}

    void do_work() const
    {
        std::cout << name << " (Trader) is executing trades and managing positions...\n";
    }

    std::string get_skills() const
    {
        return "Market Analysis, Execution, Risk Management";
    }

    double calculate_bonus() const
    {
        double base_bonus = salary * 0.15;
        // 基于盈亏的奖励（10% 的盈利作为奖金）
        return base_bonus + (pnl > 0 ? pnl * 0.10 : 0.0);
    }
};

// 风控经理（无继承关系）
struct RiskManager
{
    std::string name;
    double salary;
    EmployeeLevel level;
    int incidents_prevented = 0;

    RiskManager(std::string n, double s, EmployeeLevel lvl, int prevented = 0)
        : name(std::move(n)), salary(s), level(lvl), incidents_prevented(prevented) {}

    void do_work() const
    {
        std::cout << name << " (Risk Manager) is monitoring portfolio risk and setting limits...\n";
    }

    std::string get_skills() const
    {
        return "Risk Assessment, Compliance, VaR Modeling";
    }

    double calculate_bonus() const
    {
        double base_bonus = salary * 0.16;
        // 基于预防风险事件的奖励
        return base_bonus * (1.0 + incidents_prevented * 0.05);
    }
};

// ============================================================================
// Employee variant - 值语义多态容器
// ============================================================================
using Employee = std::variant<QuantResearcher, QuantDeveloper, Trader, RiskManager>;

// ============================================================================
// 访问者（Visitor）- 统一操作不同类型
// ============================================================================

// 工作访问者
struct DoWorkVisitor
{
    void operator()(const QuantResearcher &qr) const { qr.do_work(); }
    void operator()(const QuantDeveloper &qd) const { qd.do_work(); }
    void operator()(const Trader &t) const { t.do_work(); }
    void operator()(const RiskManager &rm) const { rm.do_work(); }
};

// 技能访问者
struct GetSkillsVisitor
{
    std::string operator()(const QuantResearcher &qr) const { return qr.get_skills(); }
    std::string operator()(const QuantDeveloper &qd) const { return qd.get_skills(); }
    std::string operator()(const Trader &t) const { return t.get_skills(); }
    std::string operator()(const RiskManager &rm) const { return rm.get_skills(); }
};

// 奖金计算访问者
struct CalculateBonusVisitor
{
    double operator()(const QuantResearcher &qr) const { return qr.calculate_bonus(); }
    double operator()(const QuantDeveloper &qd) const { return qd.calculate_bonus(); }
    double operator()(const Trader &t) const { return t.calculate_bonus(); }
    double operator()(const RiskManager &rm) const { return rm.calculate_bonus(); }
};

// 姓名访问者
struct GetNameVisitor
{
    std::string operator()(const QuantResearcher &qr) const { return qr.name; }
    std::string operator()(const QuantDeveloper &qd) const { return qd.name; }
    std::string operator()(const Trader &t) const { return t.name; }
    std::string operator()(const RiskManager &rm) const { return rm.name; }
};

// 薪资访问者
struct GetSalaryVisitor
{
    double operator()(const QuantResearcher &qr) const { return qr.salary; }
    double operator()(const QuantDeveloper &qd) const { return qd.salary; }
    double operator()(const Trader &t) const { return t.salary; }
    double operator()(const RiskManager &rm) const { return rm.salary; }
};

// ============================================================================
// C++20 重载 lambda 辅助（overloaded pattern）
// ============================================================================
template <class... Ts>
struct overloaded : Ts...
{
    using Ts::operator()...;
};

// C++17 需要显式推导指引
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;
