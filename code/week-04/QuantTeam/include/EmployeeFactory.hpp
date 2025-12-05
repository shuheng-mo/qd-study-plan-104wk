#pragma once

#include <string>
#include <memory>
#include "Employee.hpp"

// 工厂模式 - 员工创建工厂
class EmployeeFactory
{
public:
    static std::unique_ptr<Employee> createEmployee(
        EmployeeType type,
        const std::string &name,
        double salary,
        EmployeeLevel level = EmployeeLevel::SENIOR);

private:
    // 私有构造函数，工厂类不应该被实例化
    EmployeeFactory() = default;
};