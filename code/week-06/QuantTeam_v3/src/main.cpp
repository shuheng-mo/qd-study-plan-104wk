#include "QuantTeam.hpp"
#include "StrategyDecorator.hpp"
#include "AdvancedPatterns.hpp"
#include <iostream>
#include <iomanip>
#include <memory>

void print_section_header(const std::string &title)
{
    std::cout << "\n\n";
    std::cout << "╔═══════════════════════════════════════════════════════════════╗\n";
    std::cout << "║  " << std::left << std::setw(60) << title << "║\n";
    std::cout << "╚═══════════════════════════════════════════════════════════════╝\n\n";
}

// 演示 std::variant 值语义多态
void demo_variant_polymorphism()
{
    print_section_header("Demo 1: std::variant 值语义多态");

    std::cout << "创建量化团队，使用 std::variant 实现值语义多态...\n\n";

    QuantTeam team("Sigma-X Quant Fund");

    // 雇佣不同类型的员工 - 无需指针！
    team.hire(QuantResearcher{"Alice Zhang", 600000, EmployeeLevel::SENIOR, 8});
    team.hire(QuantDeveloper{"Bob Chen", 550000, EmployeeLevel::SENIOR, 150});
    team.hire(Trader{"Charlie Wang", 500000, EmployeeLevel::LEAD, 1500000.0});
    team.hire(RiskManager{"Diana Li", 520000, EmployeeLevel::SENIOR, 12});

    // 打印团队信息
    team.print_team_info();

    // 开始日常工作
    team.start_daily_operations();

    // 值语义的好处：可以直接拷贝！
    std::cout << "复制团队（值语义）...\n";
    auto team_copy = team;
    std::cout << "复制成功！原团队大小: " << team.size()
              << ", 副本大小: " << team_copy.size() << "\n";
}

// 演示 Decorator 装饰器模式
void demo_decorator_pattern()
{
    print_section_header("Demo 2: Decorator 装饰器模式");

    std::cout << "创建基础策略并动态添加功能...\n\n";

    MarketData apple{"AAPL", 150.0, 1000000};
    MarketData tesla{"TSLA", 200.0, 2000000};

    // 1. 基础策略
    std::cout << "1. 基础动量策略:\n";
    std::unique_ptr<Strategy> strategy = std::make_unique<MomentumStrategy>(0.02);
    strategy->execute(apple);
    std::cout << "\n";

    // 2. 添加日志装饰
    std::cout << "2. 添加日志装饰:\n";
    strategy = std::make_unique<LoggingDecorator>(std::move(strategy));
    strategy->execute(apple);

    // 3. 添加缓存装饰
    std::cout << "3. 添加缓存装饰:\n";
    strategy = std::make_unique<CachingDecorator>(std::move(strategy));
    strategy->execute(apple);  // Miss
    strategy->execute(apple);  // Hit!
    strategy->execute(tesla);  // Miss
    strategy->execute(apple);  // Hit!
    std::cout << "\n";

    // 4. 添加计时装饰
    std::cout << "4. 添加计时装饰:\n";
    strategy = std::make_unique<TimingDecorator>(std::move(strategy));
    strategy->execute(apple); // Hit + Timing
    std::cout << "\n";

    // 5. 添加信号过滤装饰
    std::cout << "5. 添加信号过滤装饰:\n";
    strategy = std::make_unique<SignalFilterDecorator>(std::move(strategy), 1.0, 5.0);
    strategy->execute(apple);
    strategy->execute(tesla);
}

// 演示 PIMPL 编译防火墙
void demo_pimpl_pattern()
{
    print_section_header("Demo 3: PIMPL 编译防火墙");

    std::cout << "创建投资组合（PIMPL 隐藏实现细节）...\n\n";

    Portfolio portfolio("Alpha Strategy Portfolio", 1000000.0);

    std::cout << "\n添加持仓:\n";
    portfolio.add_position("AAPL", 1000, 150.0);
    portfolio.add_position("GOOGL", 500, 280.0);
    portfolio.add_position("MSFT", 800, 350.0);

    portfolio.print_positions();

    std::cout << "移除部分持仓:\n";
    portfolio.remove_position("GOOGL");

    portfolio.print_positions();

    // PIMPL 支持拷贝
    std::cout << "拷贝投资组合:\n";
    Portfolio portfolio_copy = portfolio;
    std::cout << "拷贝成功！原组合: " << portfolio.get_name()
              << ", 副本: " << portfolio_copy.get_name() << "\n";
}

// 演示 Prototype 原型模式
void demo_prototype_pattern()
{
    print_section_header("Demo 4: Prototype 原型模式");

    std::cout << "创建策略原型并克隆...\n\n";

    // 创建原型策略
    std::vector<std::unique_ptr<CloneableStrategy>> strategies;

    auto momentum = std::make_unique<CloneableMomentumStrategy>(0.015, "Momentum-1");
    auto mean_rev = std::make_unique<CloneableMeanReversionStrategy>(120.0, "MeanRev-1");

    strategies.push_back(std::move(momentum));
    strategies.push_back(std::move(mean_rev));

    // 测试原型
    MarketData data{"AAPL", 150.0};
    std::cout << "测试原型策略:\n";
    for (const auto &strat : strategies)
    {
        strat->execute(data);
    }

    // 克隆策略
    std::cout << "\n克隆策略（虚构造函数）:\n";
    std::vector<std::unique_ptr<CloneableStrategy>> cloned_strategies;

    for (const auto &strat : strategies)
    {
        auto cloned = strat->clone();
        std::cout << "克隆了策略: " << cloned->get_name() << "\n";
        cloned_strategies.push_back(std::move(cloned));
    }

    std::cout << "\n测试克隆的策略:\n";
    for (const auto &strat : cloned_strategies)
    {
        strat->execute(data);
    }
}

// 演示 Visitor 访问者模式
void demo_visitor_pattern()
{
    print_section_header("Demo 5: Visitor 访问者模式");

    std::cout << "创建可访问的员工并使用不同访问者...\n\n";

    // 创建员工（可访问版本）
    std::vector<std::unique_ptr<VisitableEmployee>> employees;

    employees.push_back(std::make_unique<VisitableQuantResearcher>("Alice", 600000, 8));
    employees.push_back(std::make_unique<VisitableQuantDeveloper>("Bob", 550000, 150));
    employees.push_back(std::make_unique<VisitableTrader>("Charlie", 500000, 1500000.0));

    // 访问者 1: 薪资报告
    std::cout << "访问者 1: 生成薪资报告\n";
    SalaryReportVisitor salary_visitor;
    for (const auto &emp : employees)
    {
        emp->accept(salary_visitor);
    }
    salary_visitor.print_report();

    // 访问者 2: 性能评估
    std::cout << "访问者 2: 性能评估\n";
    PerformanceEvaluator perf_visitor;
    for (const auto &emp : employees)
    {
        emp->accept(perf_visitor);
    }
    perf_visitor.print_evaluation();
}

int main()
{
    std::cout << "\n";
    std::cout << "╔═══════════════════════════════════════════════════════════════╗\n";
    std::cout << "║                                                               ║\n";
    std::cout << "║      Week 6: OOP 现代化 - 值语义多态与现代设计模式            ║\n";
    std::cout << "║                                                               ║\n";
    std::cout << "║  技术栈:                                                      ║\n";
    std::cout << "║    1. std::variant - 值语义多态                               ║\n";
    std::cout << "║    2. Decorator - 装饰器模式                                  ║\n";
    std::cout << "║    3. PIMPL - 编译防火墙                                      ║\n";
    std::cout << "║    4. Prototype - 原型模式                                    ║\n";
    std::cout << "║    5. Visitor - 访问者模式                                    ║\n";
    std::cout << "║                                                               ║\n";
    std::cout << "╚═══════════════════════════════════════════════════════════════╝\n";

    try
    {
        // 演示所有 Week 6 的 OOP 技术
        demo_variant_polymorphism();
        demo_decorator_pattern();
        demo_pimpl_pattern();
        demo_prototype_pattern();
        demo_visitor_pattern();

        std::cout << "\n\n";
        std::cout << "╔═══════════════════════════════════════════════════════════════╗\n";
        std::cout << "║                     所有演示完成！                             ║\n";
        std::cout << "╚═══════════════════════════════════════════════════════════════╝\n\n";
    }
    catch (const std::exception &e)
    {
        std::cerr << "\n错误: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
