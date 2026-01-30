"""
Marchenko-Pastur分布动画
展示随机矩阵特征值分布与MP理论预测
"""
from manim import *
import numpy as np


class MarchenkoPastur(Scene):
    """完整版：MP分布与特征值"""

    def construct(self):
        # 标题
        title = Text("Marchenko-Pastur分布", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 参数说明
        params = MathTex(
            r"\gamma = \frac{p}{n}",
            font_size=28
        )
        params.next_to(title, DOWN)
        self.play(Write(params))

        # 创建坐标系
        axes = Axes(
            x_range=[0, 4, 0.5],
            y_range=[0, 1.2, 0.2],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(DOWN * 0.5)

        x_label = MathTex(r"\lambda", font_size=24).next_to(axes, RIGHT, buff=0.1)
        y_label = Text("Density", font_size=18).next_to(axes, UP, buff=0.1).shift(LEFT * 4)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # MP分布参数
        gamma = 0.4  # p/n
        sigma_sq = 1.0
        lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2
        lambda_minus = sigma_sq * (1 - np.sqrt(gamma))**2

        # MP分布曲线
        def mp_pdf(x):
            if x <= lambda_minus or x >= lambda_plus:
                return 0
            return (1 / (2 * np.pi * sigma_sq * gamma * x)) * \
                   np.sqrt((lambda_plus - x) * (x - lambda_minus))

        mp_curve = axes.plot(
            lambda x: mp_pdf(x),
            x_range=[lambda_minus + 0.01, lambda_plus - 0.01, 0.01],
            color=RED,
            stroke_width=3
        )

        self.play(Create(mp_curve), run_time=2)

        # 边界线
        lambda_minus_line = axes.get_vertical_line(
            axes.c2p(lambda_minus, 0.8),
            color=GREEN,
            stroke_width=2
        )
        lambda_plus_line = axes.get_vertical_line(
            axes.c2p(lambda_plus, 0.8),
            color=ORANGE,
            stroke_width=2
        )

        lambda_minus_label = MathTex(r"\lambda_-", font_size=24, color=GREEN)
        lambda_minus_label.next_to(lambda_minus_line, UP)

        lambda_plus_label = MathTex(r"\lambda_+", font_size=24, color=ORANGE)
        lambda_plus_label.next_to(lambda_plus_line, UP)

        self.play(
            Create(lambda_minus_line),
            Create(lambda_plus_line),
            Write(lambda_minus_label),
            Write(lambda_plus_label)
        )

        # 模拟特征值（直方图）
        np.random.seed(42)
        n, p = 500, 200
        X = np.random.randn(n, p)
        cov = X.T @ X / n
        eigenvalues = np.linalg.eigvalsh(cov)

        # 创建直方图
        hist_bars = VGroup()
        bins = np.linspace(0, 4, 30)
        hist, _ = np.histogram(eigenvalues, bins=bins, density=True)

        for i in range(len(hist)):
            if hist[i] > 0:
                bar = Rectangle(
                    width=(bins[i+1] - bins[i]) * axes.x_length / 4,
                    height=hist[i] * axes.y_length / 1.2,
                    fill_color=BLUE,
                    fill_opacity=0.5,
                    stroke_width=0.5
                )
                bar.move_to(axes.c2p((bins[i] + bins[i+1])/2, hist[i]/2))
                hist_bars.add(bar)

        self.play(Create(hist_bars), run_time=2)

        # 说明（移到右上角，避免与坐标系重叠）
        note = Text(
            "蓝色：样本特征值分布\n红色：MP理论预测",
            font_size=18,
            line_spacing=0.8
        ).to_corner(UR).shift(LEFT * 0.3 + DOWN * 1.5)
        self.play(Write(note))

        # 标注信号特征值（放在说明下方）
        n_signal = np.sum(eigenvalues > lambda_plus)
        if n_signal > 0:
            signal_note = Text(
                f"超出边界的{n_signal}个特征值\n可能是信号",
                font_size=16,
                color=YELLOW,
                line_spacing=0.8
            ).next_to(note, DOWN, buff=0.3)
            self.play(Write(signal_note))

        self.wait(2)


class MPSimple(Scene):
    """简化版：用于GIF"""

    def construct(self):
        title = Text("Marchenko-Pastur分布", font_size=28)
        title.to_edge(UP)
        self.add(title)

        # 简化坐标系
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 1, 0.5],
            x_length=8,
            y_length=4,
        ).shift(DOWN * 0.3)
        self.add(axes)

        # 参数
        gamma = 0.4
        lambda_plus = (1 + np.sqrt(gamma))**2
        lambda_minus = (1 - np.sqrt(gamma))**2

        # MP曲线
        def mp_pdf(x):
            if x <= lambda_minus or x >= lambda_plus:
                return 0
            return (1 / (2 * np.pi * gamma * x)) * \
                   np.sqrt((lambda_plus - x) * (x - lambda_minus))

        mp_curve = axes.plot(
            lambda x: mp_pdf(x),
            x_range=[lambda_minus + 0.01, lambda_plus - 0.01, 0.01],
            color=RED,
            stroke_width=3
        )

        # 边界
        line_minus = DashedLine(
            axes.c2p(lambda_minus, 0),
            axes.c2p(lambda_minus, 0.8),
            color=GREEN
        )
        line_plus = DashedLine(
            axes.c2p(lambda_plus, 0),
            axes.c2p(lambda_plus, 0.8),
            color=ORANGE
        )

        label_minus = MathTex(r"\lambda_-", font_size=20, color=GREEN)
        label_minus.next_to(line_minus, UP, buff=0.1)
        label_plus = MathTex(r"\lambda_+", font_size=20, color=ORANGE)
        label_plus.next_to(line_plus, UP, buff=0.1)

        self.play(
            Create(mp_curve),
            Create(line_minus),
            Create(line_plus),
            run_time=2
        )
        self.add(label_minus, label_plus)

        # 添加区域标注（调整位置避免重叠）
        noise_region = Text("噪声区域", font_size=16).move_to(axes.c2p(1.0, 0.6))
        signal_region = Text("信号", font_size=16, color=YELLOW).move_to(axes.c2p(2.6, 0.15))

        self.play(Write(noise_region), Write(signal_region))
        self.wait(2)
