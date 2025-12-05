#include "../include/EmployeeFactory.hpp"
#include "../include/CoreMembers.hpp"
#include <stdexcept>

std::unique_ptr<Employee> EmployeeFactory::createEmployee(
    EmployeeType type,
    const std::string &name,
    double salary,
    EmployeeLevel level)
{
    switch (type)
    {
    case EmployeeType::QUANT_RESEARCHER:
        return std::make_unique<QuantResearcher>(name, salary, level);
    case EmployeeType::QUANT_DEVELOPER:
        return std::make_unique<QuantDeveloper>(name, salary, level);
    case EmployeeType::TRADER:
        return std::make_unique<Trader>(name, salary, level);
    case EmployeeType::RISK_MANAGER:
        return std::make_unique<RiskManager>(name, salary, level);
    case EmployeeType::PORTFOLIO_MANAGER:
        return std::make_unique<PortfolioManager>(name, salary, level);
    case EmployeeType::DATA_SCIENTIST:
        return std::make_unique<DataScientist>(name, salary, level);
    case EmployeeType::COMPLIANCE_OFFICER:
        return std::make_unique<ComplianceOfficer>(name, salary, level);
    default:
        throw std::invalid_argument("未知的员工类型");
    }
}