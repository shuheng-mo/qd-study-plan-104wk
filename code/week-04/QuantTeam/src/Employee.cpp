#include "../include/Employee.hpp"
#include "../include/TeamEvent.hpp"
#include <iostream>

Employee::Employee(const std::string &n, double s, EmployeeLevel lvl, EmployeeType t)
    : name(n), base_salary(s), level(lvl), type(t), is_busy(false) {}

void Employee::collaborate_with(const Employee &colleague) const
{
    std::cout << "[协作] " << name << " 正在与 " << colleague.get_name()
              << " 协作处理项目" << std::endl;
}

double Employee::calculate_bonus() const
{
    double bonus_multiplier = 1.0;
    switch (level)
    {
    case EmployeeLevel::JUNIOR:
        bonus_multiplier = 0.8;
        break;
    case EmployeeLevel::SENIOR:
        bonus_multiplier = 1.2;
        break;
    case EmployeeLevel::PRINCIPAL:
        bonus_multiplier = 1.5;
        break;
    case EmployeeLevel::DIRECTOR:
        bonus_multiplier = 2.0;
        break;
    }
    return base_salary * 0.2 * bonus_multiplier; // 20% 基础奖金
}

void Employee::onEvent(const TeamEvent &event)
{
    switch (event.get_type())
    {
    case EventType::STRATEGY_PROPOSED:
        std::cout << "[事件响应] " << name << " 收到策略提议: "
                  << event.get_message() << std::endl;
        break;
    case EventType::CODE_REVIEW_REQUESTED:
        if (type == EmployeeType::QUANT_DEVELOPER)
        {
            std::cout << "[事件响应] " << name << " 开始代码审查..." << std::endl;
        }
        break;
    case EventType::RISK_ALERT:
        if (type == EmployeeType::RISK_MANAGER || type == EmployeeType::PORTFOLIO_MANAGER)
        {
            std::cout << "[事件响应] " << name << " 响应风险警报!" << std::endl;
        }
        break;
    default:
        break;
    }
}

void Employee::prepare_work() const
{
    std::cout << "[准备] " << name << " 正在准备工作..." << std::endl;
}

void Employee::wrap_up_work() const
{
    std::cout << "[结束] " << name << " 完成了今日工作。" << std::endl;
}