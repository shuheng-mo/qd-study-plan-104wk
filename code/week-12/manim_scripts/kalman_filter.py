"""
卡尔曼滤波动画
展示预测-更新两步递归过程
"""
from manim import *
import numpy as np


class KalmanFilterAnimation(Scene):
    """完整版：卡尔曼滤波递归"""

    def construct(self):
        # 标题
        title = Text("卡尔曼滤波：预测-更新循环", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 状态空间模型
        model_eqs = VGroup(
            MathTex(r"x_t = Ax_{t-1} + w_t", font_size=24),
            MathTex(r"y_t = Cx_t + v_t", font_size=24)
        ).arrange(DOWN, buff=0.3)
        model_eqs.next_to(title, DOWN)

        model_label = Text("状态空间模型", font_size=20)
        model_label.next_to(model_eqs, LEFT)

        self.play(Write(model_eqs), Write(model_label))

        # 创建坐标系显示时变贝塔
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0.5, 2, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 1)

        x_label = Text("时间", font_size=18).next_to(axes, DOWN)
        y_label = Text("Beta", font_size=18).next_to(axes, LEFT).rotate(PI/2)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 生成真实贝塔
        np.random.seed(42)
        t = np.arange(100)
        true_beta = 1.0 + 0.3 * np.sin(2 * np.pi * t / 50)

        # 真实贝塔曲线
        true_curve = axes.plot_line_graph(
            x_values=t,
            y_values=true_beta,
            line_color=WHITE,
            stroke_width=2,
            add_vertex_dots=False
        )
        true_label = Text("真实Beta", font_size=16, color=WHITE)
        true_label.to_corner(UR).shift(DOWN * 2)

        self.play(Create(true_curve["line_graph"]), Write(true_label))

        # 卡尔曼滤波估计（逐步动画）
        est_beta = np.zeros(100)
        x = 1.0
        P = 1.0
        Q = 0.01
        R = 0.1

        # 模拟观测
        observations = true_beta + np.random.randn(100) * 0.1

        # 创建估计曲线（动态更新）
        est_points = VGroup()
        kalman_label = Text("卡尔曼估计", font_size=16, color=BLUE)
        kalman_label.next_to(true_label, DOWN)
        self.add(kalman_label)

        for i in range(0, 100, 5):
            # 预测
            x_pred = x
            P_pred = P + Q

            # 更新
            K = P_pred / (P_pred + R)
            x = x_pred + K * (observations[i] - x_pred)
            P = (1 - K) * P_pred

            est_beta[i] = x

            # 添加点
            point = Dot(axes.c2p(i, x), color=BLUE, radius=0.05)
            est_points.add(point)

            if i < 30:
                self.play(Create(point), run_time=0.1)
            else:
                self.add(point)

        # 连接估计点
        est_line = VMobject(color=BLUE, stroke_width=2)
        points_list = [axes.c2p(i*5, est_beta[i*5]) for i in range(20) if est_beta[i*5] > 0]
        if len(points_list) > 1:
            est_line.set_points_smoothly(points_list)
            self.play(Create(est_line))

        # 卡尔曼增益说明（移到右侧，避免与x轴标签重叠）
        gain_text = Text(
            "卡尔曼增益K:\n平衡模型预测\n与观测更新",
            font_size=16,
            line_spacing=0.8
        ).to_corner(DR).shift(UP * 1.5 + LEFT * 0.3)
        self.play(Write(gain_text))

        self.wait(2)


class KalmanSimple(Scene):
    """简化版：用于GIF"""

    def construct(self):
        title = Text("卡尔曼滤波", font_size=28)
        title.to_edge(UP)
        self.add(title)

        # 两步框图
        predict_box = Rectangle(width=3, height=1.5, color=BLUE)
        predict_box.shift(LEFT * 2.5)
        predict_text = Text("预测", font_size=20)
        predict_text.move_to(predict_box)
        predict_eq = MathTex(r"\hat{x}_{t|t-1}", font_size=18)
        predict_eq.next_to(predict_box, DOWN)

        update_box = Rectangle(width=3, height=1.5, color=GREEN)
        update_box.shift(RIGHT * 2.5)
        update_text = Text("更新", font_size=20)
        update_text.move_to(update_box)
        update_eq = MathTex(r"\hat{x}_{t|t}", font_size=18)
        update_eq.next_to(update_box, DOWN)

        # 箭头
        arrow1 = Arrow(predict_box.get_right(), update_box.get_left(), color=WHITE)
        arrow2 = CurvedArrow(
            update_box.get_bottom() + DOWN * 0.3,
            predict_box.get_bottom() + DOWN * 0.3,
            angle=-PI/2,
            color=YELLOW
        )

        self.play(
            Create(predict_box),
            Create(update_box),
            Write(predict_text),
            Write(update_text)
        )
        self.add(predict_eq, update_eq)

        self.play(Create(arrow1))
        self.play(Create(arrow2))

        # 观测输入
        obs_arrow = Arrow(UP * 2 + RIGHT * 2.5, update_box.get_top(), color=RED)
        obs_label = Text("观测 y_t", font_size=16, color=RED)
        obs_label.next_to(obs_arrow, UP)

        self.play(Create(obs_arrow), Write(obs_label))

        # 卡尔曼增益（放在底部中央偏上，避免与边框太近）
        gain_text = MathTex(r"K_t = \frac{P_{t|t-1}}{P_{t|t-1} + R}", font_size=20)
        gain_text.to_edge(DOWN, buff=0.8)
        self.play(Write(gain_text))

        self.wait(2)
