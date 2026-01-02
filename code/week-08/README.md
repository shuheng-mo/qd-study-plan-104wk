# Week 8 - C++ 异常处理与错误管理

## 项目概述

本项目演示了现代 C++ 中的异常处理与错误管理技术，是量化私募团队框架 Week 8 的学习内容。

## 学习内容

### 1. 异常层次结构 (Exceptions.hpp)
- ✅ 基础异常类 `QuantTeamException`
- ✅ 数据异常 `DataException` 及其派生类
- ✅ 业务异常 `BusinessException` 及其派生类
- ✅ 系统异常 `SystemException` 及其派生类
- ✅ 使用 `std::source_location` 记录异常位置

### 2. RAII 与异常安全 (ExceptionSafety.hpp)
- ✅ `Transaction` 事务模板 - 强异常安全保证
- ✅ `ScopeGuard` - 自动资源清理
- ✅ `ResourceGuard` - 通用资源管理
- ✅ 异常安全的容器操作
- ✅ `noexcept` 的正确使用

### 3. Expected<T, E> (Expected.hpp)
- ✅ 函数式错误处理
- ✅ `and_then` 链式调用
- ✅ `transform` 值转换
- ✅ `or_else` 错误处理
- ✅ `value_or` 提供默认值

### 4. error_code 系统 (ErrorCode.hpp)
- ✅ 自定义错误码枚举
- ✅ 错误类别 `error_category`
- ✅ 与标准库错误处理集成
- ✅ `Result<T>` 包装返回值和错误

### 5. 异常传播 (ExceptionPropagation.hpp)
- ✅ `exception_ptr` 捕获和重新抛出
- ✅ 嵌套异常 `std::throw_with_nested`
- ✅ 多线程异常传播 `AsyncTaskManager`
- ✅ 异常聚合器 `ExceptionAggregator`
- ✅ 重试策略 `RetryPolicy`

## 项目结构

```
week-08/
├── include/
│   ├── Exceptions.hpp              # 异常层次结构
│   ├── ExceptionSafety.hpp         # RAII 与异常安全
│   ├── Expected.hpp                # Expected<T, E> 实现
│   ├── ErrorCode.hpp               # error_code 系统
│   └── ExceptionPropagation.hpp    # 异常传播
├── src/
│   └── main.cpp                    # 主程序和演示
├── CMakeLists.txt                  # 构建配置
└── README.md                       # 本文件
```

## 编译和运行

### 要求
- C++20 或更高版本
- CMake 3.20 或更高版本
- 支持 C++20 的编译器 (GCC 10+, Clang 10+, MSVC 2019+)

### 编译步骤

```bash
# 创建构建目录
mkdir build
cd build

# 配置项目
cmake ..

# 编译
cmake --build .

# 运行
./bin/week08_demo
```

### macOS/Linux
```bash
cd build
cmake ..
make
./bin/week08_demo
```

### Windows
```bash
cd build
cmake ..
cmake --build . --config Release
.\bin\Release\week08_demo.exe
```

## 演示内容

程序包含 5 个演示场景：

### 演示 1: 异常层次结构
展示如何使用细粒度的异常分类来处理不同类型的错误。

### 演示 2: RAII 与异常安全
演示 Transaction 事务模式和 ScopeGuard 的使用，确保强异常安全保证。

### 演示 3: Expected<T, E>
展示函数式错误处理的优势，包括链式调用和零开销。

### 演示 4: error_code
演示轻量级的错误码系统，适合系统级错误处理。

### 演示 5: 异常传播
展示多线程异常传播、嵌套异常和异常聚合等高级模式。

## 核心概念

### 异常 vs Expected vs error_code

| 特性 | 异常 | Expected | error_code |
|------|------|----------|-----------|
| **性能** | 有开销 | 零开销 | 零开销 |
| **显式性** | 隐式 | 显式 | 显式 |
| **类型安全** | ✓ | ✓ | ✓ |
| **适用场景** | 罕见错误 | 预期错误 | 系统错误 |
| **控制流** | 非本地跳转 | 本地处理 | 本地处理 |

### 何时使用

- **异常**: 真正的异常情况，不期望发生的错误
- **Expected**: 可预期的错误，需要显式处理
- **error_code**: 系统级错误，与标准库集成

## 最佳实践

1. **异常层次**: 设计清晰的异常层次结构，支持细粒度捕获
2. **RAII**: 使用 RAII 管理资源，确保异常安全
3. **noexcept**: 为移动构造和移动赋值标记 noexcept
4. **强异常保证**: 使用 Transaction 模式实现强异常安全
5. **显式错误**: 对于可预期的错误，使用 Expected 而非异常

## 与 Week 7 的关联

Week 8 建立在 Week 7 的基础上：
- Week 7 解决了 IO 和文件管理问题
- Week 8 解决了错误处理和异常安全问题
- 两者结合，构建了健壮的系统

## 参考资料

- C++20 标准
- [cppreference - Exception handling](https://en.cppreference.com/w/cpp/error)
- [C++ Core Guidelines - Error handling](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-errors)
- Week 7-8 优化计划文档

## 作者

SigmaX 量化团队 - Week 8 学习项目
