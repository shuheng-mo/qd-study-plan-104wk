#pragma once

#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <type_traits>
#include <format>
#include <stdexcept>

/**
 * @brief 二进制序列化工具类
 *
 * 提供类型安全的二进制序列化功能
 */
class BinarySerializer {
private:
    std::ofstream& os;

public:
    explicit BinarySerializer(std::ofstream& stream) : os(stream) {}

    /**
     * @brief 写入基本类型（POD类型）
     */
    template<typename T>
    void write(const T& value) {
        static_assert(std::is_trivially_copyable_v<T>,
                     "Type must be trivially copyable");
        os.write(reinterpret_cast<const char*>(&value), sizeof(T));
    }

    /**
     * @brief 写入字符串
     */
    void write_string(const std::string& str) {
        size_t size = str.size();
        write(size);
        os.write(str.data(), size);
    }

    /**
     * @brief 写入vector（基本类型）
     */
    template<typename T>
    void write_vector(const std::vector<T>& vec) {
        size_t size = vec.size();
        write(size);

        for (const auto& item : vec) {
            if constexpr (std::is_same_v<T, std::string>) {
                write_string(item);
            } else {
                write(item);
            }
        }
    }
};

/**
 * @brief 二进制反序列化工具类
 */
class BinaryDeserializer {
private:
    std::ifstream& is;

public:
    explicit BinaryDeserializer(std::ifstream& stream) : is(stream) {}

    /**
     * @brief 读取基本类型
     */
    template<typename T>
    T read() {
        static_assert(std::is_trivially_copyable_v<T>,
                     "Type must be trivially copyable");
        T value;
        is.read(reinterpret_cast<char*>(&value), sizeof(T));
        if (!is) {
            throw std::runtime_error("Failed to read data from stream");
        }
        return value;
    }

    /**
     * @brief 读取字符串
     */
    std::string read_string() {
        size_t size = read<size_t>();
        std::string str(size, '\0');
        is.read(str.data(), size);
        if (!is) {
            throw std::runtime_error("Failed to read string from stream");
        }
        return str;
    }

    /**
     * @brief 读取vector
     */
    template<typename T>
    std::vector<T> read_vector() {
        size_t size = read<size_t>();
        std::vector<T> vec;
        vec.reserve(size);

        for (size_t i = 0; i < size; ++i) {
            if constexpr (std::is_same_v<T, std::string>) {
                vec.push_back(read_string());
            } else {
                vec.push_back(read<T>());
            }
        }

        return vec;
    }

    /**
     * @brief 检查是否到达文件末尾
     */
    bool eof() const {
        return is.eof();
    }
};

/**
 * @brief 策略数据结构
 */
struct StrategyData {
    std::string name;
    double annual_return;
    double sharpe_ratio;
    double max_drawdown;
    int total_trades;
    std::vector<double> daily_returns;

    /**
     * @brief 序列化到流
     */
    void serialize(BinarySerializer& ser) const {
        ser.write_string(name);
        ser.write(annual_return);
        ser.write(sharpe_ratio);
        ser.write(max_drawdown);
        ser.write(total_trades);
        ser.write_vector(daily_returns);
    }

    /**
     * @brief 从流反序列化
     */
    static StrategyData deserialize(BinaryDeserializer& deser) {
        StrategyData data;
        data.name = deser.read_string();
        data.annual_return = deser.read<double>();
        data.sharpe_ratio = deser.read<double>();
        data.max_drawdown = deser.read<double>();
        data.total_trades = deser.read<int>();
        data.daily_returns = deser.read_vector<double>();
        return data;
    }

    /**
     * @brief 打印策略信息
     */
    void print() const {
        std::cout << std::format("\nStrategy: {}\n", name);
        std::cout << std::format("  Annual Return:  {:>8.2f}%\n", annual_return * 100);
        std::cout << std::format("  Sharpe Ratio:   {:>8.2f}\n", sharpe_ratio);
        std::cout << std::format("  Max Drawdown:   {:>8.2f}%\n", max_drawdown * 100);
        std::cout << std::format("  Total Trades:   {:>8}\n", total_trades);
        std::cout << std::format("  Daily Returns:  {:>8} records\n", daily_returns.size());
    }
};

/**
 * @brief 投资组合持仓数据
 */
struct Position {
    std::string symbol;
    double quantity;
    double price;
    double market_value;

    void serialize(BinarySerializer& ser) const {
        ser.write_string(symbol);
        ser.write(quantity);
        ser.write(price);
        ser.write(market_value);
    }

    static Position deserialize(BinaryDeserializer& deser) {
        Position pos;
        pos.symbol = deser.read_string();
        pos.quantity = deser.read<double>();
        pos.price = deser.read<double>();
        pos.market_value = deser.read<double>();
        return pos;
    }
};

/**
 * @brief 投资组合数据
 */
struct PortfolioData {
    std::string name;
    double total_value;
    std::vector<Position> positions;

    void serialize(BinarySerializer& ser) const {
        ser.write_string(name);
        ser.write(total_value);
        size_t pos_count = positions.size();
        ser.write(pos_count);
        for (const auto& pos : positions) {
            pos.serialize(ser);
        }
    }

    static PortfolioData deserialize(BinaryDeserializer& deser) {
        PortfolioData portfolio;
        portfolio.name = deser.read_string();
        portfolio.total_value = deser.read<double>();
        size_t pos_count = deser.read<size_t>();
        portfolio.positions.reserve(pos_count);
        for (size_t i = 0; i < pos_count; ++i) {
            portfolio.positions.push_back(Position::deserialize(deser));
        }
        return portfolio;
    }
};

/**
 * @brief 数据持久化管理器
 */
class DataPersistence {
public:
    // 文件魔数：用于验证文件格式
    static constexpr uint32_t MAGIC_NUMBER = 0x5154414D;  // "QTAM" in hex
    static constexpr uint32_t VERSION = 1;

    /**
     * @brief 保存策略数据
     */
    static void save_strategy(const std::string& filename, const StrategyData& strategy) {
        std::ofstream ofs(filename, std::ios::binary);
        if (!ofs) {
            throw std::runtime_error(
                std::format("Failed to open file for writing: {}", filename)
            );
        }

        BinarySerializer ser(ofs);

        // 写入魔数和版本号
        ser.write(MAGIC_NUMBER);
        ser.write(VERSION);

        // 写入策略数据
        strategy.serialize(ser);

        std::cout << std::format("✓ Strategy saved: {} ({} bytes)\n",
                               filename, static_cast<size_t>(ofs.tellp()));
    }

    /**
     * @brief 加载策略数据
     */
    static StrategyData load_strategy(const std::string& filename) {
        std::ifstream ifs(filename, std::ios::binary);
        if (!ifs) {
            throw std::runtime_error(
                std::format("Failed to open file for reading: {}", filename)
            );
        }

        BinaryDeserializer deser(ifs);

        // 验证魔数
        uint32_t magic = deser.read<uint32_t>();
        if (magic != MAGIC_NUMBER) {
            throw std::runtime_error("Invalid file format: magic number mismatch");
        }

        // 检查版本
        uint32_t version = deser.read<uint32_t>();
        if (version != VERSION) {
            throw std::runtime_error(
                std::format("Unsupported version: {}", version)
            );
        }

        // 读取策略数据
        auto strategy = StrategyData::deserialize(deser);

        std::cout << std::format("✓ Strategy loaded: {}\n", filename);
        return strategy;
    }

    /**
     * @brief 保存投资组合数据
     */
    static void save_portfolio(const std::string& filename, const PortfolioData& portfolio) {
        std::ofstream ofs(filename, std::ios::binary);
        if (!ofs) {
            throw std::runtime_error(
                std::format("Failed to open file for writing: {}", filename)
            );
        }

        BinarySerializer ser(ofs);
        ser.write(MAGIC_NUMBER);
        ser.write(VERSION);
        portfolio.serialize(ser);

        std::cout << std::format("✓ Portfolio saved: {} ({} bytes)\n",
                               filename, static_cast<size_t>(ofs.tellp()));
    }

    /**
     * @brief 加载投资组合数据
     */
    static PortfolioData load_portfolio(const std::string& filename) {
        std::ifstream ifs(filename, std::ios::binary);
        if (!ifs) {
            throw std::runtime_error(
                std::format("Failed to open file for reading: {}", filename)
            );
        }

        BinaryDeserializer deser(ifs);

        uint32_t magic = deser.read<uint32_t>();
        if (magic != MAGIC_NUMBER) {
            throw std::runtime_error("Invalid file format");
        }

        uint32_t version = deser.read<uint32_t>();
        if (version != VERSION) {
            throw std::runtime_error(std::format("Unsupported version: {}", version));
        }

        auto portfolio = PortfolioData::deserialize(deser);
        std::cout << std::format("✓ Portfolio loaded: {}\n", filename);
        return portfolio;
    }
};
