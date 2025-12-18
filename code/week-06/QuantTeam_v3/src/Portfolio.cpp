#include "AdvancedPatterns.hpp"
#include <map>
#include <iostream>
#include <iomanip>

// ============================================================================
// Portfolio::Impl - PIMPL 实现细节（隐藏在 cpp 文件中）
// ============================================================================

struct Position
{
    double quantity;
    double avg_price;
    double current_price;

    Position(double q, double p) : quantity(q), avg_price(p), current_price(p) {}

    double get_value() const { return quantity * current_price; }
    double get_pnl() const { return quantity * (current_price - avg_price); }
};

class Portfolio::Impl
{
public:
    std::string portfolio_name;
    double initial_capital;
    double cash;
    std::map<std::string, Position> positions;

    Impl(std::string name, double capital)
        : portfolio_name(std::move(name)),
          initial_capital(capital),
          cash(capital) {}

    void add_position(const std::string &symbol, double quantity, double price)
    {
        double cost = quantity * price;

        if (cost > cash)
        {
            std::cout << "[Portfolio] Insufficient cash for " << symbol
                      << " (Need: $" << cost << ", Available: $" << cash << ")\n";
            return;
        }

        auto it = positions.find(symbol);
        if (it != positions.end())
        {
            // 更新现有持仓
            double total_quantity = it->second.quantity + quantity;
            double total_cost = it->second.quantity * it->second.avg_price + cost;
            it->second.quantity = total_quantity;
            it->second.avg_price = total_cost / total_quantity;
            it->second.current_price = price;
        }
        else
        {
            // 新建持仓
            positions.emplace(symbol, Position{quantity, price});
        }

        cash -= cost;
        std::cout << "[Portfolio] Added " << quantity << " shares of " << symbol
                  << " at $" << price << " (Cash remaining: $" << cash << ")\n";
    }

    void remove_position(const std::string &symbol)
    {
        auto it = positions.find(symbol);
        if (it == positions.end())
        {
            std::cout << "[Portfolio] Position " << symbol << " not found\n";
            return;
        }

        double proceeds = it->second.get_value();
        cash += proceeds;

        std::cout << "[Portfolio] Sold all " << symbol
                  << " for $" << proceeds << " (P&L: $" << it->second.get_pnl() << ")\n";

        positions.erase(it);
    }

    double get_total_value() const
    {
        double total = cash;
        for (const auto &[symbol, pos] : positions)
        {
            total += pos.get_value();
        }
        return total;
    }

    double get_pnl() const
    {
        return get_total_value() - initial_capital;
    }

    void print_positions() const
    {
        std::cout << "\n===== Portfolio: " << portfolio_name << " =====\n";
        std::cout << "Cash: $" << std::fixed << std::setprecision(2) << cash << "\n\n";

        if (positions.empty())
        {
            std::cout << "No positions\n";
        }
        else
        {
            std::cout << std::left << std::setw(10) << "Symbol"
                      << std::right << std::setw(12) << "Quantity"
                      << std::setw(12) << "Avg Price"
                      << std::setw(12) << "Curr Price"
                      << std::setw(12) << "Value"
                      << std::setw(12) << "P&L" << "\n";
            std::cout << std::string(70, '-') << "\n";

            for (const auto &[symbol, pos] : positions)
            {
                std::cout << std::left << std::setw(10) << symbol
                          << std::right << std::setw(12) << pos.quantity
                          << std::setw(12) << pos.avg_price
                          << std::setw(12) << pos.current_price
                          << std::setw(12) << pos.get_value()
                          << std::setw(12) << pos.get_pnl() << "\n";
            }
        }

        std::cout << "\nTotal Value: $" << get_total_value() << "\n";
        std::cout << "Total P&L: $" << get_pnl() << "\n";
        std::cout << "===============================\n\n";
    }
};

// ============================================================================
// Portfolio 公共接口实现
// ============================================================================

Portfolio::Portfolio(std::string name, double initial_capital)
    : pimpl(std::make_unique<Impl>(std::move(name), initial_capital)) {}

Portfolio::~Portfolio() = default;

Portfolio::Portfolio(const Portfolio &other)
    : pimpl(std::make_unique<Impl>(*other.pimpl)) {}

Portfolio::Portfolio(Portfolio &&other) noexcept = default;

Portfolio &Portfolio::operator=(const Portfolio &other)
{
    if (this != &other)
    {
        pimpl = std::make_unique<Impl>(*other.pimpl);
    }
    return *this;
}

Portfolio &Portfolio::operator=(Portfolio &&other) noexcept = default;

void Portfolio::add_position(const std::string &symbol, double quantity, double price)
{
    pimpl->add_position(symbol, quantity, price);
}

void Portfolio::remove_position(const std::string &symbol)
{
    pimpl->remove_position(symbol);
}

double Portfolio::get_total_value() const
{
    return pimpl->get_total_value();
}

double Portfolio::get_pnl() const
{
    return pimpl->get_pnl();
}

void Portfolio::print_positions() const
{
    pimpl->print_positions();
}

std::string Portfolio::get_name() const
{
    return pimpl->portfolio_name;
}
