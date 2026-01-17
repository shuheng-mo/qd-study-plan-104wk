"""
Week 10 - Part 2: 矩阵分解三剑客
- SVD（奇异值分解）：A = UΣVᵀ
- PCA（主成分分析）：降维与因子提取
- LU/QR分解：数值计算效率

运行方式：
manim -pql matrix_decomposition.py Scene名称
例如：manim -pql matrix_decomposition.py SVDImageCompression
"""

from manim import *
import numpy as np


# ============================================================
# Scene 1: SVD 奇异值分解
# ============================================================
class SVDImageCompression(Scene):
    """SVD图像压缩示意"""

    def construct(self):
        title = Text("SVD应用：图像压缩", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 原始矩阵示意
        original = VGroup(
            Rectangle(width=3, height=3, color=BLUE, fill_opacity=0.3),
            Text("原始图像\nm×n像素", font_size=22)
        )
        original[1].move_to(original[0])
        original.shift(LEFT * 4 + DOWN * 0.3)

        # SVD分解
        U_rect = Rectangle(width=1.5, height=3, color=RED, fill_opacity=0.3)
        U_label = MathTex("U", font_size=28).move_to(U_rect)
        U_size = Text("m×k", font_size=18).next_to(U_rect, DOWN)

        S_rect = Rectangle(width=1.5, height=1.5, color=GREEN, fill_opacity=0.3)
        S_label = MathTex(r"\Sigma", font_size=28).move_to(S_rect)
        S_size = Text("k×k", font_size=18).next_to(S_rect, DOWN)

        V_rect = Rectangle(width=3, height=1.5, color=ORANGE, fill_opacity=0.3)
        V_label = MathTex("V^T", font_size=28).move_to(V_rect)
        V_size = Text("k×n", font_size=18).next_to(V_rect, DOWN)

        decomposed = VGroup(
            VGroup(U_rect, U_label, U_size),
            VGroup(S_rect, S_label, S_size),
            VGroup(V_rect, V_label, V_size)
        ).arrange(RIGHT, buff=0.3)
        decomposed.shift(RIGHT * 2 + DOWN * 0.3)

        # 动画
        self.play(Create(original))
        self.wait()

        arrow = Arrow(original.get_right(), decomposed.get_left() + LEFT * 0.5, color=YELLOW)
        self.play(GrowArrow(arrow))
        self.play(Create(decomposed))
        self.wait()

        # 压缩原理 - 移至右下角
        compress_formula = VGroup(
            Text("压缩比", font_size=18),
            MathTex(r"\approx \frac{k(m+n+1)}{mn}", font_size=20)
        ).arrange(RIGHT, buff=0.1)
        explanation = VGroup(
            Text("只保留前k个奇异值", font_size=20, color=YELLOW),
            Text("k越小 压缩率越高", font_size=18),
            compress_formula,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.to_corner(DR).shift(UP * 0.5 + LEFT * 0.5)

        self.play(Write(explanation))
        self.wait(2)


class SVDLowRankApprox(Scene):
    """SVD低秩近似"""

    def construct(self):
        title = Text("SVD低秩近似", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 公式
        formula = MathTex(
            r"A \approx \sum_{i=1}^{k} \sigma_i \vec{u}_i \vec{v}_i^T",
            font_size=36
        ).shift(UP * 1.8)

        self.play(Write(formula))
        self.wait()

        # 奇异值重要性示意（条形图）
        bars = VGroup()
        values = [10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05]
        max_height = 2.5
        bar_width = 0.4

        for i, val in enumerate(values):
            height = val / 10 * max_height
            bar = Rectangle(
                width=bar_width,
                height=height,
                fill_color=BLUE if i < 3 else GRAY,
                fill_opacity=0.8,
                stroke_color=WHITE
            )
            bar.move_to(LEFT * 2 + RIGHT * i * 0.6 + DOWN * 0.8)
            bar.align_to(DOWN * 2.3, DOWN)

            label = MathTex(rf"\sigma_{i+1}", font_size=18)
            label.next_to(bar, DOWN, buff=0.1)
            bars.add(VGroup(bar, label))

        self.play(Create(bars))
        self.wait()

        # 说明
        keep_box = SurroundingRectangle(
            VGroup(*[bars[i][0] for i in range(3)]),
            color=YELLOW,
            buff=0.1
        )
        keep_label = Text("保留", font_size=22, color=YELLOW)
        keep_label.next_to(keep_box, UP)

        discard_label = Text("丢弃（噪声）", font_size=22, color=GRAY)
        discard_label.next_to(VGroup(*[bars[i][0] for i in range(3, 8)]), UP)

        self.play(Create(keep_box), Write(keep_label), Write(discard_label))
        self.wait()

        # 结论
        conclusion = Text(
            "前几个奇异值包含了大部分信息！",
            font_size=28,
            color=GREEN
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(conclusion))
        self.wait(2)


# ============================================================
# Scene 2: PCA 主成分分析
# ============================================================
class PCAIntro(Scene):
    """PCA的基本思想"""

    def construct(self):
        title = Text("PCA: 主成分分析", font_size=48)
        title.to_edge(UP).shift(DOWN * 0.1)
        subtitle = Text("找到数据中方差最大的方向", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))
        self.wait()

        # 数据点云
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={"stroke_opacity": 0.2}
        ).shift(DOWN * 0.6)

        self.play(Create(plane))

        # 生成倾斜的椭圆分布点
        np.random.seed(123)
        n_points = 50
        # 旋转角度
        theta = 30 * np.pi / 180
        # 生成数据
        x = np.random.randn(n_points) * 2
        y = np.random.randn(n_points) * 0.5
        # 旋转
        x_rot = x * np.cos(theta) - y * np.sin(theta)
        y_rot = x * np.sin(theta) + y * np.cos(theta)

        dots = VGroup()
        for xi, yi in zip(x_rot, y_rot):
            dot = Dot(plane.c2p(xi, yi), color=BLUE, radius=0.05)
            dots.add(dot)

        self.play(Create(dots))
        self.wait()

        # 主成分方向
        pc1_dir = np.array([np.cos(theta), np.sin(theta)]) * 3
        pc1 = Arrow(
            plane.c2p(-pc1_dir[0], -pc1_dir[1]),
            plane.c2p(pc1_dir[0], pc1_dir[1]),
            buff=0,
            color=RED,
            stroke_width=4
        )
        pc1_label = Text("PC1 (最大方差方向)", font_size=22, color=RED)
        pc1_label.next_to(pc1.get_end(), UR)

        pc2_dir = np.array([-np.sin(theta), np.cos(theta)]) * 1
        pc2 = Arrow(
            plane.c2p(-pc2_dir[0], -pc2_dir[1]),
            plane.c2p(pc2_dir[0], pc2_dir[1]),
            buff=0,
            color=GREEN,
            stroke_width=4
        )
        pc2_label = Text("PC2", font_size=22, color=GREEN)
        pc2_label.next_to(pc2.get_end(), UL)

        self.play(GrowArrow(pc1), Write(pc1_label))
        self.play(GrowArrow(pc2), Write(pc2_label))
        self.wait(2)


class PCADimensionReduction(Scene):
    """PCA降维示意"""

    def construct(self):
        title = Text("PCA降维：从高维到低维", font_size=38)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 左边：2D数据
        plane_2d = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            background_line_style={"stroke_opacity": 0.3}
        ).shift(LEFT * 3.5 + DOWN * 0.3)

        label_2d = Text("原始2D数据", font_size=22).next_to(plane_2d, DOWN)

        # 生成数据
        np.random.seed(456)
        n = 30
        x = np.random.randn(n) * 1.5
        y = 0.7 * x + np.random.randn(n) * 0.3

        dots_2d = VGroup()
        for xi, yi in zip(x, y):
            dot = Dot(plane_2d.c2p(xi, yi), color=BLUE, radius=0.05)
            dots_2d.add(dot)

        self.play(Create(plane_2d), Write(label_2d), Create(dots_2d))
        self.wait()

        # 主成分方向
        pc_dir = np.array([1, 0.7])
        pc_dir = pc_dir / np.linalg.norm(pc_dir) * 2.5
        pc_line = Line(
            plane_2d.c2p(-pc_dir[0], -pc_dir[1]),
            plane_2d.c2p(pc_dir[0], pc_dir[1]),
            color=RED,
            stroke_width=3
        )

        self.play(Create(pc_line))
        self.wait()

        # 箭头
        arrow = Arrow(LEFT * 1, RIGHT * 1, color=YELLOW)
        arrow_label = Text("投影到PC1", font_size=20, color=YELLOW)
        arrow_label.next_to(arrow, UP)

        self.play(GrowArrow(arrow), Write(arrow_label))

        # 右边：1D数据（数轴）
        line_1d = NumberLine(
            x_range=[-3, 3, 1],
            length=5,
            include_numbers=True
        ).shift(RIGHT * 3.5 + DOWN * 0.3)

        label_1d = Text("降维后1D数据", font_size=22).next_to(line_1d, DOWN, buff=0.5)

        # 投影点
        proj_dots = VGroup()
        for xi, yi in zip(x, y):
            proj_val = (xi + 0.7 * yi) / np.sqrt(1 + 0.7 ** 2)
            proj_val = np.clip(proj_val, -2.8, 2.8)
            dot = Dot(line_1d.n2p(proj_val), color=GREEN, radius=0.08)
            proj_dots.add(dot)

        self.play(Create(line_1d), Write(label_1d))
        self.play(Create(proj_dots))
        self.wait()

        # 说明
        note = Text("保留了最重要的信息（最大方差方向）", font_size=24, color=GREEN)
        note.to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(note))
        self.wait(2)


class PCAFactorModel(Scene):
    """PCA在金融中的应用：因子模型"""

    def construct(self):
        title = Text("PCA提取风险因子", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.1)
        subtitle = Text("100只股票 → 5个因子", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 左边：高维数据
        left_rect = Rectangle(width=2, height=3, color=BLUE, fill_opacity=0.3)
        left_label = Text("100只股票\n收益率", font_size=20)
        left_label.move_to(left_rect)
        left_group = VGroup(left_rect, left_label).shift(LEFT * 4 + DOWN * 0.3)

        # 箭头
        arrow = Arrow(LEFT * 2, RIGHT * 0.5, color=YELLOW)
        arrow_label = Text("PCA", font_size=24, color=YELLOW)
        arrow_label.next_to(arrow, UP)

        # 右边：低维因子
        right_rect = Rectangle(width=1, height=3, color=GREEN, fill_opacity=0.3)
        right_label = Text("5个\n因子", font_size=20)
        right_label.move_to(right_rect)
        right_group = VGroup(right_rect, right_label).shift(RIGHT * 2 + DOWN * 0.3)

        self.play(Create(left_group))
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.play(Create(right_group))
        self.wait()

        # 因子解释
        factors = VGroup(
            Text("因子1: 市场因子 (45%)", font_size=22),
            Text("因子2: 行业因子 (20%)", font_size=22),
            Text("因子3: 规模因子 (10%)", font_size=22),
            Text("因子4: 动量因子 (8%)", font_size=22),
            Text("因子5: 波动因子 (5%)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        factors.shift(RIGHT * 4 + DOWN * 0.3)

        for i, factor in enumerate(factors):
            color = [RED, ORANGE, YELLOW, GREEN, BLUE][i]
            factor.set_color(color)

        self.play(Write(factors))
        self.wait()

        # 结论
        conclusion = Text(
            "5个因子解释了88%的方差！",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(conclusion))
        self.wait(2)


# ============================================================
# Scene 3: LU/QR分解
# ============================================================
class LUDecomposition(Scene):
    """LU分解介绍"""

    def construct(self):
        title = Text("LU分解：快速解方程组", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 公式
        formula = MathTex(r"A = LU", font_size=48)
        formula.shift(UP * 1.8)
        self.play(Write(formula))

        # L和U的形状
        L_matrix = MathTex(
            r"L = \begin{bmatrix} 1 & 0 & 0 \\ * & 1 & 0 \\ * & * & 1 \end{bmatrix}",
            font_size=32
        ).shift(LEFT * 3 + DOWN * 0.3)
        L_label = Text("下三角矩阵", font_size=22, color=RED)
        L_label.next_to(L_matrix, DOWN)

        U_matrix = MathTex(
            r"U = \begin{bmatrix} * & * & * \\ 0 & * & * \\ 0 & 0 & * \end{bmatrix}",
            font_size=32
        ).shift(RIGHT * 3 + DOWN * 0.3)
        U_label = Text("上三角矩阵", font_size=22, color=BLUE)
        U_label.next_to(U_matrix, DOWN)

        self.play(Write(L_matrix), Write(L_label))
        self.play(Write(U_matrix), Write(U_label))
        self.wait()

        # 优势
        advantage = VGroup(
            Text("解 Ax = b 的步骤:", font_size=26, color=YELLOW),
            Text("1. Ly = b (前代，O(n²))", font_size=24),
            Text("2. Ux = y (回代，O(n²))", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        advantage.to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(advantage))
        
        # 对比文本单独显示在右下角
        comparison = Text("对比直接求逆: O(n³)", font_size=22, color=GRAY)
        comparison.to_corner(DR).shift(UP * 0.3 + LEFT * 0.3)
        self.play(Write(comparison))
        self.wait(2)


class QRDecomposition(Scene):
    """QR分解介绍"""

    def construct(self):
        title = Text("QR分解：数值稳定的选择", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 公式
        formula = MathTex(r"A = QR", font_size=48)
        formula.shift(UP * 1.8)
        self.play(Write(formula))

        # Q和R的特点
        Q_box = VGroup(
            Text("Q: 正交矩阵", font_size=28, color=GREEN),
            MathTex(r"Q^T Q = I", font_size=28),
            Text("• 列向量相互垂直", font_size=22),
            Text("• 列向量长度为1", font_size=22),
            Text("• 条件数 = 1", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.2)
        Q_box.shift(LEFT * 3 + DOWN * 0.3)

        R_box = VGroup(
            Text("R: 上三角矩阵", font_size=28, color=BLUE),
            MathTex(
                r"R = \begin{bmatrix} * & * & * \\ 0 & * & * \\ 0 & 0 & * \end{bmatrix}",
                font_size=24
            ),
        ).arrange(DOWN, buff=0.3)
        R_box.shift(RIGHT * 3 + DOWN * 0.3)

        self.play(Write(Q_box))
        self.play(Write(R_box))
        self.wait()

        # 应用
        applications = VGroup(
            Text("主要应用:", font_size=26, color=YELLOW),
            Text("• 最小二乘法", font_size=24),
            Text("• 特征值计算", font_size=24),
            Text("• 正交化（Gram-Schmidt）", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        applications.to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(applications))
        self.wait(2)


class DecompositionComparison(Scene):
    """三种分解的比较"""

    def construct(self):
        title = Text("矩阵分解对比", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 表格
        table_data = [
            ["", "SVD", "PCA", "LU", "QR"],
            ["公式", r"A=U\Sigma V^T", "协方差特征分解", "A=LU", "A=QR"],
            ["适用", "任意矩阵", "数据降维", "方阵", "任意矩阵"],
            ["特点", "万能分解", "找方差最大方向", "解方程快", "数值稳定"],
            ["用途", "压缩/推荐", "因子提取", "线性方程组", "最小二乘"],
        ]

        table = VGroup()
        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                if i == 0 or j == 0:
                    text = Text(cell, font_size=22, color=YELLOW if i == 0 else WHITE)
                else:
                    if "\\" in cell:
                        text = MathTex(cell, font_size=22)
                    else:
                        text = Text(cell, font_size=20)
                # j从0-4，减2使其居中，i从0-4，减2使其居中
                text.move_to(RIGHT * (j - 2) * 2.3 + UP * (2 - i) * 0.65)
                row_group.add(text)
            table.add(row_group)

        for row in table:
            self.play(Write(row), run_time=0.5)

        self.wait(2)


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    print("Week 10 - Part 2: 矩阵分解动画")
    print("运行示例: manim -pql matrix_decomposition.py SVDImageCompression")
    print("\n可用场景:")
    print("  - DecompositionComparison: 分解对比")
    print("  - LUDecomposition: LU分解")
    print("  - PCADimensionReduction: 降维示意")
    print("  - PCAFactorModel: 因子模型应用")
    print("  - PCAIntro: PCA基本思想")
    print("  - QRDecomposition: QR分解")
    print("  - SVDImageCompression: 图像压缩应用")
    print("  - SVDLowRankApprox: 低秩近似")
