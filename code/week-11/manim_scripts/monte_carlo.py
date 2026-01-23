"""
蒙特卡洛模拟动画
展示使用Cholesky分解生成相关资产收益率
"""
from manim import *
import numpy as np

class MonteCarloSimulation(Scene):
    def construct(self):
        # 标题
        title = Text("蒙特卡洛模拟：从独立到相关", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 左右两个坐标系
        axes_left = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": False},
        ).shift(LEFT * 3.5)

        axes_right = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": False},
        ).shift(RIGHT * 3.5)

        label_left = Text("独立随机数 z", font_size=20).next_to(axes_left, DOWN)
        label_right = Text("相关随机数 Lz", font_size=20).next_to(axes_right, DOWN)

        self.play(
            Create(axes_left), Create(axes_right),
            Write(label_left), Write(label_right)
        )

        # Cholesky分解公式
        formula = MathTex(
            r"z \sim N(0, I)",
            r"\quad \rightarrow \quad",
            r"Lz \sim N(0, \Sigma)",
            font_size=28
        ).shift(DOWN * 3)
        self.play(Write(formula))

        # 相关矩阵和Cholesky分解
        correlation = 0.7
        Sigma = np.array([[1, correlation], [correlation, 1]])
        L = np.linalg.cholesky(Sigma)

        # 生成并动画显示点
        np.random.seed(42)
        n_points = 100

        dots_left = VGroup()
        dots_right = VGroup()

        for i in range(n_points):
            # 独立随机点
            z = np.random.randn(2) * 0.8

            # 通过Cholesky变换
            lz = L @ z

            # 创建点
            dot_left = Dot(
                axes_left.c2p(*z),
                color=BLUE,
                radius=0.05,
                fill_opacity=0.7
            )
            dot_right = Dot(
                axes_right.c2p(*lz),
                color=RED,
                radius=0.05,
                fill_opacity=0.7
            )

            dots_left.add(dot_left)
            dots_right.add(dot_right)

        # 分批显示点
        batch_size = 10
        for i in range(0, n_points, batch_size):
            batch_left = dots_left[i:i+batch_size]
            batch_right = dots_right[i:i+batch_size]
            self.play(
                *[FadeIn(d, scale=0.5) for d in batch_left],
                *[FadeIn(d, scale=0.5) for d in batch_right],
                run_time=0.3
            )

        # 显示相关系数
        corr_left = Text(f"相关系数: 0.00", font_size=18, color=BLUE)
        corr_left.next_to(axes_left, UP)
        corr_right = Text(f"相关系数: {correlation:.2f}", font_size=18, color=RED)
        corr_right.next_to(axes_right, UP)

        self.play(Write(corr_left), Write(corr_right))

        # 画椭圆拟合（右侧）
        eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
        angle = np.degrees(np.arctan2(eigenvectors[1, 1], eigenvectors[0, 1]))

        ellipse = Ellipse(
            width=4 * np.sqrt(eigenvalues[1]) * 4/6,
            height=4 * np.sqrt(eigenvalues[0]) * 4/6,
            color=YELLOW,
            stroke_width=3
        ).rotate(angle * DEGREES).move_to(axes_right.c2p(0, 0))

        self.play(Create(ellipse))

        self.wait(2)


class MonteCarloSimple(Scene):
    """简化版，适合GIF"""
    def construct(self):
        # 两个坐标系
        axes_left = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
        ).shift(LEFT * 3)

        axes_right = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
        ).shift(RIGHT * 3)

        self.add(axes_left, axes_right)

        # 标签
        title_left = Text("独立", font_size=24).next_to(axes_left, UP)
        title_right = Text("相关", font_size=24).next_to(axes_right, UP)
        self.add(title_left, title_right)

        # 箭头
        arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=WHITE)
        arrow_label = MathTex("L", font_size=24).next_to(arrow, UP)
        self.add(arrow, arrow_label)

        # Cholesky
        correlation = 0.7
        Sigma = np.array([[1, correlation], [correlation, 1]])
        L = np.linalg.cholesky(Sigma)

        np.random.seed(42)

        # 逐点动画
        for i in range(50):
            z = np.random.randn(2) * 0.8
            lz = L @ z

            dot_left = Dot(axes_left.c2p(*z), color=BLUE, radius=0.06)
            dot_right = Dot(axes_right.c2p(*lz), color=RED, radius=0.06)

            self.play(
                FadeIn(dot_left, scale=0.5),
                FadeIn(dot_right, scale=0.5),
                run_time=0.1
            )

        self.wait(1)
