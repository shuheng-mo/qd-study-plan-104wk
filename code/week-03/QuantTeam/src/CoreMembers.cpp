#include "../include/CoreMembers.hpp"

// 1. 量化研究员 (QR) 实现
QuantResearcher::QuantResearcher(const std::string &n, double s) : Employee(n, s) {}

void QuantResearcher::do_work() const
{
    // QR 的日常：挖因子，搞模型，也许还在抱怨数据不干净
    std::cout << "[QR] " << name << " 正在阅读 ICML 论文，并尝试挖掘新的 Alpha 因子..." << std::endl;
}

// QR 特有的技能
void QuantResearcher::propose_strategy()
{
    std::cout << "[QR] " << name << " 提出只要在这个参数上过拟合一下，回测夏普比率能到 5.0！" << std::endl;
}

// 2. 量化开发 (QD) 实现
QuantDeveloper::QuantDeveloper(const std::string &n, double s) : Employee(n, s) {}

void QuantDeveloper::do_work() const
{
    // QD 的日常：优化代码，骂编译器，骂网络延迟
    std::cout << "[QD] " << name << " 正在重写订单网关，试图削减掉 5 微秒的延迟..." << std::endl;
}

// QD 特有的技能
void QuantDeveloper::reject_bad_code()
{
    std::cout << "[QD] " << name << " 拒绝了 QR 的代码提交：'内存泄漏太严重，不能上线'。" << std::endl;
}

// 3. 交易员 (Trader) 实现
Trader::Trader(const std::string &n, double s) : Employee(n, s) {}

void Trader::do_work() const
{
    // Trader 的日常：盯盘，甚至有点迷信
    std::cout << "[Trader] " << name << " 正在紧盯波动率指数，并祈祷今天不要爆仓。" << std::endl;
}