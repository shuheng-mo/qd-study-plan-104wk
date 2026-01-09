# Manim 环境安装与编译指南

面向线性代数可视化项目的完整 Manim 开发环境指南，涵盖依赖安装、常见问题修复及最佳实践。

## 系统要求

- Python 3.8 或更高版本
- ffmpeg（视频处理）
- LaTeX（数学公式渲染）
- 操作系统：macOS、Linux、Windows 均支持

## 第一步：安装 Python 依赖

### 使用 venv（推荐）

为避免全局环境污染，使用虚拟环境：

```bash
cd /path/to/qd-study-plan-104wk/code/week-09

python3 -m venv manim_env

source manim_env/bin/activate
```

（Windows 用户：`manim_env\Scripts\activate`）

### 安装 Manim

激活虚拟环境后，使用 pip 安装 Manim Community 版本：

```bash
pip install --upgrade pip

pip install manim
```

安装完成后验证：

```bash
manim --version
```

应输出类似 `Manim Community v0.19.1` 的版本号。

## 第二步：安装系统依赖

### macOS

使用 Homebrew 安装必要工具：

```bash
brew install cairo pango ffmpeg
```

如果需要 LaTeX 支持（用于数学公式），安装 TeX Live：

```bash
brew install texlive
```

或直接从 <https://tug.org/mactex/> 下载 MacTeX。

### Linux（Ubuntu/Debian）

```bash
sudo apt update

sudo apt install -y libcairo2-dev libpango1.0-dev ffmpeg

sudo apt install -y texlive-base texlive-latex-extra
```

### Windows

使用 Chocolatey（推荐）或手动安装：

```bash
choco install cairo pango ffmpeg

choco install miktex
```

或从以下官网下载安装器：

- FFmpeg: <https://ffmpeg.org/download.html>
- MiKTeX: <https://miktex.org/>

## 第三步：脚本运行

### 激活虚拟环境

每次使用前激活虚拟环境：

```bash
source manim_env/bin/activate
```

### 渲染单个场景

使用 manim 命令渲染脚本中的特定场景：

```bash
manim -ql vectors.py VectorIntro

manim -ql matrix_transform.py RotationTransform

manim -ql linear_systems.py LinearSystemGeometry

manim -ql determinant_rank.py DeterminantAsArea
```

### 质量参数说明

| 参数 | 分辨率 | 帧率 | 用途 | 渲染时间 |
|------|--------|------|------|----------|
| -ql | 480p | 15fps | 快速预览 | 最快 |
| -qm | 720p | 30fps | 标准预览 | 中等 |
| -qh | 1080p | 60fps | 标准输出 | 较慢 |
| -qk | 2160p | 60fps | 4K输出 | 最慢 |

### 常用参数组合

```bash
manim -pql vectors.py VectorIntro
```

参数说明：

- `-p`: 渲染完成后自动播放视频
- `-ql`: 低质量快速预览
- `-a`: 渲染文件中所有场景

### 渲染所有场景

```bash
manim -pql vectors.py -a

manim -pql matrix_transform.py -a

manim -pql linear_systems.py -a

manim -pql determinant_rank.py -a
```

## 项目结构

```
code/week-09/
├── manim_scripts/          脚本目录
│   ├── vectors.py          向量几何直觉
│   ├── matrix_transform.py 矩阵变换
│   ├── linear_systems.py   线性方程组与逆矩阵
│   └── determinant_rank.py 行列式与秩
├── vids/                   渲染输出目录
│   ├── vectors/
│   ├── matrix_transform/
│   ├── linear_systems/
│   └── determinant_rank/
├── manim_files/            原始脚本与测试
├── manim_env/              Python 虚拟环境
└── MANIM_GUIDE.md         本指南文件
```

## 已知问题与修复

### 问题 1：已废弃的 fix_in_frame() 方法

Manim v0.19 及更高版本中，`fix_in_frame()` 已被删除。

修复：直接使用 `add_fixed_in_frame_mobjects()` 替代。

```python
self.add_fixed_in_frame_mobjects(title)
```

### 问题 2：LinearTransformationScene 中的前景对象不兼容

在 LinearTransformationScene 中使用 `add_background_rectangle()` 后的 MathTex 对象作为前景会导致向量形状不匹配错误。

修复方案：

1. 移除 `add_background_rectangle()` 调用
2. 用 `Text` 代替 `MathTex` 显示说明（特别是包含中文时）
3. 避免在变换过程中添加复杂的前景对象

```python
title = Text("缩放变换", font_size=42)
self.add_foreground_mobject(title)

square = Square(side_length=1, color=YELLOW, fill_opacity=0.3)
self.add_transformable_mobject(square)

self.apply_matrix([[2, 0], [0, 0.5]])
```

### 问题 3：中文在 LaTeX 中无法编译

MathTex 不直接支持中文字符，会导致 LaTeX 编译错误。

修复：使用 Text 对象处理中文说明：

```python
label_cn = Text("系数矩阵", font_size=28)

label_math = MathTex(r"A:", font_size=28)

labels = VGroup(label_math, label_cn).arrange(RIGHT, buff=0.2)
```

### 问题 4：3D 场景无法正确渲染固定元素

使用 `fix_in_frame()` 的 3D 场景会崩溃。

修复：使用正确的 API：

```bash
manim -pql script.py ThreeDScene --renderer=opengl
```

## 脚本结构与最佳实践

### 避免的做法

不要在 LinearTransformationScene 的前景中使用复杂对象：

```python
MathTex(...).add_background_rectangle()
```

不要依赖过时的方法如 `fix_in_frame()`。

### 推荐做法

将说明添加为前景对象，但保持简洁：

```python
title = Text("变换名称", font_size=42)
self.add_foreground_mobject(title)

self.add_transformable_mobject(square)
self.apply_matrix(matrix)
```

将 LaTeX 公式添加在变换之前，变换后移除：

```python
self.play(Write(formula))
self.wait()

self.play(FadeOut(formula))
self.apply_matrix(matrix)
```

## 脚本文件说明

### vectors.py

包含 9 个场景，覆盖向量、点积、叉积及范数概念。

示例运行：

```bash
manim -pql vectors.py VectorIntro

manim -pql vectors.py DotProductIntro

manim -pql vectors.py CrossProduct2DArea
```

### matrix_transform.py

包含 11 个场景，展示各类矩阵变换的几何意义。

示例运行：

```bash
manim -pql matrix_transform.py ScalingTransform

manim -pql matrix_transform.py RotationTransform

manim -pql matrix_transform.py ProjectionTransform
```

### linear_systems.py

包含 12 个场景，讲解线性方程组、逆矩阵及伪逆。

示例运行：

```bash
manim -pql linear_systems.py LinearSystemGeometry

manim -pql linear_systems.py SingularMatrixDemo

manim -pql linear_systems.py LinearSystemMatrix
```

### determinant_rank.py

包含 11 个场景，深入讲解行列式、秩及其应用。

示例运行：

```bash
manim -pql determinant_rank.py DeterminantAsArea

manim -pql determinant_rank.py RankVisualization

manim -pql determinant_rank.py DeterminantZero
```

## 输出文件位置

所有渲染的视频默认保存在：

```
code/week-09/manim_files/media/videos/[脚本名]/[质量]/[场景名].mp4
```

对应关系示例：

```
manim -ql vectors.py VectorIntro
-> code/week-09/manim_files/media/videos/vectors/480p15/VectorIntro.mp4
```

## 性能优化建议

### 使用低质量预览快速迭代

开发阶段用 `-ql` 快速测试：

```bash
manim -pql matrix_transform.py RotationTransform
```

### 渲染时关闭不必要的功能

减少背景线条密度，简化对象数量。

### 并行渲染多个场景

在后台运行多个渲染任务（需多核 CPU）。

## 故障排查

### 错误：latex error converting to dvi

原因：LaTeX 中文编译失败或缺少 TeX Live。

解决：

1. 安装完整的 TeX Live
2. 用 Text 代替包含中文的 MathTex

### 错误：operands could not be broadcast

原因：LinearTransformationScene 中前景对象结构不兼容。

解决：移除 `add_background_rectangle()`，用 Text 替代 MathTex。

### 错误：ffmpeg not found

原因：未安装 ffmpeg 或未加入 PATH。

解决：

- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`
- Windows: 从 <https://ffmpeg.org/download.html> 下载并加入 PATH

### 脚本运行缓慢

原因：质量参数过高或场景过于复杂。

解决：

1. 使用 `-ql` 预览
2. 简化场景中的对象数量
3. 减少动画帧数（修改 run_time 参数）

## 扩展资源

- Manim 官方文档: <https://docs.manim.community/>
- Manim 示例库: <https://docs.manim.community/en/stable/examples.html>
- 3Blue1Brown 频道: <https://www.youtube.com/c/3blue1brown>

## 常见命令速查表

```bash
source manim_env/bin/activate

manim -pql vectors.py VectorIntro

manim -pql vectors.py -a

manim -pqh matrix_transform.py RotationTransform

manim -ql linear_systems.py LinearSystemGeometry -s

manim -pql determinant_rank.py DeterminantAsArea
```

## 注意事项

1. 始终在虚拟环境中运行脚本
2. 第一次渲染会花时间生成 LaTeX 缓存，后续渲染会更快
3. 修改场景后需要重新渲染，无增量编译
4. 避免使用相对路径指定输入输出，使用绝对路径更稳定
