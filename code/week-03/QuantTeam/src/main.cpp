#include "../include/QuantTeam.hpp"
#include "../include/CoreMembers.hpp"
#include <memory>

int main()
{
    QuantTeam sigma_x;

    // 1. 组建团队 (使用智能指针，更安全的内存管理)
    // 注意：QR 通常比较贵，QD 比较苦，Trader 比较像赌徒
    sigma_x.hire(std::make_unique<QuantResearcher>("Alice", 500000));
    sigma_x.hire(std::make_unique<QuantDeveloper>("Bob", 400000));
    sigma_x.hire(std::make_unique<QuantDeveloper>("Charlie", 350000)); // 需要两个 QD 才能伺候一个 QR
    sigma_x.hire(std::make_unique<Trader>("Dave", 300000));

    // 2. 运作
    // 你会看到每个人根据自己的身份，做出了不同的反应
    sigma_x.start_daily_operations();

    // 3. 甚至可以进行强制类型转换 (dynamic_cast) 来展示特定的互动
    // 假设我们要找一个能写 C++ 的人来修 Bug
    // 这在 C++ 中叫 RTTI (Run-Time Type Information)
    /* 注意：虽然通常不建议过度使用 dynamic_cast，
       但在量化团队管理中，有时你确实需要知道“谁是专门负责写代码的”
    */

    return 0;
}