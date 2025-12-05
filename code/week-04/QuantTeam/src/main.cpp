#include "../include/QuantTeam.hpp"
#include "../include/EmployeeFactory.hpp"
#include "../include/CoreMembers.hpp"
#include "../include/Exceptions.hpp"
#include <memory>
#include <iostream>

int main()
{
    try
    {
        // 创建量化团队
        QuantTeam sigma_x("Sigma-X Quant Fund", 15000000.0);

        std::cout << "\n=== 开始组建量化团队 ===\n"
                  << std::endl;

        // 使用工厂模式创建团队成员
        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::QUANT_RESEARCHER, "Alice Chen", 600000, EmployeeLevel::PRINCIPAL));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::QUANT_DEVELOPER, "Bob Wilson", 500000, EmployeeLevel::SENIOR));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::QUANT_DEVELOPER, "Charlie Zhang", 450000, EmployeeLevel::SENIOR));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::TRADER, "David Park", 400000, EmployeeLevel::SENIOR));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::RISK_MANAGER, "Eva Rodriguez", 550000, EmployeeLevel::PRINCIPAL));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::DATA_SCIENTIST, "Frank Liu", 480000, EmployeeLevel::SENIOR));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::PORTFOLIO_MANAGER, "Grace Kim", 650000, EmployeeLevel::DIRECTOR));

        sigma_x.hire(EmployeeFactory::createEmployee(
            EmployeeType::COMPLIANCE_OFFICER, "Henry Brown", 350000, EmployeeLevel::SENIOR));

        // 显示团队信息
        sigma_x.show_team_composition();
        sigma_x.show_budget_status();

        // 开始日常运营
        sigma_x.start_daily_operations();

        // 演示协作
        std::cout << "\n=== 团队协作演示 ===" << std::endl;
        auto alice = sigma_x.find_employee("Alice Chen");
        auto bob = sigma_x.find_employee("Bob Wilson");
        if (alice && bob)
        {
            alice->collaborate_with(*bob);
        }

        // 演示奖金计算
        std::cout << "\n=== 奖金计算演示 ===" << std::endl;
        for (size_t i = 0; i < sigma_x.get_team_size() && i < 3; ++i)
        {
            // 这里简化演示，实际中需要更好的访问方式
            if (alice)
            {
                std::cout << alice->get_name() << " 的年终奖金: $"
                          << alice->calculate_bonus() << std::endl;
                break;
            }
        }
    }
    catch (const QuantTeamException &e)
    {
        std::cerr << "[错误] 团队运营异常: " << e.what() << std::endl;
        return 1;
    }
    catch (const std::exception &e)
    {
        std::cerr << "[错误] 系统异常: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "\n=== 程序执行完成 ===" << std::endl;
    return 0;
}