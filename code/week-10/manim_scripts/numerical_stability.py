"""
Week 10 - Part 4: 数值稳定性
- 为什么不要直接求逆
- 条件数的概念
- 病态矩阵的问题
- 稀疏矩阵

运行方式：
manim -pql numerical_stability.py Scene名称
例如：manim -pql numerical_stability.py ConditionNumberGeometry
"""

from manim import *
import numpy as np


# ============================================================
# Scene 1: 条件数的几何意义
# ============================================================
class ConditionNumberGeometry(Scene):
    """条件数的几何意义"""

    def construct(self):
        title = Text("条件数的几何意义", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 两个对比
        # 左边：良态矩阵（圆形）
        plane_left = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            background_line_style={"stroke_opacity": 0.2}
        ).shift(LEFT * 3 + DOWN * 0.8)

        circle = Circle(radius=1, color=GREEN, stroke_width=3)
        circle.move_to(plane_left.get_center())

        label_left = VGroup(
            Text("良态矩阵", font_size=22, color=GREEN),
            MathTex(r"\kappa \approx 1", font_size=24),
            Text("单位圆→圆", font_size=20),
        ).arrange(DOWN, buff=0.1)
        label_left.next_to(plane_left, DOWN)

        # 右边：病态矩阵（扁椭圆）
        plane_right = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            background_line_style={"stroke_opacity": 0.2}
        ).shift(RIGHT * 3 + DOWN * 0.8)

        ellipse = Ellipse(width=2.5, height=0.3, color=RED, stroke_width=3)
        ellipse.move_to(plane_right.get_center())

        label_right = VGroup(
            Text("病态矩阵", font_size=22, color=RED),
            MathTex(r"\kappa \gg 1", font_size=24),
            Text("单位圆→扁椭圆", font_size=20),
        ).arrange(DOWN, buff=0.1)
        label_right.next_to(plane_right, DOWN)

        self.play(Create(plane_left), Create(plane_right))
        self.play(Create(circle), Create(ellipse))
        self.play(Write(label_left), Write(label_right))
        self.wait()

        # 解释
        explanation = Text(
            "条件数 = 长轴/短轴，椭圆越扁 → 条件数越大 → 数值越不稳定",
            font_size=22,
            color=YELLOW
        ).shift(UP * 2.5)

        self.play(Write(explanation))
        self.wait(2)


# ============================================================
# Scene 2: 稀疏矩阵
# ============================================================
class SparseMatrixIntro(Scene):
    """稀疏矩阵介绍"""

    def construct(self):
        # Title at top
        title = Text("稀疏矩阵：大规模数据的必备", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # Left side: Dense matrix grid (6x6 smaller)
        np.random.seed(42)
        dense_grid = VGroup()
        non_zero_positions = []
        for i in range(6):
            for j in range(6):
                val = np.random.choice([0, 0, 0, 0, 0, 0, 0, 1])
                if val == 1:
                    non_zero_positions.append((i, j, 1))
                color = BLUE if val == 1 else GRAY
                opacity = 0.8 if val == 1 else 0.1
                cell = Square(side_length=0.4, fill_color=color, fill_opacity=opacity, stroke_width=0.5)
                cell.move_to(RIGHT * j * 0.45 + UP * 0.5 - DOWN * i * 0.45)
                dense_grid.add(cell)

        dense_grid.shift(LEFT * 3.5)
        dense_label = Text("稠密存储: 36个数字", font_size=20)
        dense_label.next_to(dense_grid, DOWN, buff=0.3)

        self.play(Create(dense_grid), Write(dense_label))
        self.wait()

        # Arrow in middle
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, color=YELLOW)
        self.play(GrowArrow(arrow))

        # Right side: Sparse text representation
        row_indices = [pos[0] for pos in non_zero_positions[:5]]
        col_indices = [pos[1] for pos in non_zero_positions[:5]]
        
        sparse_rep = VGroup(
            Text("稀疏存储:", font_size=22, color=GREEN),
            Text("只存5个非零元素", font_size=18),
            Text(f"行: {row_indices}", font_size=16),
            Text(f"列: {col_indices}", font_size=16),
            Text("值: [1,1,1,1,1]", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sparse_rep.shift(RIGHT * 2.5)

        self.play(Write(sparse_rep))
        self.wait()

        # Bottom: Savings text
        saving = Text(
            "存储节省: 36 → 15 (58%)",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(saving))
        self.wait(2)


class SVDTruncation(Scene):
    """SVD截断处理病态矩阵"""

    def construct(self):
        title = Text("SVD截断：另一种正则化", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 原始SVD
        svd = MathTex(
            r"A = U\Sigma V^T = \sum_{i=1}^{n} \sigma_i u_i v_i^T",
            font_size=32
        ).shift(UP * 1.8)
        self.play(Write(svd))
        self.wait()

        # 奇异值条形图
        bars = VGroup()
        values = [10, 5, 2, 1, 0.1, 0.01, 0.001]
        max_height = 2
        bar_width = 0.5

        for i, val in enumerate(values):
            height = np.log10(val + 1) / np.log10(11) * max_height + 0.2
            color = GREEN if val > 0.5 else RED
            bar = Rectangle(
                width=bar_width,
                height=height,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=WHITE
            )
            bar.move_to(LEFT * 2.5 + RIGHT * i * 0.7 + DOWN * 0.8)
            bar.align_to(DOWN * 1.8, DOWN)

            label = MathTex(rf"\sigma_{i+1}", font_size=16)
            label.next_to(bar, DOWN, buff=0.1)
            bars.add(VGroup(bar, label))

        self.play(Create(bars))
        self.wait()

        # 截断线
        cutoff = DashedLine(
            LEFT * 2.5 + RIGHT * 3.5 * 0.7 + UP * 0.3,
            LEFT * 2.5 + RIGHT * 3.5 * 0.7 + DOWN * 1.8,
            color=YELLOW
        )
        cutoff_label = Text("截断", font_size=20, color=YELLOW)
        cutoff_label.next_to(cutoff, RIGHT)

        self.play(Create(cutoff), Write(cutoff_label))

        # 说明
        explanation = VGroup(
            Text("保留大奇异值", font_size=22, color=GREEN),
            Text("丢弃小奇异值（噪声/不稳定）", font_size=22, color=RED),
        ).arrange(DOWN, buff=0.2)
        explanation.shift(RIGHT * 3 + DOWN * 0.5)

        self.play(Write(explanation))

        # 结果
        result = MathTex(
            r"A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T",
            font_size=32,
            color=YELLOW
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(result))
        self.wait(2)


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    print("Week 10 - Part 4: 数值稳定性动画")
    print("运行示例: manim -pql numerical_stability.py ConditionNumberGeometry")
    print("\n可用场景:")
    print("  - ConditionNumberGeometry: 条件数几何意义")
    print("  - SparseMatrixIntro: 稀疏矩阵介绍")
    print("  - SVDTruncation: SVD截断")
