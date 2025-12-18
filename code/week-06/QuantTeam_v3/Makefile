CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Iinclude
RELEASE_FLAGS = -O3 -DNDEBUG -march=native
DEBUG_FLAGS = -g -O0

SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin
TEST_DIR = tests

# 创建必要的目录
$(shell mkdir -p $(OBJ_DIR) $(BIN_DIR))

# 源文件
SOURCES = $(SRC_DIR)/main.cpp $(SRC_DIR)/Portfolio.cpp
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SOURCES))

# 测试文件
TEST_SOURCES = $(TEST_DIR)/test_all.cpp $(SRC_DIR)/Portfolio.cpp
TEST_OBJECTS = $(patsubst %.cpp,$(OBJ_DIR)/%.o,$(TEST_SOURCES))

# 可执行文件
TARGET = $(BIN_DIR)/QuantTeam_v3
TEST_TARGET = $(BIN_DIR)/tests

# 默认目标：Release 版本
.PHONY: all
all: release

# Release 版本
.PHONY: release
release: CXXFLAGS += $(RELEASE_FLAGS)
release: $(TARGET)
	@echo "✓ Release build completed!"

# Debug 版本
.PHONY: debug
debug: CXXFLAGS += $(DEBUG_FLAGS)
debug: $(TARGET)
	@echo "✓ Debug build completed!"

# 编译主程序
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@
	@echo "✓ Linked $@"

# 编译测试
.PHONY: test
test: CXXFLAGS += $(DEBUG_FLAGS)
test: $(TEST_TARGET)
	@echo "✓ Test build completed!"
	@echo "Running tests..."
	@./$(TEST_TARGET)

$(TEST_TARGET): $(TEST_OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# 编译规则
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@
	@echo "✓ Compiled $<"

$(OBJ_DIR)/src/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@
	@echo "✓ Compiled $<"

$(OBJ_DIR)/$(TEST_DIR)/%.o: $(TEST_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@
	@echo "✓ Compiled $<"

# 运行程序
.PHONY: run
run: release
	@echo "========================================\n"
	@echo "Running QuantTeam_v3...\n"
	@echo "========================================\n"
	@./$(TARGET)

# 清理
.PHONY: clean
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "✓ Cleaned build artifacts!"

# 帮助信息
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make           - Build release version (default)"
	@echo "  make release   - Build release version with optimizations"
	@echo "  make debug     - Build debug version"
	@echo "  make test      - Build and run tests"
	@echo "  make run       - Build and run the program"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make help      - Show this help message"

.PHONY: info
info:
	@echo "Compiler: $(CXX)"
	@echo "C++ Standard: C++17"
	@echo "Release Flags: $(RELEASE_FLAGS)"
	@echo "Debug Flags: $(DEBUG_FLAGS)"
	@echo "Source Files: $(SOURCES)"
