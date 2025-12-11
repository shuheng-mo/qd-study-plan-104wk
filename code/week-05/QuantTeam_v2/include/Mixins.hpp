#pragma once

#include <iostream>
#include <string>
#include <chrono>

/**
 * Mixin 类 - 通过多重继承组合功能
 * 优势：不修改原类，遵循开闭原则，功能正交
 */

// ========== Mixin 1: 日志功能 ==========
template<typename Base>
class Loggable : public Base {
public:
    using Base::Base;  // 继承构造函数

    void log(const std::string& message) const {
        std::cout << "  [日志] [" << Base::get_name() << "] " << message << "\n";
    }

    // 增强基类方法
    void do_work() const {
        log("开始工作");
        Base::do_work();
        log("工作完成");
    }
};

// ========== Mixin 2: 指标采集 ==========
template<typename Base>
class MetricsCollector : public Base {
private:
    mutable std::chrono::steady_clock::time_point start_time;
    mutable size_t task_count = 0;

public:
    using Base::Base;

    void do_work() const {
        start_time = std::chrono::steady_clock::now();
        ++task_count;

        Base::do_work();

        auto duration = std::chrono::steady_clock::now() - start_time;
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
        std::cout << "  [指标] 任务 #" << task_count << " 耗时: " << ms << "ms\n";
    }

    size_t get_task_count() const { return task_count; }
};

// ========== Mixin 3: 权限控制 ==========
template<typename Base>
class Permissioned : public Base {
private:
    int permission_level = 1;

public:
    using Base::Base;

    void set_permission_level(int level) { permission_level = level; }
    int get_permission_level() const { return permission_level; }

    void do_work() const {
        if (permission_level < 2) {
            std::cout << "  [权限] " << Base::get_name()
                      << " 权限不足 (需要等级 >= 2，当前: " << permission_level << ")\n";
            return;
        }
        Base::do_work();
    }
};

// ========== 组合多个 Mixin ==========

// 带日志的员工
template<typename EmployeeType>
using LoggableEmployee = Loggable<EmployeeType>;

// 带指标采集的员工
template<typename EmployeeType>
using MetricsEmployee = MetricsCollector<EmployeeType>;

// 完全增强的员工（日志 + 指标）
template<typename EmployeeType>
using EnhancedEmployee = Loggable<MetricsCollector<EmployeeType>>;

// 完整功能员工（权限 + 日志 + 指标）
template<typename EmployeeType>
using FullFeaturedEmployee = Permissioned<Loggable<MetricsCollector<EmployeeType>>>;
