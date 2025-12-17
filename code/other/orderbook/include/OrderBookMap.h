#pragma once

#include "Order.h"
#include <map>
#include <unordered_map>
#include <memory>

class OrderBookMap
{
private:
    // 使用 std::map 存储价格级别，key 是价格，value 是该价格的总量
    std::map<double, uint64_t> buyLevels;  // 买单：价格从高到低
    std::map<double, uint64_t> sellLevels; // 卖单：价格从低到高

    // 存储订单 ID 到订单的映射，用于快速查找和删除
    std::unordered_map<uint64_t, Order> orders;

public:
    OrderBookMap() = default;

    // 添加订单
    void addOrder(const Order &order)
    {
        orders[order.orderId] = order;

        if (order.side == OrderSide::BUY)
        {
            buyLevels[order.price] += order.quantity;
        }
        else
        {
            sellLevels[order.price] += order.quantity;
        }
    }

    // 取消订单
    bool cancelOrder(uint64_t orderId)
    {
        auto it = orders.find(orderId);
        if (it == orders.end())
        {
            return false;
        }

        const Order &order = it->second;

        if (order.side == OrderSide::BUY)
        {
            auto levelIt = buyLevels.find(order.price);
            if (levelIt != buyLevels.end())
            {
                levelIt->second -= order.quantity;
                if (levelIt->second == 0)
                {
                    buyLevels.erase(levelIt);
                }
            }
        }
        else
        {
            auto levelIt = sellLevels.find(order.price);
            if (levelIt != sellLevels.end())
            {
                levelIt->second -= order.quantity;
                if (levelIt->second == 0)
                {
                    sellLevels.erase(levelIt);
                }
            }
        }

        orders.erase(it);
        return true;
    }

    // 修改订单数量
    bool modifyOrder(uint64_t orderId, uint64_t newQuantity)
    {
        auto it = orders.find(orderId);
        if (it == orders.end())
        {
            return false;
        }

        Order &order = it->second;
        uint64_t quantityDiff = newQuantity - order.quantity;

        if (order.side == OrderSide::BUY)
        {
            buyLevels[order.price] += quantityDiff;
        }
        else
        {
            sellLevels[order.price] += quantityDiff;
        }

        order.quantity = newQuantity;
        return true;
    }

    // 获取最佳买价
    bool getBestBid(double &price, uint64_t &quantity) const
    {
        if (buyLevels.empty())
        {
            return false;
        }
        // map 默认升序，rbegin() 获取最大值（最高买价）
        auto it = buyLevels.rbegin();
        price = it->first;
        quantity = it->second;
        return true;
    }

    // 获取最佳卖价
    bool getBestAsk(double &price, uint64_t &quantity) const
    {
        if (sellLevels.empty())
        {
            return false;
        }
        // map 默认升序，begin() 获取最小值（最低卖价）
        auto it = sellLevels.begin();
        price = it->first;
        quantity = it->second;
        return true;
    }

    // 获取订单总数
    size_t getOrderCount() const
    {
        return orders.size();
    }

    // 获取买价级别数
    size_t getBuyLevelCount() const
    {
        return buyLevels.size();
    }

    // 获取卖价级别数
    size_t getSellLevelCount() const
    {
        return sellLevels.size();
    }

    // 清空订单簿
    void clear()
    {
        orders.clear();
        buyLevels.clear();
        sellLevels.clear();
    }
};
