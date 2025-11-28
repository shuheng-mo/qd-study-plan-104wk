#include "../include/QuantTeam.hpp"

// 团队管理类实现

// 招人 - 使用智能指针
void QuantTeam::hire(std::unique_ptr<Employee> e)
{
    team_members.push_back(std::move(e));
}

// 每日早会：一声令下，全员开工
void QuantTeam::start_daily_operations()
{
    std::cout << "--- 市场开盘，团队开始运作 ---" << std::endl;

    // 这里的 e 是 Employee 指针
    // 但编译器会在运行时（Runtime）去查看它指向的到底是 QR 还是 QD
    // 这就是 动态绑定 (Dynamic Binding)
    for (const auto &e : team_members)
    {
        e->do_work();
    }
    std::cout << "-----------------------------" << std::endl;
}