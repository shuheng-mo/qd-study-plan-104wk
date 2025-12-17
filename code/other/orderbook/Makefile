CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Iinclude
RELEASE_FLAGS = -O3 -DNDEBUG -march=native
DEBUG_FLAGS = -g -O0

SRC_DIR = src
BUILD_DIR = build
BIN_DIR = bin

# 创建必要的目录
$(shell mkdir -p $(BUILD_DIR) $(BIN_DIR))

# 默认目标：Release 版本
.PHONY: all
all: release

# Release 版本
.PHONY: release
release: CXXFLAGS += $(RELEASE_FLAGS)
release: $(BIN_DIR)/benchmark
	@echo "Release build completed!"

# Debug 版本
.PHONY: debug
debug: CXXFLAGS += $(DEBUG_FLAGS)
debug: $(BIN_DIR)/benchmark
	@echo "Debug build completed!"

# 编译 benchmark
$(BIN_DIR)/benchmark: $(SRC_DIR)/benchmark.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# 运行基准测试
.PHONY: run
run: release
	@echo "Running benchmark..."
	@./$(BIN_DIR)/benchmark

# 清理
.PHONY: clean
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	@echo "Cleaned build artifacts!"

# 帮助信息
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make           - Build release version (default)"
	@echo "  make release   - Build release version with optimizations"
	@echo "  make debug     - Build debug version"
	@echo "  make run       - Build and run benchmark"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make help      - Show this help message"
