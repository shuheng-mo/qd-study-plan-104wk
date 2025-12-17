#pragma once

#include <cstdint>

enum class OrderSide
{
    BUY,
    SELL
};

struct Order
{
    uint64_t orderId;
    double price;
    uint64_t quantity;
    OrderSide side;

    Order(uint64_t id, double p, uint64_t q, OrderSide s)
        : orderId(id), price(p), quantity(q), side(s) {}

    Order() : orderId(0), price(0.0), quantity(0), side(OrderSide::BUY) {}
};

struct PriceLevel
{
    double price;
    uint64_t totalQuantity;

    PriceLevel(double p = 0.0, uint64_t q = 0)
        : price(p), totalQuantity(q) {}
};
