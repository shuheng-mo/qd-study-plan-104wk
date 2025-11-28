# QuantTeam C++ 项目

量化团队的C++抽象，展示面向对象编程的核心概念。

## 📁 项目结构

```
QuantTeam/
├── include/                 # 头文件目录
│   ├── Employee.hpp        # 员工基类声明
│   ├── CoreMembers.hpp     # 团队成员类声明
│   └── QuantTeam.hpp       # 团队管理类声明
├── src/                    # 源文件目录
│   ├── CoreMembers.cpp     # 团队成员类实现
│   ├── QuantTeam.cpp       # 团队管理类实现
│   └── main.cpp           # 主程序
├── CMakeLists.txt         # CMake 构建文件
├── Makefile              # Make 构建文件
└── README.md             # 项目说明
```

## 🚀 构建与运行

### 使用 CMake

```bash
# 创建构建目录
mkdir build && cd build

# 配置项目
cmake ..

# 构建项目
make

# 运行程序
./QuantTeam
```

### 使用 Makefile

```bash
# 构建发布版本
make release

# 构建调试版本
make debug

# 构建并运行
make run

# 清理构建文件
make clean

# 查看帮助
make help
```
