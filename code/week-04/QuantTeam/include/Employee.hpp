#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <memory>

// 前向声明
class TeamEvent;

// 观察者接口
class EventObserver
{
public:
    virtual ~EventObserver() = default;
    virtual void onEvent(const TeamEvent &event) = 0;
};

// 员工等级枚举
enum class EmployeeLevel
{
    JUNIOR,
    SENIOR,
    PRINCIPAL,
    DIRECTOR
};

// 员工类型枚举
enum class EmployeeType
{
    QUANT_RESEARCHER,
    QUANT_DEVELOPER,
    TRADER,
    RISK_MANAGER,
    PORTFOLIO_MANAGER,
    DATA_SCIENTIST,
    COMPLIANCE_OFFICER
};

// 这是一个抽象基类（Abstract Base Class）
class Employee : public EventObserver
{
protected:
    std::string name;
    double base_salary;
    EmployeeLevel level;
    EmployeeType type;
    bool is_busy;

public:
    Employee(const std::string &n, double s, EmployeeLevel lvl, EmployeeType t);
    virtual ~Employee() = default;

    // 纯虚函数 - 必须由子类实现
    virtual void do_work() const = 0;

    // 虚函数 - 子类可以重写
    virtual void collaborate_with(const Employee &colleague) const;
    virtual std::string get_skills() const = 0;
    virtual double calculate_bonus() const;

    // 普通成员函数
    std::string get_name() const { return name; }
    double get_salary() const { return base_salary; }
    EmployeeType get_type() const { return type; }
    EmployeeLevel get_level() const { return level; }
    bool is_available() const { return !is_busy; }

    void set_busy(bool busy) { is_busy = busy; }

    // 事件观察者实现
    void onEvent(const TeamEvent &event) override;

protected:
    // 模板方法模式 - 定义工作流程
    virtual void prepare_work() const;
    virtual void execute_main_task() const = 0;
    virtual void wrap_up_work() const;
};