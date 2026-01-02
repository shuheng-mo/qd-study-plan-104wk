#pragma once

#include <utility>
#include <type_traits>
#include <memory>
#include <vector>
#include <functional>

/**
 * Week 8 - RAII 与异常安全
 *
 * 本文件演示了：
 * 1. Transaction 事务模板 - 强异常安全保证
 * 2. ScopeGuard - 自动清理资源
 * 3. 异常安全的容器操作
 * 4. noexcept 的使用
 */

// ============================================================================
// Transaction 事务模板 - 强异常安全保证
// ============================================================================

/**
 * Transaction 提供事务语义：
 * - 构造时备份原始状态
 * - 析构时如果未提交则自动回滚
 * - 只有显式调用 commit() 才会保留修改
 */
template<typename T>
class Transaction {
private:
    T& target;
    T backup;
    bool committed = false;

public:
    explicit Transaction(T& obj)
        : target(obj)
        , backup(obj) {  // 保存原始状态
    }

    ~Transaction() {
        if (!committed) {
            // 未提交则回滚
            try {
                target = std::move(backup);
            } catch (...) {
                // 析构函数中不能抛异常
                // 这里只能记录日志或终止程序
            }
        }
    }

    // 删除拷贝操作
    Transaction(const Transaction&) = delete;
    Transaction& operator=(const Transaction&) = delete;

    // 允许移动
    Transaction(Transaction&& other) noexcept
        : target(other.target)
        , backup(std::move(other.backup))
        , committed(other.committed) {
        other.committed = true;  // 防止其析构时回滚
    }

    void commit() noexcept {
        committed = true;
    }

    void rollback() {
        if (!committed) {
            target = std::move(backup);
            committed = true;  // 标记为已处理
        }
    }
};

// ============================================================================
// ScopeGuard - 自动执行清理操作
// ============================================================================

/**
 * ScopeGuard 在作用域结束时自动执行清理函数
 * 类似于 Python 的 with 语句或 Go 的 defer
 */
class ScopeGuard {
private:
    std::function<void()> cleanup_func;
    bool dismissed = false;

public:
    explicit ScopeGuard(std::function<void()> func)
        : cleanup_func(std::move(func)) {}

    ~ScopeGuard() {
        if (!dismissed && cleanup_func) {
            try {
                cleanup_func();
            } catch (...) {
                // 析构函数中捕获所有异常
            }
        }
    }

    // 禁止拷贝和移动
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;

    void dismiss() noexcept {
        dismissed = true;
    }
};

// 辅助函数 - 创建 ScopeGuard
inline ScopeGuard make_scope_guard(std::function<void()> func) {
    return ScopeGuard(std::move(func));
}

// ============================================================================
// ResourceGuard - 通用资源管理
// ============================================================================

/**
 * ResourceGuard 使用 RAII 管理任意资源
 * 类似于 std::unique_ptr 但更通用
 */
template<typename Resource, typename Deleter>
class ResourceGuard {
private:
    Resource resource;
    Deleter deleter;
    bool owns_resource = true;

public:
    ResourceGuard(Resource res, Deleter del)
        : resource(std::move(res))
        , deleter(std::move(del)) {}

    ~ResourceGuard() {
        if (owns_resource) {
            try {
                deleter(resource);
            } catch (...) {
                // 吞掉异常
            }
        }
    }

    // 禁止拷贝
    ResourceGuard(const ResourceGuard&) = delete;
    ResourceGuard& operator=(const ResourceGuard&) = delete;

    // 允许移动
    ResourceGuard(ResourceGuard&& other) noexcept
        : resource(std::move(other.resource))
        , deleter(std::move(other.deleter))
        , owns_resource(other.owns_resource) {
        other.owns_resource = false;
    }

    Resource& get() noexcept {
        return resource;
    }

    const Resource& get() const noexcept {
        return resource;
    }

    void release() noexcept {
        owns_resource = false;
    }
};

// 辅助函数 - 创建 ResourceGuard
template<typename Resource, typename Deleter>
ResourceGuard<Resource, Deleter> make_resource_guard(Resource res, Deleter del) {
    return ResourceGuard<Resource, Deleter>(std::move(res), std::move(del));
}

// ============================================================================
// 异常安全的向量操作
// ============================================================================

namespace ExceptionSafeOps {
    /**
     * 异常安全的批量添加操作
     * 使用拷贝-交换习惯用法提供强异常保证
     */
    template<typename T>
    void append_all(std::vector<T>& vec, const std::vector<T>& items) {
        std::vector<T> temp = vec;  // 拷贝当前状态
        temp.reserve(temp.size() + items.size());

        for (const auto& item : items) {
            temp.push_back(item);  // 可能抛异常
        }

        // 只有全部成功才交换
        vec.swap(temp);  // noexcept
    }

    /**
     * 异常安全的条件过滤
     */
    template<typename T, typename Predicate>
    void filter(std::vector<T>& vec, Predicate pred) {
        std::vector<T> temp;
        temp.reserve(vec.size());

        for (const auto& item : vec) {
            if (pred(item)) {
                temp.push_back(item);
            }
        }

        vec.swap(temp);  // noexcept
    }

    /**
     * 异常安全的映射操作
     */
    template<typename T, typename U, typename Func>
    std::vector<U> map(const std::vector<T>& vec, Func func) {
        std::vector<U> result;
        result.reserve(vec.size());

        for (const auto& item : vec) {
            result.push_back(func(item));  // 如果抛异常，result 会自动清理
        }

        return result;
    }
}

// ============================================================================
// 异常安全级别检查工具
// ============================================================================

namespace ExceptionSafetyCheck {
    // 检查类型是否具有 noexcept 移动构造
    template<typename T>
    inline constexpr bool has_noexcept_move_constructor() {
        return std::is_nothrow_move_constructible_v<T>;
    }

    // 检查类型是否具有 noexcept 移动赋值
    template<typename T>
    inline constexpr bool has_noexcept_move_assignment() {
        return std::is_nothrow_move_assignable_v<T>;
    }

    // 检查类型是否具有 noexcept 析构
    template<typename T>
    inline constexpr bool has_noexcept_destructor() {
        return std::is_nothrow_destructible_v<T>;
    }

    // 检查类型是否完全 noexcept（移动和析构）
    template<typename T>
    inline constexpr bool is_fully_noexcept() {
        return has_noexcept_move_constructor<T>() &&
               has_noexcept_move_assignment<T>() &&
               has_noexcept_destructor<T>();
    }
}

// ============================================================================
// 异常安全的交换函数
// ============================================================================

/**
 * 条件 noexcept 的 swap 函数
 * 只有当 T 的移动构造和移动赋值都是 noexcept 时，swap 才是 noexcept
 */
template<typename T>
void safe_swap(T& a, T& b) noexcept(
    std::is_nothrow_move_constructible_v<T> &&
    std::is_nothrow_move_assignable_v<T>) {

    T temp(std::move(a));
    a = std::move(b);
    b = std::move(temp);
}
