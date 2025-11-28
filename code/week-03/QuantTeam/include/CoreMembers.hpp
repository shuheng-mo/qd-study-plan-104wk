#pragma once

#include <string>
#include <iostream>
#include "Employee.hpp"

// 1. 量化研究员 (QR) 声明
class QuantResearcher : public Employee
{
public:
    QuantResearcher(const std::string &n, double s);
    void do_work() const override;
    void propose_strategy();
};

// 2. 量化开发 (QD) 声明
class QuantDeveloper : public Employee
{
public:
    QuantDeveloper(const std::string &n, double s);
    void do_work() const override;
    void reject_bad_code();
};

// 3. 交易员 (Trader) 声明
class Trader : public Employee
{
public:
    Trader(const std::string &n, double s);
    void do_work() const override;
};