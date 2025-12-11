# Makefile for QuantTeam_v2

CXX = g++
CXXFLAGS = -std=c++20 -Wall -Wextra -pedantic -O2
INCLUDES = -Iinclude

SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

TARGET = $(BIN_DIR)/QuantTeam_v2

SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

# 默认目标
all: directories $(TARGET)

# 创建目录
directories:
	@mkdir -p $(OBJ_DIR)
	@mkdir -p $(BIN_DIR)

# 链接
$(TARGET): $(OBJECTS)
	@echo "链接: $@"
	@$(CXX) $(CXXFLAGS) $^ -o $@
	@echo "✅ 构建成功: $@"

# 编译
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "编译: $<"
	@$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# 运行
run: all
	@echo "\n运行程序...\n"
	@./$(TARGET)

# 清理
clean:
	@echo "清理..."
	@rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "✅ 清理完成"

# 重新构建
rebuild: clean all

.PHONY: all directories run clean rebuild
