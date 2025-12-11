# 量化私募团队框架 v2.0 - Week 5

## 项目概述

这是 Week 5 的量化私募团队框架，在 Week 4 的基础上应用了 **5 种 C++ OOP 高级技术**：

1. ✅ **CRTP (奇异递归模板模式)** - 零虚函数开销的静态多态
2. ✅ **Mixin 类** - 通过多重继承组合功能
3. ✅ **Policy-Based Design** - 策略作为模板参数
4. ✅ **Type Erasure** - 无需继承的统一接口
5. ✅ **强类型 ID 系统** - 编译期类型安全

## 技术亮点

### CRTP 静态多态
- 消除虚函数调用开销
- 所有调用在编译期解析
- 可完全内联优化

### Mixin 功能组合
- 不修改原类添加新功能
- 遵循开闭原则
- 零运行时开销

### Policy-Based Design
- 编译期策略绑定
- 灵活组合不同 Policy
- 完全内联

### Type Erasure
- 任何类型都可使用
- 无需继承
- 值语义

### 强类型 ID
- 编译期类型检查
- 防止 ID 混淆
- 零运行时开销

## 项目结构

```
QuantTeam_v2/
├── include/              # 头文件
│   ├── StrongID.hpp      # 强类型 ID 系统
│   ├── Types.hpp         # 基础类型定义
│   ├── EmployeeBase.hpp  # CRTP Employee 基类
│   ├── StrategyBase.hpp  # CRTP Strategy 基类
│   ├── Employees.hpp     # 具体 Employee 实现
│   ├── Mixins.hpp        # Mixin 功能类
│   ├── PolicyBased.hpp   # Policy-Based Design
│   └── TypeErasure.hpp   # Type Erasure 实现
├── src/
│   └── main.cpp          # 主程序（演示所有特性）
├── CMakeLists.txt        # CMake 构建文件
├── Makefile              # Makefile 构建文件
└── README.md             # 本文件
```

## 编译和运行

### 方法 1: 使用 Makefile（推荐）

```bash
# 编译
make

# 编译并运行
make run

# 清理
make clean

# 重新构建
make rebuild
```

### 方法 2: 使用 CMake

```bash
# 创建构建目录
mkdir build && cd build

# 配置
cmake ..

# 编译
make

# 运行
./bin/QuantTeam_v2
```

### 方法 3: 直接编译

```bash
g++ -std=c++20 -Iinclude src/main.cpp -o QuantTeam_v2
./QuantTeam_v2
```

## 系统要求

- **C++ 标准**: C++20 或更高
- **编译器**:
  - GCC 10+ 或
  - Clang 10+ 或
  - MSVC 2019+
- **CMake**: 3.15+ (可选)

## 主程序演示

主程序 `main.cpp` 包含 6 个演示场景：

1. **demo_crtp()** - CRTP 静态多态演示
2. **demo_mixins()** - Mixin 功能组合演示
3. **demo_policy_based()** - Policy-Based Design 演示
4. **demo_strong_id()** - 强类型 ID 系统演示
5. **demo_type_erasure()** - Type Erasure 演示
6. **demo_combined()** - 综合技术演示

## 学习要点

### CRTP 关键点
- 派生类作为基类的模板参数
- `static_cast<Derived*>(this)` 实现静态转换
- 编译期多态，零开销

### Mixin 关键点
- 模板参数是基类
- 继承构造函数 `using Base::Base`
- 可以无限叠加功能

### Policy-Based 关键点
- Policy 是纯静态类
- 所有方法都是 static
- 编译期完全展开

### Type Erasure 关键点
- 内部使用虚函数（对外隐藏）
- 模板构造函数接受任何类型
- clone() 实现拷贝语义

### 强类型 ID 关键点
- 使用 Tag 类型区分不同 ID
- explicit 构造函数防止隐式转换
- constexpr 支持编译期使用

## 与 Week 4 的对比

| 特性 | Week 4 | Week 5 |
|------|--------|--------|
| 多态方式 | 运行时（虚函数） | 编译期（CRTP） |
| 功能扩展 | 修改基类 | Mixin 组合 |
| 策略选择 | 运行时指针 | 编译期模板 |
| ID 类型 | 字符串 | 强类型 ID |
| 性能开销 | 虚函数调用 | 零开销抽象 |

## 性能提升

- **虚函数消除**: CRTP 消除了所有虚函数调用
- **完全内联**: 编译期绑定允许编译器完全内联
- **零运行时开销**: Policy-Based 和 Mixin 零运行时开销
- **类型安全**: 强类型 ID 在编译期捕获错误

## 作者

量化转行学习 - Week 5 OOP 高级技术实践

## 许可

MIT License
