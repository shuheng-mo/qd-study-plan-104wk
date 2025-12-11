#pragma once

#include "EmployeeBase.hpp"
#include "StrategyBase.hpp"
#include <iostream>

// ========== 具体策略实现 ==========

class ResearchStrategy : public StrategyBase<ResearchStrategy> {
public:
    static constexpr std::string_view strategy_name = "量化研究策略";

    void execute_impl(const std::string& name) const {
        std::cout << "    → " << name << " 正在分析市场数据\n";
        std::cout << "    → " << name << " 正在回测策略\n";
    }
};

class DevelopmentStrategy : public StrategyBase<DevelopmentStrategy> {
public:
    static constexpr std::string_view strategy_name = "开发策略";

    void execute_impl(const std::string& name) const {
        std::cout << "    → " << name << " 正在编写 C++ 代码\n";
        std::cout << "    → " << name << " 正在优化系统性能\n";
    }
};

class TradingStrategy : public StrategyBase<TradingStrategy> {
public:
    static constexpr std::string_view strategy_name = "交易策略";

    void execute_impl(const std::string& name) const {
        std::cout << "    → " << name << " 正在执行交易订单\n";
        std::cout << "    → " << name << " 正在监控持仓\n";
    }
};

// ========== 具体 Employee 类（使用 CRTP）==========

class QuantResearcher : public EmployeeBase<QuantResearcher> {
public:
    using EmployeeBase::EmployeeBase;  // 继承构造函数

    void execute_main_task() const {
        std::cout << "  [核心任务] " << get_name() << " 正在进行量化研究\n";
        ResearchStrategy strategy;
        strategy.execute(get_name());
    }

    std::string get_skills_impl() const {
        return "统计学、机器学习、回测";
    }

    static constexpr double bonus_multiplier() { return 0.30; }
};

class QuantDeveloper : public EmployeeBase<QuantDeveloper> {
public:
    using EmployeeBase::EmployeeBase;

    void execute_main_task() const {
        std::cout << "  [核心任务] " << get_name() << " 正在开发交易系统\n";
        DevelopmentStrategy strategy;
        strategy.execute(get_name());
    }

    std::string get_skills_impl() const {
        return "C++、Python、低延迟系统";
    }

    static constexpr double bonus_multiplier() { return 0.25; }
};

class Trader : public EmployeeBase<Trader> {
public:
    using EmployeeBase::EmployeeBase;

    void execute_main_task() const {
        std::cout << "  [核心任务] " << get_name() << " 正在执行交易\n";
        TradingStrategy strategy;
        strategy.execute(get_name());
    }

    std::string get_skills_impl() const {
        return "市场分析、订单执行、风险控制";
    }

    static constexpr double bonus_multiplier() { return 0.20; }
};

class RiskManager : public EmployeeBase<RiskManager> {
public:
    using EmployeeBase::EmployeeBase;

    void execute_main_task() const {
        std::cout << "  [核心任务] " << get_name() << " 正在进行风险管理\n";
        std::cout << "    → 计算 VaR\n";
        std::cout << "    → 检查风险限额\n";
    }

    std::string get_skills_impl() const {
        return "风险建模、VaR、压力测试";
    }

    static constexpr double bonus_multiplier() { return 0.28; }
};
