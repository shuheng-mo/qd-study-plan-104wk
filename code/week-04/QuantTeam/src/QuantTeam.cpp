#include "../include/QuantTeam.hpp"
#include <iostream>
#include <algorithm>
#include <iomanip>

QuantTeam::QuantTeam(const std::string &name, double budget)
    : team_name(name), total_budget(budget), used_budget(0.0)
{
    std::cout << "[成立] 量化团队 '" << team_name << "' 成立，预算: $"
              << std::fixed << std::setprecision(0) << total_budget << std::endl;
}

void QuantTeam::hire(std::unique_ptr<Employee> employee)
{
    if (!employee)
    {
        throw std::invalid_argument("员工指针不能为空");
    }

    try
    {
        validate_budget(employee->get_salary());
        update_budget(employee->get_salary());

        std::cout << "[成功] 招聘成功: " << employee->get_name()
                  << " (薪资: $" << employee->get_salary() << ")" << std::endl;

        team_members.push_back(std::move(employee));
    }
    catch (const QuantTeamException &e)
    {
        std::cout << "[失败] 招聘失败: " << e.what() << std::endl;
        throw;
    }
}

void QuantTeam::fire(const std::string &employee_name)
{
    auto it = std::find_if(team_members.begin(), team_members.end(),
                           [&employee_name](const std::unique_ptr<Employee> &emp)
                           {
                               return emp->get_name() == employee_name;
                           });

    if (it != team_members.end())
    {
        double salary = (*it)->get_salary();
        used_budget -= salary;
        std::cout << "[解雇] " << employee_name << " 已被解雇，释放预算: $" << salary << std::endl;
        team_members.erase(it);
    }
}

Employee *QuantTeam::find_employee(const std::string &name) const
{
    auto it = std::find_if(team_members.begin(), team_members.end(),
                           [&name](const std::unique_ptr<Employee> &emp)
                           {
                               return emp->get_name() == name;
                           });

    return (it != team_members.end()) ? it->get() : nullptr;
}

Employee *QuantTeam::find_employee_by_type(EmployeeType type) const
{
    auto it = std::find_if(team_members.begin(), team_members.end(),
                           [type](const std::unique_ptr<Employee> &emp)
                           {
                               return emp->get_type() == type;
                           });

    return (it != team_members.end()) ? it->get() : nullptr;
}

void QuantTeam::start_daily_operations()
{
    std::cout << "\n======== " << team_name << " 日常运营开始 ========" << std::endl;

    try
    {
        conduct_morning_meeting();
        strategy_discussion();
        code_review_session();
        risk_assessment();
        performance_review();

        std::cout << "\n======== 今日运营完成 ========" << std::endl;
    }
    catch (const QuantTeamException &e)
    {
        std::cout << "[警告] 运营中出现异常: " << e.what() << std::endl;
    }
}

void QuantTeam::conduct_morning_meeting()
{
    std::cout << "\n=== 早会时间 ===" << std::endl;
    for (const auto &member : team_members)
    {
        member->do_work();
    }
}

void QuantTeam::strategy_discussion()
{
    std::cout << "\n=== 策略讨论 ===" << std::endl;

    // QR 提出策略
    auto qr = find_employee_by_type(EmployeeType::QUANT_RESEARCHER);
    if (qr)
    {
        TeamEvent strategy_event(EventType::STRATEGY_PROPOSED, qr->get_name(),
                                 "新的均值回归策略");
        broadcast_event(strategy_event);
    }
}

void QuantTeam::code_review_session()
{
    std::cout << "\n=== 代码审查 ===" << std::endl;

    auto qd = find_employee_by_type(EmployeeType::QUANT_DEVELOPER);
    if (qd)
    {
        TeamEvent review_event(EventType::CODE_REVIEW_REQUESTED, qd->get_name(),
                               "请审查交易引擎代码");
        broadcast_event(review_event);
    }
}

void QuantTeam::risk_assessment()
{
    std::cout << "\n=== 风险评估 ===" << std::endl;

    auto rm = find_employee_by_type(EmployeeType::RISK_MANAGER);
    if (rm)
    {
        TeamEvent risk_event(EventType::RISK_ALERT, rm->get_name(),
                             "市场波动率上升，需要关注");
        broadcast_event(risk_event);
    }
}

void QuantTeam::performance_review()
{
    std::cout << "\n=== 绩效回顾 ===" << std::endl;

    auto pm = find_employee_by_type(EmployeeType::PORTFOLIO_MANAGER);
    if (pm)
    {
        TeamEvent perf_event(EventType::PERFORMANCE_REVIEW, pm->get_name(),
                             "本月收益率达到3.2%");
        broadcast_event(perf_event);
    }
}

void QuantTeam::broadcast_event(const TeamEvent &event)
{
    for (const auto &member : team_members)
    {
        member->onEvent(event);
    }
}

void QuantTeam::show_team_composition() const
{
    std::cout << "\n=== " << team_name << " 团队构成 ===" << std::endl;
    std::cout << "团队规模: " << team_members.size() << " 人" << std::endl;

    for (const auto &member : team_members)
    {
        std::cout << "• " << member->get_name()
                  << " - 技能: " << member->get_skills()
                  << " - 薪资: $" << member->get_salary() << std::endl;
    }
}

void QuantTeam::show_budget_status() const
{
    std::cout << "\n=== 预算状态 ===" << std::endl;
    std::cout << "总预算: $" << std::fixed << std::setprecision(0) << total_budget << std::endl;
    std::cout << "已用预算: $" << used_budget << std::endl;
    std::cout << "剩余预算: $" << (total_budget - used_budget) << std::endl;
    std::cout << "预算使用率: " << std::setprecision(1)
              << (used_budget / total_budget * 100) << "%" << std::endl;
}

double QuantTeam::get_total_salary_cost() const
{
    double total = 0.0;
    for (const auto &member : team_members)
    {
        total += member->get_salary();
    }
    return total;
}

void QuantTeam::validate_budget(double salary) const
{
    if (used_budget + salary > total_budget)
    {
        throw InsufficientFundsException("薪资超出预算限制");
    }
}

void QuantTeam::update_budget(double amount)
{
    used_budget += amount;
}