#pragma once

#include <fstream>
#include <sstream>
#include <filesystem>
#include <string>
#include <format>
#include <stdexcept>

namespace fs = std::filesystem;

/**
 * @brief 安全文件读取器 - 完善的流状态管理
 *
 * 提供健壮的文件IO错误处理
 */
class SafeFileReader {
public:
    /**
     * @brief 安全读取文件内容
     * @param path 文件路径
     * @return 文件内容
     * @throws std::runtime_error 如果读取失败
     */
    static std::string read_file(const fs::path& path) {
        // 检查文件是否存在
        if (!fs::exists(path)) {
            throw std::runtime_error(
                std::format("File does not exist: {}", path.string())
            );
        }

        // 检查是否是普通文件
        if (!fs::is_regular_file(path)) {
            throw std::runtime_error(
                std::format("Not a regular file: {}", path.string())
            );
        }

        std::ifstream ifs(path);

        // 检查打开状态
        if (!ifs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot open file: {}", path.string())
            );
        }

        // 启用异常（对于严重错误）
        ifs.exceptions(std::ifstream::badbit);

        try {
            std::ostringstream oss;
            oss << ifs.rdbuf();

            // 检查读取状态
            if (ifs.bad()) {
                throw std::runtime_error(
                    std::format("Bad bit set while reading: {}", path.string())
                );
            }

            return oss.str();

        } catch (const std::ios_base::failure& e) {
            throw std::runtime_error(
                std::format("IO error reading {}: {}", path.string(), e.what())
            );
        }
    }

    /**
     * @brief 按行读取文件
     */
    static std::vector<std::string> read_lines(const fs::path& path) {
        if (!fs::exists(path)) {
            throw std::runtime_error(
                std::format("File does not exist: {}", path.string())
            );
        }

        std::ifstream ifs(path);
        if (!ifs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot open file: {}", path.string())
            );
        }

        std::vector<std::string> lines;
        std::string line;

        while (std::getline(ifs, line)) {
            lines.push_back(line);
        }

        // 检查是否因为错误而结束（而非EOF）
        if (ifs.bad()) {
            throw std::runtime_error(
                std::format("Error reading file: {}", path.string())
            );
        }

        return lines;
    }

    /**
     * @brief 读取二进制文件
     */
    static std::vector<char> read_binary(const fs::path& path) {
        if (!fs::exists(path)) {
            throw std::runtime_error(
                std::format("File does not exist: {}", path.string())
            );
        }

        std::ifstream ifs(path, std::ios::binary | std::ios::ate);
        if (!ifs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot open file: {}", path.string())
            );
        }

        // 获取文件大小
        auto size = ifs.tellg();
        ifs.seekg(0, std::ios::beg);

        // 读取整个文件
        std::vector<char> buffer(size);
        ifs.read(buffer.data(), size);

        if (!ifs) {
            throw std::runtime_error(
                std::format("Error reading binary file: {}", path.string())
            );
        }

        return buffer;
    }
};

/**
 * @brief 安全文件写入器
 */
class SafeFileWriter {
public:
    /**
     * @brief 安全写入文件内容
     * @param path 文件路径
     * @param content 要写入的内容
     * @throws std::runtime_error 如果写入失败
     */
    static void write_file(const fs::path& path, const std::string& content) {
        // 确保父目录存在
        if (path.has_parent_path()) {
            fs::create_directories(path.parent_path());
        }

        std::ofstream ofs(path);

        if (!ofs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot create file: {}", path.string())
            );
        }

        // 启用异常
        ofs.exceptions(std::ofstream::badbit | std::ofstream::failbit);

        try {
            ofs << content;
            ofs.flush();

            // 最终检查
            if (!ofs.good()) {
                throw std::runtime_error("Stream not in good state after write");
            }

        } catch (const std::ios_base::failure& e) {
            throw std::runtime_error(
                std::format("IO error writing {}: {}", path.string(), e.what())
            );
        }
    }

    /**
     * @brief 写入多行文本
     */
    static void write_lines(const fs::path& path, const std::vector<std::string>& lines) {
        if (path.has_parent_path()) {
            fs::create_directories(path.parent_path());
        }

        std::ofstream ofs(path);
        if (!ofs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot create file: {}", path.string())
            );
        }

        for (const auto& line : lines) {
            ofs << line << '\n';
            if (!ofs) {
                throw std::runtime_error(
                    std::format("Error writing to file: {}", path.string())
                );
            }
        }

        ofs.flush();
    }

    /**
     * @brief 追加内容到文件
     */
    static void append_file(const fs::path& path, const std::string& content) {
        std::ofstream ofs(path, std::ios::app);

        if (!ofs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot open file for appending: {}", path.string())
            );
        }

        ofs << content;
        if (!ofs) {
            throw std::runtime_error(
                std::format("Error appending to file: {}", path.string())
            );
        }

        ofs.flush();
    }

    /**
     * @brief 写入二进制数据
     */
    static void write_binary(const fs::path& path, const std::vector<char>& data) {
        if (path.has_parent_path()) {
            fs::create_directories(path.parent_path());
        }

        std::ofstream ofs(path, std::ios::binary);
        if (!ofs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot create binary file: {}", path.string())
            );
        }

        ofs.write(data.data(), data.size());
        if (!ofs) {
            throw std::runtime_error(
                std::format("Error writing binary file: {}", path.string())
            );
        }

        ofs.flush();
    }
};

/**
 * @brief 流状态检查器 - 诊断工具
 */
class StreamStateChecker {
public:
    /**
     * @brief 打印流状态信息
     */
    static void print_state(const std::ios& stream, const std::string& stream_name = "Stream") {
        std::cout << "\n" << stream_name << " State:\n";
        std::cout << "  good():  " << (stream.good() ? "true" : "false") << "\n";
        std::cout << "  eof():   " << (stream.eof() ? "true" : "false") << "\n";
        std::cout << "  fail():  " << (stream.fail() ? "true" : "false") << "\n";
        std::cout << "  bad():   " << (stream.bad() ? "true" : "false") << "\n";
        std::cout << "  bool():  " << (stream ? "true" : "false") << "\n";
    }

    /**
     * @brief 获取状态描述
     */
    static std::string get_state_description(const std::ios& stream) {
        if (stream.good()) {
            return "Stream is in good state";
        }

        std::string desc;
        if (stream.eof()) {
            desc += "EOF reached; ";
        }
        if (stream.fail()) {
            desc += "Logical error (failbit set); ";
        }
        if (stream.bad()) {
            desc += "Read/write error (badbit set); ";
        }

        return desc.empty() ? "Unknown state" : desc;
    }
};

/**
 * @brief 文件IO工具类 - 集成所有安全IO操作
 */
class FileIOUtils {
public:
    /**
     * @brief 安全拷贝文件
     */
    static void safe_copy(const fs::path& src, const fs::path& dest) {
        if (!fs::exists(src)) {
            throw std::runtime_error(
                std::format("Source file does not exist: {}", src.string())
            );
        }

        try {
            // 读取源文件
            auto content = SafeFileReader::read_binary(src);

            // 写入目标文件
            SafeFileWriter::write_binary(dest, content);

            std::cout << std::format("✓ File copied: {} → {}\n",
                                   src.string(), dest.string());

        } catch (const std::exception& e) {
            throw std::runtime_error(
                std::format("Failed to copy {} to {}: {}",
                          src.string(), dest.string(), e.what())
            );
        }
    }

    /**
     * @brief 检查文件完整性（简单校验）
     */
    static bool verify_file_integrity(const fs::path& path) {
        try {
            // 尝试读取文件
            auto content = SafeFileReader::read_file(path);

            // 检查文件大小是否匹配
            auto actual_size = content.size();
            auto expected_size = fs::file_size(path);

            return actual_size == expected_size;

        } catch (const std::exception&) {
            return false;
        }
    }
};
