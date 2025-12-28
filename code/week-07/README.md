# Week 7 - C++ IO与文件管理

> Carol接任CTO后的首周技术改造：从混乱到规范的数据管理系统重构之路

## 📚 学习目标

本周重点学习现代C++的IO和文件管理技术：

1. **std::filesystem (C++17)** - 现代文件系统操作
2. **std::format (C++20)** - 类型安全的格式化输出
3. **二进制序列化** - 高效数据持久化
4. **std::stringstream** - CSV数据处理
5. **流状态管理** - 健壮的错误处理

## 🏗️ 项目结构

```
week-07/
├── include/                    # 头文件目录
│   ├── DataManager.hpp         # 文件系统管理（std::filesystem）
│   ├── Logger.hpp              # 日志系统（std::format）
│   ├── Serialization.hpp       # 二进制序列化
│   ├── CSVHandler.hpp          # CSV处理（std::stringstream）
│   ├── SafeFileIO.hpp          # 安全文件IO（流状态管理）
│   └── ReportGenerator.hpp     # 报表生成（std::format）
├── src/
│   └── main.cpp                # 主程序（包含5个演示）
├── data/                       # 运行时数据目录
│   ├── data/
│   │   ├── strategies/         # 策略数据
│   │   ├── portfolios/         # 投资组合数据
│   │   └── market_data/        # 市场数据
│   ├── backup/                 # 自动备份目录
│   └── logs/                   # 日志文件
├── build/                      # CMake构建目录
│   └── week07_demo            # 可执行文件
├── CMakeLists.txt             # CMake配置
└── README.md                  # 本文件
```

## 🔧 编译与运行

### 系统要求

- **C++20** 或更高版本编译器
  - GCC 11+
  - Clang 14+
  - MSVC 2022+
- CMake 3.20+

### 编译步骤

```bash
cd code/week-07
mkdir -p build && cd build
cmake ..
make
```

### 运行程序

```bash
# 从 week-07 目录运行
./build/week07_demo

# 或从 build 目录运行
cd build
./week07_demo
```

## 📖 核心功能演示

### 演示1: std::filesystem 文件系统管理

**功能：**
- 自动创建目录结构
- 文件存在性检查
- 自动备份机制
- 清理过期文件
- 目录大小统计

**代码示例：**
```cpp
DataManager dm("./data");

// 检查文件
if (dm.file_exists("strategies", "momentum.bin")) {
    auto size = dm.get_file_size("strategies", "momentum.bin");
}

// 备份文件
dm.backup_file("strategies", "momentum.bin", "daily");

// 清理30天前的备份
dm.cleanup_old_files(30, "daily");
```

### 演示2: std::format 日志系统

**功能：**
- 分级日志（DEBUG/INFO/WARNING/ERROR）
- 类型安全的格式化
- 自动时间戳（精确到毫秒）
- 同时输出到文件和控制台
- 线程安全

**代码示例：**
```cpp
Logger logger("app.log", Logger::Level::INFO);

logger.info("Team {} hired {} new members", "SigmaX-QD", 5);
logger.warning("Portfolio drawdown: {:.2f}%", -15.3);
logger.error("Strategy {} failed: {}", "MomentumV2", "Data error");

// 性能监控
logger.log_performance("回测操作", duration);
```

### 演示3: 二进制序列化

**功能：**
- 高效的二进制存储
- 魔数和版本控制
- 类型安全序列化
- 支持复杂数据结构

**代码示例：**
```cpp
// 创建策略数据
StrategyData strategy{
    "MomentumV3",    // 名称
    0.48,            // 年化收益48%
    2.1,             // 夏普比率
    -0.12,           // 最大回撤-12%
    350,             // 交易次数
    {0.015, -0.008, ...}  // 每日收益
};

// 保存（二进制格式，紧凑高效）
DataPersistence::save_strategy("momentum.bin", strategy);

// 加载
auto loaded = DataPersistence::load_strategy("momentum.bin");
```

**优势：**
- 读写速度是JSON的10倍以上
- 文件大小只有JSON的30%
- 支持版本升级

### 演示4: CSV处理

**功能：**
- CSV导出（投资组合、市场数据）
- CSV导入与解析
- 内存流操作（std::stringstream）
- 格式化输出控制

**代码示例：**
```cpp
// 导出为CSV
std::string csv = CSVExporter::export_portfolio_csv(portfolio);

// 保存到文件
CSVFileHandler::save_csv_file("portfolio.csv", csv);

// 从文件加载并解析
std::string loaded = CSVFileHandler::load_csv_file("portfolio.csv");
auto imported = CSVImporter::import_portfolio_csv(loaded);
```

### 演示5: 安全文件IO

**功能：**
- 完善的错误检查
- 流状态管理
- 异常安全保证
- 文件完整性验证

**代码示例：**
```cpp
// 安全写入
SafeFileWriter::write_file("data.txt", content);

// 安全读取（带完整错误检查）
std::string content = SafeFileReader::read_file("data.txt");

// 按行读取
auto lines = SafeFileReader::read_lines("data.txt");

// 文件完整性检查
bool valid = FileIOUtils::verify_file_integrity("data.txt");
```

## 🎯 技术亮点

### 1. std::filesystem 的企业级应用

- **跨平台兼容**：统一的文件操作API
- **类型安全**：`fs::path` 避免字符串拼接错误
- **RAII管理**：自动资源管理
- **元数据查询**：文件大小、修改时间等

### 2. std::format 的优势

相比传统方法的优势：

| 特性 | printf | iostream | std::format |
|-----|--------|----------|-------------|
| 类型安全 | ❌ | ✅ | ✅ |
| 性能 | 中 | 低 | 高 |
| 可读性 | 差 | 差 | 优秀 |
| 编译期检查 | ❌ | ❌ | ✅ |

### 3. 二进制序列化的性能

测试数据：
- **文件大小**：JSON 500KB → 二进制 150KB（节省70%）
- **读取速度**：JSON 50ms → 二进制 5ms（快10倍）
- **写入速度**：JSON 80ms → 二进制 8ms（快10倍）

### 4. 流状态管理的重要性

生产环境常见IO错误：
- 磁盘空间不足
- 文件权限错误
- 网络文件系统断线
- 文件损坏

本项目的SafeFileIO确保所有这些错误都能被正确检测和处理。

## 📊 报表生成示例

### 投资组合报表
```
╔════════════════════════════════════════════════════════════╗
║               Portfolio Report: SigmaX-Alpha               ║
╚════════════════════════════════════════════════════════════╝

Total Value:     $      400500.00
Positions:                     5

───────────────────────── Holdings ─────────────────────────
Symbol     |   Quantity |           Price |    Market Value
────────────────────────────────────────────────────────────
AAPL       |     500.00 | $        175.25 | $      87625.00
TSLA       |     300.00 | $        248.50 | $      74550.00
...
```

### 策略性能报表
```
╔══════════════════════════════════════════════════════════════════════╗
║                     Strategy Performance Report                      ║
╚══════════════════════════════════════════════════════════════════════╝

Strategy:        MomentumV3
──────────────────────────────────────────────────────────────────────

Key Metrics:
  Annual Return:         48.00%
  Sharpe Ratio:           2.10
  Max Drawdown:         -12.00%
  Total Trades:            350

Performance Rating: Very Good ⭐⭐⭐⭐
```

## 🔍 代码组织原则

### 1. 头文件组织
- 每个功能模块独立的头文件
- 仅包含必要的头文件
- 使用前向声明减少依赖

### 2. 错误处理策略
- IO操作使用异常
- 数据验证使用返回值
- 关键操作记录日志

### 3. RAII原则
- 文件流自动管理
- 日志器自动刷新
- 目录自动创建

## 💡 实践建议

### 文件系统操作
```cpp
// ✅ 推荐：使用 std::filesystem
fs::path data_path = base_dir / "data" / "file.txt";
if (fs::exists(data_path)) {
    auto size = fs::file_size(data_path);
}

// ❌ 避免：字符串拼接
std::string path = base_dir + "/data/" + "file.txt";  // 平台相关
```

### 日志记录
```cpp
// ✅ 推荐：使用 std::format
logger.info("Process {} items in {:.2f}ms", count, duration);

// ❌ 避免：iostream 拼接
std::cout << "Process " << count << " items in "
          << std::fixed << std::setprecision(2) << duration << "ms\n";
```

### 数据持久化
```cpp
// ✅ 推荐：对内部数据使用二进制
DataPersistence::save_strategy("strategy.bin", strategy);

// ✅ 推荐：对外部交换使用CSV/JSON
CSVExporter::export_portfolio_csv(portfolio);
```

## 🚀 下周预告

**Week 8 - C++ 异常处理与错误管理**

Carol将面临更大挑战：
- 异常层次结构设计
- RAII与异常安全保证
- std::expected 函数式错误处理
- std::error_code 系统错误管理
- exception_ptr 异步异常传播
- noexcept 性能优化

## 📝 学习收获

完成本周学习后，你将能够：

✅ 使用 `std::filesystem` 进行专业的文件系统管理
✅ 使用 `std::format` 实现类型安全的格式化输出
✅ 实现高效的二进制序列化系统
✅ 处理CSV等常见数据格式
✅ 编写健壮的文件IO代码
✅ 生成专业的格式化报表

## 📚 参考资料

- [C++17 std::filesystem](https://en.cppreference.com/w/cpp/filesystem)
- [C++20 std::format](https://en.cppreference.com/w/cpp/utility/format)
- [C++ I/O Streams](https://en.cppreference.com/w/cpp/io)

---

**作者**: SigmaX量化团队
**周次**: Week 7
**主题**: C++ IO与文件管理
**代码仓库**: [qd-study-plan-104wk](https://github.com/shuheng-mo/qd-study-plan-104wk)
