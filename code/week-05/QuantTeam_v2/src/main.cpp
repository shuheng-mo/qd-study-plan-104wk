#include <iostream>
#include <vector>
#include <memory>
#include "../include/StrongID.hpp"
#include "../include/Types.hpp"
#include "../include/EmployeeBase.hpp"
#include "../include/Employees.hpp"
#include "../include/Mixins.hpp"
#include "../include/PolicyBased.hpp"
#include "../include/TypeErasure.hpp"

void print_section(const std::string& title) {
    std::cout << "\n" << std::string(60, '=') << "\n";
    std::cout << "  " << title << "\n";
    std::cout << std::string(60, '=') << "\n";
}

// 演示 CRTP 静态多态
void demo_crtp() {
    print_section("优化 1: CRTP 静态多态 - 零虚函数开销");

    QuantResearcher alice(EmployeeID{1001}, "Alice Chen", 600000, EmployeeLevel::PRINCIPAL);
    QuantDeveloper bob(EmployeeID{1002}, "Bob Wilson", 500000, EmployeeLevel::SENIOR);
    Trader charlie(EmployeeID{1003}, "Charlie Zhang", 400000, EmployeeLevel::SENIOR);

    std::cout << "\n【普通 CRTP 员工工作演示】\n";
    alice.do_work();
    std::cout << "  技能: " << alice.get_skills() << "\n";
    std::cout << "  年终奖: $" << alice.calculate_bonus() << "\n";

    std::cout << "\n";
    bob.do_work();
    std::cout << "  技能: " << bob.get_skills() << "\n";
    std::cout << "  年终奖: $" << bob.calculate_bonus() << "\n";
}

// 演示 Mixin 功能组合
void demo_mixins() {
    print_section("优化 2: Mixin 类 - 功能组合（不修改原类）");

    // 带日志的研究员
    std::cout << "\n【组合 1: 带日志功能的员工】\n";
    LoggableEmployee<QuantResearcher> alice_with_log(
        EmployeeID{2001}, "Alice (日志版)", 600000, EmployeeLevel::PRINCIPAL
    );
    alice_with_log.do_work();

    // 带指标采集的开发员
    std::cout << "\n【组合 2: 带指标采集的员工】\n";
    MetricsEmployee<QuantDeveloper> bob_with_metrics(
        EmployeeID{2002}, "Bob (指标版)", 500000, EmployeeLevel::SENIOR
    );
    bob_with_metrics.do_work();
    bob_with_metrics.do_work();  // 第二次
    std::cout << "  总任务数: " << bob_with_metrics.get_task_count() << "\n";

    // 完全增强的交易员（日志 + 指标）
    std::cout << "\n【组合 3: 完全增强（日志 + 指标）】\n";
    EnhancedEmployee<Trader> charlie_enhanced(
        EmployeeID{2003}, "Charlie (增强版)", 400000, EmployeeLevel::SENIOR
    );
    charlie_enhanced.do_work();

    // 完整功能（权限 + 日志 + 指标）
    std::cout << "\n【组合 4: 完整功能（权限 + 日志 + 指标）】\n";
    FullFeaturedEmployee<RiskManager> david_full(
        EmployeeID{2004}, "David (完整版)", 550000, EmployeeLevel::PRINCIPAL
    );

    std::cout << "\n  权限不足时：\n";
    david_full.do_work();  // 权限等级 1，失败

    std::cout << "\n  提升权限后：\n";
    david_full.set_permission_level(3);
    david_full.do_work();  // 成功
}

// 演示 Policy-Based Design
void demo_policy_based() {
    print_section("优化 3: Policy-Based Design - 编译期策略绑定");

    std::cout << "\n【Policy-Based 员工 - 策略在编译期决定】\n";

    PolicyResearcher researcher("Emma (研究员)", 600000);
    researcher.do_work();
    researcher.set_performance(1.2);
    researcher.show_bonus_info();

    PolicyDeveloper developer("Frank (开发员)", 500000);
    developer.do_work();
    developer.show_bonus_info();

    PolicyTrader trader("Grace (交易员)", 450000);
    trader.do_work();
    trader.set_performance(1.5);
    trader.show_bonus_info();
}

// 演示强类型 ID 系统
void demo_strong_id() {
    print_section("优化 4: 强类型 ID 系统 - 编译期类型检查");

    EmployeeID emp_id{1001};
    OrderID order_id{5001};

    std::cout << "\n【类型安全的 ID】\n";
    std::cout << "  员工 ID: " << emp_id.get() << " (有效: "
              << (emp_id.is_valid() ? "是" : "否") << ")\n";
    std::cout << "  订单 ID: " << order_id.get() << " (有效: "
              << (order_id.is_valid() ? "是" : "否") << ")\n";

    // 编译期类型检查
    std::cout << "\n  ID 比较:\n";
    EmployeeID emp_id2{1001};
    if (emp_id == emp_id2) {
        std::cout << "    ✓ 相同类型的 ID 可以比较\n";
    }

    // 以下代码会导致编译错误（已注释）：
    // if (emp_id == order_id) {  // 编译错误！不同类型的 ID 不能比较
    //     ...
    // }

    std::cout << "    ✓ 不同类型的 ID 无法比较（编译期保证）\n";
}

// 演示 Type Erasure
void demo_type_erasure() {
    print_section("优化 5: Type Erasure - 无需继承的统一接口");

    std::cout << "\n【Type Erasure - 可以包装任何类型】\n";

    // 创建策略容器 - 包装不同类型
    std::vector<AnyStrategy> strategies;

    // 添加不同类型的策略（无需继承共同基类）
    strategies.emplace_back(SimpleStrategy{});
    strategies.emplace_back(ComplexStrategy{});
    strategies.emplace_back(LambdaStrategy{[](const std::string& name) {
        std::cout << "  [Lambda策略] " << name << " 使用 lambda 执行动态策略\n";
    }});

    // 统一调用
    std::cout << "\n  执行所有策略（统一接口）:\n";
    for (const auto& strategy : strategies) {
        std::cout << "\n  策略名称: " << strategy.get_name() << "\n";
        strategy.execute("测试员工");
    }

    // 测试拷贝语义
    std::cout << "\n【值语义 - 可以拷贝】\n";
    AnyStrategy copy = strategies[0];
    std::cout << "  拷贝的策略: " << copy.get_name() << "\n";
    copy.execute("拷贝测试");
}

// 综合演示
void demo_combined() {
    print_section("综合演示：组合多种技术");

    std::cout << "\n【场景：使用 Mixin + CRTP 创建高级员工】\n";

    // 创建一个带日志和指标的研究员
    using AdvancedResearcher = EnhancedEmployee<QuantResearcher>;

    AdvancedResearcher advanced_alice(
        EmployeeID{9001}, "Alice (高级版)", 700000, EmployeeLevel::DIRECTOR
    );

    std::cout << "\n  第一次执行:\n";
    advanced_alice.do_work();

    std::cout << "\n  第二次执行:\n";
    advanced_alice.do_work();

    std::cout << "\n  员工信息:\n";
    std::cout << "    姓名: " << advanced_alice.get_name() << "\n";
    std::cout << "    薪资: $" << advanced_alice.get_salary() << "\n";
    std::cout << "    等级: " << level_to_string(advanced_alice.get_level()) << "\n";
    std::cout << "    技能: " << advanced_alice.get_skills() << "\n";
    std::cout << "    年终奖: $" << advanced_alice.calculate_bonus() << "\n";
    std::cout << "    任务数: " << advanced_alice.get_task_count() << "\n";
}

int main() {
    std::cout << "\n";
    std::cout << "╔════════════════════════════════════════════════════════════╗\n";
    std::cout << "║   量化私募团队框架 v2.0 - Week 5 OOP 高级技术演示         ║\n";
    std::cout << "╚════════════════════════════════════════════════════════════╝\n";

    try {
        // 1. CRTP 静态多态
        demo_crtp();

        // 2. Mixin 功能组合
        demo_mixins();

        // 3. Policy-Based Design
        demo_policy_based();

        // 4. 强类型 ID
        demo_strong_id();

        // 5. Type Erasure
        demo_type_erasure();

        // 6. 综合演示
        demo_combined();

        print_section("所有演示完成！");
        std::cout << "\n✅ Week 5 所有 OOP 高级技术已成功展示\n\n";

        std::cout << "技术总结:\n";
        std::cout << "  1. CRTP - 零虚函数开销的静态多态\n";
        std::cout << "  2. Mixin - 功能组合（日志、指标、权限）\n";
        std::cout << "  3. Policy-Based - 编译期策略绑定\n";
        std::cout << "  4. 强类型 ID - 编译期类型安全\n";
        std::cout << "  5. Type Erasure - 无继承的统一接口\n\n";

        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "\n❌ 错误: " << e.what() << "\n";
        return 1;
    }
}
