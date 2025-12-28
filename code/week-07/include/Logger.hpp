#pragma once

#include <format>
#include <fstream>
#include <iostream>
#include <string>
#include <chrono>
#include <filesystem>
#include <mutex>

namespace fs = std::filesystem;

/**
 * @brief 日志系统 - 使用 std::format 实现类型安全的格式化日志
 *
 * 核心功能：
 * - 分级日志（DEBUG/INFO/WARNING/ERROR）
 * - 类型安全的格式化
 * - 自动时间戳
 * - 同时输出到文件和控制台
 * - 线程安全
 */
class Logger {
public:
    enum class Level {
        DEBUG = 0,
        INFO = 1,
        WARNING = 2,
        ERROR = 3
    };

private:
    Level min_level;
    std::ofstream log_file;
    std::mutex log_mutex;  // 线程安全

    /**
     * @brief 将日志级别转换为字符串
     */
    static std::string level_to_string(Level level) {
        switch (level) {
            case Level::DEBUG:   return "DEBUG";
            case Level::INFO:    return "INFO ";
            case Level::WARNING: return "WARN ";
            case Level::ERROR:   return "ERROR";
            default:             return "UNKNOWN";
        }
    }

    /**
     * @brief 获取当前时间戳
     */
    static std::string get_timestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()) % 1000;

        std::tm tm_buf;
        #ifdef _WIN32
        localtime_s(&tm_buf, &time);
        #else
        localtime_r(&time, &tm_buf);
        #endif

        return std::format("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:03d}",
                          tm_buf.tm_year + 1900,
                          tm_buf.tm_mon + 1,
                          tm_buf.tm_mday,
                          tm_buf.tm_hour,
                          tm_buf.tm_min,
                          tm_buf.tm_sec,
                          ms.count());
    }

public:
    /**
     * @brief 构造函数
     * @param log_path 日志文件路径
     * @param level 最小日志级别
     */
    explicit Logger(const fs::path& log_path, Level level = Level::INFO)
        : min_level(level) {

        // 确保日志目录存在
        if (log_path.has_parent_path()) {
            fs::create_directories(log_path.parent_path());
        }

        // 以追加模式打开日志文件
        log_file.open(log_path, std::ios::app);
        if (!log_file.is_open()) {
            throw std::runtime_error(
                std::format("Failed to open log file: {}", log_path.string())
            );
        }

        // 写入启动标记
        info("========== Logger Started ==========");
    }

    /**
     * @brief 析构函数
     */
    ~Logger() {
        if (log_file.is_open()) {
            info("========== Logger Stopped ==========");
            log_file.close();
        }
    }

    // 禁止拷贝
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    /**
     * @brief 设置最小日志级别
     */
    void set_min_level(Level level) {
        std::lock_guard<std::mutex> lock(log_mutex);
        min_level = level;
    }

    /**
     * @brief 通用日志函数 - 类型安全的格式化
     */
    template<typename... Args>
    void log(Level level, std::format_string<Args...> fmt, Args&&... args) {
        if (level < min_level) return;

        std::lock_guard<std::mutex> lock(log_mutex);

        auto message = std::format(fmt, std::forward<Args>(args)...);
        auto log_line = std::format("[{}] [{}] {}\n",
                                    get_timestamp(),
                                    level_to_string(level),
                                    message);

        // 写入文件
        log_file << log_line;
        log_file.flush();

        // 同时输出到控制台（WARNING和ERROR使用stderr）
        if (level >= Level::WARNING) {
            std::cerr << log_line;
        } else {
            std::cout << log_line;
        }
    }

    /**
     * @brief 便捷方法 - DEBUG级别
     */
    template<typename... Args>
    void debug(std::format_string<Args...> fmt, Args&&... args) {
        log(Level::DEBUG, fmt, std::forward<Args>(args)...);
    }

    /**
     * @brief 便捷方法 - INFO级别
     */
    template<typename... Args>
    void info(std::format_string<Args...> fmt, Args&&... args) {
        log(Level::INFO, fmt, std::forward<Args>(args)...);
    }

    /**
     * @brief 便捷方法 - WARNING级别
     */
    template<typename... Args>
    void warning(std::format_string<Args...> fmt, Args&&... args) {
        log(Level::WARNING, fmt, std::forward<Args>(args)...);
    }

    /**
     * @brief 便捷方法 - ERROR级别
     */
    template<typename... Args>
    void error(std::format_string<Args...> fmt, Args&&... args) {
        log(Level::ERROR, fmt, std::forward<Args>(args)...);
    }

    /**
     * @brief 记录性能指标
     */
    template<typename Duration>
    void log_performance(const std::string& operation, Duration duration) {
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
        info("Performance: {} completed in {}ms", operation, ms);
    }
};

/**
 * @brief 全局日志器实例（单例模式）
 */
class GlobalLogger {
private:
    static std::unique_ptr<Logger> instance;

public:
    static void initialize(const fs::path& log_path, Logger::Level level = Logger::Level::INFO) {
        instance = std::make_unique<Logger>(log_path, level);
    }

    static Logger& get() {
        if (!instance) {
            throw std::runtime_error("GlobalLogger not initialized");
        }
        return *instance;
    }
};

// 静态成员定义
inline std::unique_ptr<Logger> GlobalLogger::instance = nullptr;
