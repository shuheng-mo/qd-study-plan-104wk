#pragma once

#include <string>
#include <string_view>
#include <iostream>

/**
 * CRTP 策略基类 - 零虚函数开销的策略模式
 */
template<typename Derived>
class StrategyBase {
public:
    // CRTP 接口
    void execute(const std::string& employee_name) const {
        std::cout << "  [策略执行] " << name() << "\n";
        static_cast<const Derived*>(this)->execute_impl(employee_name);
    }

    constexpr std::string_view name() const {
        return Derived::strategy_name;
    }

    void log_execution() const {
        std::cout << "  [" << name() << "] 策略开始执行\n";
    }
};
