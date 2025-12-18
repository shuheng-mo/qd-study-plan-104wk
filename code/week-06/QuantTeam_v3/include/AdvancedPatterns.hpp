#pragma once

#include "Types.hpp"
#include <memory>
#include <string>
#include <iostream>
#include <vector>

// ============================================================================
// Week 6 优化 6.3: PIMPL (Pointer to Implementation)
// ============================================================================
// 核心思想：隐藏实现细节，减少编译依赖，实现二进制兼容
// 优势：编译防火墙、隐藏细节、ABI 稳定
// ============================================================================

// Portfolio 类 - 使用 PIMPL 隐藏实现
class Portfolio
{
private:
    class Impl; // 前向声明
    std::unique_ptr<Impl> pimpl;

public:
    Portfolio(std::string name, double initial_capital);
    ~Portfolio(); // 必须在 cpp 中定义

    // Rule of Five - 正确处理 unique_ptr<Impl>
    Portfolio(const Portfolio &other);
    Portfolio(Portfolio &&other) noexcept;
    Portfolio &operator=(const Portfolio &other);
    Portfolio &operator=(Portfolio &&other) noexcept;

    // 公共接口
    void add_position(const std::string &symbol, double quantity, double price);
    void remove_position(const std::string &symbol);
    double get_total_value() const;
    double get_pnl() const;
    void print_positions() const;
    std::string get_name() const;
};

// ============================================================================
// Week 6 优化 6.4: Prototype Pattern - 原型模式
// ============================================================================
// 核心思想：通过克隆现有对象创建新对象，实现"虚构造函数"
// 优势：基类指针可以克隆、类型安全、深拷贝
// ============================================================================

// CRTP 版本的 Cloneable
template <typename Derived>
class Cloneable
{
public:
    std::unique_ptr<Derived> clone() const
    {
        return std::make_unique<Derived>(static_cast<const Derived &>(*this));
    }
};

// 可克隆的策略基类
class CloneableStrategy
{
public:
    virtual ~CloneableStrategy() = default;

    // 虚构造函数
    virtual std::unique_ptr<CloneableStrategy> clone() const = 0;

    virtual double execute(const MarketData &data) = 0;
    virtual std::string get_name() const = 0;
};

// 可克隆的动量策略
class CloneableMomentumStrategy : public CloneableStrategy,
                                  public Cloneable<CloneableMomentumStrategy>
{
private:
    double threshold;
    std::string custom_name;

public:
    explicit CloneableMomentumStrategy(double thresh = 0.01, std::string name = "Momentum")
        : threshold(thresh), custom_name(std::move(name)) {}

    // 实现克隆（使用 CRTP 的 clone）
    std::unique_ptr<CloneableStrategy> clone() const override
    {
        return Cloneable<CloneableMomentumStrategy>::clone();
    }

    double execute(const MarketData &data) override
    {
        double signal = data.price * threshold;
        std::cout << "[" << custom_name << "] Signal for " << data.symbol << ": " << signal << "\n";
        return signal;
    }

    std::string get_name() const override { return custom_name; }

    // 可修改的接口
    void set_threshold(double thresh) { threshold = thresh; }
    double get_threshold() const { return threshold; }
};

// 可克隆的均值回归策略
class CloneableMeanReversionStrategy : public CloneableStrategy,
                                       public Cloneable<CloneableMeanReversionStrategy>
{
private:
    double mean_price;
    std::string custom_name;

public:
    explicit CloneableMeanReversionStrategy(double mean = 100.0, std::string name = "MeanReversion")
        : mean_price(mean), custom_name(std::move(name)) {}

    std::unique_ptr<CloneableStrategy> clone() const override
    {
        return Cloneable<CloneableMeanReversionStrategy>::clone();
    }

    double execute(const MarketData &data) override
    {
        double deviation = (mean_price - data.price) / mean_price;
        double signal = deviation * 10.0;
        std::cout << "[" << custom_name << "] Signal for " << data.symbol << ": " << signal << "\n";
        return signal;
    }

    std::string get_name() const override { return custom_name; }

    void set_mean_price(double mean) { mean_price = mean; }
    double get_mean_price() const { return mean_price; }
};

// ============================================================================
// Week 6 优化 6.5: Visitor Pattern - 访问者模式
// ============================================================================
// 核心思想：在不修改类的情况下添加新操作（双重分派）
// 优势：开闭原则、双重分派、集中操作
// ============================================================================

// 前向声明（用于 Visitor 模式的版本）
class VisitableQuantResearcher;
class VisitableQuantDeveloper;
class VisitableTrader;
class VisitableRiskManager;

// 访问者接口
class EmployeeVisitor
{
public:
    virtual ~EmployeeVisitor() = default;

    virtual void visit(const VisitableQuantResearcher &qr) = 0;
    virtual void visit(const VisitableQuantDeveloper &qd) = 0;
    virtual void visit(const VisitableTrader &t) = 0;
    virtual void visit(const VisitableRiskManager &rm) = 0;
};

// 被访问的基类（用于 Visitor 模式）
class VisitableEmployee
{
public:
    virtual ~VisitableEmployee() = default;

    // 接受访问者
    virtual void accept(EmployeeVisitor &visitor) const = 0;

    virtual std::string get_name() const = 0;
    virtual double get_salary() const = 0;
    virtual std::string get_skills() const = 0;
};

// 可访问的量化研究员
class VisitableQuantResearcher : public VisitableEmployee
{
private:
    std::string name;
    double salary;
    int publications;

public:
    VisitableQuantResearcher(std::string n, double s, int pubs = 0)
        : name(std::move(n)), salary(s), publications(pubs) {}

    void accept(EmployeeVisitor &visitor) const override
    {
        visitor.visit(*this);
    }

    std::string get_name() const override { return name; }
    double get_salary() const override { return salary; }
    int get_publications() const { return publications; }

    std::string get_skills() const override
    {
        return "Statistics, ML, Backtesting (" + std::to_string(publications) + " papers)";
    }
};

// 可访问的量化开发员
class VisitableQuantDeveloper : public VisitableEmployee
{
private:
    std::string name;
    double salary;
    int code_commits;

public:
    VisitableQuantDeveloper(std::string n, double s, int commits = 0)
        : name(std::move(n)), salary(s), code_commits(commits) {}

    void accept(EmployeeVisitor &visitor) const override
    {
        visitor.visit(*this);
    }

    std::string get_name() const override { return name; }
    double get_salary() const override { return salary; }
    int get_commits() const { return code_commits; }

    std::string get_skills() const override
    {
        return "C++, Python (" + std::to_string(code_commits) + " commits)";
    }
};

// 可访问的交易员
class VisitableTrader : public VisitableEmployee
{
private:
    std::string name;
    double salary;
    double pnl;

public:
    VisitableTrader(std::string n, double s, double profit = 0.0)
        : name(std::move(n)), salary(s), pnl(profit) {}

    void accept(EmployeeVisitor &visitor) const override
    {
        visitor.visit(*this);
    }

    std::string get_name() const override { return name; }
    double get_salary() const override { return salary; }
    double get_pnl() const { return pnl; }

    std::string get_skills() const override
    {
        return "Trading, Risk (P&L: $" + std::to_string(static_cast<int>(pnl)) + ")";
    }
};

// 可访问的风控经理
class VisitableRiskManager : public VisitableEmployee
{
private:
    std::string name;
    double salary;
    int incidents_prevented;

public:
    VisitableRiskManager(std::string n, double s, int prevented = 0)
        : name(std::move(n)), salary(s), incidents_prevented(prevented) {}

    void accept(EmployeeVisitor &visitor) const override
    {
        visitor.visit(*this);
    }

    std::string get_name() const override { return name; }
    double get_salary() const override { return salary; }
    int get_incidents_prevented() const { return incidents_prevented; }

    std::string get_skills() const override
    {
        return "Risk Management (" + std::to_string(incidents_prevented) + " incidents prevented)";
    }
};

// ============================================================================
// 具体访问者实现
// ============================================================================

// 薪资报告访问者
class SalaryReportVisitor : public EmployeeVisitor
{
private:
    double total_salary = 0.0;
    std::vector<std::string> report_lines;

public:
    void visit(const VisitableQuantResearcher &qr) override
    {
        double bonus = qr.get_salary() * 0.2 * (1.0 + qr.get_publications() * 0.1);
        total_salary += qr.get_salary() + bonus;

        report_lines.push_back("[Researcher] " + qr.get_name() +
                               " | Salary: $" + std::to_string(static_cast<int>(qr.get_salary())) +
                               " | Bonus: $" + std::to_string(static_cast<int>(bonus)) +
                               " | Publications: " + std::to_string(qr.get_publications()));
    }

    void visit(const VisitableQuantDeveloper &qd) override
    {
        double bonus = qd.get_salary() * 0.18 * (1.0 + qd.get_commits() * 0.001);
        total_salary += qd.get_salary() + bonus;

        report_lines.push_back("[Developer] " + qd.get_name() +
                               " | Salary: $" + std::to_string(static_cast<int>(qd.get_salary())) +
                               " | Bonus: $" + std::to_string(static_cast<int>(bonus)) +
                               " | Commits: " + std::to_string(qd.get_commits()));
    }

    void visit(const VisitableTrader &t) override
    {
        double bonus = t.get_salary() * 0.15 + (t.get_pnl() > 0 ? t.get_pnl() * 0.10 : 0.0);
        total_salary += t.get_salary() + bonus;

        report_lines.push_back("[Trader] " + t.get_name() +
                               " | Salary: $" + std::to_string(static_cast<int>(t.get_salary())) +
                               " | Bonus: $" + std::to_string(static_cast<int>(bonus)) +
                               " | P&L: $" + std::to_string(static_cast<int>(t.get_pnl())));
    }

    void visit(const VisitableRiskManager &rm) override
    {
        double bonus = rm.get_salary() * 0.16 * (1.0 + rm.get_incidents_prevented() * 0.05);
        total_salary += rm.get_salary() + bonus;

        report_lines.push_back("[Risk Manager] " + rm.get_name() +
                               " | Salary: $" + std::to_string(static_cast<int>(rm.get_salary())) +
                               " | Bonus: $" + std::to_string(static_cast<int>(bonus)) +
                               " | Incidents Prevented: " + std::to_string(rm.get_incidents_prevented()));
    }

    double get_total() const { return total_salary; }

    void print_report() const
    {
        std::cout << "\n===== Salary Report =====\n";
        for (const auto &line : report_lines)
        {
            std::cout << line << "\n";
        }
        std::cout << "\nTotal Compensation: $" << static_cast<int>(total_salary) << "\n";
        std::cout << "=========================\n\n";
    }
};

// 性能评估访问者
class PerformanceEvaluator : public EmployeeVisitor
{
private:
    std::vector<std::string> high_performers;
    std::vector<std::string> needs_improvement;

public:
    void visit(const VisitableQuantResearcher &qr) override
    {
        if (qr.get_publications() >= 5)
        {
            high_performers.push_back(qr.get_name() + " (Researcher) - " +
                                      std::to_string(qr.get_publications()) + " publications");
        }
        else if (qr.get_publications() < 2)
        {
            needs_improvement.push_back(qr.get_name() + " (Researcher) - Only " +
                                        std::to_string(qr.get_publications()) + " publications");
        }
    }

    void visit(const VisitableQuantDeveloper &qd) override
    {
        if (qd.get_commits() >= 100)
        {
            high_performers.push_back(qd.get_name() + " (Developer) - " +
                                      std::to_string(qd.get_commits()) + " commits");
        }
        else if (qd.get_commits() < 50)
        {
            needs_improvement.push_back(qd.get_name() + " (Developer) - Only " +
                                        std::to_string(qd.get_commits()) + " commits");
        }
    }

    void visit(const VisitableTrader &t) override
    {
        if (t.get_pnl() > 1000000.0)
        {
            high_performers.push_back(t.get_name() + " (Trader) - P&L: $" +
                                      std::to_string(static_cast<int>(t.get_pnl())));
        }
        else if (t.get_pnl() < 0.0)
        {
            needs_improvement.push_back(t.get_name() + " (Trader) - Negative P&L: $" +
                                        std::to_string(static_cast<int>(t.get_pnl())));
        }
    }

    void visit(const VisitableRiskManager &rm) override
    {
        if (rm.get_incidents_prevented() >= 10)
        {
            high_performers.push_back(rm.get_name() + " (Risk Manager) - " +
                                      std::to_string(rm.get_incidents_prevented()) + " incidents prevented");
        }
        else if (rm.get_incidents_prevented() < 3)
        {
            needs_improvement.push_back(rm.get_name() + " (Risk Manager) - Only " +
                                        std::to_string(rm.get_incidents_prevented()) + " incidents prevented");
        }
    }

    void print_evaluation() const
    {
        std::cout << "\n===== Performance Evaluation =====\n";

        std::cout << "\nHigh Performers:\n";
        if (high_performers.empty())
        {
            std::cout << "  (None)\n";
        }
        else
        {
            for (const auto &name : high_performers)
            {
                std::cout << "  ✓ " << name << "\n";
            }
        }

        std::cout << "\nNeeds Improvement:\n";
        if (needs_improvement.empty())
        {
            std::cout << "  (None)\n";
        }
        else
        {
            for (const auto &name : needs_improvement)
            {
                std::cout << "  ✗ " << name << "\n";
            }
        }

        std::cout << "\n==================================\n\n";
    }
};
