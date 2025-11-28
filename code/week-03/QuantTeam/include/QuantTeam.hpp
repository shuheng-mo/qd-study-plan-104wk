#pragma once

#include <iostream>
#include <vector>
#include <memory>
#include "Employee.hpp"

// 团队管理类声明
class QuantTeam
{
private:
    // 使用智能指针管理内存，更安全
    std::vector<std::unique_ptr<Employee>> team_members;

public:
    // 招人 - 使用智能指针
    void hire(std::unique_ptr<Employee> e);

    // 每日早会：一声令下，全员开工
    void start_daily_operations();

    // 析构函数：使用智能指针后，自动管理内存
    ~QuantTeam() = default;
};