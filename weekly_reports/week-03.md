## 104周转行Quant | W03 - C++的OOP魔法(上)

> 以“SigmaX私募基金管理有限公司”的组织结构为例搞懂C++的OOP基本技术

## 🏦SigmaX的崛起之路

大家周五好!!!

🔈好消息好消息! 黑犬这周找富婆融到了资，现在开始组建自己的量化私募团队了。“SigmaX私募基金管理有限公司”超绝招募中...

虽然富婆给了钱，但是架不住黑犬心黑且没有什么文化（更没读过MBA），准备自己拍脑袋找人组建团队，找了个人美心坏的HRBP，招聘的大小事务都听她的处理， 最重要先把团队的架构搭出来。黑犬比较笨，只会写代码，就用C++中的OOP的知识来梳理HRBP告诉我的HR知识。

HRBP告诉我，无论招聘什么角色（QR、QD 还是 QT），他们都是公司的雇员。他们都有名字、工号，都得发工资，最重要的是——**他们都得干活**。

嗷嗷嗷，黑犬明白了，黑犬帮牛马们创了一个**抽象类**，另外，员工除了基本信息之外，肯定还有一些 敏感的信息，比如薪资，那就需要**封装**起来（Bonus?什么Bonus，我都给工资了还敢要奖金?）。

```C++
#include <iostream>
#include <string>
#include <vector>

// 这是一个抽象基类（Abstract Base Class）
class Employee {
protected: 
    // protected 意味着：外部不能访问，但子类（QR, QD）可以访问
    // 毕竟只有继承了“员工”身份，才有资格谈薪水
    std::string name;
    double base_salary;

public:
    Employee(std::string n, double s) : name(n), base_salary(s) {}

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
```

HRBP扭扭屁股说，量化“三大金刚”你别忘了招，但是要注意它们的工作内容不一样哦。

对喔🚨，黑犬把这三种典型的量化岗位的职能梳理了下，发现它们**都有职员的共性**但落实到实际工作又需要**个性的分离**：

1. **Quant Researcher (QR)**：业余数学家，整天读论文，写 Python，负责**寻找 Alpha**。

2. **Quant Developer (QD)**：C++ Nerd，关注延迟和架构，负责**把 QR 的 Python 变成高性能 C++**。

3. **Quant Trader（QT）**：赌徒，盯着屏幕，关注风险，甚至干预交易，负责**风险控制与执行**。

一个个写它们的职能太🥱累，不如直接继承基本的雇员类，这样很快就能写好：

```C++
// 1. 量化研究员 (QR)
class QuantResearcher : public Employee {
public:
    QuantResearcher(std::string n, double s) : Employee(n, s) {}

    void do_work() const override {
        // QR 的日常：挖因子，搞模型，也许还在抱怨数据不干净
        std::cout << "[QR] " << name << " 正在阅读 ICML 论文，并尝试挖掘新的 Alpha 因子..." << std::endl;
    }

    // QR 特有的技能
    void propose_strategy() {
        std::cout << "[QR] " << name << " 提出只要在这个参数上过拟合一下，回测夏普比率能到 5.0！" << std::endl;
    }
};

// 2. 量化开发 (QD)
class QuantDeveloper : public Employee {
public:
    QuantDeveloper(std::string n, double s) : Employee(n, s) {}

    void do_work() const override {
        // QD 的日常：优化代码，骂编译器，骂网络延迟
        std::cout << "[QD] " << name << " 正在重写订单网关，试图削减掉 5 微秒的延迟..." << std::endl;
    }

    // QD 特有的技能
    void reject_bad_code() {
        std::cout << "[QD] " << name << " 拒绝了 QR 的代码提交：'内存泄漏太严重，不能上线'。" << std::endl;
    }
};

// 3. 交易员 (Trader)
class Trader : public Employee {
public:
    Trader(std::string n, double s) : Employee(n, s) {}

    void do_work() const override {
        // Trader 的日常：盯盘，甚至有点迷信
        std::cout << "[Trader] " << name << " 正在紧盯波动率指数，并祈祷今天不要爆仓。" << std::endl;
    }
};
```

但是我是老板诶，我管你这的那的，走进办公室那你们就都是帮我挣法拉利的牛马，什么个性不个性 ，就像HRBP说的，老子喊一声你们都要马上get things done。为了体现这一管理学智慧，我对员工们使用了**多态(Polymorphism**，读作PUA)，只要你是我的牛马，喊一声你就要立马排除万难适应工作：

```C++
// 团队管理类
class QuantTeam {
private:
    // 我们存的是基类的指针！
    // 这是一个异构容器：虽然类型都是 Employee*，但指向的实际对象不同
    std::vector<Employee*> team_members;

public:
    // 招人
    void hire(Employee* e) {
        team_members.push_back(e);
    }

    // 每日早会：一声令下，全员开工
    void start_daily_operations() {
        std::cout << "--- 市场开盘，团队开始运作 ---" << std::endl;
        
        // 这里的 e 是 Employee 指针
        // 但编译器会在运行时（Runtime）去查看它指向的到底是 QR 还是 QD
        // 这就是 动态绑定 (Dynamic Binding)
        for (auto* e : team_members) {
            e->do_work(); 
        }
        std::cout << "-----------------------------" << std::endl;
    }

    // 析构函数：公司倒闭时，要解雇所有人，释放内存
    ~QuantTeam() {
        for (auto* e : team_members) {
            delete e;
        }
    }
};
```

很好，现在团队已经搭建完毕了，可以向市场发出猛烈的进攻了：

```C++
int main() {
    QuantTeam sigma_x;

    // 1. 组建团队 (Upcasting: 子类指针自动转为父类指针)
    // 注意：QR 通常比较贵，QD 比较苦，Trader 比较像赌徒
    sigma_x.hire(new QuantResearcher("Alice", 500000));
    sigma_x.hire(new QuantDeveloper("Bob", 400000));
    sigma_x.hire(new QuantDeveloper("Charlie", 350000)); // 需要两个 QD 才能伺候一个 QR
    sigma_x.hire(new Trader("Dave", 300000));

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
```

大功告成，黑犬现在在办公室搂着黑丝小秘书看着自己的量化私募公司有条不紊地在运作中，心中 怀着未来成为中国版詹姆斯西蒙斯的壮志：

```C++
// 参考输出
--- 市场开盘，团队开始运作 ---
[QR] Alice 正在阅读 ICML 论文，并尝试挖掘新的 Alpha 因子...
[QD] Bob 正在重写订单网关，试图削减掉 5 微秒的延迟...
[QD] Charlie 正在重写订单网关，试图削减掉 5 微秒的延迟...
[Trader] Dave 正在紧盯波动率指数，并祈祷今天不要爆仓。
-----------------------------
```

## 📒补充说明

黑犬抱着黑丝小秘书笑醒了...一觉醒来，黑犬没有钱搞公司，依然只是一个学习量化技术的牛马。😮‍💨

比起从C++底层代码开始研究OOP，我觉得一个有趣的例子将这些知识串联起来或许能帮读者更直观地理解OOP的核心技术和概念，比起我上学时单独去学每一个OOP技术细节会好很多。

本周的这个小故事的代码依旧会上传到Github仓库🔗：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)

在这周的例子中已经涵盖了C++最常见的OOP技术：抽象类（接口设计）、继承、多态（虚函数机制）以及容器和指针，但是显然，这样的OOP程序设计并不完善。

比如，如果我想做一个好老板，给员工发奖金，QR和QT的奖金通常与PnL挂钩，QD却无所谓，只看系统uptime，那奖金分配的接口怎么设计？（参考**多重继承**）；又比如，传统的QR→QD→QT的执行路径，我想要在不同的员工之间建立直接的需求传递机制，这在代码上怎么实现？（对象之间的解耦和通信机制，考虑**设计模式**以及**接口隔离原则**）；甚至我们可以想，如果这三大金刚其中的一个离职（对象销毁）了，那么和它相关的工作会不会没有人对接（其他对象对它的指针悬空了）？这都是可以考虑的场景，也会很有趣。

关于量化团队的职位，除了上述的三大金刚之外，量化团队常见的角色也会有**数据工程师 (Data Engineer)、风险控制经理 (Risk Manager)、系统/网络工程师 (SRE / Infrastructure)、执行算法量化 (Execution Algo Quant)、投资组合经理 (Portfolio Manager, PM)，**但是这些职位并不是必须的，重要的是一个成熟的投资团队应该在投研、技术、风控、后勤和行政管理都要有中流砥柱。

受限于篇幅和深度，本周的分享就到这里，后续我还会在Github仓库维护每周帖子中提到的代码如果正在阅读的各位有更好更新奇的想法也非常欢迎给我的项目一个star或者参与贡献，也欢迎任何形式的私信/评论。

**下周预告：W04 - C++的OOP魔法（深入）**

👋下周五见，我是在做梦成立自己量化公司的黑犬momo酱。
