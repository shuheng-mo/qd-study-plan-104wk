#pragma once

#include "VariantEmployees.hpp"
#include <vector>
#include <string>
#include <algorithm>

// ============================================================================
// QuantTeam 类 - 使用 std::variant 实现值语义的团队管理
// ============================================================================

class QuantTeam
{
private:
    std::vector<Employee> team_members; // 值语义容器！
    std::string team_name;

public:
    explicit QuantTeam(std::string name) : team_name(std::move(name)) {}

    // 添加员工 - 直接拷贝/移动
    void hire(Employee emp)
    {
        std::string emp_name = std::visit(GetNameVisitor{}, emp);
        std::cout << "[Team] Hiring " << emp_name << "...\n";
        team_members.push_back(std::move(emp));
    }

    // 查找员工
    Employee *find_employee(const std::string &name)
    {
        for (auto &emp : team_members)
        {
            bool found = std::visit([&name](const auto &e)
                                     { return e.name == name; }, emp);

            if (found)
                return &emp;
        }
        return nullptr;
    }

    // 统一操作 - 所有员工开始工作
    void start_daily_operations()
    {
        std::cout << "\n========================================\n";
        std::cout << "=== " << team_name << " Daily Operations ===\n";
        std::cout << "========================================\n\n";

        for (auto &emp : team_members)
        {
            std::visit(DoWorkVisitor{}, emp);
        }

        std::cout << "\n";
    }

    // 计算总薪资
    double get_total_salary() const
    {
        double total = 0.0;
        for (const auto &emp : team_members)
        {
            total += std::visit(GetSalaryVisitor{}, emp);
        }
        return total;
    }

    // 计算总奖金
    double get_total_bonus() const
    {
        double total = 0.0;
        for (const auto &emp : team_members)
        {
            total += std::visit(CalculateBonusVisitor{}, emp);
        }
        return total;
    }

    // 打印团队信息
    void print_team_info() const
    {
        std::cout << "\n========================================\n";
        std::cout << "Team: " << team_name << "\n";
        std::cout << "Members: " << team_members.size() << "\n";
        std::cout << "========================================\n\n";

        for (const auto &emp : team_members)
        {
            std::visit(overloaded{
                           [](const QuantResearcher &qr)
                           {
                               std::cout << "  [Researcher] " << qr.name
                                         << " | Salary: $" << qr.salary
                                         << " | Level: " << level_to_string(qr.level)
                                         << " | Publications: " << qr.publications << "\n";
                           },
                           [](const QuantDeveloper &qd)
                           {
                               std::cout << "  [Developer] " << qd.name
                                         << " | Salary: $" << qd.salary
                                         << " | Level: " << level_to_string(qd.level)
                                         << " | Commits: " << qd.code_commits << "\n";
                           },
                           [](const Trader &t)
                           {
                               std::cout << "  [Trader] " << t.name
                                         << " | Salary: $" << t.salary
                                         << " | Level: " << level_to_string(t.level)
                                         << " | P&L: $" << t.pnl << "\n";
                           },
                           [](const RiskManager &rm)
                           {
                               std::cout << "  [Risk Manager] " << rm.name
                                         << " | Salary: $" << rm.salary
                                         << " | Level: " << level_to_string(rm.level)
                                         << " | Incidents Prevented: " << rm.incidents_prevented << "\n";
                           }},
                       emp);
        }

        std::cout << "\nTotal Salary: $" << get_total_salary() << "\n";
        std::cout << "Total Bonus: $" << get_total_bonus() << "\n";
        std::cout << "Total Compensation: $" << (get_total_salary() + get_total_bonus()) << "\n";
        std::cout << "========================================\n\n";
    }

    // 获取团队规模
    size_t size() const { return team_members.size(); }

    // 直接访问员工（用于测试）
    const std::vector<Employee> &get_members() const { return team_members; }
};
