"""
正则化回归几何动画
展示L1和L2约束的几何解释
"""
from manim import *
import numpy as np


class RegularizationGeometry(Scene):
    """完整版：正则化几何"""

    def construct(self):
        # 标题
        title = Text("正则化回归的几何解释", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 分成左右两部分
        # 左：Ridge (L2)
        # 右：LASSO (L1)

        # 创建坐标系
        axes_l2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).shift(LEFT * 3.5 + DOWN * 0.5)

        axes_l1 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
        ).shift(RIGHT * 3.5 + DOWN * 0.5)

        l2_label = Text("Ridge (L2)", font_size=24).next_to(axes_l2, UP)
        l1_label = Text("LASSO (L1)", font_size=24).next_to(axes_l1, UP)

        self.play(
            Create(axes_l2),
            Create(axes_l1),
            Write(l2_label),
            Write(l1_label)
        )

        # OLS解位置
        ols_x, ols_y = 1.5, 1.5

        # RSS等高线
        def create_contours(axes, center_x, center_y):
            contours = VGroup()
            for r in [0.3, 0.6, 0.9, 1.2, 1.5]:
                ellipse = Ellipse(
                    width=2*r,
                    height=2*r,
                    color=BLUE,
                    stroke_width=1,
                    stroke_opacity=0.6
                ).move_to(axes.c2p(center_x, center_y))
                contours.add(ellipse)
            return contours

        contours_l2 = create_contours(axes_l2, ols_x, ols_y)
        contours_l1 = create_contours(axes_l1, ols_x, ols_y)

        self.play(Create(contours_l2), Create(contours_l1))

        # OLS解点
        ols_dot_l2 = Dot(axes_l2.c2p(ols_x, ols_y), color=YELLOW, radius=0.1)
        ols_dot_l1 = Dot(axes_l1.c2p(ols_x, ols_y), color=YELLOW, radius=0.1)
        ols_text_l2 = Text("OLS", font_size=14).next_to(ols_dot_l2, UR, buff=0.1)
        ols_text_l1 = Text("OLS", font_size=14).next_to(ols_dot_l1, UR, buff=0.1)

        self.play(
            Create(ols_dot_l2),
            Create(ols_dot_l1),
            Write(ols_text_l2),
            Write(ols_text_l1)
        )

        # L2约束：圆
        l2_constraint = Circle(
            radius=1.0 * axes_l2.x_length / 4,
            color=GREEN,
            stroke_width=3
        ).move_to(axes_l2.c2p(0, 0))

        # L1约束：菱形
        diamond_points = [
            axes_l1.c2p(1, 0),
            axes_l1.c2p(0, 1),
            axes_l1.c2p(-1, 0),
            axes_l1.c2p(0, -1),
            axes_l1.c2p(1, 0)
        ]
        l1_constraint = Polygon(*diamond_points, color=GREEN, stroke_width=3)

        self.play(Create(l2_constraint), Create(l1_constraint))

        # 公式
        l2_formula = MathTex(r"||\beta||_2^2 \leq t", font_size=20, color=GREEN)
        l2_formula.next_to(axes_l2, DOWN)
        l1_formula = MathTex(r"||\beta||_1 \leq t", font_size=20, color=GREEN)
        l1_formula.next_to(axes_l1, DOWN)

        self.play(Write(l2_formula), Write(l1_formula))

        # 正则化解
        # L2解：圆与等高线的切点
        l2_solution = Dot(axes_l2.c2p(0.75, 0.75), color=RED, radius=0.1)
        l2_sol_text = Text("Ridge解", font_size=14, color=RED)
        l2_sol_text.next_to(l2_solution, DL, buff=0.1)

        # L1解：菱形角点
        l1_solution = Dot(axes_l1.c2p(1, 0), color=RED, radius=0.1)
        l1_sol_text = Text("LASSO解", font_size=14, color=RED)
        l1_sol_text.next_to(l1_solution, RIGHT, buff=0.1)

        self.play(
            Create(l2_solution),
            Create(l1_solution),
            Write(l2_sol_text),
            Write(l1_sol_text)
        )

        # 稀疏性说明
        sparse_text = Text("LASSO解落在角点 → β₂ = 0（稀疏）", font_size=18, color=YELLOW)
        sparse_text.to_edge(DOWN)
        self.play(Write(sparse_text))

        self.wait(2)


class RegularizationSimple(Scene):
    """简化版：用于GIF"""

    def construct(self):
        title = Text("L1 vs L2 正则化", font_size=28)
        title.to_edge(UP)
        self.add(title)

        # 简化版本
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
        ).shift(DOWN * 0.3)
        self.add(axes)

        # 等高线
        for r in [0.5, 1.0, 1.5]:
            ellipse = Ellipse(
                width=2*r,
                height=2*r,
                color=BLUE,
                stroke_width=1,
                stroke_opacity=0.5
            ).move_to(axes.c2p(1.2, 1.2))
            self.add(ellipse)

        # L2约束
        l2_circle = Circle(
            radius=1.0 * axes.x_length / 4,
            color=GREEN,
            stroke_width=2
        ).move_to(axes.c2p(0, 0))

        # L1约束
        diamond = Polygon(
            axes.c2p(1, 0),
            axes.c2p(0, 1),
            axes.c2p(-1, 0),
            axes.c2p(0, -1),
            color=RED,
            stroke_width=2
        )

        self.play(Create(l2_circle), run_time=1)
        l2_text = Text("L2 (圆)", font_size=16, color=GREEN)
        l2_text.move_to(axes.c2p(-1.5, 1.5))
        self.add(l2_text)

        self.play(Create(diamond), run_time=1)
        l1_text = Text("L1 (菱形)", font_size=16, color=RED)
        l1_text.move_to(axes.c2p(1.5, -1.5))
        self.add(l1_text)

        # 解的位置
        l2_sol = Dot(axes.c2p(0.6, 0.6), color=GREEN, radius=0.1)
        l1_sol = Dot(axes.c2p(1, 0), color=RED, radius=0.1)

        self.play(Create(l2_sol), Create(l1_sol))

        # 说明
        note = Text("L1在角点产生稀疏解", font_size=16)
        note.to_edge(DOWN)
        self.play(Write(note))

        self.wait(2)
