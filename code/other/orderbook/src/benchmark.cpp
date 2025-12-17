#include "OrderBookMap.h"
#include "OrderBookVector.h"
#include <chrono>
#include <iostream>
#include <random>
#include <iomanip>
#include <vector>

using namespace std::chrono;

class BenchmarkTimer {
private:
    high_resolution_clock::time_point startTime;
    std::string name;

public:
    BenchmarkTimer(const std::string& n) : name(n) {
        startTime = high_resolution_clock::now();
    }

    ~BenchmarkTimer() {
        auto endTime = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(endTime - startTime).count();
        std::cout << std::setw(40) << std::left << name
                  << ": " << std::setw(12) << std::right << duration
                  << " μs" << std::endl;
    }

    static double getDuration(high_resolution_clock::time_point start) {
        auto end = high_resolution_clock::now();
        return duration_cast<microseconds>(end - start).count();
    }
};

// 生成随机订单
std::vector<Order> generateRandomOrders(size_t count, double minPrice, double maxPrice) {
    std::vector<Order> orders;
    orders.reserve(count);

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> priceDist(minPrice, maxPrice);
    std::uniform_int_distribution<> quantityDist(100, 10000);
    std::uniform_int_distribution<> sideDist(0, 1);

    for (size_t i = 0; i < count; ++i) {
        double price = std::round(priceDist(gen) * 100.0) / 100.0;  // 保留两位小数
        uint64_t quantity = quantityDist(gen);
        OrderSide side = sideDist(gen) == 0 ? OrderSide::BUY : OrderSide::SELL;
        orders.emplace_back(i, price, quantity, side);
    }

    return orders;
}

// 测试添加订单性能
template<typename OrderBookType>
void benchmarkAddOrders(const std::string& name, const std::vector<Order>& orders) {
    OrderBookType orderBook;

    auto start = high_resolution_clock::now();
    for (const auto& order : orders) {
        orderBook.addOrder(order);
    }
    auto duration = BenchmarkTimer::getDuration(start);

    std::cout << std::setw(40) << std::left << (name + " - Add " + std::to_string(orders.size()) + " orders")
              << ": " << std::setw(12) << std::right << duration << " μs" << std::endl;
}

// 测试取消订单性能
template<typename OrderBookType>
void benchmarkCancelOrders(const std::string& name, const std::vector<Order>& orders) {
    OrderBookType orderBook;

    // 先添加所有订单
    for (const auto& order : orders) {
        orderBook.addOrder(order);
    }

    // 随机选择订单进行取消
    std::random_device rd;
    std::mt19937 gen(rd());
    std::vector<uint64_t> orderIds;
    for (const auto& order : orders) {
        orderIds.push_back(order.orderId);
    }
    std::shuffle(orderIds.begin(), orderIds.end(), gen);

    // 取消一半的订单
    size_t cancelCount = orderIds.size() / 2;
    auto start = high_resolution_clock::now();
    for (size_t i = 0; i < cancelCount; ++i) {
        orderBook.cancelOrder(orderIds[i]);
    }
    auto duration = BenchmarkTimer::getDuration(start);

    std::cout << std::setw(40) << std::left << (name + " - Cancel " + std::to_string(cancelCount) + " orders")
              << ": " << std::setw(12) << std::right << duration << " μs" << std::endl;
}

// 测试修改订单性能
template<typename OrderBookType>
void benchmarkModifyOrders(const std::string& name, const std::vector<Order>& orders) {
    OrderBookType orderBook;

    // 先添加所有订单
    for (const auto& order : orders) {
        orderBook.addOrder(order);
    }

    // 随机修改订单数量
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> quantityDist(100, 10000);

    size_t modifyCount = orders.size() / 2;
    auto start = high_resolution_clock::now();
    for (size_t i = 0; i < modifyCount; ++i) {
        orderBook.modifyOrder(orders[i].orderId, quantityDist(gen));
    }
    auto duration = BenchmarkTimer::getDuration(start);

    std::cout << std::setw(40) << std::left << (name + " - Modify " + std::to_string(modifyCount) + " orders")
              << ": " << std::setw(12) << std::right << duration << " μs" << std::endl;
}

// 测试获取最佳价格性能
template<typename OrderBookType>
void benchmarkGetBestPrices(const std::string& name, const std::vector<Order>& orders) {
    OrderBookType orderBook;

    // 先添加所有订单
    for (const auto& order : orders) {
        orderBook.addOrder(order);
    }

    const int iterations = 1000000;  // 100万次查询
    double price;
    uint64_t quantity;

    auto start = high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
        orderBook.getBestBid(price, quantity);
        orderBook.getBestAsk(price, quantity);
    }
    auto duration = BenchmarkTimer::getDuration(start);

    std::cout << std::setw(40) << std::left << (name + " - Get best prices " + std::to_string(iterations) + " times")
              << ": " << std::setw(12) << std::right << duration << " μs" << std::endl;
}

// 测试混合操作性能
template<typename OrderBookType>
void benchmarkMixedOperations(const std::string& name, size_t operationCount) {
    OrderBookType orderBook;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> priceDist(100.0, 200.0);
    std::uniform_int_distribution<> quantityDist(100, 10000);
    std::uniform_int_distribution<> sideDist(0, 1);
    std::uniform_int_distribution<> opDist(0, 100);

    uint64_t nextOrderId = 0;
    std::vector<uint64_t> activeOrderIds;

    auto start = high_resolution_clock::now();

    for (size_t i = 0; i < operationCount; ++i) {
        int op = opDist(gen);

        if (op < 60 || activeOrderIds.empty()) {  // 60% 添加订单
            double price = std::round(priceDist(gen) * 100.0) / 100.0;
            uint64_t quantity = quantityDist(gen);
            OrderSide side = sideDist(gen) == 0 ? OrderSide::BUY : OrderSide::SELL;
            Order order(nextOrderId++, price, quantity, side);
            orderBook.addOrder(order);
            activeOrderIds.push_back(order.orderId);
        } else if (op < 80) {  // 20% 取消订单
            if (!activeOrderIds.empty()) {
                std::uniform_int_distribution<> indexDist(0, activeOrderIds.size() - 1);
                size_t index = indexDist(gen);
                orderBook.cancelOrder(activeOrderIds[index]);
                activeOrderIds.erase(activeOrderIds.begin() + index);
            }
        } else if (op < 95) {  // 15% 修改订单
            if (!activeOrderIds.empty()) {
                std::uniform_int_distribution<> indexDist(0, activeOrderIds.size() - 1);
                size_t index = indexDist(gen);
                orderBook.modifyOrder(activeOrderIds[index], quantityDist(gen));
            }
        } else {  // 5% 查询最佳价格
            double price;
            uint64_t quantity;
            orderBook.getBestBid(price, quantity);
            orderBook.getBestAsk(price, quantity);
        }
    }

    auto duration = BenchmarkTimer::getDuration(start);

    std::cout << std::setw(40) << std::left << (name + " - Mixed " + std::to_string(operationCount) + " operations")
              << ": " << std::setw(12) << std::right << duration << " μs" << std::endl;
}

void printSeparator() {
    std::cout << std::string(60, '=') << std::endl;
}

int main() {
    std::cout << "\n订单簿性能基准测试\n" << std::endl;
    std::cout << "编译器优化: ";
    #ifdef NDEBUG
        std::cout << "Release (-O3)" << std::endl;
    #else
        std::cout << "Debug (未优化)" << std::endl;
    #endif
    std::cout << std::endl;

    // 生成测试数据
    const size_t smallSize = 1000;
    const size_t mediumSize = 10000;
    const size_t largeSize = 100000;

    std::cout << "生成测试数据..." << std::endl;
    auto smallOrders = generateRandomOrders(smallSize, 100.0, 200.0);
    auto mediumOrders = generateRandomOrders(mediumSize, 100.0, 200.0);
    auto largeOrders = generateRandomOrders(largeSize, 100.0, 200.0);
    std::cout << "测试数据生成完成\n" << std::endl;

    // 测试添加订单
    printSeparator();
    std::cout << "测试 1: 添加订单性能" << std::endl;
    printSeparator();
    benchmarkAddOrders<OrderBookMap>("Map", smallOrders);
    benchmarkAddOrders<OrderBookVector>("Vector", smallOrders);
    std::cout << std::endl;
    benchmarkAddOrders<OrderBookMap>("Map", mediumOrders);
    benchmarkAddOrders<OrderBookVector>("Vector", mediumOrders);
    std::cout << std::endl;
    benchmarkAddOrders<OrderBookMap>("Map", largeOrders);
    benchmarkAddOrders<OrderBookVector>("Vector", largeOrders);
    std::cout << std::endl;

    // 测试取消订单
    printSeparator();
    std::cout << "测试 2: 取消订单性能" << std::endl;
    printSeparator();
    benchmarkCancelOrders<OrderBookMap>("Map", smallOrders);
    benchmarkCancelOrders<OrderBookVector>("Vector", smallOrders);
    std::cout << std::endl;
    benchmarkCancelOrders<OrderBookMap>("Map", mediumOrders);
    benchmarkCancelOrders<OrderBookVector>("Vector", mediumOrders);
    std::cout << std::endl;

    // 测试修改订单
    printSeparator();
    std::cout << "测试 3: 修改订单性能" << std::endl;
    printSeparator();
    benchmarkModifyOrders<OrderBookMap>("Map", smallOrders);
    benchmarkModifyOrders<OrderBookVector>("Vector", smallOrders);
    std::cout << std::endl;
    benchmarkModifyOrders<OrderBookMap>("Map", mediumOrders);
    benchmarkModifyOrders<OrderBookVector>("Vector", mediumOrders);
    std::cout << std::endl;

    // 测试获取最佳价格
    printSeparator();
    std::cout << "测试 4: 获取最佳价格性能" << std::endl;
    printSeparator();
    benchmarkGetBestPrices<OrderBookMap>("Map", smallOrders);
    benchmarkGetBestPrices<OrderBookVector>("Vector", smallOrders);
    std::cout << std::endl;

    // 测试混合操作
    printSeparator();
    std::cout << "测试 5: 混合操作性能" << std::endl;
    printSeparator();
    benchmarkMixedOperations<OrderBookMap>("Map", 10000);
    benchmarkMixedOperations<OrderBookVector>("Vector", 10000);
    std::cout << std::endl;
    benchmarkMixedOperations<OrderBookMap>("Map", 100000);
    benchmarkMixedOperations<OrderBookVector>("Vector", 100000);
    std::cout << std::endl;

    printSeparator();
    std::cout << "所有测试完成！" << std::endl;
    printSeparator();

    return 0;
}
