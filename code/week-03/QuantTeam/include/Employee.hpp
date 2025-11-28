#pragma once

#include <iostream>
#include <string>
#include <vector>

// 这是一个抽象基类（Abstract Base Class）
class Employee
{
protected:
    // protected 意味着：外部不能访问，但子类（QR, QD）可以访问
    // 毕竟只有继承了“员工”身份，才有资格谈薪水
    std::string name;
    double base_salary;

public:
    Employee(const std::string &n, double s) : name(n), base_salary(s) {}

    // 虚析构函数：非常重要！
    // 否则当你解雇（delete）一个员工时，只会清理基类部分，导致内存泄漏
    virtual ~Employee() {}

    // 纯虚函数 (Pure Virtual Function)
    // "= 0" 的意思是：我作为基类不知道具体怎么干活，
    // 但凡是我的子类，必须把这个函数实现了，否则不能入职。
    virtual void do_work() const = 0;

    // 普通成员函数
    std::string get_name() const { return name; }
};