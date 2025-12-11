#pragma once

#include <iostream>
#include <string>

/**
 * Policy-Based Design - 策略作为模板参数
 * 优势：编译期绑定，完全内联，零开销
 */

// ========== 工作策略 Policy ==========

struct ResearchWorkPolicy {
    static void execute_task(const std::string& name) {
        std::cout << "  [研究工作] " << name << " 正在分析数据并回测策略\n";
    }
};

struct DevelopmentWorkPolicy {
    static void execute_task(const std::string& name) {
        std::cout << "  [开发工作] " << name << " 正在编写代码并优化性能\n";
    }
};

struct TradingWorkPolicy {
    static void execute_task(const std::string& name) {
        std::cout << "  [交易工作] " << name << " 正在执行订单并监控风险\n";
    }
};

// ========== 奖金计算 Policy ==========

struct PerformanceBasedBonusPolicy {
    static double calculate(double base_salary, double performance_score) {
        return base_salary * 0.20 * performance_score;
    }
    static constexpr const char* name = "绩效奖金";
};

struct FixedBonusPolicy {
    static double calculate(double base_salary, double /*unused*/) {
        return base_salary * 0.15;
    }
    static constexpr const char* name = "固定奖金";
};

struct HighPerformanceBonusPolicy {
    static double calculate(double base_salary, double performance_score) {
        return base_salary * 0.35 * performance_score;
    }
    static constexpr const char* name = "高绩效奖金";
};

// ========== Policy-Based Employee ==========

template<typename WorkPolicy, typename BonusPolicy>
class PolicyBasedEmployee {
private:
    std::string name;
    double base_salary;
    double performance_score = 1.0;

public:
    PolicyBasedEmployee(std::string n, double s)
        : name(std::move(n)), base_salary(s) {}

    void do_work() const {
        std::cout << "\n【Policy-Based 员工: " << name << "】\n";
        WorkPolicy::execute_task(name);  // 编译期决定
    }

    double calculate_bonus() const {
        return BonusPolicy::calculate(base_salary, performance_score);
    }

    void set_performance(double score) { performance_score = score; }

    std::string get_name() const { return name; }
    double get_salary() const { return base_salary; }

    void show_bonus_info() const {
        std::cout << "  [奖金] " << name << " - " << BonusPolicy::name
                  << ": $" << calculate_bonus() << "\n";
    }
};

// ========== 类型别名 ==========

using PolicyResearcher = PolicyBasedEmployee<ResearchWorkPolicy, PerformanceBasedBonusPolicy>;
using PolicyDeveloper = PolicyBasedEmployee<DevelopmentWorkPolicy, FixedBonusPolicy>;
using PolicyTrader = PolicyBasedEmployee<TradingWorkPolicy, HighPerformanceBonusPolicy>;
