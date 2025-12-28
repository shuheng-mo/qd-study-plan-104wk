#pragma once

#include <filesystem>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <format>

namespace fs = std::filesystem;

/**
 * @brief 数据管理器 - 使用 std::filesystem 管理文件系统
 *
 * 核心功能：
 * - 自动创建和管理目录结构
 * - 文件存在性检查
 * - 自动备份机制
 * - 清理过期文件
 * - 目录大小统计
 */
class DataManager {
private:
    fs::path base_dir;
    fs::path data_dir;
    fs::path backup_dir;
    fs::path log_dir;

public:
    /**
     * @brief 构造函数 - 初始化目录结构
     * @param base_path 基础目录路径
     */
    explicit DataManager(const fs::path& base_path)
        : base_dir(base_path)
        , data_dir(base_path / "data")
        , backup_dir(base_path / "backup")
        , log_dir(base_path / "logs") {

        // 确保目录存在
        fs::create_directories(data_dir / "strategies");
        fs::create_directories(data_dir / "portfolios");
        fs::create_directories(data_dir / "market_data");
        fs::create_directories(backup_dir / "daily");
        fs::create_directories(backup_dir / "weekly");
        fs::create_directories(log_dir);

        std::cout << std::format("✓ DataManager initialized at: {}\n", base_dir.string());
    }

    /**
     * @brief 检查文件是否存在
     * @param category 分类（strategies/portfolios/market_data）
     * @param filename 文件名
     * @return 文件是否存在
     */
    bool file_exists(const std::string& category, const std::string& filename) const {
        auto path = data_dir / category / filename;
        return fs::exists(path);
    }

    /**
     * @brief 获取文件大小
     * @param category 分类
     * @param filename 文件名
     * @return 文件大小（字节）
     */
    std::uintmax_t get_file_size(const std::string& category, const std::string& filename) const {
        auto path = data_dir / category / filename;
        if (!fs::exists(path)) {
            throw std::runtime_error(std::format("File not found: {}", path.string()));
        }
        return fs::file_size(path);
    }

    /**
     * @brief 列出指定分类下的所有文件
     * @param category 分类
     * @return 文件名列表
     */
    std::vector<std::string> list_files(const std::string& category) const {
        std::vector<std::string> files;
        auto dir_path = data_dir / category;

        if (!fs::exists(dir_path)) {
            return files;
        }

        for (const auto& entry : fs::directory_iterator(dir_path)) {
            if (entry.is_regular_file()) {
                files.push_back(entry.path().filename().string());
            }
        }

        return files;
    }

    /**
     * @brief 备份文件到备份目录
     * @param category 分类
     * @param filename 文件名
     * @param backup_type 备份类型（daily/weekly）
     */
    void backup_file(const std::string& category, const std::string& filename,
                     const std::string& backup_type = "daily") {
        auto source = data_dir / category / filename;
        auto dest = backup_dir / backup_type / (filename + ".bak");

        if (!fs::exists(source)) {
            throw std::runtime_error(std::format("Source file not found: {}", source.string()));
        }

        fs::copy_file(source, dest, fs::copy_options::overwrite_existing);
        std::cout << std::format("✓ Backed up: {} → {}\n", filename, backup_type);
    }

    /**
     * @brief 清理旧文件
     * @param days_threshold 天数阈值，清理超过此天数的文件
     * @param backup_type 备份类型（daily/weekly）
     */
    void cleanup_old_files(int days_threshold, const std::string& backup_type = "daily") {
        auto backup_path = backup_dir / backup_type;
        if (!fs::exists(backup_path)) {
            return;
        }

        auto now = fs::file_time_type::clock::now();
        int removed_count = 0;

        for (const auto& entry : fs::directory_iterator(backup_path)) {
            if (entry.is_regular_file()) {
                auto ftime = fs::last_write_time(entry);
                auto age_duration = now - ftime;

                // 将duration转换为天数
                auto age_days = std::chrono::duration_cast<std::chrono::hours>(age_duration).count() / 24;

                if (age_days > days_threshold) {
                    fs::remove(entry.path());
                    removed_count++;
                }
            }
        }

        if (removed_count > 0) {
            std::cout << std::format("✓ Cleaned up {} old backup files (>{} days)\n",
                                   removed_count, days_threshold);
        }
    }

    /**
     * @brief 获取指定分类目录的总大小
     * @param category 分类
     * @return 目录大小（字节）
     */
    std::uintmax_t get_directory_size(const std::string& category) const {
        std::uintmax_t size = 0;
        auto dir_path = data_dir / category;

        if (!fs::exists(dir_path)) {
            return 0;
        }

        for (const auto& entry : fs::recursive_directory_iterator(dir_path)) {
            if (entry.is_regular_file()) {
                size += fs::file_size(entry);
            }
        }

        return size;
    }

    /**
     * @brief 获取完整文件路径
     * @param category 分类
     * @param filename 文件名
     * @return 完整路径
     */
    fs::path get_file_path(const std::string& category, const std::string& filename) const {
        return data_dir / category / filename;
    }

    /**
     * @brief 获取日志文件路径
     * @param date 日期（YYYY-MM-DD格式）
     * @return 日志文件路径
     */
    fs::path get_log_path(const std::string& date) const {
        return log_dir / (date + ".log");
    }

    /**
     * @brief 打印目录统计信息
     */
    void print_statistics() const {
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "Data Manager Statistics\n";
        std::cout << std::string(60, '=') << "\n";

        auto print_category = [this](const std::string& category) {
            auto files = list_files(category);
            auto size = get_directory_size(category);
            std::cout << std::format("{:15} | {:>5} files | {:>10} bytes\n",
                                   category, files.size(), size);
        };

        print_category("strategies");
        print_category("portfolios");
        print_category("market_data");

        std::cout << std::string(60, '=') << "\n\n";
    }
};
