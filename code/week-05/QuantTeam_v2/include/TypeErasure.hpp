#pragma once

#include <memory>
#include <string>
#include <iostream>

/**
 * Type Erasure - 类型擦除包装器
 * 优势：无需继承，统一接口，值语义
 * 类似 std::function 的实现原理
 */

class AnyStrategy {
private:
    // 内部抽象接口
    struct StrategyInterface {
        virtual ~StrategyInterface() = default;
        virtual void execute(const std::string& name) const = 0;
        virtual std::string get_name() const = 0;
        virtual std::unique_ptr<StrategyInterface> clone() const = 0;
    };

    // 模板实现类 - 包装任何类型
    template<typename T>
    struct StrategyImpl : StrategyInterface {
        T strategy;

        explicit StrategyImpl(T s) : strategy(std::move(s)) {}

        void execute(const std::string& name) const override {
            // 调用 T 的 execute 方法（无需继承）
            strategy.execute(name);
        }

        std::string get_name() const override {
            return std::string(strategy.name());
        }

        std::unique_ptr<StrategyInterface> clone() const override {
            return std::make_unique<StrategyImpl>(strategy);
        }
    };

    std::unique_ptr<StrategyInterface> impl;

public:
    // 接受任何有 execute 和 name 方法的类型
    template<typename T>
    AnyStrategy(T strategy)
        : impl(std::make_unique<StrategyImpl<T>>(std::move(strategy))) {}

    // 拷贝构造
    AnyStrategy(const AnyStrategy& other)
        : impl(other.impl ? other.impl->clone() : nullptr) {}

    // 移动构造
    AnyStrategy(AnyStrategy&&) noexcept = default;

    // 拷贝赋值
    AnyStrategy& operator=(const AnyStrategy& other) {
        if (this != &other) {
            impl = other.impl ? other.impl->clone() : nullptr;
        }
        return *this;
    }

    // 移动赋值
    AnyStrategy& operator=(AnyStrategy&&) noexcept = default;

    // 统一接口
    void execute(const std::string& name) const {
        if (impl) {
            impl->execute(name);
        }
    }

    std::string get_name() const {
        return impl ? impl->get_name() : "None";
    }
};

// ========== 无需继承的策略类 ==========

struct SimpleStrategy {
    void execute(const std::string& name) const {
        std::cout << "  [简单策略] " << name << " 执行简单策略\n";
    }

    constexpr std::string_view name() const {
        return "简单策略";
    }
};

struct ComplexStrategy {
    void execute(const std::string& name) const {
        std::cout << "  [复杂策略] " << name << " 执行复杂多步骤策略\n";
        std::cout << "    步骤 1: 数据预处理\n";
        std::cout << "    步骤 2: 模型计算\n";
        std::cout << "    步骤 3: 结果输出\n";
    }

    constexpr std::string_view name() const {
        return "复杂策略";
    }
};

struct LambdaStrategy {
    std::function<void(const std::string&)> func;

    explicit LambdaStrategy(std::function<void(const std::string&)> f)
        : func(std::move(f)) {}

    void execute(const std::string& name) const {
        func(name);
    }

    constexpr std::string_view name() const {
        return "Lambda策略";
    }
};
