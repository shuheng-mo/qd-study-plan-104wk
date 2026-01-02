#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include "../include/Exceptions.hpp"
#include "../include/ExceptionSafety.hpp"
#include "../include/Expected.hpp"
#include "../include/ErrorCode.hpp"
#include "../include/ExceptionPropagation.hpp"

/**
 * Week 8 - C++ 异常处理演示程序
 *
 * 演示内容：
 * 1. 异常层次结构 - 细粒度的异常处理
 * 2. RAII 与异常安全 - Transaction 和 ScopeGuard
 * 3. Expected<T, E> - 函数式错误处理
 * 4. error_code - 轻量级错误码
 * 5. 异常传播 - 多线程和嵌套异常
 */

// 演示函数声明
void demo_exception_hierarchy();
void demo_exception_safety();
void demo_expected();
void demo_error_code();
void demo_exception_propagation();

// 辅助数据结构
struct Employee {
    int id;
    std::string name;
    double salary;

    Employee() : id(0), name(""), salary(0.0) {}
    Employee(int i, std::string n, double s)
        : id(i), name(std::move(n)), salary(s) {}
};

// 业务类 - 用于演示
class QuantTeam {
private:
    std::vector<Employee> members;
    double budget;

public:
    QuantTeam() : budget(1000000.0) {}

    void add_employee(const Employee& emp) {
        // 验证
        if (emp.id <= 0) {
            throw InvalidEmployeeException("Employee ID must be positive");
        }

        // 检查重复
        for (const auto& m : members) {
            if (m.id == emp.id) {
                throw DuplicateEmployeeException(
                    std::format("Employee with ID {} already exists", emp.id));
            }
        }

        // 检查预算
        if (emp.salary > budget) {
            throw InsufficientFundsException(
                std::format("Insufficient budget. Need ${:.2f}, have ${:.2f}",
                           emp.salary, budget));
        }

        // 使用事务保证强异常安全
        Transaction tx(members);
        members.push_back(emp);
        tx.commit();

        budget -= emp.salary;
    }

    const std::vector<Employee>& get_members() const { return members; }
    double get_budget() const { return budget; }
    size_t size() const { return members.size(); }
};

int main() {
    std::cout << R"(
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           Week 8 - C++ 异常处理与错误管理演示程序                   ║
║                                                                   ║
║  本周学习内容：                                                     ║
║  1. 异常层次结构 - 细粒度的异常分类与处理                          ║
║  2. RAII 与异常安全 - 强异常保证                                   ║
║  3. Expected<T, E> - 函数式错误处理                               ║
║  4. error_code - 轻量级系统错误处理                                ║
║  5. 异常传播 - 多线程和嵌套异常                                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
)" << std::endl;

    try {
        // 演示1: 异常层次结构
        demo_exception_hierarchy();

        // 演示2: RAII 与异常安全
        demo_exception_safety();

        // 演示3: Expected
        demo_expected();

        // 演示4: error_code
        demo_error_code();

        // 演示5: 异常传播
        demo_exception_propagation();

        std::cout << "\n✓ 所有演示完成！\n" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "❌ Fatal Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

/**
 * 演示1: 异常层次结构
 */
void demo_exception_hierarchy() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示1: 异常层次结构 - 细粒度异常处理\n";
    std::cout << std::string(70, '=') << "\n";

    QuantTeam team;

    // 场景1: 无效员工ID
    std::cout << "\n场景1: 尝试添加无效ID的员工...\n";
    try {
        team.add_employee(Employee{-1, "Invalid", 80000});
    } catch (const InvalidEmployeeException& e) {
        std::cout << "✓ 捕获到 InvalidEmployeeException: " << e.get_message() << "\n";
        std::cout << "  位置: " << e.where().file_name()
                  << ":" << e.where().line() << "\n";
    }

    // 场景2: 重复员工
    std::cout << "\n场景2: 尝试添加重复员工...\n";
    try {
        team.add_employee(Employee{1, "Alice", 120000});
        team.add_employee(Employee{1, "Bob", 110000});  // 重复ID
    } catch (const DuplicateEmployeeException& e) {
        std::cout << "✓ 捕获到 DuplicateEmployeeException: " << e.get_message() << "\n";
    }

    // 场景3: 资金不足
    std::cout << "\n场景3: 尝试添加超出预算的员工...\n";
    try {
        team.add_employee(Employee{2, "Charlie", 2000000});  // 超出预算
    } catch (const InsufficientFundsException& e) {
        std::cout << "✓ 捕获到 InsufficientFundsException: " << e.get_message() << "\n";
    }

    // 场景4: 分层捕获
    std::cout << "\n场景4: 分层捕获演示...\n";
    try {
        team.add_employee(Employee{-5, "Invalid", 80000});
    } catch (const InvalidEmployeeException& e) {
        std::cout << "✓ 捕获到具体异常: InvalidEmployeeException\n";
    } catch (const BusinessException& e) {
        std::cout << "  捕获到业务异常（不会到这里）\n";
    } catch (const QuantTeamException& e) {
        std::cout << "  捕获到框架异常（不会到这里）\n";
    }

    std::cout << "\n当前团队成员数: " << team.size() << "\n";
    std::cout << "剩余预算: $" << team.get_budget() << "\n";
    std::cout << "\n✓ 异常层次结构演示完成\n";
}

/**
 * 演示2: RAII 与异常安全
 */
void demo_exception_safety() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示2: RAII 与异常安全 - 强异常保证\n";
    std::cout << std::string(70, '=') << "\n";

    // 场景1: Transaction 事务保证
    std::cout << "\n场景1: Transaction 提供强异常保证...\n";
    {
        std::vector<int> data = {1, 2, 3, 4, 5};
        std::cout << "原始数据: ";
        for (int x : data) std::cout << x << " ";
        std::cout << "\n";

        try {
            Transaction tx(data);
            data.push_back(6);
            data.push_back(7);
            std::cout << "修改后数据: ";
            for (int x : data) std::cout << x << " ";
            std::cout << "\n";

            // 模拟错误 - 事务会自动回滚
            throw std::runtime_error("Simulated error");

            tx.commit();  // 不会执行
        } catch (const std::exception& e) {
            std::cout << "✓ 捕获异常，事务自动回滚\n";
        }

        std::cout << "回滚后数据: ";
        for (int x : data) std::cout << x << " ";
        std::cout << "\n";
    }

    // 场景2: ScopeGuard 自动清理
    std::cout << "\n场景2: ScopeGuard 确保资源释放...\n";
    {
        bool resource_released = false;

        try {
            auto guard = make_scope_guard([&resource_released]() {
                resource_released = true;
                std::cout << "✓ ScopeGuard 执行清理操作\n";
            });

            std::cout << "执行一些操作...\n";
            throw std::runtime_error("Something went wrong");

        } catch (const std::exception& e) {
            std::cout << "捕获异常: " << e.what() << "\n";
        }

        std::cout << "资源是否释放: " << (resource_released ? "是" : "否") << "\n";
    }

    // 场景3: 异常安全的向量操作
    std::cout << "\n场景3: 异常安全的批量操作...\n";
    {
        std::vector<int> vec = {1, 2, 3};
        std::vector<int> items = {4, 5, 6};

        std::cout << "原始向量: ";
        for (int x : vec) std::cout << x << " ";
        std::cout << "\n";

        ExceptionSafeOps::append_all(vec, items);

        std::cout << "添加后向量: ";
        for (int x : vec) std::cout << x << " ";
        std::cout << "\n";
    }

    std::cout << "\n✓ RAII与异常安全演示完成\n";
}

/**
 * 演示3: Expected<T, E> - 函数式错误处理
 */

// 模拟数据加载函数
Expected<Employee, std::string> load_employee(int id) {
    if (id <= 0) {
        return Unexpected<std::string>("Invalid employee ID");
    }

    if (id == 999) {
        return Unexpected<std::string>("Employee not found");
    }

    return Employee{id, "Alice Johnson", 120000};
}

// 验证薪资
Expected<double, std::string> validate_salary(const Employee& emp) {
    if (emp.salary < 50000) {
        return Unexpected<std::string>("Salary too low");
    }
    if (emp.salary > 500000) {
        return Unexpected<std::string>("Salary too high");
    }
    return emp.salary;
}

void demo_expected() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示3: Expected<T, E> - 函数式错误处理\n";
    std::cout << std::string(70, '=') << "\n";

    // 场景1: 基本使用
    std::cout << "\n场景1: 加载员工数据...\n";
    {
        auto result = load_employee(1);
        if (result) {
            std::cout << "✓ 成功加载: " << result->name
                      << ", 薪资: $" << result->salary << "\n";
        } else {
            std::cout << "❌ 加载失败: " << result.error() << "\n";
        }
    }

    // 场景2: 错误处理
    std::cout << "\n场景2: 处理加载错误...\n";
    {
        auto result = load_employee(-1);
        if (!result) {
            std::cout << "✓ 预期的错误: " << result.error() << "\n";
        }
    }

    // 场景3: value_or 提供默认值
    std::cout << "\n场景3: 使用默认值...\n";
    {
        auto result = load_employee(999);
        Employee emp = result.value_or(Employee{0, "Default Employee", 50000});
        std::cout << "✓ 使用的员工: " << emp.name << "\n";
    }

    // 场景4: 链式调用 and_then
    std::cout << "\n场景4: 链式调用...\n";
    {
        auto result = load_employee(1)
            .and_then([](const Employee& emp) -> Expected<double, std::string> {
                return validate_salary(emp);
            });

        if (result) {
            std::cout << "✓ 验证通过，薪资: $" << *result << "\n";
        } else {
            std::cout << "❌ 验证失败: " << result.error() << "\n";
        }
    }

    // 场景5: transform 转换值
    std::cout << "\n场景5: 转换值...\n";
    {
        auto result = load_employee(1)
            .transform([](const Employee& emp) {
                return emp.salary * 1.1;  // 加薪10%
            });

        if (result) {
            std::cout << "✓ 加薪后: $" << *result << "\n";
        }
    }

    std::cout << "\n✓ Expected 演示完成\n";
}

/**
 * 演示4: error_code - 轻量级错误码
 */

// 使用 error_code 的函数
std::error_code hire_employee(QuantTeam& team, const Employee& emp) {
    if (emp.id <= 0) {
        return QuantTeamError::INVALID_EMPLOYEE_ID;
    }

    for (const auto& m : team.get_members()) {
        if (m.id == emp.id) {
            return QuantTeamError::DUPLICATE_EMPLOYEE;
        }
    }

    if (emp.salary > team.get_budget()) {
        return QuantTeamError::INSUFFICIENT_FUNDS;
    }

    try {
        const_cast<QuantTeam&>(team).add_employee(emp);
    } catch (...) {
        return QuantTeamError::STRATEGY_FAILED;
    }

    return QuantTeamError::SUCCESS;
}

void demo_error_code() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示4: error_code - 轻量级错误码\n";
    std::cout << std::string(70, '=') << "\n";

    QuantTeam team;

    // 场景1: 成功情况
    std::cout << "\n场景1: 成功雇佣员工...\n";
    {
        auto ec = hire_employee(team, Employee{1, "Alice", 120000});
        if (!ec) {
            std::cout << "✓ 员工雇佣成功\n";
        } else {
            std::cout << "❌ 错误: " << ec.message() << "\n";
        }
    }

    // 场景2: 错误处理
    std::cout << "\n场景2: 处理各种错误...\n";
    {
        // 无效ID
        auto ec1 = hire_employee(team, Employee{-1, "Bob", 110000});
        if (ec1) {
            std::cout << "✓ 捕获错误: " << ErrorCodeUtils::format_error(ec1) << "\n";
        }

        // 重复员工
        auto ec2 = hire_employee(team, Employee{1, "Charlie", 100000});
        if (ec2) {
            std::cout << "✓ 捕获错误: " << ErrorCodeUtils::format_error(ec2) << "\n";
        }

        // 资金不足
        auto ec3 = hire_employee(team, Employee{10, "David", 5000000});
        if (ec3) {
            std::cout << "✓ 捕获错误: " << ErrorCodeUtils::format_error(ec3) << "\n";
        }
    }

    // 场景3: Result 类型
    std::cout << "\n场景3: Result 包装返回值和错误...\n";
    {
        auto get_employee_name = [&team](int id) -> Result<std::string> {
            if (id <= 0) {
                return Result<std::string>(QuantTeamError::INVALID_EMPLOYEE_ID);
            }

            for (const auto& m : team.get_members()) {
                if (m.id == id) {
                    return Result<std::string>(m.name);
                }
            }

            return Result<std::string>(QuantTeamError::DUPLICATE_EMPLOYEE);
        };

        auto result = get_employee_name(1);
        if (result) {
            std::cout << "✓ 找到员工: " << result.get() << "\n";
        } else {
            std::cout << "❌ 错误: " << result.error.message() << "\n";
        }
    }

    std::cout << "\n✓ error_code 演示完成\n";
}

/**
 * 演示5: 异常传播
 */
void demo_exception_propagation() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示5: 异常传播 - 多线程和嵌套异常\n";
    std::cout << std::string(70, '=') << "\n";

    // 场景1: 多线程异常传播
    std::cout << "\n场景1: 多线程异常传播...\n";
    {
        AsyncTaskManager manager;

        // 运行一些任务，其中一些会失败
        manager.run_task([]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
            std::cout << "  Task 1 完成\n";
        });

        manager.run_task([]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(30));
            throw std::runtime_error("Task 2 失败");
        });

        manager.run_task([]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(20));
            std::cout << "  Task 3 完成\n";
        });

        manager.wait_all();

        if (manager.has_exceptions()) {
            std::cout << "✓ 检测到 " << manager.exception_count() << " 个异常\n";
            manager.handle_all_exceptions([](const std::exception& e) {
                std::cout << "  处理异常: " << e.what() << "\n";
            });
        }
    }

    // 场景2: 嵌套异常
    std::cout << "\n场景2: 嵌套异常演示...\n";
    {
        auto inner_function = []() {
            throw std::runtime_error("Inner error: database connection failed");
        };

        auto middle_function = [&inner_function]() {
            try {
                inner_function();
            } catch (...) {
                std::throw_with_nested(
                    std::runtime_error("Middle error: failed to load data")
                );
            }
        };

        auto outer_function = [&middle_function]() {
            try {
                middle_function();
            } catch (...) {
                std::throw_with_nested(
                    std::runtime_error("Outer error: operation failed")
                );
            }
        };

        try {
            outer_function();
        } catch (const std::exception& e) {
            std::cout << "✓ 捕获嵌套异常，深度: "
                      << NestedExceptionUtils::get_nesting_depth(e) << "\n";
            std::cout << "\n完整调用链:\n";
            NestedExceptionUtils::print_nested_exception(e);
        }
    }

    // 场景3: 异常聚合
    std::cout << "\n场景3: 异常聚合...\n";
    {
        ExceptionAggregator aggregator;

        aggregator.try_execute([]() {
            std::cout << "  操作1 成功\n";
        }, "Operation 1");

        aggregator.try_execute([]() {
            throw std::runtime_error("操作2失败");
        }, "Operation 2");

        aggregator.try_execute([]() {
            std::cout << "  操作3 成功\n";
        }, "Operation 3");

        aggregator.try_execute([]() {
            throw std::runtime_error("操作4失败");
        }, "Operation 4");

        if (aggregator.has_exceptions()) {
            std::cout << "\n✓ 收集到 " << aggregator.exception_count() << " 个异常:\n";
            aggregator.print_all();
        }
    }

    // 场景4: 重试策略
    std::cout << "\n场景4: 重试策略...\n";
    {
        int attempt_count = 0;
        RetryPolicy retry(2, 100);  // 最多重试2次，每次延迟100ms

        try {
            retry.execute_with_retry([&attempt_count]() {
                attempt_count++;
                std::cout << "  尝试次数: " << attempt_count << "\n";
                if (attempt_count < 2) {
                    throw std::runtime_error("操作暂时失败");
                }
                std::cout << "  ✓ 操作成功!\n";
            });
        } catch (const std::exception& e) {
            std::cout << "❌ 所有重试失败: " << e.what() << "\n";
        }
    }

    std::cout << "\n✓ 异常传播演示完成\n";
}
