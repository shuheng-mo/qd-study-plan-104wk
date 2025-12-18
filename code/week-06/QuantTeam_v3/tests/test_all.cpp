#include "QuantTeam.hpp"
#include "StrategyDecorator.hpp"
#include "AdvancedPatterns.hpp"
#include <iostream>
#include <iomanip>
#include <cassert>
#include <cmath>

// 简单的测试断言宏
#define TEST_ASSERT(condition, message)                        \
    do                                                         \
    {                                                          \
        if (!(condition))                                      \
        {                                                      \
            std::cerr << "✗ Test failed: " << message << "\n"; \
            std::cerr << "  at " << __FILE__ << ":" << __LINE__ << "\n"; \
            return false;                                      \
        }                                                      \
    } while (0)

#define RUN_TEST(test_func)                                      \
    do                                                           \
    {                                                            \
        std::cout << "Running " << #test_func << "...\n";        \
        if (test_func())                                         \
        {                                                        \
            std::cout << "✓ " << #test_func << " passed\n\n";    \
        }                                                        \
        else                                                     \
        {                                                        \
            std::cout << "✗ " << #test_func << " failed\n\n";    \
            failed_tests++;                                      \
        }                                                        \
        total_tests++;                                           \
    } while (0)

// 测试 std::variant 值语义多态
bool test_variant_polymorphism()
{
    QuantTeam team("Test Team");

    team.hire(QuantResearcher{"Alice", 600000, EmployeeLevel::SENIOR, 5});
    team.hire(QuantDeveloper{"Bob", 550000, EmployeeLevel::SENIOR, 100});

    TEST_ASSERT(team.size() == 2, "Team should have 2 members");

    double total_salary = team.get_total_salary();
    TEST_ASSERT(std::abs(total_salary - 1150000.0) < 1.0, "Total salary should be correct");

    // 测试值语义拷贝
    auto team_copy = team;
    TEST_ASSERT(team_copy.size() == 2, "Copied team should have same size");

    return true;
}

// 测试 Decorator 装饰器模式
bool test_decorator_pattern()
{
    MarketData data{"AAPL", 150.0};

    std::unique_ptr<Strategy> strategy = std::make_unique<MomentumStrategy>(0.01);
    double signal1 = strategy->execute(data);
    TEST_ASSERT(signal1 > 0.0, "Strategy should return positive signal");

    // 添加缓存装饰器
    strategy = std::make_unique<CachingDecorator>(std::move(strategy));
    double signal2 = strategy->execute(data); // Miss
    double signal3 = strategy->execute(data); // Hit
    TEST_ASSERT(std::abs(signal2 - signal3) < 0.01, "Cached results should match");

    return true;
}

// 测试 PIMPL 编译防火墙
bool test_pimpl_pattern()
{
    Portfolio portfolio("Test Portfolio", 100000.0);

    portfolio.add_position("AAPL", 100, 150.0);
    TEST_ASSERT(portfolio.get_total_value() > 0.0, "Portfolio should have value");

    double initial_value = portfolio.get_total_value();

    // 测试拷贝
    Portfolio portfolio_copy = portfolio;
    TEST_ASSERT(std::abs(portfolio_copy.get_total_value() - initial_value) < 1.0,
                "Copied portfolio should have same value");

    return true;
}

// 测试 Prototype 原型模式
bool test_prototype_pattern()
{
    auto original = std::make_unique<CloneableMomentumStrategy>(0.015, "Original");

    // 克隆策略
    auto cloned = original->clone();
    TEST_ASSERT(cloned != nullptr, "Clone should not be null");
    TEST_ASSERT(cloned->get_name() == "Original", "Clone should have same name");

    // 测试克隆是独立的
    MarketData data{"AAPL", 150.0};
    double signal1 = original->execute(data);
    double signal2 = cloned->execute(data);
    TEST_ASSERT(std::abs(signal1 - signal2) < 0.01, "Clone should produce same results");

    return true;
}

// 测试 Visitor 访问者模式
bool test_visitor_pattern()
{
    std::vector<std::unique_ptr<VisitableEmployee>> employees;
    employees.push_back(std::make_unique<VisitableQuantResearcher>("Alice", 600000, 8));
    employees.push_back(std::make_unique<VisitableQuantDeveloper>("Bob", 550000, 150));

    TEST_ASSERT(employees.size() == 2, "Should have 2 employees");

    // 薪资报告访问者
    SalaryReportVisitor salary_visitor;
    for (const auto &emp : employees)
    {
        emp->accept(salary_visitor);
    }

    double total = salary_visitor.get_total();
    TEST_ASSERT(total > 1000000.0, "Total compensation should exceed 1M");

    return true;
}

// 测试 Employee variant 的各种访问者
bool test_employee_visitors()
{
    QuantResearcher researcher{"Alice", 600000, EmployeeLevel::SENIOR, 8};
    Employee emp = researcher;

    // 测试各种访问者
    std::string name = std::visit(GetNameVisitor{}, emp);
    TEST_ASSERT(name == "Alice", "Name visitor should work");

    double salary = std::visit(GetSalaryVisitor{}, emp);
    TEST_ASSERT(std::abs(salary - 600000.0) < 1.0, "Salary visitor should work");

    double bonus = std::visit(CalculateBonusVisitor{}, emp);
    TEST_ASSERT(bonus > 100000.0, "Bonus should be calculated");

    std::string skills = std::visit(GetSkillsVisitor{}, emp);
    TEST_ASSERT(!skills.empty(), "Skills visitor should work");

    return true;
}

int main()
{
    std::cout << "\n";
    std::cout << "╔════════════════════════════════════════════════════╗\n";
    std::cout << "║      Week 6: QuantTeam v3 单元测试                 ║\n";
    std::cout << "╚════════════════════════════════════════════════════╝\n\n";

    int total_tests = 0;
    int failed_tests = 0;

    // 运行所有测试
    RUN_TEST(test_variant_polymorphism);
    RUN_TEST(test_decorator_pattern);
    RUN_TEST(test_pimpl_pattern);
    RUN_TEST(test_prototype_pattern);
    RUN_TEST(test_visitor_pattern);
    RUN_TEST(test_employee_visitors);

    // 输出测试总结
    std::cout << "\n";
    std::cout << "╔════════════════════════════════════════════════════╗\n";
    std::cout << "║                  测试总结                           ║\n";
    std::cout << "╠════════════════════════════════════════════════════╣\n";
    std::cout << "║  总测试数: " << std::setw(3) << total_tests << "                                   ║\n";
    std::cout << "║  通过数:   " << std::setw(3) << (total_tests - failed_tests) << "                                   ║\n";
    std::cout << "║  失败数:   " << std::setw(3) << failed_tests << "                                   ║\n";

    if (failed_tests == 0)
    {
        std::cout << "║                                                    ║\n";
        std::cout << "║            ✓ 所有测试通过！                        ║\n";
    }
    else
    {
        std::cout << "║                                                    ║\n";
        std::cout << "║            ✗ 部分测试失败                          ║\n";
    }

    std::cout << "╚════════════════════════════════════════════════════╝\n\n";

    return failed_tests == 0 ? 0 : 1;
}
