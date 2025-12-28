#pragma once

#include <sstream>
#include <iomanip>
#include <vector>
#include <string>
#include <format>
#include "Serialization.hpp"

/**
 * @brief CSV导出器 - 使用 std::stringstream 进行格式化
 *
 * 提供CSV格式的数据导入导出功能
 */
class CSVExporter {
public:
    /**
     * @brief 导出投资组合为CSV格式
     */
    static std::string export_portfolio_csv(const PortfolioData& portfolio) {
        std::ostringstream oss;

        // CSV头
        oss << "Symbol,Quantity,Price,MarketValue\n";

        // 数据行
        for (const auto& pos : portfolio.positions) {
            oss << pos.symbol << ","
                << std::fixed << std::setprecision(2) << pos.quantity << ","
                << pos.price << ","
                << pos.market_value << "\n";
        }

        return oss.str();
    }

    /**
     * @brief 导出策略数据为CSV格式
     */
    static std::string export_strategy_csv(const StrategyData& strategy) {
        std::ostringstream oss;

        // 基本信息
        oss << "Strategy Name," << strategy.name << "\n";
        oss << "Annual Return," << std::fixed << std::setprecision(4)
            << (strategy.annual_return * 100) << "%\n";
        oss << "Sharpe Ratio," << strategy.sharpe_ratio << "\n";
        oss << "Max Drawdown," << (strategy.max_drawdown * 100) << "%\n";
        oss << "Total Trades," << strategy.total_trades << "\n";
        oss << "\n";

        // 每日收益数据
        oss << "Day,DailyReturn\n";
        for (size_t i = 0; i < strategy.daily_returns.size(); ++i) {
            oss << i + 1 << ","
                << std::fixed << std::setprecision(6)
                << (strategy.daily_returns[i] * 100) << "%\n";
        }

        return oss.str();
    }

    /**
     * @brief 导出市场数据为CSV格式
     */
    static std::string export_market_data_csv(
        const std::vector<std::string>& symbols,
        const std::vector<double>& prices,
        const std::vector<double>& volumes) {

        if (symbols.size() != prices.size() || symbols.size() != volumes.size()) {
            throw std::invalid_argument("Vector sizes must match");
        }

        std::ostringstream oss;

        // CSV头
        oss << "Symbol,Price,Volume\n";

        // 数据行
        for (size_t i = 0; i < symbols.size(); ++i) {
            oss << symbols[i] << ","
                << std::fixed << std::setprecision(2) << prices[i] << ","
                << std::fixed << std::setprecision(0) << volumes[i] << "\n";
        }

        return oss.str();
    }
};

/**
 * @brief CSV导入器
 */
class CSVImporter {
public:
    /**
     * @brief 从CSV导入投资组合数据
     */
    static PortfolioData import_portfolio_csv(const std::string& csv_data) {
        std::istringstream iss(csv_data);
        PortfolioData portfolio;
        portfolio.name = "Imported Portfolio";
        portfolio.total_value = 0.0;

        std::string line;

        // 跳过头行
        std::getline(iss, line);

        // 解析数据行
        while (std::getline(iss, line)) {
            if (line.empty()) continue;

            std::istringstream line_stream(line);
            std::string symbol, quantity_str, price_str, value_str;

            // 使用逗号分隔
            std::getline(line_stream, symbol, ',');
            std::getline(line_stream, quantity_str, ',');
            std::getline(line_stream, price_str, ',');
            std::getline(line_stream, value_str, ',');

            Position pos;
            pos.symbol = symbol;
            pos.quantity = std::stod(quantity_str);
            pos.price = std::stod(price_str);
            pos.market_value = std::stod(value_str);

            portfolio.positions.push_back(pos);
            portfolio.total_value += pos.market_value;
        }

        return portfolio;
    }

    /**
     * @brief 解析市场数据CSV（简化版）
     */
    struct MarketData {
        std::vector<std::string> symbols;
        std::vector<double> prices;
        std::vector<double> volumes;

        void print() const {
            std::cout << "\nMarket Data:\n";
            std::cout << std::format("{:>10} | {:>10} | {:>15}\n", "Symbol", "Price", "Volume");
            std::cout << std::string(40, '-') << "\n";
            for (size_t i = 0; i < symbols.size(); ++i) {
                std::cout << std::format("{:>10} | ${:>9.2f} | {:>15.0f}\n",
                                       symbols[i], prices[i], volumes[i]);
            }
        }
    };

    static MarketData import_market_data_csv(const std::string& csv_data) {
        std::istringstream iss(csv_data);
        MarketData data;
        std::string line;

        // 跳过头行
        std::getline(iss, line);

        // 解析数据行
        while (std::getline(iss, line)) {
            if (line.empty()) continue;

            std::istringstream line_stream(line);
            std::string symbol, price_str, volume_str;

            std::getline(line_stream, symbol, ',');
            std::getline(line_stream, price_str, ',');
            std::getline(line_stream, volume_str, ',');

            data.symbols.push_back(symbol);
            data.prices.push_back(std::stod(price_str));
            data.volumes.push_back(std::stod(volume_str));
        }

        return data;
    }
};

/**
 * @brief CSV文件处理器 - 提供完整的文件读写功能
 */
class CSVFileHandler {
public:
    /**
     * @brief 保存CSV到文件
     */
    static void save_csv_file(const std::string& filename, const std::string& csv_content) {
        std::ofstream ofs(filename);
        if (!ofs) {
            throw std::runtime_error(
                std::format("Failed to open file for writing: {}", filename)
            );
        }

        ofs << csv_content;
        std::cout << std::format("✓ CSV saved: {} ({} bytes)\n", filename, csv_content.size());
    }

    /**
     * @brief 从文件加载CSV
     */
    static std::string load_csv_file(const std::string& filename) {
        std::ifstream ifs(filename);
        if (!ifs) {
            throw std::runtime_error(
                std::format("Failed to open file for reading: {}", filename)
            );
        }

        std::ostringstream oss;
        oss << ifs.rdbuf();

        std::string content = oss.str();
        std::cout << std::format("✓ CSV loaded: {} ({} bytes)\n", filename, content.size());
        return content;
    }
};
