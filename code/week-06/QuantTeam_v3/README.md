# QuantTeam v3 - Week 6: OOP 现代化

## 项目简介

本项目是量化私募团队框架的第三版，重点实现 **Week 6 的 OOP 现代化技术**，包括：

1. **std::variant** - 值语义多态
2. **Decorator Pattern** - 装饰器模式
3. **PIMPL** - 编译防火墙
4. **Prototype Pattern** - 原型模式
5. **Visitor Pattern** - 访问者模式

## 项目结构

```
QuantTeam_v3/
├── include/                      # 头文件
│   ├── Types.hpp                # 基础类型定义
│   ├── VariantEmployees.hpp     # std::variant 值语义多态
│   ├── StrategyDecorator.hpp    # Decorator 装饰器模式
│   ├── AdvancedPatterns.hpp     # PIMPL、Prototype、Visitor
│   └── QuantTeam.hpp            # 团队管理类
├── src/                         # 源文件
│   ├── main.cpp                 # 主程序演示
│   └── Portfolio.cpp            # PIMPL 实现
├── tests/                       # 测试文件
│   └── test_all.cpp            # 单元测试
├── bin/                         # 可执行文件
├── obj/                         # 目标文件
├── CMakeLists.txt              # CMake 构建配置
├── Makefile                    # Make 构建配置
└── README.md                   # 项目文档
```

## 核心技术详解

### 1. std::variant 值语义多态 ⭐⭐⭐

**核心思想**：使用 C++17 的 `std::variant` 实现无继承的多态，提供值语义。

**优势**：

- ✅ 可拷贝、可移动（值语义）
- ✅ 无虚函数开销
- ✅ 内存紧凑、缓存友好
- ✅ 编译期类型安全

**示例**：

```cpp
// 定义员工类型（无继承关系）
struct QuantResearcher { ... };
struct QuantDeveloper { ... };
struct Trader { ... };

// 使用 variant 实现多态
using Employee = std::variant<QuantResearcher, QuantDeveloper, Trader>;

// 值语义容器 - 可以直接拷贝！
std::vector<Employee> team_members;
team_members.push_back(QuantResearcher{"Alice", 600000, ...});

// 使用访问者模式访问
std::visit([](const auto& emp) { emp.do_work(); }, employee);
```

### 2. Decorator 装饰器模式 ⭐⭐

**核心思想**：动态地给对象添加额外功能，不修改原类。

**优势**：

- ✅ 开闭原则：不修改原类
- ✅ 灵活组合：可任意叠加功能
- ✅ 单一职责：每个装饰器专注一个功能
- ✅ 运行时配置：动态添加/移除功能

**示例**：

```cpp
// 基础策略
std::unique_ptr<Strategy> strategy = std::make_unique<MomentumStrategy>();

// 添加日志功能
strategy = std::make_unique<LoggingDecorator>(std::move(strategy));

// 添加缓存功能
strategy = std::make_unique<CachingDecorator>(std::move(strategy));

// 添加计时功能
strategy = std::make_unique<TimingDecorator>(std::move(strategy));

// 功能叠加：计时 -> 缓存 -> 日志 -> 基础策略
strategy->execute(market_data);
```

### 3. PIMPL (Pointer to Implementation) ⭐⭐

**核心思想**：隐藏实现细节，减少编译依赖，实现二进制兼容。

**优势**：

- ✅ 编译防火墙：实现变更不影响使用者
- ✅ 隐藏细节：私有成员完全隐藏
- ✅ ABI 稳定：二进制接口兼容

**示例**：

```cpp
// Portfolio.hpp - 公共接口
class Portfolio {
private:
    class Impl;  // 前向声明
    std::unique_ptr<Impl> pimpl;

public:
    Portfolio(std::string name, double capital);
    ~Portfolio();
    // ...
};

// Portfolio.cpp - 实现细节（完全隐藏）
class Portfolio::Impl {
    // 所有实现细节在这里
};
```

### 4. Prototype 原型模式 ⭐⭐

**核心思想**：通过克隆现有对象创建新对象，实现"虚构造函数"。

**优势**：

- ✅ 虚构造函数：基类指针可以克隆
- ✅ 类型安全：返回正确的派生类型
- ✅ 深拷贝：完整复制对象
- ✅ CRTP 简化：避免重复代码

**示例**：

```cpp
// CRTP 版本的 Cloneable
template<typename Derived>
class Cloneable {
public:
    std::unique_ptr<Derived> clone() const {
        return std::make_unique<Derived>(static_cast<const Derived&>(*this));
    }
};

// 策略类自动获得 clone 能力
class MomentumStrategy : public Cloneable<MomentumStrategy> {
    // 只需实现拷贝构造函数
};

// 使用
auto original = std::make_unique<MomentumStrategy>();
auto cloned = original->clone();  // 自动生成的克隆方法
```

### 5. Visitor 访问者模式 ⭐⭐

**核心思想**：在不修改类的情况下添加新操作（双重分派）。

**优势**：

- ✅ 开闭原则：添加新操作无需修改类
- ✅ 双重分派：根据类型和访问者分派
- ✅ 集中操作：相关操作集中在访问者中

**示例**：

```cpp
// 访问者接口
class EmployeeVisitor {
public:
    virtual void visit(const QuantResearcher& qr) = 0;
    virtual void visit(const QuantDeveloper& qd) = 0;
};

// 具体访问者 - 薪资报告
class SalaryReportVisitor : public EmployeeVisitor {
    void visit(const QuantResearcher& qr) override {
        // 生成研究员薪资报告
    }
    void visit(const QuantDeveloper& qd) override {
        // 生成开发员薪资报告
    }
};

// 使用
for (auto& employee : employees) {
    employee->accept(salary_visitor);
}
```

## 编译和运行

### 方式一：使用 Makefile（推荐）

```bash
# 编译 Release 版本
make release

# 运行主程序
make run

# 编译并运行测试
make test

# 清理
make clean
```

### 方式二：使用 CMake

```bash
# 创建构建目录
mkdir build && cd build

# 配置（Release 模式）
cmake -DCMAKE_BUILD_TYPE=Release ..

# 编译
make

# 运行
./QuantTeam_v3
./tests
```

## 程序输出示例

运行主程序后，你将看到 5 个演示：

```
╔═══════════════════════════════════════════════════════════════╗
║      Week 6: OOP 现代化 - 值语义多态与现代设计模式            ║
║  技术栈:                                                      ║
║    1. std::variant - 值语义多态                               ║
║    2. Decorator - 装饰器模式                                  ║
║    3. PIMPL - 编译防火墙                                      ║
║    4. Prototype - 原型模式                                    ║
║    5. Visitor - 访问者模式                                    ║
╚═══════════════════════════════════════════════════════════════╝

Demo 1: std::variant 值语义多态
- 创建量化团队
- 雇佣不同类型的员工（无需指针！）
- 值语义拷贝团队

Demo 2: Decorator 装饰器模式
- 创建基础策略
- 动态添加日志、缓存、计时、过滤功能
- 功能自由组合

Demo 3: PIMPL 编译防火墙
- 创建投资组合
- 实现细节完全隐藏
- 支持拷贝和移动

Demo 4: Prototype 原型模式
- 创建策略原型
- 使用虚构造函数克隆
- CRTP 自动生成 clone 方法

Demo 5: Visitor 访问者模式
- 创建可访问的员工
- 薪资报告访问者
- 性能评估访问者
```

## 单元测试

运行测试：

```bash
make test
```

测试覆盖：

- ✅ std::variant 值语义多态
- ✅ Decorator 装饰器模式
- ✅ PIMPL 编译防火墙
- ✅ Prototype 原型模式
- ✅ Visitor 访问者模式
- ✅ Employee 访问者

## Week 5 vs Week 6 对比

| 维度 | Week 5 | Week 6 |
|------|--------|--------|
| **核心主题** | 编译期多态 | 值语义多态 |
| **技术栈** | CRTP、Policy、Mixin | variant、Decorator、PIMPL |
| **多态方式** | 静态多态 | 动态值多态 |
| **代码风格** | 模板密集 | 现代 C++ |
| **学习曲线** | 陡峭 | 平缓 |
| **适用场景** | 高性能关键路径 | 通用业务逻辑 |

## 技术亮点

### 1. 值语义的好处

```cpp
// Week 4/5: 必须使用指针，无法拷贝
std::vector<std::unique_ptr<Employee>> team;

// Week 6: 值语义，可以自然拷贝
std::vector<Employee> team;
auto team_copy = team;  // ✅ 直接拷贝！
```

### 2. 装饰器的灵活性

```cpp
// 可以任意组合功能，顺序可变
strategy = make_unique<LoggingDecorator>(
           make_unique<CachingDecorator>(
           make_unique<TimingDecorator>(
           make_unique<BaseStrategy>())));
```

### 3. PIMPL 的编译隔离

```cpp
// 修改 Portfolio 的实现细节
// 无需重新编译使用 Portfolio 的所有代码
// 实现了编译防火墙
```

### 4. Prototype 的简洁性

```cpp
// 使用 CRTP，派生类自动获得 clone 能力
// 无需手动实现 clone 方法
class MyStrategy : public Cloneable<MyStrategy> {
    // 自动获得 clone()！
};
```

### 5. Visitor 的扩展性

```cpp
// 添加新操作（如 XML 导出）
// 无需修改 Employee 类
class XMLExportVisitor : public EmployeeVisitor {
    // 实现 visit 方法即可
};
```

## 学习收获

完成本项目后，你将掌握：

### 技术层面

- ✅ 现代 C++ 多态的多种实现方式
- ✅ 值语义 vs 指针语义的权衡
- ✅ 装饰器模式的实际应用
- ✅ 编译依赖管理技术
- ✅ 访问者模式的双重分派

### 设计层面

- ✅ 开闭原则的实际应用
- ✅ 单一职责原则
- ✅ 接口隔离原则
- ✅ 依赖倒置原则
- ✅ 设计模式的组合使用

### 工程层面

- ✅ 编译防火墙技术
- ✅ 二进制兼容性
- ✅ 头文件依赖管理
- ✅ 单元测试编写
- ✅ 构建系统配置

## 扩展方向

1. **性能对比**：对比 variant vs 虚函数的性能差异
2. **更多装饰器**：添加重试、熔断、限流等装饰器
3. **序列化**：使用 Visitor 实现对象序列化
4. **持久化**：使用 PIMPL 隐藏数据库实现
5. **插件系统**：使用 Prototype 实现策略克隆和注册

## 作者

量化转行学习计划 - Week 6

## 许可

本项目仅供学习使用。
