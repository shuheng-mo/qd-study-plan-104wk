#pragma once

#include <format>
#include <string>
#include <vector>
#include <chrono>
#include "Serialization.hpp"

/**
 * @brief 报表生成器 - 使用 std::format 生成专业报表
 *
 * 提供各种格式化报表的生成功能
 */
class ReportGenerator {
public:
    /**
     * @brief 生成投资组合报表
     */
    static std::string generate_portfolio_report(const PortfolioData& portfolio) {
        std::string report;

        // 报表头部
        report += std::format("╔{:═^60}╗\n", "");
        report += std::format("║{:^60}║\n", " Portfolio Report: " + portfolio.name + " ");
        report += std::format("╚{:═^60}╝\n", "");
        report += "\n";

        // 总览信息
        report += std::format("Total Value:     ${:>15.2f}\n", portfolio.total_value);
        report += std::format("Positions:       {:>15}\n", portfolio.positions.size());
        report += "\n";

        // 持仓明细表头
        report += std::format("{:─^60}\n", " Holdings ");
        report += std::format("{:<10} | {:>10} | {:>15} | {:>15}\n",
                             "Symbol", "Quantity", "Price", "Market Value");
        report += std::format("{:─^60}\n", "");

        // 持仓明细
        for (const auto& pos : portfolio.positions) {
            report += std::format("{:<10} | {:>10.2f} | ${:>14.2f} | ${:>14.2f}\n",
                                 pos.symbol,
                                 pos.quantity,
                                 pos.price,
                                 pos.market_value);
        }

        // 底部分隔线
        report += std::format("{:─^60}\n", "");
        report += std::format("{:<10} | {:>10} | {:>15} | ${:>14.2f}\n",
                             "TOTAL", "", "", portfolio.total_value);
        report += std::format("{:═^60}\n", "");

        return report;
    }

    /**
     * @brief 生成策略性能报表
     */
    static std::string generate_strategy_report(const StrategyData& strategy) {
        std::string report;

        // 报表头部
        report += std::format("\n╔{:═^70}╗\n", "");
        report += std::format("║{:^70}║\n", " Strategy Performance Report ");
        report += std::format("╚{:═^70}╝\n\n", "");

        // 策略名称
        report += std::format("Strategy:        {}\n", strategy.name);
        report += std::format("{:─^70}\n\n", "");

        // 关键指标
        report += "Key Metrics:\n";
        report += std::format("  Annual Return:    {:>10.2f}%\n", strategy.annual_return * 100);
        report += std::format("  Sharpe Ratio:     {:>10.2f}\n", strategy.sharpe_ratio);
        report += std::format("  Max Drawdown:     {:>10.2f}%\n", strategy.max_drawdown * 100);
        report += std::format("  Total Trades:     {:>10}\n", strategy.total_trades);
        report += std::format("  Daily Returns:    {:>10} records\n", strategy.daily_returns.size());
        report += "\n";

        // 统计信息
        if (!strategy.daily_returns.empty()) {
            double avg_return = 0.0;
            double max_return = strategy.daily_returns[0];
            double min_return = strategy.daily_returns[0];

            for (double ret : strategy.daily_returns) {
                avg_return += ret;
                if (ret > max_return) max_return = ret;
                if (ret < min_return) min_return = ret;
            }
            avg_return /= strategy.daily_returns.size();

            report += "Daily Returns Statistics:\n";
            report += std::format("  Average:          {:>10.4f}%\n", avg_return * 100);
            report += std::format("  Maximum:          {:>10.4f}%\n", max_return * 100);
            report += std::format("  Minimum:          {:>10.4f}%\n", min_return * 100);
            report += "\n";
        }

        // 评级
        std::string rating = "N/A";
        if (strategy.sharpe_ratio >= 3.0) {
            rating = "Excellent ⭐⭐⭐⭐⭐";
        } else if (strategy.sharpe_ratio >= 2.0) {
            rating = "Very Good ⭐⭐⭐⭐";
        } else if (strategy.sharpe_ratio >= 1.0) {
            rating = "Good ⭐⭐⭐";
        } else if (strategy.sharpe_ratio >= 0.5) {
            rating = "Fair ⭐⭐";
        } else {
            rating = "Poor ⭐";
        }

        report += std::format("Performance Rating: {}\n", rating);
        report += std::format("{:═^70}\n", "");

        return report;
    }

    /**
     * @brief 生成系统状态报表
     */
    static std::string generate_system_status_report(
        const std::string& system_name,
        const std::vector<std::pair<std::string, std::string>>& metrics) {

        std::string report;

        // 获取当前时间
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);

        std::tm tm_buf;
        #ifdef _WIN32
        localtime_s(&tm_buf, &time);
        #else
        localtime_r(&time, &tm_buf);
        #endif

        std::string timestamp = std::format("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}",
                                           tm_buf.tm_year + 1900,
                                           tm_buf.tm_mon + 1,
                                           tm_buf.tm_mday,
                                           tm_buf.tm_hour,
                                           tm_buf.tm_min,
                                           tm_buf.tm_sec);

        // 报表头部
        report += std::format("\n╔{:═^60}╗\n", "");
        report += std::format("║{:^60}║\n", " System Status Report ");
        report += std::format("╚{:═^60}╝\n\n", "");

        // 系统信息
        report += std::format("System:          {}\n", system_name);
        report += std::format("Timestamp:       {}\n", timestamp);
        report += std::format("{:─^60}\n\n", "");

        // 指标列表
        report += "Metrics:\n";
        for (const auto& [key, value] : metrics) {
            report += std::format("  {:20} : {}\n", key, value);
        }

        report += std::format("\n{:═^60}\n", "");

        return report;
    }

    /**
     * @brief 生成对比报表
     */
    static std::string generate_comparison_report(
        const std::vector<StrategyData>& strategies) {

        std::string report;

        // 报表头部
        report += std::format("\n╔{:═^80}╗\n", "");
        report += std::format("║{:^80}║\n", " Strategy Comparison Report ");
        report += std::format("╚{:═^80}╝\n\n", "");

        // 表头
        report += std::format("{:<20} | {:>12} | {:>12} | {:>12} | {:>10}\n",
                             "Strategy", "Return", "Sharpe", "Drawdown", "Trades");
        report += std::format("{:─^80}\n", "");

        // 策略数据
        for (const auto& strategy : strategies) {
            report += std::format("{:<20} | {:>11.2f}% | {:>12.2f} | {:>11.2f}% | {:>10}\n",
                                 strategy.name,
                                 strategy.annual_return * 100,
                                 strategy.sharpe_ratio,
                                 strategy.max_drawdown * 100,
                                 strategy.total_trades);
        }

        report += std::format("{:═^80}\n", "");

        // 找出最佳策略
        if (!strategies.empty()) {
            auto best_return = std::max_element(strategies.begin(), strategies.end(),
                [](const StrategyData& a, const StrategyData& b) {
                    return a.annual_return < b.annual_return;
                });

            auto best_sharpe = std::max_element(strategies.begin(), strategies.end(),
                [](const StrategyData& a, const StrategyData& b) {
                    return a.sharpe_ratio < b.sharpe_ratio;
                });

            report += "\nBest Performers:\n";
            report += std::format("  Highest Return:  {} ({:.2f}%)\n",
                                 best_return->name, best_return->annual_return * 100);
            report += std::format("  Highest Sharpe:  {} ({:.2f})\n",
                                 best_sharpe->name, best_sharpe->sharpe_ratio);
            report += std::format("{:═^80}\n", "");
        }

        return report;
    }

    /**
     * @brief 生成数据目录摘要
     */
    static std::string generate_directory_summary(
        const std::string& category,
        const std::vector<std::string>& files,
        std::uintmax_t total_size) {

        std::string report;

        report += std::format("\n{:=^50}\n", " " + category + " ");
        report += std::format("Total Files:  {}\n", files.size());
        report += std::format("Total Size:   {} bytes ({:.2f} KB)\n",
                             total_size, total_size / 1024.0);

        if (!files.empty()) {
            report += "\nFiles:\n";
            int count = 0;
            for (const auto& file : files) {
                report += std::format("  {:2}. {}\n", ++count, file);
                if (count >= 10) {  // 最多显示10个
                    report += std::format("  ... and {} more files\n", files.size() - count);
                    break;
                }
            }
        }

        report += std::format("{:=^50}\n", "");

        return report;
    }
};
