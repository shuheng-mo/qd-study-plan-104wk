#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include "../include/DataManager.hpp"
#include "../include/Logger.hpp"
#include "../include/Serialization.hpp"
#include "../include/CSVHandler.hpp"
#include "../include/SafeFileIO.hpp"
#include "../include/ReportGenerator.hpp"

/**
 * Week 7 - C++ IO与文件管理演示程序
 *
 * 演示内容：
 * 1. std::filesystem - 文件系统管理
 * 2. std::format - 日志系统
 * 3. 二进制序列化 - 数据持久化
 * 4. std::stringstream - CSV处理
 * 5. 流状态管理 - 安全文件IO
 */

void demo_filesystem_and_logger();
void demo_serialization();
void demo_csv_handling();
void demo_safe_file_io();
void demo_report_generation();

int main() {
    std::cout << R"(
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           Week 7 - C++ IO与文件管理演示程序                        ║
║                                                                   ║
║  本周学习内容：                                                     ║
║  1. std::filesystem - 现代文件系统操作                             ║
║  2. std::format - 类型安全的格式化日志                             ║
║  3. 二进制序列化 - 高效数据持久化                                  ║
║  4. std::stringstream - CSV数据处理                               ║
║  5. 流状态管理 - 健壮的错误处理                                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
)" << std::endl;

    try {
        // 演示1: 文件系统管理和日志系统
        demo_filesystem_and_logger();

        // 演示2: 二进制序列化
        demo_serialization();

        // 演示3: CSV处理
        demo_csv_handling();

        // 演示4: 安全文件IO
        demo_safe_file_io();

        // 演示5: 报表生成
        demo_report_generation();

        std::cout << "\n✓ 所有演示完成！\n" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "❌ Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

/**
 * 演示1: std::filesystem 和 Logger
 */
void demo_filesystem_and_logger() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示1: std::filesystem 文件系统管理 + Logger 日志系统\n";
    std::cout << std::string(70, '=') << "\n";

    // 创建数据管理器
    DataManager dm("./data");

    // 初始化全局日志器
    GlobalLogger::initialize(dm.get_log_path("2024-12-26"), Logger::Level::INFO);
    auto& logger = GlobalLogger::get();

    logger.info("SigmaX量化交易系统启动");
    logger.info("CTO Carol正式上任，开始系统现代化改造");

    // 演示文件操作
    logger.info("开始检查数据文件...");

    auto strategy_files = dm.list_files("strategies");
    logger.info("发现 {} 个策略文件", strategy_files.size());

    // 演示备份功能（如果有文件的话）
    if (!strategy_files.empty()) {
        dm.backup_file("strategies", strategy_files[0]);
        logger.info("策略文件已备份");
    }

    // 打印统计信息
    dm.print_statistics();

    // 演示不同级别的日志
    logger.debug("这是调试信息");
    logger.info("这是普通信息");
    logger.warning("投资组合回撤达到 {:.2f}%", 15.3);
    logger.error("策略 MomentumV2 执行失败: 数据不足");

    // 性能监控示例
    auto start = std::chrono::steady_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    auto end = std::chrono::steady_clock::now();
    logger.log_performance("策略回测", end - start);

    std::cout << "\n✓ 文件系统管理和日志系统演示完成\n";
}

/**
 * 演示2: 二进制序列化
 */
void demo_serialization() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示2: 二进制序列化 - 策略数据持久化\n";
    std::cout << std::string(70, '=') << "\n";

    auto& logger = GlobalLogger::get();
    logger.info("开始策略数据序列化演示");

    // 创建策略数据
    StrategyData momentum_strategy{
        "MomentumV3",               // 名称
        0.48,                       // 年化收益率
        2.1,                        // 夏普比率
        -0.12,                      // 最大回撤
        350,                        // 总交易次数
        {0.015, -0.008, 0.022, 0.011, -0.005, 0.018, 0.009, -0.003, 0.025, 0.012}  // 每日收益
    };

    logger.info("创建策略: {}, 年化收益: {:.2f}%",
                momentum_strategy.name, momentum_strategy.annual_return * 100);

    // 保存策略
    std::string strategy_file = "./data/data/strategies/momentum_v3.bin";
    DataPersistence::save_strategy(strategy_file, momentum_strategy);
    logger.info("策略数据已保存到: {}", strategy_file);

    // 加载策略
    auto loaded_strategy = DataPersistence::load_strategy(strategy_file);
    logger.info("策略数据已从文件加载");

    // 验证数据
    if (loaded_strategy.name == momentum_strategy.name &&
        loaded_strategy.annual_return == momentum_strategy.annual_return) {
        logger.info("✓ 数据完整性验证通过");
        loaded_strategy.print();
    } else {
        logger.error("❌ 数据完整性验证失败");
    }

    // 创建投资组合数据
    PortfolioData portfolio{
        "Alpha-Fund",
        0.0,
        {
            {"AAPL", 500.0, 175.25, 87625.0},
            {"TSLA", 300.0, 248.50, 74550.0},
            {"NVDA", 200.0, 495.75, 99150.0}
        }
    };
    portfolio.total_value = 261325.0;

    // 保存投资组合
    std::string portfolio_file = "./data/data/portfolios/alpha_fund.bin";
    DataPersistence::save_portfolio(portfolio_file, portfolio);
    logger.info("投资组合已保存");

    std::cout << "\n✓ 二进制序列化演示完成\n";
}

/**
 * 演示3: CSV处理
 */
void demo_csv_handling() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示3: CSV处理 - 与第三方数据对接\n";
    std::cout << std::string(70, '=') << "\n";

    auto& logger = GlobalLogger::get();
    logger.info("开始CSV数据处理演示");

    // 创建投资组合
    PortfolioData portfolio{
        "Growth-Portfolio",
        0.0,
        {
            {"AAPL", 500.0, 175.25, 87625.0},
            {"GOOGL", 200.0, 140.50, 28100.0},
            {"MSFT", 300.0, 370.25, 111075.0}
        }
    };
    portfolio.total_value = 226800.0;

    // 导出为CSV
    std::string csv_content = CSVExporter::export_portfolio_csv(portfolio);
    logger.info("投资组合已导出为CSV格式");
    std::cout << "\n导出的CSV内容:\n" << csv_content << std::endl;

    // 保存到文件
    std::string csv_file = "./data/data/portfolios/portfolio.csv";
    CSVFileHandler::save_csv_file(csv_file, csv_content);
    logger.info("CSV文件已保存: {}", csv_file);

    // 从文件加载CSV
    std::string loaded_csv = CSVFileHandler::load_csv_file(csv_file);

    // 导入CSV数据
    auto imported_portfolio = CSVImporter::import_portfolio_csv(loaded_csv);
    logger.info("CSV数据已导入，包含 {} 个持仓", imported_portfolio.positions.size());

    // 演示市场数据CSV
    std::vector<std::string> symbols = {"AAPL", "TSLA", "NVDA", "GOOGL", "MSFT"};
    std::vector<double> prices = {175.25, 248.50, 495.75, 140.50, 370.25};
    std::vector<double> volumes = {45000000, 38000000, 25000000, 18000000, 22000000};

    std::string market_csv = CSVExporter::export_market_data_csv(symbols, prices, volumes);
    std::cout << "\n市场数据CSV:\n" << market_csv << std::endl;

    // 保存并加载市场数据
    std::string market_file = "./data/data/market_data/market_snapshot.csv";
    CSVFileHandler::save_csv_file(market_file, market_csv);

    std::string loaded_market_csv = CSVFileHandler::load_csv_file(market_file);
    auto market_data = CSVImporter::import_market_data_csv(loaded_market_csv);
    market_data.print();

    logger.info("✓ CSV数据处理完成");
    std::cout << "\n✓ CSV处理演示完成\n";
}

/**
 * 演示4: 安全文件IO
 */
void demo_safe_file_io() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示4: 安全文件IO - 流状态管理\n";
    std::cout << std::string(70, '=') << "\n";

    auto& logger = GlobalLogger::get();
    logger.info("开始安全文件IO演示");

    // 写入测试文件
    std::string test_file = "./data/data/test_safe_io.txt";
    std::string test_content = "SigmaX Quant Trading System\nCarol's IO System Refactoring\n";

    try {
        SafeFileWriter::write_file(test_file, test_content);
        logger.info("✓ 文件写入成功: {}", test_file);

        // 读取文件
        std::string read_content = SafeFileReader::read_file(test_file);
        logger.info("✓ 文件读取成功，内容长度: {} bytes", read_content.size());

        // 追加内容
        SafeFileWriter::append_file(test_file, "Week 7 - IO & File Management\n");
        logger.info("✓ 内容追加成功");

        // 按行读取
        auto lines = SafeFileReader::read_lines(test_file);
        logger.info("✓ 读取 {} 行内容", lines.size());

        std::cout << "\n文件内容:\n";
        for (size_t i = 0; i < lines.size(); ++i) {
            std::cout << std::format("  Line {}: {}\n", i + 1, lines[i]);
        }

        // 文件完整性验证
        bool is_valid = FileIOUtils::verify_file_integrity(test_file);
        logger.info("文件完整性检查: {}", is_valid ? "通过" : "失败");

    } catch (const std::exception& e) {
        logger.error("文件IO错误: {}", e.what());
    }

    // 演示错误处理
    try {
        logger.info("尝试读取不存在的文件...");
        SafeFileReader::read_file("./nonexistent_file.txt");
    } catch (const std::exception& e) {
        logger.warning("预期的错误被正确捕获: {}", e.what());
    }

    std::cout << "\n✓ 安全文件IO演示完成\n";
}

/**
 * 演示5: 报表生成
 */
void demo_report_generation() {
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "演示5: 报表生成 - std::format专业报表\n";
    std::cout << std::string(70, '=') << "\n";

    auto& logger = GlobalLogger::get();
    logger.info("开始报表生成演示");

    // 创建投资组合
    PortfolioData portfolio{
        "SigmaX-Alpha",
        0.0,
        {
            {"AAPL", 500.0, 175.25, 87625.0},
            {"TSLA", 300.0, 248.50, 74550.0},
            {"NVDA", 200.0, 495.75, 99150.0},
            {"GOOGL", 200.0, 140.50, 28100.0},
            {"MSFT", 300.0, 370.25, 111075.0}
        }
    };
    portfolio.total_value = 400500.0;

    // 生成投资组合报表
    std::string portfolio_report = ReportGenerator::generate_portfolio_report(portfolio);
    std::cout << portfolio_report << std::endl;
    logger.info("✓ 投资组合报表已生成");

    // 创建策略数据
    StrategyData strategy{
        "MomentumV3",
        0.48,
        2.1,
        -0.12,
        350,
        {0.015, -0.008, 0.022, 0.011, -0.005, 0.018, 0.009, -0.003, 0.025, 0.012}
    };

    // 生成策略报表
    std::string strategy_report = ReportGenerator::generate_strategy_report(strategy);
    std::cout << strategy_report << std::endl;
    logger.info("✓ 策略性能报表已生成");

    // 创建多个策略进行对比
    std::vector<StrategyData> strategies = {
        {"MomentumV3", 0.48, 2.1, -0.12, 350, {}},
        {"MeanReversion", 0.35, 1.8, -0.15, 280, {}},
        {"PairTrading", 0.28, 1.5, -0.10, 420, {}},
        {"StatArbitrage", 0.52, 2.3, -0.18, 510, {}}
    };

    // 生成对比报表
    std::string comparison_report = ReportGenerator::generate_comparison_report(strategies);
    std::cout << comparison_report << std::endl;
    logger.info("✓ 策略对比报表已生成");

    // 生成系统状态报表
    std::vector<std::pair<std::string, std::string>> metrics = {
        {"Active Strategies", "4"},
        {"Total Positions", "5"},
        {"Portfolio Value", "$400,500.00"},
        {"Daily P&L", "+$12,350.00"},
        {"System Uptime", "99.8%"},
        {"Avg Latency", "2.3ms"}
    };

    std::string status_report = ReportGenerator::generate_system_status_report(
        "SigmaX Quant Trading System", metrics);
    std::cout << status_report << std::endl;
    logger.info("✓ 系统状态报表已生成");

    // 生成目录摘要
    DataManager dm("./data");
    auto files = dm.list_files("strategies");
    auto size = dm.get_directory_size("strategies");

    std::string dir_summary = ReportGenerator::generate_directory_summary(
        "Strategies", files, size);
    std::cout << dir_summary << std::endl;

    logger.info("✓ 所有报表生成完成");
    std::cout << "\n✓ 报表生成演示完成\n";
}
