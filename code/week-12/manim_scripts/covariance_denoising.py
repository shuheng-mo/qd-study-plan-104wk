"""
协方差矩阵去噪动画
展示基于RMT的特征值去噪过程
"""
from manim import *
import numpy as np


class CovarianceDenoising(Scene):
    """完整版：协方差去噪过程"""

    def construct(self):
        # 标题
        title = Text("协方差矩阵去噪", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 3, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.5)

        x_label = Text("特征值索引", font_size=20).next_to(axes, DOWN)
        y_label = Text("特征值", font_size=20).next_to(axes, LEFT).rotate(PI/2)

        self.play(Create(axes), Write(x_label))

        # 生成模拟特征值
        np.random.seed(42)
        n_assets = 50

        # 信号特征值（较大）
        n_signal = 5
        signal_eigs = np.array([2.5, 2.0, 1.8, 1.5, 1.3])

        # 噪声特征值
        noise_eigs = np.random.uniform(0.3, 0.8, n_assets - n_signal)

        # 合并并排序
        all_eigs = np.concatenate([signal_eigs, noise_eigs])
        all_eigs = np.sort(all_eigs)[::-1]

        # MP边界
        lambda_plus = 1.0

        # 创建特征值柱状图
        bars = VGroup()
        for i, eig in enumerate(all_eigs):
            color = RED if eig > lambda_plus else BLUE
            bar = Rectangle(
                width=0.15,
                height=eig * axes.y_length / 3,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=0.5
            )
            bar.move_to(axes.c2p(i, eig/2))
            bars.add(bar)

        self.play(Create(bars), run_time=2)

        # MP边界线
        mp_line = DashedLine(
            axes.c2p(0, lambda_plus),
            axes.c2p(50, lambda_plus),
            color=ORANGE,
            stroke_width=2
        )
        mp_label = MathTex(r"\lambda_+", font_size=24, color=ORANGE)
        mp_label.next_to(mp_line, RIGHT)

        self.play(Create(mp_line), Write(mp_label))

        # 标注
        signal_text = Text("信号", font_size=18, color=RED)
        signal_text.move_to(axes.c2p(2, 2.8))
        noise_text = Text("噪声", font_size=18, color=BLUE)
        noise_text.move_to(axes.c2p(30, 1.2))

        self.play(Write(signal_text), Write(noise_text))
        self.wait(1)

        # 去噪过程
        denoise_title = Text("去噪: 将噪声特征值收缩到均值", font_size=24, color=GREEN)
        denoise_title.to_edge(DOWN)
        self.play(Write(denoise_title))

        # 噪声均值
        noise_mean = np.mean(noise_eigs)

        # 动画：噪声特征值收缩
        new_bars = VGroup()
        for i, eig in enumerate(all_eigs):
            if eig > lambda_plus:
                new_eig = eig  # 保持信号
                color = RED
            else:
                new_eig = noise_mean  # 收缩到均值
                color = PURPLE

            bar = Rectangle(
                width=0.15,
                height=new_eig * axes.y_length / 3,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=0.5
            )
            bar.move_to(axes.c2p(i, new_eig/2))
            new_bars.add(bar)

        self.play(Transform(bars, new_bars), run_time=2)

        # 噪声均值线
        mean_line = DashedLine(
            axes.c2p(n_signal, noise_mean),
            axes.c2p(50, noise_mean),
            color=PURPLE,
            stroke_width=2
        )
        mean_label = Text("噪声均值", font_size=16, color=PURPLE)
        mean_label.next_to(mean_line, RIGHT)

        self.play(Create(mean_line), Write(mean_label))
        self.wait(2)


class DenoisingSimple(Scene):
    """简化版：用于GIF"""

    def construct(self):
        title = Text("特征值去噪", font_size=28)
        title.to_edge(UP)
        self.add(title)

        # 简化坐标
        axes = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 2, 1],
            x_length=8,
            y_length=3,
        ).shift(DOWN * 0.3)
        self.add(axes)

        # 简化特征值
        np.random.seed(42)
        signal_eigs = [1.8, 1.5, 1.2]
        noise_eigs = list(np.random.uniform(0.3, 0.6, 17))
        all_eigs = signal_eigs + sorted(noise_eigs, reverse=True)

        lambda_plus = 0.8

        # 创建柱状图
        bars = VGroup()
        for i, eig in enumerate(all_eigs):
            color = RED if eig > lambda_plus else BLUE
            bar = Rectangle(
                width=0.3,
                height=eig * 1.5,
                fill_color=color,
                fill_opacity=0.7
            )
            bar.move_to(axes.c2p(i, eig/2))
            bars.add(bar)

        self.play(Create(bars), run_time=1.5)

        # 边界线
        mp_line = DashedLine(
            axes.c2p(0, lambda_plus),
            axes.c2p(20, lambda_plus),
            color=ORANGE
        )
        self.play(Create(mp_line))

        # 去噪
        noise_mean = np.mean(noise_eigs)
        new_bars = VGroup()
        for i, eig in enumerate(all_eigs):
            if eig > lambda_plus:
                new_eig = eig
                color = RED
            else:
                new_eig = noise_mean
                color = PURPLE

            bar = Rectangle(
                width=0.3,
                height=new_eig * 1.5,
                fill_color=color,
                fill_opacity=0.7
            )
            bar.move_to(axes.c2p(i, new_eig/2))
            new_bars.add(bar)

        self.play(Transform(bars, new_bars), run_time=2)
        self.wait(1)
