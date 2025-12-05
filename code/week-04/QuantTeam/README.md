# QuantTeam v2.0 - 重构版量化团队管理系统

现代化的量化团队管理系统，展示高级C++面向对象编程技术和量化金融业务场景。

## 🆕 v2.0 新特性

### 🎯 设计模式实现

- **工厂模式**: `EmployeeFactory` 统一管理员工创建
- **观察者模式**: 团队事件系统，成员间智能协作
- **策略模式**: 可切换的工作策略实现
- **模板方法模式**: 统一的员工工作流程框架

### 🏗️ 架构改进

- **异常处理**: 完整的自定义异常类层次
- **内存管理**: 智能指针全面应用
- **事件系统**: 团队成员间的消息传递机制
- **预算管理**: 财务约束和预算控制

### 💼 业务场景扩展

- **7种专业角色**: QR, QD, Trader, Risk Manager, Portfolio Manager, Data Scientist, Compliance Officer
- **真实工作流程**: 晨会、策略讨论、代码审查、风险评估、绩效回顾
- **协作机制**: 跨部门协作和团队互动
- **绩效系统**: 等级制度和奖金计算

## 📁 项目结构

```
QuantTeam/
├── include/                    # 头文件目录
│   ├── Employee.hpp           # 员工基类和观察者接口
│   ├── CoreMembers.hpp        # 7种核心团队成员类
│   ├── QuantTeam.hpp          # 团队管理类
│   ├── EmployeeFactory.hpp    # 工厂模式员工创建
│   ├── WorkStrategy.hpp       # 策略模式工作策略
│   ├── TeamEvent.hpp          # 团队事件系统
│   └── Exceptions.hpp         # 自定义异常类
├── src/                       # 源文件目录
│   ├── Employee.cpp           # 基类实现
│   ├── CoreMembers.cpp        # 团队成员实现
│   ├── QuantTeam.cpp          # 团队管理实现
│   ├── EmployeeFactory.cpp    # 工厂实现
│   ├── WorkStrategy.cpp       # 策略实现
│   ├── TeamEvent.cpp          # 事件系统实现
│   └── main.cpp              # 主程序演示
├── CMakeLists.txt            # CMake 构建文件
├── Makefile                  # Make 构建文件
└── README.md                 # 项目文档
```

## 🚀 构建与运行

### 使用 Make (推荐)

```bash
# 构建发布版本
make release

# 构建调试版本  
make debug

# 构建并运行
make run

# 运行测试
make test

# 清理构建文件
make clean

# 查看所有可用命令
make help
```

### 使用 CMake

```bash
# 创建构建目录
mkdir build && cd build

# 配置项目
cmake ..

# 构建项目
make

# 运行程序
./QuantTeam_v2
```

## 🎯 核心特性演示

### 1. 工厂模式创建员工

```cpp
// 统一的员工创建接口
auto researcher = EmployeeFactory::createEmployee(
    EmployeeType::QUANT_RESEARCHER, "Alice", 600000, EmployeeLevel::PRINCIPAL);
```

### 2. 观察者模式团队协作

```cpp
// 事件广播，自动通知相关团队成员
TeamEvent strategy_event(EventType::STRATEGY_PROPOSED, "Alice", "新策略提案");
team.broadcast_event(strategy_event);
```

### 3. 策略模式工作执行

```cpp
// 每种角色都有专属的工作策略
class QuantResearcher {
    std::unique_ptr<WorkStrategy> work_strategy;
    // 策略可动态切换
};
```

### 4. 异常安全的预算管理

```cpp
try {
    team.hire(expensive_employee);
} catch (const InsufficientFundsException& e) {
    // 预算不足时的优雅处理
}
```

## 🧠 学习要点

### C++ 高级特性

1. **RAII原则**: 智能指针自动资源管理
2. **设计模式**: 工厂、观察者、策略、模板方法
3. **异常安全**: 强异常安全保证
4. **多态性**: 虚函数和运行时类型识别
5. **现代C++**: C++17特性应用

### 量化金融场景

1. **团队协作**: 真实的量化团队工作流
2. **风险管理**: 实时风险监控和控制
3. **合规要求**: 监管合规检查流程
4. **业绩评估**: 多维度绩效考核体系
5. **数据科学**: ML/AI在量化投资中的应用

## 📊 运行示例

程序运行时将展示：

- 🏢 团队组建过程
- 👥 团队成员构成
- 💰 预算使用情况  
- 🌅 完整的日常运营流程
- 🤝 团队协作演示
- 💰 奖金计算示例

## 🔧 技术要求

- **C++17** 或更高版本
- **CMake 3.12+** 或 **GNU Make**
- **GCC 7+** 或 **Clang 6+** 推荐

## 🎓 教学价值

这个项目完美结合了：

- **理论学习**: 设计模式和C++高级特性
- **实践应用**: 真实的量化金融业务场景
- **工程实践**: 现代软件开发最佳实践

适合作为C++高级编程和量化金融工程的教学案例。
