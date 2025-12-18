## 104周转行Quant | W05 - C++的OOP高级用法（上）

> SigmaX逐渐做大做强，公司越大，问题越多...
> 本期关键词：CRTP、Mixin、Policy-Based Design、模板元编程、类型擦除

## 🏦死对头的崛起

上周SigmaX好不容易重回正轨，正在规划第一个盈利季度的工作，这周一开局就遇到大麻烦。

某天下午，公司的QR Alice冲进黑犬办公室：

> "老板！我们的动量策略今天完全失效了！市场上有人比我们快了至少 **50ms**，我们的单子还没发出去，机会就没了！"

QD Bob也气冲冲地跑来，拿着电脑给黑犬看系统日志：

> "老板，我看出问题了。我们现在用的**虚函数多态**，每次策略执行都要查虚表，光这个开销就有几十纳秒。高频交易场景下，这个延迟是致命的！"

黑犬皱眉调出监控系统，发现原来是隔壁金融小镇的死对头——海归高材生"**白猫**"才成立的量化冲基金“**AlphaZ**”突然杀出来，并且他家的订单总是要早一些到交易所。

可恶🤬，这能忍吗？敢抢我的钱！黑犬光速拉着QD组的Tech lead Carol开会研究，很快决定了用**CRTP静态多态**技术重构公司的基本策略类：

```cpp
// 旧方案 - 虚函数多态，参考上周的WorkStrategy.hpp
/**
 * CRTP 策略基类 - 零虚函数开销的策略模式
 */
template<typename Derived>
class StrategyBase {
public:
    // CRTP 接口
    void execute(const std::string& employee_name) const {
        std::cout << "  [策略执行] " << name() << "\n";
        static_cast<const Derived*>(this)->execute_impl(employee_name);
    }

    constexpr std::string_view name() const {
        return Derived::strategy_name;
    }

    void log_execution() const {
        std::cout << "  [" << name() << "] 策略开始执行\n";
    }
};
```

通过CRTP，黑犬成功消除了虚函数调用的开销，策略执行速度提升了40%，成功抢回了一些单子，但AlphaZ还是领先不少，这让黑犬很不爽。

## 🚸风控盲区

周二，刚刚才解决性能问题，黑犬又接到风控部的经理Eva的投诉：
> "狗哥，我发现一个严重问题！昨天有 3 笔订单的 ID 和员工 ID 搞混了，系统把**订单 ID 0991** 当成了**员工 ID 0991**，查询时返回了完全错误的数据！幸好我人工复核发现了，不然亏大了！"

好家伙，人力管理系统不是黑犬自己负责的吗🫣？黑犬马上检查员工管理系统源码，发现后来员工数量增加后虽然增加了员工ID区分员工，但是处都是 `std::string` 和 `int` 做 ID，完全没有类型区分：

```cpp
// 老代码 - 类型不安全
Employee* find_employee(int id);        // 员工 ID
Order* find_order(int id);              // 订单 ID
// 问题：可以把订单 ID 传给 find_employee！
```

黑犬先给Eva道歉，然后立刻召集QD组的Bob和Carol开会，决定用**强类型ID系统**来重构员工和订单ID：

```cpp
/**
 * 强类型 ID 模板 - 类型安全的 ID 系统
 * 使用 Tag 类型区分不同的 ID 类型，防止混淆
 */
template<typename Tag, typename ValueType = uint64_t>
class StrongID {
private:
    ValueType value;

public:
    // 只能显式构造
    constexpr explicit StrongID(ValueType val = 0) noexcept : value(val) {}

    constexpr ValueType get() const noexcept { return value; }
    constexpr bool is_valid() const noexcept { return value != 0; }

    // 比较运算符 (C++20)
    constexpr bool operator==(const StrongID& other) const noexcept = default;
    constexpr bool operator!=(const StrongID& other) const noexcept = default;
    constexpr bool operator<(const StrongID& other) const noexcept {
        return value < other.value;
    }

    // 支持哈希，可用于 unordered_map
    struct Hash {
        size_t operator()(const StrongID& id) const noexcept {
            return std::hash<ValueType>{}(id.value);
        }
    };
};

// 定义不同类型的 ID Tag
struct EmployeeTag {};
struct OrderTag {};
struct StrategyTag {};

// 具体的 ID 类型
using EmployeeID = StrongID<EmployeeTag>;
using OrderID = StrongID<OrderTag>;
using StrategyID = StrongID<StrategyTag>;
```

这样就能在编译期防止ID混淆，避免类似错误再次发生，还好Eva发现的及时，不然损失可就大了，金融系统中的类型混淆可是灾难性的， 黑犬默默掏出小本本记下下个月给Eva多发点奖金。

## 🦹又被监管盯上了

周三的晚上黑犬忙了半天刚刚要回家，就被合规官Henry叫住了：
> "老板，监管部门要求我们记录每个员工的**所有操作日志**、**任务耗时指标**，还要有**权限控制**。但如果我去修改每个员工类，要改 7 个文件，太容易出 bug 了！"

黑犬一听这话就头大，这不就是典型的**横切关注点**问题吗？如果每个员工类都要改，那维护成本太高了。黑犬立刻打电话把QD组叫了回来，决定用**Mixin功能组合**来实现这个功能：

```cpp
/**
 * Mixin 类(Mixins.hpp) - 通过多重继承组合功能
 * 优势：不修改原类，遵循开闭原则，功能正交
 */

// ========== Mixin 1: 日志功能 ==========
template<typename Base>
class Loggable : public Base {
public:
    using Base::Base;  // 继承构造函数

    void log(const std::string& message) const {
        std::cout << "  [日志] [" << Base::get_name() << "] " << message << "\n";
    }

    // 增强基类方法
    void do_work() const {
        log("开始工作");
        Base::do_work();
        log("工作完成");
    }
};

// ========== Mixin 2: 指标采集 ==========
template<typename Base>
class MetricsCollector : public Base {
private:
    mutable std::chrono::steady_clock::time_point start_time;
    mutable size_t task_count = 0;

public:
    using Base::Base;

    void do_work() const {
        start_time = std::chrono::steady_clock::now();
        ++task_count;

        Base::do_work();

        auto duration = std::chrono::steady_clock::now() - start_time;
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
        std::cout << "  [指标] 任务 #" << task_count << " 耗时: " << ms << "ms\n";
    }

    size_t get_task_count() const { return task_count; }
};

// ========== Mixin 3: 权限控制 ==========
template<typename Base>
class Permissioned : public Base {
private:
    int permission_level = 1;

public:
    using Base::Base;

    void set_permission_level(int level) { permission_level = level; }
    int get_permission_level() const { return permission_level; }

    void do_work() const {
        if (permission_level < 2) {
            std::cout << "  [权限] " << Base::get_name()
                      << " 权限不足 (需要等级 >= 2，当前: " << permission_level << ")\n";
            return;
        }
        Base::do_work();
    }
};

// 带日志的员工
template<typename EmployeeType>
using LoggableEmployee = Loggable<EmployeeType>;

// ...
```

这样黑犬就不用修改每个员工类了，只要用Mixin组合出需要的功能即可，既满足了监管要求，又避免了代码重复和维护困难的问题，比如：

```cpp
    // 带日志的研究员
    std::cout << "\n【组合 1: 带日志功能的员工】\n";
    LoggableEmployee<QuantResearcher> alice_with_log(
        EmployeeID{2001}, "Alice (日志版)", 600000, EmployeeLevel::PRINCIPAL
    );
    alice_with_log.do_work();
```

创建员工时创建这样的对象，那么公司的QR在做策略研究时就会自动记录日志了，而不需要修改原有的 `QuantResearcher` 类。

## 🧐富婆的新需求

就在黑犬以为可以松口气时，周四午休时公司神秘大客户——富婆Esme打来电话：
> "狗子啊，我这边朋友家孩子都想来你公司增长点经验，给我好好安排安排。我希望你们能给这些实习生设计一些灵活的**奖金计算方案**，听懂了么？"

好家伙，但我能说不吗？**我不能**。黑犬只好又找来了QD组，决定用**Policy-Based Design策略模板设计**来实现这个需求，把原来的员工类改成策略模板类，这样工作和奖金都能更加灵活地调整：

```cpp
/**
 * Policy-Based Design - 策略作为模板参数
 * 优势：编译期绑定，完全内联，零开销
 */

// ========== 工作策略 Policy ==========

struct ResearchWorkPolicy {
    static void execute_task(const std::string& name) {
        std::cout << "  [研究工作] " << name << " 正在分析数据并回测策略\n";
    }
};

// ... 奖金策略也同步更改
// ========== Policy-Based Employee ==========

template<typename WorkPolicy, typename BonusPolicy>
class PolicyBasedEmployee {
private:
    std::string name;
    double base_salary;
    double performance_score = 1.0;

public:
    PolicyBasedEmployee(std::string n, double s)
        : name(std::move(n)), base_salary(s) {}

    void do_work() const {
        std::cout << "\n【Policy-Based 员工: " << name << "】\n";
        WorkPolicy::execute_task(name);  // 编译期决定
    }

    double calculate_bonus() const {
        return BonusPolicy::calculate(base_salary, performance_score);
    }

    void set_performance(double score) { performance_score = score; }

    std::string get_name() const { return name; }
    double get_salary() const { return base_salary; }

    void show_bonus_info() const {
        std::cout << "  [奖金] " << name << " - " << BonusPolicy::name
                  << ": $" << calculate_bonus() << "\n";
    }
};

// ========== 类型别名 ==========

using PolicyResearcher = PolicyBasedEmployee<ResearchWorkPolicy, PerformanceBasedBonusPolicy>;
```

哪里都是人情世故，谁叫富婆给钱多呢？黑犬只好硬着头皮新增了几个HC，还和HR打好了招呼，让实习生们都用上**专门设计过**的奖金计算方案。

## 🌋策略灾难

直到这周四晚上，Alice 研发了 200 多个不同的策略，有的用 C++，有的用 Python FFI，有的甚至是外部厂商提供的：

> "老板，我们的策略现在五花八门：
>
> - MomentumStrategy（继承 Strategy）
> - MeanReversionStrategy（继承 Strategy）
> - MLStrategy（Python 接口，没继承）
> - VendorStrategy（外部库，接口完全不同）
>
> 我现在想统一管理这些策略，但它们连基类都不一样！"

黑犬头都大了，你就不能提前说吗？下次让研究组凑钱请QD组吃饭！黑犬只好又找来了QD组，决定用**类型擦除**(Type Erasure)技术来实现策略的统一管理：

```cpp
/**
 * Type Erasure - 类型擦除包装器
 * 优势：无需继承，统一接口，值语义
 * 类似 std::function 的实现原理
 */

class AnyStrategy {
private:
    // 内部抽象接口
    struct StrategyInterface {
        virtual ~StrategyInterface() = default;
        virtual void execute(const std::string& name) const = 0;
        virtual std::string get_name() const = 0;
        virtual std::unique_ptr<StrategyInterface> clone() const = 0;
    };

    // 模板实现类 - 包装任何类型
    template<typename T>
    struct StrategyImpl : StrategyInterface {
        T strategy;

        explicit StrategyImpl(T s) : strategy(std::move(s)) {}

        void execute(const std::string& name) const override {
            // 调用 T 的 execute 方法（无需继承）
            strategy.execute(name);
        }

        std::string get_name() const override {
            return std::string(strategy.name());
        }

        std::unique_ptr<StrategyInterface> clone() const override {
            return std::make_unique<StrategyImpl>(strategy);
        }
    };

    std::unique_ptr<StrategyInterface> impl;

public:
    // 接受任何有 execute 和 name 方法的类型
    template<typename T>
    AnyStrategy(T strategy)
        : impl(std::make_unique<StrategyImpl<T>>(std::move(strategy))) {}

    // 拷贝构造
    AnyStrategy(const AnyStrategy& other)
        : impl(other.impl ? other.impl->clone() : nullptr) {}

    // 移动构造
    AnyStrategy(AnyStrategy&&) noexcept = default;

    // 拷贝赋值
    AnyStrategy& operator=(const AnyStrategy& other) {
        if (this != &other) {
            impl = other.impl ? other.impl->clone() : nullptr;
        }
        return *this;
    }

    // 移动赋值
    AnyStrategy& operator=(AnyStrategy&&) noexcept = default;

    // 统一接口
    void execute(const std::string& name) const {
        if (impl) {
            impl->execute(name);
        }
    }

    std::string get_name() const {
        return impl ? impl->get_name() : "None";
    }
};
```

直接使用类型擦除重构了策略类之后，Alice现在终于能够统一的管理不同类型的策略了：

```cpp
    // 使用 AnyStrategy 管理不同类型的策略
    std::vector<AnyStrategy> strategies;
    strategies.emplace_back(MomentumStrategy{});
    strategies.emplace_back(MeanReversionStrategy{});
    strategies.emplace_back(MLStrategy{});
    strategies.emplace_back(VendorStrategy{});

    // 统一执行所有策略
    std::cout << "\n【类型擦除管理的策略列表】\n";
    for (const auto& strat : strategies) {
        strat.execute("Alice");
    }
```

## 🌈雨后彩虹

经过一周的奋战，黑犬终于带领QD组解决了公司面临的各种棘手问题，现在比AlphaZ的订单执行速度 **快了 30 微秒**！气得白猫直跳脚。富婆Esme也非常满意，追加了 2000 万投资。黑犬站在办公室落地窗前，看着团队成员在工位上专注工作。

财务助理递来一杯马黛茶🧉：

> "老板，前辈 A 发来邮件，说想介绍几个 LP（有限合伙人）过来。大姐头Esme说周天晚上八点也撺了一个和投资人朋友的局，要你一定抽时间去。"

黑犬笑了笑说：

> "告诉他，SigmaX 已经准备好了。**技术债还清了，架构优化了，团队专业化了**。是时候进入下一个阶段了。"

## 📒补充说明

本周涉及了多种C++高级编程技术，你可能好奇**模板元编程**怎么没有单独讲，其实这些技术本质上都离不开模板元编程的支持，比如CRTP、Mixin、Policy-Based Design和类型擦除都大量使用了模板技术来实现编译期多态和类型抽象，模板元编程的几个重要特征（如**SFINAE、constexpr if、概念**等）在这些技术中都有所体现，比如：

- **CRTP** 利用模板参数实现静态多态，避免了虚函数开销。
- **Mixin** 通过模板继承实现功能组合，遵循开闭原则。
- **Policy-Based Design** 通过模板参数实现策略注入，增强了灵活性。
- **类型擦除** 通过模板实现对任意类型的封装，实现统一接口。

教科书对模板元编程的介绍通常比较抽象，而通过这些具体技术的应用，可以更直观理解这几项技术适用于什么场景，以及它们如何利用模板元编程的特性来实现高效、灵活的设计。

本周代码已经上传到Github仓库🔗：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)，欢迎Star⭐、贡献代码或issue。

**下周预告：W06 - C++的OOP高级用法（下）**

👋各位下周五见，下周SigmaX将会迎来更加硬核的挑战。
