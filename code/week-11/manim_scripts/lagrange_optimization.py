"""
拉格朗日乘数法动画
展示约束优化的几何意义：等高线与约束曲线的切点
"""
from manim import *
import numpy as np


class LagrangeOptimization(Scene):
    """拉格朗日乘数法可视化"""
    def construct(self):
        # 标题
        title = Text("Lagrange Multipliers", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 坐标系
        axes = Axes(
            x_range=[-0.5, 3, 0.5],
            y_range=[-0.5, 3, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True},
        ).shift(LEFT * 2)

        x_label = MathTex("w_1", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("w_2", font_size=24).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 目标函数等高线: f(x,y) = x^2 + 2y^2 (椭圆)
        contours = VGroup()
        for level in [0.5, 1, 2, 3, 5, 8]:
            # x^2 + 2y^2 = level
            # 椭圆: (x/sqrt(level))^2 + (y/sqrt(level/2))^2 = 1
            a = np.sqrt(level)
            b = np.sqrt(level / 2)

            ellipse = Ellipse(
                width=2*a * 6/3.5,
                height=2*b * 6/3.5,
                color=BLUE,
                stroke_width=1.5,
                stroke_opacity=0.6
            ).move_to(axes.c2p(0, 0))
            contours.add(ellipse)

        self.play(Create(contours), run_time=1.5)

        # 公式
        formula = VGroup(
            MathTex(r"\min \; w_1^2 + 2w_2^2", font_size=24),
            MathTex(r"\text{s.t.} \; w_1 + w_2 = 1", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 0.5)

        self.play(Write(formula))

        # 约束条件: x + y = 1 (直线)
        constraint_line = Line(
            axes.c2p(-0.5, 1.5),
            axes.c2p(1.5, -0.5),
            color=RED,
            stroke_width=3
        )
        constraint_label = Text("Constraint: w1+w2=1", font_size=16, color=RED)
        constraint_label.next_to(constraint_line, UP).shift(RIGHT * 0.5)

        self.play(Create(constraint_line), Write(constraint_label))
        self.wait(0.5)

        # 动画：沿约束移动找最优点
        # 约束线参数化: (t, 1-t), t从0到1
        moving_dot = Dot(axes.c2p(0, 1), color=YELLOW, radius=0.12)
        self.play(Create(moving_dot))

        # 目标函数值显示
        def objective(t):
            return t**2 + 2*(1-t)**2

        obj_text = Text(f"f = {objective(0):.2f}", font_size=20, color=YELLOW)
        obj_text.to_corner(DL).shift(UP)
        self.play(Write(obj_text))

        # 沿约束线移动
        t_values = np.linspace(0, 1, 30)
        for t in t_values:
            new_pos = axes.c2p(t, 1-t)
            new_text = Text(f"f = {objective(t):.2f}", font_size=20, color=YELLOW)
            new_text.to_corner(DL).shift(UP)

            self.play(
                moving_dot.animate.move_to(new_pos),
                Transform(obj_text, new_text),
                run_time=0.1
            )

        # 回到最优点
        # 最优解: df/dt = 2t - 4(1-t) = 6t - 4 = 0 => t = 2/3
        optimal_t = 2/3
        optimal_pos = axes.c2p(optimal_t, 1-optimal_t)

        self.play(
            moving_dot.animate.move_to(optimal_pos).set_color(GREEN),
            run_time=0.5
        )

        # 标记最优点
        optimal_label = MathTex(
            r"w^* = (2/3, 1/3)",
            font_size=20,
            color=GREEN
        ).next_to(moving_dot, DOWN)

        self.play(Write(optimal_label))

        # 画梯度向量
        # 目标函数梯度: (2x, 4y) at (2/3, 1/3) = (4/3, 4/3)
        gradient = Arrow(
            optimal_pos,
            axes.c2p(optimal_t + 0.5, 1-optimal_t + 0.5),
            color=PURPLE,
            buff=0,
            stroke_width=3
        )
        gradient_label = MathTex(r"\nabla f", font_size=18, color=PURPLE)
        gradient_label.next_to(gradient, UP)

        # 约束梯度: (1, 1)
        constraint_grad = Arrow(
            optimal_pos,
            axes.c2p(optimal_t + 0.4, 1-optimal_t + 0.4),
            color=ORANGE,
            buff=0,
            stroke_width=3
        )
        constraint_grad_label = MathTex(r"\nabla g", font_size=18, color=ORANGE)
        constraint_grad_label.next_to(constraint_grad, RIGHT)

        self.play(Create(gradient), Write(gradient_label))
        self.play(Create(constraint_grad), Write(constraint_grad_label))

        # KKT条件说明
        kkt = MathTex(
            r"\nabla f = \lambda \nabla g",
            font_size=24,
            color=WHITE
        ).to_edge(DOWN)

        self.play(Write(kkt))

        self.wait(2)


class LagrangeSimple(Scene):
    """简化版拉格朗日乘数法动画"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[-0.3, 2, 0.5],
            y_range=[-0.3, 2, 0.5],
            x_length=6,
            y_length=6,
        ).shift(LEFT * 1.5)

        title = Text("Lagrange Multipliers", font_size=28).to_edge(UP)
        self.add(axes, title)

        # 等高线
        contours = VGroup()
        for level in [0.3, 0.6, 1, 1.5, 2.5]:
            a = np.sqrt(level)
            b = np.sqrt(level / 2)
            ellipse = Ellipse(
                width=2*a * 6/2.3,
                height=2*b * 6/2.3,
                color=BLUE,
                stroke_width=2,
                stroke_opacity=0.5
            ).move_to(axes.c2p(0, 0))
            contours.add(ellipse)

        self.add(contours)

        # 约束线
        constraint = Line(
            axes.c2p(-0.2, 1.2),
            axes.c2p(1.2, -0.2),
            color=RED,
            stroke_width=4
        )
        self.add(constraint)

        # 问题公式
        problem = MathTex(
            r"\min f(w)", r"\;\text{s.t.}\;", r"g(w)=0",
            font_size=24
        ).to_corner(UR)
        self.add(problem)

        # 沿约束线移动的点
        def objective(t):
            return t**2 + 2*(1-t)**2

        dot = Dot(axes.c2p(0, 1), color=YELLOW, radius=0.1)
        self.add(dot)

        # 轨迹
        path_points = []
        t_values = list(np.linspace(0, 1, 40)) + list(np.linspace(1, 2/3, 20))

        for t in t_values:
            t_clamped = max(0, min(1, t))
            new_pos = axes.c2p(t_clamped, 1-t_clamped)
            path_points.append(new_pos)

            self.play(
                dot.animate.move_to(new_pos),
                run_time=0.06
            )

        # 最优点高亮
        optimal_t = 2/3
        optimal_pos = axes.c2p(optimal_t, 1-optimal_t)

        star = Star(n=5, fill_opacity=1, color=GREEN).scale(0.15).move_to(optimal_pos)
        optimal_text = MathTex(r"w^*", font_size=20, color=GREEN).next_to(star, DOWN)

        self.play(
            dot.animate.set_color(GREEN).scale(1.3),
            FadeIn(star),
            Write(optimal_text)
        )

        # 梯度平行条件
        kkt = MathTex(r"\nabla f \parallel \nabla g", font_size=24).to_edge(DOWN)
        self.play(Write(kkt))

        self.wait(1)
