"""
梯度下降动画
展示在二次函数等高线上的梯度下降过程
"""
from manim import *
import numpy as np

class GradientDescent(Scene):
    def construct(self):
        # 标题
        title = Text("梯度下降算法", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(DOWN * 0.3)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 定义函数 f(x,y) = x^2 + 2y^2
        def f(x, y):
            return x**2 + 2*y**2

        # 绘制等高线
        contour_levels = [0.5, 1, 2, 4, 8, 12]
        contours = VGroup()

        for level in contour_levels:
            # 椭圆参数: x^2 + 2y^2 = level
            # => (x/sqrt(level))^2 + (y/sqrt(level/2))^2 = 1
            a = np.sqrt(level)  # x方向半轴
            b = np.sqrt(level / 2)  # y方向半轴

            ellipse = Ellipse(
                width=2*a * axes.x_length / 6,
                height=2*b * axes.y_length / 6,
                color=BLUE,
                stroke_width=1.5,
                stroke_opacity=0.6
            ).move_to(axes.c2p(0, 0))
            contours.add(ellipse)

        self.play(Create(contours), run_time=2)

        # 公式
        formula = MathTex(r"f(x,y) = x^2 + 2y^2", font_size=28)
        formula.to_corner(UR).shift(DOWN * 0.5)
        self.play(Write(formula))

        # 梯度下降
        def gradient(x, y):
            return np.array([2*x, 4*y])

        # 起始点
        start_point = np.array([2.5, 2.0])
        learning_rate = 0.15

        # 创建点和轨迹
        dot = Dot(axes.c2p(*start_point), color=RED, radius=0.1)
        path = VMobject(color=YELLOW, stroke_width=3)
        path.set_points_as_corners([axes.c2p(*start_point)])

        self.play(Create(dot))

        # 迭代标签
        iter_label = Text("迭代: 0", font_size=24).to_corner(UL).shift(DOWN * 0.5)
        loss_label = Text(f"损失: {f(*start_point):.2f}", font_size=24).next_to(iter_label, DOWN)
        self.play(Write(iter_label), Write(loss_label))

        # 梯度下降动画
        current_point = start_point.copy()

        for i in range(12):
            # 计算梯度和新位置
            grad = gradient(*current_point)
            new_point = current_point - learning_rate * grad

            # 绘制梯度箭头
            arrow = Arrow(
                axes.c2p(*current_point),
                axes.c2p(*(current_point - 0.3 * grad / np.linalg.norm(grad))),
                color=GREEN,
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.3
            )

            self.play(Create(arrow), run_time=0.3)

            # 移动点
            new_dot_pos = axes.c2p(*new_point)
            path.add_points_as_corners([new_dot_pos])

            self.play(
                dot.animate.move_to(new_dot_pos),
                Create(path.copy()),
                FadeOut(arrow),
                iter_label.animate.become(Text(f"迭代: {i+1}", font_size=24).to_corner(UL).shift(DOWN * 0.5)),
                loss_label.animate.become(Text(f"损失: {f(*new_point):.2f}", font_size=24).next_to(iter_label, DOWN)),
                run_time=0.5
            )

            current_point = new_point

            if np.linalg.norm(grad) < 0.1:
                break

        # 标记最优点
        optimal = Dot(axes.c2p(0, 0), color=GREEN, radius=0.15)
        optimal_label = Text("最优解", font_size=20, color=GREEN).next_to(optimal, DOWN)

        self.play(Create(optimal), Write(optimal_label))

        # 结束文字
        conclusion = Text("沿负梯度方向迭代收敛到最小值", font_size=24)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))

        self.wait(2)


class GradientDescentSimple(Scene):
    """简化版梯度下降，适合生成GIF"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
        ).shift(LEFT * 0.5)

        # 等高线（椭圆）
        contours = VGroup()
        for level in [0.5, 1, 2, 4, 8]:
            a = np.sqrt(level)
            b = np.sqrt(level / 2)
            ellipse = Ellipse(
                width=2*a * 5/6,
                height=2*b * 5/6,
                color=BLUE,
                stroke_width=2,
                stroke_opacity=0.5
            ).move_to(axes.c2p(0, 0))
            contours.add(ellipse)

        self.add(axes, contours)

        # 标题和公式
        title = Text("梯度下降", font_size=32).to_edge(UP)
        formula = MathTex(r"f(x,y) = x^2 + 2y^2", font_size=24).to_corner(UR)
        self.add(title, formula)

        # 梯度下降路径
        def gradient(x, y):
            return np.array([2*x, 4*y])

        points = [np.array([2.5, 2.0])]
        lr = 0.15
        for _ in range(15):
            grad = gradient(*points[-1])
            points.append(points[-1] - lr * grad)

        # 动画：点沿路径移动
        dot = Dot(axes.c2p(*points[0]), color=RED, radius=0.12)
        self.add(dot)

        # 使用Line代替VMobject路径
        path_lines = VGroup()

        for i in range(1, len(points)):
            prev_pos = axes.c2p(*points[i-1])
            new_pos = axes.c2p(*points[i])

            line = Line(prev_pos, new_pos, color=YELLOW, stroke_width=3)
            path_lines.add(line)

            self.play(
                dot.animate.move_to(new_pos),
                Create(line),
                run_time=0.25
            )

        # 最终标记
        star = Star(n=5, fill_opacity=1, color=GREEN).scale(0.2).move_to(axes.c2p(0, 0))
        self.play(Create(star))
        self.wait(1)
