#pragma once

#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <algorithm>
#include "Employee.hpp"
#include "TeamEvent.hpp"
#include "Exceptions.hpp"

// 团队管理类 - 使用观察者模式管理事件
class QuantTeam
{
private:
    std::vector<std::unique_ptr<Employee>> team_members;
    std::string team_name;
    double total_budget;
    double used_budget;

public:
    explicit QuantTeam(const std::string &name = "Sigma-X", double budget = 10000000.0);
    ~QuantTeam() = default;

    // 团队管理
    void hire(std::unique_ptr<Employee> employee);
    void fire(const std::string &employee_name);
    Employee *find_employee(const std::string &name) const;
    Employee *find_employee_by_type(EmployeeType type) const;

    // 工作流程
    void start_daily_operations();
    void conduct_morning_meeting();
    void strategy_discussion();
    void code_review_session();
    void risk_assessment();
    void performance_review();

    // 事件广播
    void broadcast_event(const TeamEvent &event);

    // 信息获取
    void show_team_composition() const;
    void show_budget_status() const;
    size_t get_team_size() const { return team_members.size(); }
    double get_total_salary_cost() const;

private:
    void validate_budget(double salary) const;
    void update_budget(double amount);
};