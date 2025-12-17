#pragma once

#include "Order.h"
#include <vector>
#include <unordered_map>
#include <algorithm>

class OrderBookVector {
private:
    // 使用 std::vector 存储价格级别
    // 买单：价格从高到低排序
    // 卖单：价格从低到高排序
    std::vector<PriceLevel> buyLevels;
    std::vector<PriceLevel> sellLevels;

    // 存储订单 ID 到订单的映射
    std::unordered_map<uint64_t, Order> orders;

    // 二分查找买价级别（降序）
    std::vector<PriceLevel>::iterator findBuyLevel(double price) {
        return std::lower_bound(buyLevels.begin(), buyLevels.end(), price,
            [](const PriceLevel& level, double p) {
                return level.price > p;  // 降序比较
            });
    }

    // 二分查找卖价级别（升序）
    std::vector<PriceLevel>::iterator findSellLevel(double price) {
        return std::lower_bound(sellLevels.begin(), sellLevels.end(), price,
            [](const PriceLevel& level, double p) {
                return level.price < p;  // 升序比较
            });
    }

public:
    OrderBookVector() {
        // 预分配空间，减少动态扩容
        buyLevels.reserve(1000);
        sellLevels.reserve(1000);
        orders.reserve(10000);
    }

    // 添加订单
    void addOrder(const Order& order) {
        orders[order.orderId] = order;

        if (order.side == OrderSide::BUY) {
            auto it = findBuyLevel(order.price);
            if (it != buyLevels.end() && it->price == order.price) {
                // 价格级别已存在，增加数量
                it->totalQuantity += order.quantity;
            } else {
                // 插入新的价格级别
                buyLevels.insert(it, PriceLevel(order.price, order.quantity));
            }
        } else {
            auto it = findSellLevel(order.price);
            if (it != sellLevels.end() && it->price == order.price) {
                it->totalQuantity += order.quantity;
            } else {
                sellLevels.insert(it, PriceLevel(order.price, order.quantity));
            }
        }
    }

    // 取消订单
    bool cancelOrder(uint64_t orderId) {
        auto it = orders.find(orderId);
        if (it == orders.end()) {
            return false;
        }

        const Order& order = it->second;

        if (order.side == OrderSide::BUY) {
            auto levelIt = findBuyLevel(order.price);
            if (levelIt != buyLevels.end() && levelIt->price == order.price) {
                levelIt->totalQuantity -= order.quantity;
                if (levelIt->totalQuantity == 0) {
                    buyLevels.erase(levelIt);
                }
            }
        } else {
            auto levelIt = findSellLevel(order.price);
            if (levelIt != sellLevels.end() && levelIt->price == order.price) {
                levelIt->totalQuantity -= order.quantity;
                if (levelIt->totalQuantity == 0) {
                    sellLevels.erase(levelIt);
                }
            }
        }

        orders.erase(it);
        return true;
    }

    // 修改订单数量
    bool modifyOrder(uint64_t orderId, uint64_t newQuantity) {
        auto it = orders.find(orderId);
        if (it == orders.end()) {
            return false;
        }

        Order& order = it->second;
        int64_t quantityDiff = static_cast<int64_t>(newQuantity) - static_cast<int64_t>(order.quantity);

        if (order.side == OrderSide::BUY) {
            auto levelIt = findBuyLevel(order.price);
            if (levelIt != buyLevels.end() && levelIt->price == order.price) {
                levelIt->totalQuantity += quantityDiff;
            }
        } else {
            auto levelIt = findSellLevel(order.price);
            if (levelIt != sellLevels.end() && levelIt->price == order.price) {
                levelIt->totalQuantity += quantityDiff;
            }
        }

        order.quantity = newQuantity;
        return true;
    }

    // 获取最佳买价
    bool getBestBid(double& price, uint64_t& quantity) const {
        if (buyLevels.empty()) {
            return false;
        }
        // vector 已按价格从高到低排序，第一个就是最高买价
        price = buyLevels.front().price;
        quantity = buyLevels.front().totalQuantity;
        return true;
    }

    // 获取最佳卖价
    bool getBestAsk(double& price, uint64_t& quantity) const {
        if (sellLevels.empty()) {
            return false;
        }
        // vector 已按价格从低到高排序，第一个就是最低卖价
        price = sellLevels.front().price;
        quantity = sellLevels.front().totalQuantity;
        return true;
    }

    // 获取订单总数
    size_t getOrderCount() const {
        return orders.size();
    }

    // 获取买价级别数
    size_t getBuyLevelCount() const {
        return buyLevels.size();
    }

    // 获取卖价级别数
    size_t getSellLevelCount() const {
        return sellLevels.size();
    }

    // 清空订单簿
    void clear() {
        orders.clear();
        buyLevels.clear();
        sellLevels.clear();
    }
};
