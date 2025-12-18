#pragma once

#include "Types.hpp"
#include <memory>
#include <iostream>
#include <unordered_map>
#include <chrono>
#include <stdexcept>

// ============================================================================
// Week 6 优化 6.2: Decorator Pattern - 装饰器模式
// ============================================================================
// 核心思想：动态地给对象添加额外功能，不修改原类
// 优势：开闭原则、灵活组合、单一职责、运行时配置
// ============================================================================

// 策略基类接口
class Strategy
{
public:
    virtual ~Strategy() = default;

    // 执行策略，返回信号强度
    virtual double execute(const MarketData &data) = 0;

    // 获取策略名称
    virtual std::string get_name() const = 0;
};

// ============================================================================
// 具体策略实现
// ============================================================================

// 动量策略
class MomentumStrategy : public Strategy
{
private:
    double threshold;

public:
    explicit MomentumStrategy(double thresh = 0.01) : threshold(thresh) {}

    double execute(const MarketData &data) override
    {
        // 简化的动量计算：价格变化率
        double signal = data.price * threshold;
        std::cout << "[MomentumStrategy] Analyzing " << data.symbol
                  << " at $" << data.price << " -> Signal: " << signal << "\n";
        return signal;
    }

    std::string get_name() const override { return "Momentum"; }
};

// 均值回归策略
class MeanReversionStrategy : public Strategy
{
private:
    double mean_price;

public:
    explicit MeanReversionStrategy(double mean = 100.0) : mean_price(mean) {}

    double execute(const MarketData &data) override
    {
        // 简化的均值回归：偏离均值的程度
        double deviation = (mean_price - data.price) / mean_price;
        std::cout << "[MeanReversionStrategy] " << data.symbol
                  << " deviation from mean: " << deviation << "\n";
        return deviation * 10.0; // 放大信号
    }

    std::string get_name() const override { return "MeanReversion"; }
};

// ============================================================================
// 装饰器基类
// ============================================================================
class StrategyDecorator : public Strategy
{
protected:
    std::unique_ptr<Strategy> wrapped;

public:
    explicit StrategyDecorator(std::unique_ptr<Strategy> s)
        : wrapped(std::move(s)) {}

    double execute(const MarketData &data) override
    {
        return wrapped->execute(data);
    }

    std::string get_name() const override
    {
        return wrapped->get_name();
    }
};

// ============================================================================
// 具体装饰器实现
// ============================================================================

// 日志装饰器
class LoggingDecorator : public StrategyDecorator
{
public:
    using StrategyDecorator::StrategyDecorator;

    double execute(const MarketData &data) override
    {
        std::cout << "[LOG] ===== Strategy Execution Started =====\n";
        std::cout << "[LOG] Strategy: " << wrapped->get_name() << "\n";
        std::cout << "[LOG] Symbol: " << data.symbol << ", Price: $" << data.price << "\n";

        double result = wrapped->execute(data);

        std::cout << "[LOG] Signal Returned: " << result << "\n";
        std::cout << "[LOG] ===== Strategy Execution Completed =====\n\n";

        return result;
    }

    std::string get_name() const override
    {
        return "Logged<" + wrapped->get_name() + ">";
    }
};

// 缓存装饰器
class CachingDecorator : public StrategyDecorator
{
private:
    mutable std::unordered_map<std::string, double> cache;
    mutable size_t cache_hits = 0;
    mutable size_t cache_misses = 0;

public:
    using StrategyDecorator::StrategyDecorator;

    double execute(const MarketData &data) override
    {
        std::string key = data.symbol + "_" + std::to_string(static_cast<int>(data.price));

        if (auto it = cache.find(key); it != cache.end())
        {
            ++cache_hits;
            std::cout << "[CACHE] HIT for " << key
                      << " (Hits: " << cache_hits << ", Misses: " << cache_misses << ")\n";
            return it->second;
        }

        ++cache_misses;
        std::cout << "[CACHE] MISS for " << key
                  << " (Hits: " << cache_hits << ", Misses: " << cache_misses << ")\n";

        double result = wrapped->execute(data);
        cache[key] = result;
        return result;
    }

    std::string get_name() const override
    {
        return "Cached<" + wrapped->get_name() + ">";
    }

    // 缓存统计
    void print_cache_stats() const
    {
        std::cout << "\n[CACHE STATS] Hits: " << cache_hits
                  << ", Misses: " << cache_misses
                  << ", Hit Rate: "
                  << (cache_hits + cache_misses > 0 ? (100.0 * cache_hits / (cache_hits + cache_misses)) : 0.0)
                  << "%\n";
    }
};

// 计时装饰器
class TimingDecorator : public StrategyDecorator
{
public:
    using StrategyDecorator::StrategyDecorator;

    double execute(const MarketData &data) override
    {
        auto start = std::chrono::high_resolution_clock::now();

        double result = wrapped->execute(data);

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

        std::cout << "[TIMING] Execution time: " << duration.count() << " μs\n";

        return result;
    }

    std::string get_name() const override
    {
        return "Timed<" + wrapped->get_name() + ">";
    }
};

// 重试装饰器
class RetryDecorator : public StrategyDecorator
{
private:
    int max_retries;
    double failure_rate; // 模拟失败率（0.0 - 1.0）

public:
    explicit RetryDecorator(std::unique_ptr<Strategy> s, int retries = 3, double fail_rate = 0.0)
        : StrategyDecorator(std::move(s)), max_retries(retries), failure_rate(fail_rate) {}

    double execute(const MarketData &data) override
    {
        for (int attempt = 1; attempt <= max_retries; ++attempt)
        {
            try
            {
                // 模拟随机失败
                if (failure_rate > 0.0 && attempt < max_retries)
                {
                    double rand_val = static_cast<double>(rand()) / RAND_MAX;
                    if (rand_val < failure_rate)
                    {
                        throw std::runtime_error("Simulated network error");
                    }
                }

                return wrapped->execute(data);
            }
            catch (const std::exception &e)
            {
                std::cout << "[RETRY] Attempt " << attempt << "/" << max_retries
                          << " failed: " << e.what() << "\n";

                if (attempt == max_retries)
                {
                    std::cout << "[RETRY] All attempts exhausted, re-throwing exception\n";
                    throw;
                }

                std::cout << "[RETRY] Retrying...\n";
            }
        }

        return 0.0; // Should never reach here
    }

    std::string get_name() const override
    {
        return "Retry<" + wrapped->get_name() + ">";
    }
};

// 信号过滤装饰器
class SignalFilterDecorator : public StrategyDecorator
{
private:
    double min_signal;
    double max_signal;

public:
    SignalFilterDecorator(std::unique_ptr<Strategy> s, double min_sig, double max_sig)
        : StrategyDecorator(std::move(s)), min_signal(min_sig), max_signal(max_sig) {}

    double execute(const MarketData &data) override
    {
        double signal = wrapped->execute(data);

        if (signal < min_signal || signal > max_signal)
        {
            std::cout << "[FILTER] Signal " << signal << " filtered out (range: "
                      << min_signal << " - " << max_signal << ")\n";
            return 0.0;
        }

        std::cout << "[FILTER] Signal " << signal << " passed filter\n";
        return signal;
    }

    std::string get_name() const override
    {
        return "Filtered<" + wrapped->get_name() + ">";
    }
};
