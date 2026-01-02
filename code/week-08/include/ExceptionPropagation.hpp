#pragma once

#include <exception>
#include <vector>
#include <mutex>
#include <thread>
#include <functional>
#include <iostream>
#include <format>

/**
 * Week 8 - 异常传播与高级异常模式
 *
 * 本文件演示了：
 * 1. std::exception_ptr - 捕获和重新抛出异常
 * 2. 嵌套异常 - 在异常中包装另一个异常
 * 3. 多线程异常传播
 * 4. 异常安全的回调管理
 */

// ============================================================================
// 异步任务管理器 - 多线程异常传播
// ============================================================================

/**
 * AsyncTaskManager 允许在多个线程中运行任务
 * 并捕获任何抛出的异常，稍后在主线程中处理
 */
class AsyncTaskManager {
private:
    std::vector<std::exception_ptr> exceptions;
    mutable std::mutex exceptions_mutex;  // mutable 允许在 const 函数中锁定
    std::vector<std::thread> threads;

public:
    AsyncTaskManager() = default;

    ~AsyncTaskManager() {
        // 等待所有线程完成
        wait_all();
    }

    // 禁止拷贝
    AsyncTaskManager(const AsyncTaskManager&) = delete;
    AsyncTaskManager& operator=(const AsyncTaskManager&) = delete;

    /**
     * 在新线程中运行任务，捕获任何异常
     */
    void run_task(std::function<void()> task) {
        threads.emplace_back([this, task = std::move(task)]() {
            try {
                task();
            } catch (...) {
                // 捕获当前异常并存储
                std::lock_guard<std::mutex> lock(exceptions_mutex);
                exceptions.push_back(std::current_exception());
            }
        });
    }

    /**
     * 等待所有任务完成
     */
    void wait_all() {
        for (auto& thread : threads) {
            if (thread.joinable()) {
                thread.join();
            }
        }
        threads.clear();
    }

    /**
     * 检查是否有异常
     */
    bool has_exceptions() const {
        std::lock_guard<std::mutex> lock(exceptions_mutex);
        return !exceptions.empty();
    }

    /**
     * 获取异常数量
     */
    size_t exception_count() const {
        std::lock_guard<std::mutex> lock(exceptions_mutex);
        return exceptions.size();
    }

    /**
     * 重新抛出第一个异常（如果有）
     */
    void rethrow_first_exception() {
        std::lock_guard<std::mutex> lock(exceptions_mutex);
        if (!exceptions.empty()) {
            std::rethrow_exception(exceptions.front());
        }
    }

    /**
     * 处理所有异常
     */
    void handle_all_exceptions(std::function<void(const std::exception&)> handler) {
        std::lock_guard<std::mutex> lock(exceptions_mutex);
        for (auto& ex_ptr : exceptions) {
            try {
                std::rethrow_exception(ex_ptr);
            } catch (const std::exception& e) {
                handler(e);
            } catch (...) {
                std::cerr << "Unknown exception caught\n";
            }
        }
    }

    /**
     * 清除所有异常
     */
    void clear_exceptions() {
        std::lock_guard<std::mutex> lock(exceptions_mutex);
        exceptions.clear();
    }
};

// ============================================================================
// 嵌套异常工具
// ============================================================================

namespace NestedExceptionUtils {
    /**
     * 递归打印嵌套异常的完整调用链
     */
    inline void print_nested_exception(const std::exception& e, int level = 0) {
        std::string indent(level * 2, ' ');
        std::cerr << indent << "Exception: " << e.what() << '\n';

        try {
            std::rethrow_if_nested(e);
        } catch (const std::exception& nested) {
            print_nested_exception(nested, level + 1);
        } catch (...) {
            std::cerr << indent << "  Unknown nested exception\n";
        }
    }

    /**
     * 收集嵌套异常的所有消息
     */
    inline std::vector<std::string> collect_exception_messages(const std::exception& e) {
        std::vector<std::string> messages;
        messages.push_back(e.what());

        try {
            std::rethrow_if_nested(e);
        } catch (const std::exception& nested) {
            auto nested_messages = collect_exception_messages(nested);
            messages.insert(messages.end(), nested_messages.begin(), nested_messages.end());
        } catch (...) {
            messages.push_back("Unknown nested exception");
        }

        return messages;
    }

    /**
     * 获取嵌套深度
     */
    inline int get_nesting_depth(const std::exception& e) {
        int depth = 1;

        try {
            std::rethrow_if_nested(e);
        } catch (const std::exception& nested) {
            depth += get_nesting_depth(nested);
        } catch (...) {
            depth++;
        }

        return depth;
    }

    /**
     * 包装异常并添加上下文
     */
    template<typename Exception>
    [[noreturn]] void throw_with_context(const std::string& context) {
        try {
            throw;
        } catch (...) {
            std::throw_with_nested(Exception(context));
        }
    }
}

// ============================================================================
// 异常聚合器 - 收集多个异常
// ============================================================================

/**
 * ExceptionAggregator 收集多个操作中的所有异常
 * 并在最后一次性处理
 */
class ExceptionAggregator {
private:
    std::vector<std::exception_ptr> exceptions;
    std::vector<std::string> contexts;

public:
    /**
     * 执行操作并捕获任何异常
     */
    void try_execute(std::function<void()> func, const std::string& context = "") {
        try {
            func();
        } catch (...) {
            exceptions.push_back(std::current_exception());
            contexts.push_back(context);
        }
    }

    /**
     * 检查是否有异常
     */
    bool has_exceptions() const {
        return !exceptions.empty();
    }

    /**
     * 获取异常数量
     */
    size_t exception_count() const {
        return exceptions.size();
    }

    /**
     * 打印所有异常
     */
    void print_all() const {
        for (size_t i = 0; i < exceptions.size(); ++i) {
            std::cerr << std::format("Exception #{}: ", i + 1);
            if (!contexts[i].empty()) {
                std::cerr << "[" << contexts[i] << "] ";
            }

            try {
                std::rethrow_exception(exceptions[i]);
            } catch (const std::exception& e) {
                std::cerr << e.what() << '\n';
            } catch (...) {
                std::cerr << "Unknown exception\n";
            }
        }
    }

    /**
     * 抛出聚合异常（如果有）
     */
    void throw_if_any() const {
        if (!exceptions.empty()) {
            // 创建一个包含所有错误信息的异常
            std::string message = std::format("Multiple exceptions occurred ({} errors):\n",
                                             exceptions.size());

            for (size_t i = 0; i < exceptions.size(); ++i) {
                message += std::format("  {}. ", i + 1);
                if (!contexts[i].empty()) {
                    message += "[" + contexts[i] + "] ";
                }

                try {
                    std::rethrow_exception(exceptions[i]);
                } catch (const std::exception& e) {
                    message += e.what();
                } catch (...) {
                    message += "Unknown exception";
                }
                message += "\n";
            }

            throw std::runtime_error(message);
        }
    }

    /**
     * 清除所有异常
     */
    void clear() {
        exceptions.clear();
        contexts.clear();
    }
};

// ============================================================================
// 异常链 - 链式异常处理
// ============================================================================

/**
 * ExceptionChain 支持在多个步骤中逐步添加上下文信息
 */
class ExceptionChain {
private:
    std::exception_ptr current_exception;
    std::vector<std::string> contexts;

public:
    /**
     * 添加上下文并重新抛出异常
     */
    template<typename Exception>
    [[noreturn]] void add_context_and_throw(const std::string& context) {
        contexts.push_back(context);

        // 构建完整的错误消息
        std::string full_message;
        for (const auto& ctx : contexts) {
            full_message += ctx + " -> ";
        }

        try {
            if (current_exception) {
                std::rethrow_exception(current_exception);
            }
        } catch (const std::exception& e) {
            full_message += e.what();
        } catch (...) {
            full_message += "Unknown exception";
        }

        throw Exception(full_message);
    }

    /**
     * 捕获当前异常
     */
    void capture() {
        current_exception = std::current_exception();
    }
};

// ============================================================================
// 异常处理策略
// ============================================================================

/**
 * RetryPolicy - 重试策略，在失败时自动重试
 */
class RetryPolicy {
private:
    int max_retries;
    int retry_delay_ms;

public:
    RetryPolicy(int retries = 3, int delay_ms = 100)
        : max_retries(retries), retry_delay_ms(delay_ms) {}

    /**
     * 执行函数，失败时自动重试
     */
    template<typename Func>
    void execute_with_retry(Func func) {
        int attempt = 0;
        std::exception_ptr last_exception;

        while (attempt <= max_retries) {
            try {
                func();
                return;  // 成功，直接返回
            } catch (...) {
                last_exception = std::current_exception();
                attempt++;

                if (attempt <= max_retries) {
                    std::cerr << std::format("Attempt {} failed, retrying in {}ms...\n",
                                           attempt, retry_delay_ms);
                    std::this_thread::sleep_for(
                        std::chrono::milliseconds(retry_delay_ms));
                }
            }
        }

        // 所有重试都失败，重新抛出最后一个异常
        std::cerr << std::format("All {} attempts failed\n", max_retries + 1);
        if (last_exception) {
            std::rethrow_exception(last_exception);
        }
    }
};
