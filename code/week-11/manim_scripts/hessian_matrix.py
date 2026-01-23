"""
Hessian矩阵与曲率动画
展示Hessian矩阵的特征值如何决定函数的曲率
"""
from manim import *
import numpy as np


class HessianVisualization(Scene):
    """Hessian矩阵与曲率可视化"""
    def construct(self):
        # 标题
        title = Text("Hessian Matrix: Curvature at Critical Points", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))

        # 三个子场景：正定、负定、不定
        cases = [
            {"name": "Positive Definite", "H": np.array([[2, 0], [0, 3]]), "type": "minimum", "color": GREEN},
            {"name": "Negative Definite", "H": np.array([[-2, 0], [0, -3]]), "type": "maximum", "color": RED},
            {"name": "Indefinite", "H": np.array([[2, 0], [0, -3]]), "type": "saddle", "color": YELLOW},
        ]

        # 创建三个坐标系
        axes_group = VGroup()
        for i in range(3):
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=3,
                y_length=3,
                axis_config={"include_tip": False}
            )
            axes_group.add(ax)

        axes_group.arrange(RIGHT, buff=0.8).shift(DOWN * 0.5)

        self.play(Create(axes_group))

        # 为每个case添加等高线和标签
        for i, (ax, case) in enumerate(zip(axes_group, cases)):
            H = case["H"]
            eigenvalues = np.linalg.eigvalsh(H)

            # 等高线
            contours = VGroup()
            for level in [0.5, 1, 2, 3]:
                if case["type"] == "saddle":
                    # 双曲线 (2x^2 - 3y^2 = level)
                    # 需要分支绘制
                    for sign in [1, -1]:
                        points = []
                        for x in np.linspace(-1.8, 1.8, 50):
                            discriminant = (H[0,0]*x**2 - sign*level) / (-H[1,1])
                            if discriminant >= 0:
                                y = sign * np.sqrt(discriminant)
                                if abs(y) <= 2:
                                    points.append(ax.c2p(x, y))
                        if len(points) > 2:
                            curve = VMobject(color=YELLOW, stroke_width=1.5)
                            curve.set_points_smoothly(points)
                            contours.add(curve)
                else:
                    # 椭圆
                    a = np.sqrt(abs(level / H[0,0]))
                    b = np.sqrt(abs(level / H[1,1]))
                    if a < 2 and b < 2:
                        ellipse = Ellipse(
                            width=2*a * 3/4,
                            height=2*b * 3/4,
                            color=case["color"],
                            stroke_width=1.5,
                            stroke_opacity=0.6
                        ).move_to(ax.c2p(0, 0))
                        contours.add(ellipse)

            self.play(Create(contours), run_time=0.5)

            # 临界点
            dot = Dot(ax.c2p(0, 0), color=case["color"], radius=0.1)
            self.play(Create(dot))

            # 标签
            label = Text(case["name"], font_size=14, color=case["color"])
            label.next_to(ax, DOWN)

            eig_text = MathTex(
                rf"\lambda_1={eigenvalues[0]:.0f}, \lambda_2={eigenvalues[1]:.0f}",
                font_size=16
            ).next_to(label, DOWN)

            type_text = Text(f"({case['type']})", font_size=12, color=case["color"])
            type_text.next_to(eig_text, DOWN)

            self.play(Write(label), Write(eig_text), Write(type_text))

        # 底部总结
        summary = VGroup(
            MathTex(r"\text{All } \lambda_i > 0 \Rightarrow \text{Minimum}", font_size=20, color=GREEN),
            MathTex(r"\text{All } \lambda_i < 0 \Rightarrow \text{Maximum}", font_size=20, color=RED),
            MathTex(r"\text{Mixed signs} \Rightarrow \text{Saddle}", font_size=20, color=YELLOW),
        ).arrange(RIGHT, buff=1).to_edge(DOWN)

        self.play(Write(summary))

        self.wait(2)


class HessianSimple(Scene):
    """简化版Hessian动画"""
    def construct(self):
        title = Text("Hessian & Curvature", font_size=28).to_edge(UP)
        self.add(title)

        # 单个坐标系，展示从正定到鞍点的过渡
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
        )
        self.add(axes)

        # 参数化Hessian: H = [[2, 0], [0, lambda2]]
        # lambda2从3变到-3

        lambda2_text = MathTex(r"\lambda_2 = 3.0", font_size=24, color=YELLOW)
        lambda2_text.to_corner(UR)
        self.add(lambda2_text)

        type_text = Text("Minimum", font_size=20, color=GREEN)
        type_text.to_corner(DR)
        self.add(type_text)

        current_contours = VGroup()

        for lambda2 in np.linspace(3, -3, 30):
            H = np.array([[2, 0], [0, lambda2]])

            new_contours = VGroup()

            if abs(lambda2) > 0.3:
                for level in [0.5, 1, 2, 3]:
                    if lambda2 > 0:
                        # 椭圆
                        a = np.sqrt(level / 2)
                        b = np.sqrt(level / lambda2) if lambda2 > 0 else 1
                        if a < 2 and b < 2:
                            ellipse = Ellipse(
                                width=2*a * 5/4,
                                height=2*b * 5/4,
                                color=GREEN,
                                stroke_width=2,
                                stroke_opacity=0.6
                            ).move_to(axes.c2p(0, 0))
                            new_contours.add(ellipse)
                    else:
                        # 双曲线
                        for sign_level in [level, -level]:
                            points_upper = []
                            points_lower = []
                            for x in np.linspace(-1.8, 1.8, 50):
                                discriminant = (2*x**2 - sign_level) / (-lambda2)
                                if discriminant >= 0:
                                    y = np.sqrt(discriminant)
                                    if y <= 2:
                                        points_upper.append(axes.c2p(x, y))
                                        points_lower.append(axes.c2p(x, -y))

                            if len(points_upper) > 2:
                                curve_up = VMobject(color=YELLOW, stroke_width=2)
                                curve_up.set_points_smoothly(points_upper)
                                new_contours.add(curve_up)

                                curve_down = VMobject(color=YELLOW, stroke_width=2)
                                curve_down.set_points_smoothly(points_lower)
                                new_contours.add(curve_down)

            # 更新文本
            new_lambda_text = MathTex(rf"\lambda_2 = {lambda2:.1f}", font_size=24, color=YELLOW)
            new_lambda_text.to_corner(UR)

            if lambda2 > 0.3:
                new_type = Text("Minimum", font_size=20, color=GREEN)
            elif lambda2 < -0.3:
                new_type = Text("Saddle Point", font_size=20, color=YELLOW)
            else:
                new_type = Text("Degenerate", font_size=20, color=WHITE)
            new_type.to_corner(DR)

            self.play(
                ReplacementTransform(current_contours, new_contours),
                Transform(lambda2_text, new_lambda_text),
                Transform(type_text, new_type),
                run_time=0.12
            )
            current_contours = new_contours

        self.wait(1)
