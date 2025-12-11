#pragma once

#include <string>
#include <iostream>
#include "Types.hpp"
#include "StrongID.hpp"

/**
 * CRTP 基类 - 使用奇异递归模板模式实现静态多态
 * 优势：零虚函数开销，所有调用在编译期解析，可内联
 */
template<typename Derived>
class EmployeeBase {
protected:
    EmployeeID id;
    std::string name;
    double base_salary;
    EmployeeLevel level;

public:
    EmployeeBase(EmployeeID emp_id, std::string n, double s, EmployeeLevel lvl)
        : id(emp_id), name(std::move(n)), base_salary(s), level(lvl) {}

    // CRTP 接口 - 模板方法模式
    void do_work() const {
        prepare_work();
        // 静态向下转型，编译期解析
        static_cast<const Derived*>(this)->execute_main_task();
        wrap_up_work();
    }

    // CRTP 接口 - 获取技能
    std::string get_skills() const {
        return static_cast<const Derived*>(this)->get_skills_impl();
    }

    // CRTP 接口 - 计算奖金
    double calculate_bonus() const {
        // 调用派生类的 bonus_multiplier()
        return base_salary * static_cast<const Derived*>(this)->bonus_multiplier();
    }

    // 普通访问器
    EmployeeID get_id() const noexcept { return id; }
    std::string get_name() const { return name; }
    double get_salary() const { return base_salary; }
    EmployeeLevel get_level() const { return level; }

protected:
    void prepare_work() const {
        std::cout << "  [准备] " << name << " 开始准备工作...\n";
    }

    void wrap_up_work() const {
        std::cout << "  [收尾] " << name << " 完成工作收尾\n";
    }
};
