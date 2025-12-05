# Makefile for QuantTeam v2.0 project

# 编译器设置
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic
DEBUGFLAGS = -g -O0 -DDEBUG
RELEASEFLAGS = -O3 -DNDEBUG

# 目录设置
SRCDIR = src
INCDIR = include
OBJDIR = obj
BINDIR = bin

# 文件设置
TARGET = $(BINDIR)/QuantTeam_v2
SOURCES = $(wildcard $(SRCDIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)
HEADERS = $(wildcard $(INCDIR)/*.hpp)

# 包含路径
INCLUDES = -I$(INCDIR)

# 默认目标
.PHONY: all clean debug release run help test

all: release

# 发布版本
release: CXXFLAGS += $(RELEASEFLAGS)
release: $(TARGET)

# 调试版本
debug: CXXFLAGS += $(DEBUGFLAGS)
debug: $(TARGET)

# 创建可执行文件
$(TARGET): $(OBJECTS) | $(BINDIR)
	@echo "Linking $@"
	$(CXX) $(OBJECTS) -o $@
	@echo "Build complete: $@"

# 编译目标文件
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp $(HEADERS) | $(OBJDIR)
	@echo "Compiling $<"
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# 创建目录
$(OBJDIR):
	@mkdir -p $(OBJDIR)

$(BINDIR):
	@mkdir -p $(BINDIR)

# 运行程序
run: $(TARGET)
	@echo "Running $(TARGET)"
	@./$(TARGET)

# 测试编译
test: debug
	@echo "Running tests..."
	@./$(TARGET) || true

# 清理
clean:
	@echo "Cleaning up..."
	@rm -rf $(OBJDIR) $(BINDIR)
	@echo "Clean complete"

# 重新构建
rebuild: clean all

# 安装（复制到系统路径）
install: $(TARGET)
	@echo "Installing to /usr/local/bin"
	@cp $(TARGET) /usr/local/bin/
	@echo "Installation complete"

# 卸载
uninstall:
	@echo "Removing from /usr/local/bin"
	@rm -f /usr/local/bin/QuantTeam_v2
	@echo "Uninstallation complete"

# 显示帮助
help:
	@echo "Available targets:"
	@echo "  all       - Build release version (default)"
	@echo "  debug     - Build debug version"
	@echo "  release   - Build release version"
	@echo "  run       - Build and run the program"
	@echo "  test      - Build debug and run tests"
	@echo "  clean     - Remove built files"
	@echo "  rebuild   - Clean and build"
	@echo "  install   - Install to system"
	@echo "  uninstall - Remove from system"
	@echo "  help      - Show this help"

# 显示编译信息
info:
	@echo "Compiler: $(CXX)"
	@echo "Flags: $(CXXFLAGS)"
	@echo "Sources: $(SOURCES)"
	@echo "Objects: $(OBJECTS)"
	@echo "Target: $(TARGET)"