## 104周转行Quant | W04 - C++的OOP魔法(下)

> 又是发生在“SigmaX私募基金管理有限公司”这家公司的有趣故事

## 🏦SigmaX的日常

承接上周的故事，很不幸，SigmaX的量化团队在经历了A股的大回撤以及几个重要投资策略的失败之后，决定进行一次大规模的团队重组和优化。不过万幸的是，富婆给的投资还剩一半，黑犬痛定思痛，裁掉了人美心坏的HRBP，找了几个在量化行业有经验的前辈的咨询公司帮忙进行组织优化。

前辈们经过调研，发现SigmaX的量化团队存在几个问题：

1. 团队成员角色不清晰，职责重叠，导致效率低下
2. 团队成员之间缺乏有效的沟通和协作，信息孤岛严重
3. 团队缺乏明确的目标和绩效评估
4. 除了量化三大金刚的核心岗位（QR、QD、Trader）之外，缺乏必要的支持岗位（如数据工程师、风险管理、投资组合管理等）

基于这些发现，前辈A建议：**“重新设计员工之间的协作模式，捋清公司业务架构，并且对公司不同的业务要有实时的监控和感知”**。

黑犬点点头，准备还是用自己最擅长的代码来进行业务的重新设计。想了半天，不如使用**设计模式**来对原有的OOP代码进行优化吧:

- 岗位角色：硬编码每一个不同的岗位 -> 使用**工厂模式**来创建不同类型的员工对象
- 团队协作：成员角色之间没有统一的协作模式 -> 使用**观察者模式**来实现成员之间的事件通知和协作：创建一个团队事件系统
- 业务管理：每个岗位的职责和工作内容不清晰 -> 使用**策略模式**来定义每个岗位的工作职责和任务

这样一来，刚刚前辈提到的几个问题都能迎刃而解，并且代码的设计也会更加清晰和易于维护，重要的是也符合OOP程序代码设计的几大原则：

- **单一职责原则（SRP）**
- **开闭原则（OCP）**
- **依赖倒置原则（DIP）**

这时前辈B站了出来：**“还不够，要做好风控、投资组合管理、合规，数据方面也得有专人去管吧，数据工程、数据科学家或者SRE至少得有一个，另外订单执行、盈亏的实时监控和告警，多少也该有吧...”**

啊对对对，黑犬用小本本记下了所有前辈给的建议，并且对原有代码做了整体的改进：

```cpp
/* !只展示核心修改代码，完整代码请参考仓库 */
// 工厂模式 - 员工创建工厂
class EmployeeFactory
{
public:
    static std::unique_ptr<Employee> createEmployee(
        EmployeeType type,
        const std::string &name,
        double salary,
        EmployeeLevel level = EmployeeLevel::SENIOR);

private:
    // 私有构造函数，工厂类不应该被实例化
    EmployeeFactory() = default;
};
// ...

// 策略模式 - 工作策略接口
class WorkStrategy
{
public:
    virtual ~WorkStrategy() = default;
    virtual void execute(const std::string &employee_name) const = 0;
    virtual std::string get_strategy_name() const = 0;
};
// ...
// 团队事件观察者接口，相关成员实现该接口以接收事件通知实现通信
class EventObserver
{
public:
    virtual ~EventObserver() = default;
    virtual void onEvent(const TeamEvent &event) = 0;
};
// ...
// 自定义异常类层次结构, 做好风控！
class QuantTeamException : public std::exception
{
protected:
    std::string message;

public:
    explicit QuantTeamException(const std::string &msg) : message(msg) {}
    const char *what() const noexcept override { return message.c_str(); }
};
```

在以上核心代码之外，黑犬还充分使用了**智能指针**、RAII等现代C++特性来保证代码的安全性和性能，在原有的团队架构增加并完善7种专业角色: QR、QD、Trader、Risk Manager、Portfolio Manager、Data Scientist、Compliance Officer，并且定下了公司的日常工作流：晨会→策略讨论→代码审查→风险评估→绩效回顾,同时也增加了预算管理、绩效、投资组合管理、监控系统的相关工作逻辑。

最终，黑犬尝试重新招募了一批有经验的量化团队成员，并且使用新设计的代码系统来管理和协作，这是在SigmaX量化团队的一天：

```bash
# 执行效果展示
[成立] 量化团队 'Sigma-X Quant Fund' 成立，预算: $15000000

=== 开始组建量化团队 ===

[成功] 招聘成功: Alice Chen (薪资: $600000)
[成功] 招聘成功: Bob Wilson (薪资: $500000)
[成功] 招聘成功: Charlie Zhang (薪资: $450000)
[成功] 招聘成功: David Park (薪资: $400000)
[成功] 招聘成功: Eva Rodriguez (薪资: $550000)
[成功] 招聘成功: Frank Liu (薪资: $480000)
[成功] 招聘成功: Grace Kim (薪资: $650000)
[成功] 招聘成功: Henry Brown (薪资: $350000)

=== Sigma-X Quant Fund 团队构成 ===
团队规模: 8 人
• Alice Chen - 技能: Python, R, 统计学, 机器学习, 金融理论, 数据挖掘 - 薪资: $600000
• Bob Wilson - 技能: C++, Python, 系统架构, 低延迟交易, 数据库优化, Linux - 薪资: $500000
• Charlie Zhang - 技能: C++, Python, 系统架构, 低延迟交易, 数据库优化, Linux - 薪资: $450000
• David Park - 技能: 市场分析, 风险控制, 交易执行, 衍生品, 套利策略 - 薪资: $400000
• Eva Rodriguez - 技能: 风险建模, VaR计算, 压力测试, 监管合规, 风险报告 - 薪资: $550000
• Frank Liu - 技能: 机器学习, 深度学习, 大数据处理, 特征工程, TensorFlow, PyTorch - 薪资: $480000
• Grace Kim - 技能: 资产配置, 投资组合理论, 业绩归因, 再平衡策略, 客户管理 - 薪资: $650000
• Henry Brown - 技能: 金融法规, 合规监管, 内部审计, 风险评估, 报告撰写 - 薪资: $350000

=== 预算状态 ===
总预算: $15000000
已用预算: $3980000
剩余预算: $11020000
预算使用率: 26.5%

======== Sigma-X Quant Fund 日常运营开始 ========

=== 早会时间 ===
[准备] Alice Chen 正在准备工作...
[研究策略] Alice Chen 正在阅读最新论文，挖掘Alpha因子，构建量化模型...
[策略提议] Alice Chen 提出新的量化策略: 基于深度学习的动量因子!
[回测] Alice Chen 正在进行历史数据回测，夏普比率达到了 2.8!
[结束] Alice Chen 完成了今日工作。
[准备] Bob Wilson 正在准备工作...
[开发策略] Bob Wilson 正在优化交易系统，减少延迟，提升系统性能...
[代码审查] Bob Wilson 发现了性能瓶颈，建议使用内存池优化!
[系统优化] Bob Wilson 成功将延迟降低了15微秒!
[结束] Bob Wilson 完成了今日工作。
[准备] Charlie Zhang 正在准备工作...
[开发策略] Charlie Zhang 正在优化交易系统，减少延迟，提升系统性能...
[代码审查] Charlie Zhang 发现了性能瓶颈，建议使用内存池优化!
[系统优化] Charlie Zhang 成功将延迟降低了15微秒!
[结束] Charlie Zhang 完成了今日工作。
[准备] David Park 正在准备工作...
[交易策略] David Park 正在监控市场，执行交易策略，管理风险敞口...
[订单执行] David Park 成功执行了100万美元的交易订单!
[仓位监控] David Park 当前投资组合的Beta值为0.95，风险可控。
[结束] David Park 完成了今日工作。
[准备] Eva Rodriguez 正在准备工作...
[风险管理策略] Eva Rodriguez 正在计算VaR，监控仓位，评估市场风险...
[风险计算] Eva Rodriguez 计算得出今日VaR为250万美元 (95%置信度)。
[限额检查] Eva Rodriguez 检查发现所有仓位均在风险限额内。
[风险报告] Eva Rodriguez 生成了详细的风险评估报告。
[结束] Eva Rodriguez 完成了今日工作。
[准备] Frank Liu 正在准备工作...
[数据分析策略] Frank Liu 正在清洗数据，构建机器学习模型，进行特征工程...
[数据清洗] Frank Liu 处理了500GB的市场数据，清除了异常值。
[模型构建] Frank Liu 构建了LSTM预测模型，准确率达到78%。
[结束] Frank Liu 完成了今日工作。
[准备] Grace Kim 正在准备工作...
[风险管理策略] Grace Kim 正在计算VaR，监控仓位，评估市场风险...
[组合再平衡] Grace Kim 调整了资产配置，股票/债券比例优化至70/30。
[配置优化] Grace Kim 使用马科维茨模型优化了投资组合权重。
[结束] Grace Kim 完成了今日工作。
[准备] Henry Brown 正在准备工作...
[合规策略] Henry Brown 正在审查交易记录，检查监管合规性，生成合规报告...
[交易审查] Henry Brown 审查了今日所有交易，未发现违规行为。
[监管检查] Henry Brown 确认所有操作符合SEC和CFTC要求。
[结束] Henry Brown 完成了今日工作。

=== 策略讨论 ===
[事件响应] Alice Chen 收到策略提议: 新的均值回归策略
[事件响应] Bob Wilson 收到策略提议: 新的均值回归策略
[事件响应] Charlie Zhang 收到策略提议: 新的均值回归策略
[事件响应] David Park 收到策略提议: 新的均值回归策略
[事件响应] Eva Rodriguez 收到策略提议: 新的均值回归策略
[事件响应] Frank Liu 收到策略提议: 新的均值回归策略
[事件响应] Grace Kim 收到策略提议: 新的均值回归策略
[事件响应] Henry Brown 收到策略提议: 新的均值回归策略

=== 代码审查 ===
[事件响应] Bob Wilson 开始代码审查...
[事件响应] Charlie Zhang 开始代码审查...

=== 风险评估 ===
[事件响应] Eva Rodriguez 响应风险警报!
[事件响应] Grace Kim 响应风险警报!

=== 绩效回顾 ===

======== 今日运营完成 ========

=== 团队协作演示 ===
[协作] Alice Chen 正在与 Bob Wilson 协作处理项目

=== 奖金计算演示 ===
Alice Chen 的年终奖金: $180000.0

=== 程序执行完成 ===
```

好不容易，SigmaX再次回归了正轨，黑犬也松了一口气。再给两位前辈送了两箱茅台之后，黑犬回到老板办公室，扔掉了原木大桌和皮椅，换上了简约风的办公桌和人体工学椅，把书架上的手办也给扔了，换成了营销和商业管理书籍，最后把黑丝小秘书也给辞退了，换成了一个十年金融行业经验的财务助理。

创业不是过家家，量化更不是玩票，**专业的人做专业的事，才能走得更远。**

## 📒补充说明

本周的SigmaX的故事中，黑犬主要给大家介绍了三个基础的设计模式：**单例模式、观察者模式和策略模式**，这些设计模式在实际的C++项目中都有广泛的应用，尤其是在复杂系统的设计中，能够帮助我们更好地组织代码结构，提高代码的可维护性和扩展性。

当你在使用OOP进行项目设计时，设计模式是绕不开的一个话题，实际上常见的设计模式有20余种，需要你结合实际的业务场景去灵活运用、去悟。三大原则（SRP、OCP、DIP）也是每一个OOP程序员必须要牢记的设计准则，这几个准则能够帮助我们避免代码的过度耦合和复杂性，提高代码的质量。**市面上已经有很多关于设计模式的书籍和资源，大家选择自己喜欢的进行学习即可，重点是找到自己善于理解的场景去实践它，这玩意背不下来的**，希望SigmaX的故事能给你一个有趣的角度去理解它们。

本周代码已经上传到Github仓库🔗：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)

**下周预告：W04 - C++的OOP高级用法（上）**

👋各位下周五见，我是在做梦成立自己量化公司的黑犬momo酱。
