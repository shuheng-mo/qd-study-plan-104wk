"""
特征值分散问题动画
展示当p/n比例增加时，样本协方差矩阵特征值的分布变化
"""
from manim import *
import numpy as np


class EigenvalueSpread(Scene):
    """特征值分布随p/n比例变化的动画"""
    def construct(self):
        # 标题
        title = Text("Eigenvalue Spread: The Curse of Dimensionality", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))

        # 坐标系
        axes = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 30, 5],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.5)

        x_label = Text("Eigenvalue", font_size=18).next_to(axes.x_axis, DOWN)
        y_label = Text("Count", font_size=18).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)

        self.play(Create(axes), Write(x_label))

        # p/n比例显示
        ratio_text = Text("p/n = 0.1", font_size=24, color=YELLOW)
        ratio_text.to_corner(UR).shift(DOWN * 0.5)
        self.play(Write(ratio_text))

        # 真实特征值（全部为1）
        true_line = DashedLine(
            axes.c2p(1, 0),
            axes.c2p(1, 25),
            color=GREEN,
            stroke_width=2
        )
        true_label = Text("True eigenvalue", font_size=14, color=GREEN)
        true_label.next_to(true_line, UP)
        self.play(Create(true_line), Write(true_label))

        # 模拟不同p/n比例下的特征值分布
        n = 200  # 固定样本数
        ratios = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95]
        np.random.seed(42)

        current_bars = VGroup()

        for i, ratio in enumerate(ratios):
            p = int(n * ratio)

            # 生成样本协方差矩阵
            X = np.random.randn(n, p)
            sample_cov = X.T @ X / n
            eigenvalues = np.linalg.eigvalsh(sample_cov)

            # 直方图
            hist, bin_edges = np.histogram(eigenvalues, bins=25, range=(0, 2.5))

            # 创建条形图
            new_bars = VGroup()
            for j in range(25):
                bar_width = 0.1 * 8 / 2.5
                bar_height = hist[j] * 5 / 30
                bar_center = (bin_edges[j] + bin_edges[j+1]) / 2

                bar = Rectangle(
                    width=bar_width * 0.85,
                    height=max(bar_height, 0.01),
                    fill_color=BLUE,
                    fill_opacity=0.7,
                    stroke_width=0.5
                )
                bar.move_to(axes.c2p(bar_center, hist[j]/2))
                new_bars.add(bar)

            # 更新比例文字
            new_ratio_text = Text(f"p/n = {ratio}", font_size=24, color=YELLOW)
            new_ratio_text.to_corner(UR).shift(DOWN * 0.5)

            # Marchenko-Pastur边界（理论分布边界）
            if ratio < 1:
                lambda_min = (1 - np.sqrt(ratio))**2
                lambda_max = (1 + np.sqrt(ratio))**2

                mp_min_line = DashedLine(
                    axes.c2p(lambda_min, 0),
                    axes.c2p(lambda_min, 20),
                    color=RED,
                    stroke_width=2
                )
                mp_max_line = DashedLine(
                    axes.c2p(lambda_max, 0),
                    axes.c2p(lambda_max, 20),
                    color=RED,
                    stroke_width=2
                )
            else:
                mp_min_line = VGroup()
                mp_max_line = VGroup()

            if i == 0:
                self.play(
                    *[GrowFromEdge(bar, DOWN) for bar in new_bars],
                    Transform(ratio_text, new_ratio_text),
                    Create(mp_min_line),
                    Create(mp_max_line),
                    run_time=1
                )
                current_bars = new_bars
                current_mp_min = mp_min_line
                current_mp_max = mp_max_line
            else:
                self.play(
                    ReplacementTransform(current_bars, new_bars),
                    Transform(ratio_text, new_ratio_text),
                    ReplacementTransform(current_mp_min, mp_min_line),
                    ReplacementTransform(current_mp_max, mp_max_line),
                    run_time=0.8
                )
                current_bars = new_bars
                current_mp_min = mp_min_line
                current_mp_max = mp_max_line

            self.wait(0.5)

        # 最终说明
        conclusion = VGroup(
            Text("As p/n increases:", font_size=18),
            Text("- Eigenvalues spread out", font_size=16),
            Text("- Small eigenvalues underestimated", font_size=16),
            Text("- Large eigenvalues overestimated", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DL)

        self.play(Write(conclusion))
        self.wait(2)


class EigenvalueSimple(Scene):
    """简化版特征值分散动画"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 25, 5],
            x_length=8,
            y_length=5,
        ).shift(DOWN * 0.3)

        title = Text("Eigenvalue Spread", font_size=28).to_edge(UP)
        x_label = Text("Eigenvalue", font_size=16).next_to(axes.x_axis, DOWN)

        self.add(axes, title, x_label)

        # 真实特征值线
        true_line = DashedLine(
            axes.c2p(1, 0),
            axes.c2p(1, 20),
            color=GREEN,
            stroke_width=2
        )
        true_label = Text("True", font_size=14, color=GREEN).next_to(true_line, UP)
        self.add(true_line, true_label)

        # 比例显示
        ratio_text = Text("p/n = 0.1", font_size=22, color=YELLOW).to_corner(UR)
        self.add(ratio_text)

        # 动画不同比例
        n = 200
        ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        np.random.seed(42)

        current_bars = None

        for ratio in ratios:
            p = int(n * ratio)

            X = np.random.randn(n, p)
            sample_cov = X.T @ X / n
            eigenvalues = np.linalg.eigvalsh(sample_cov)

            hist, bin_edges = np.histogram(eigenvalues, bins=30, range=(0, 2.5))

            new_bars = VGroup()
            for j in range(30):
                bar_width = (2.5/30) * 8 / 2.5
                bar_height = hist[j] * 5 / 25
                bar_center = (bin_edges[j] + bin_edges[j+1]) / 2

                bar = Rectangle(
                    width=bar_width * 0.85,
                    height=max(bar_height, 0.01),
                    fill_color=BLUE,
                    fill_opacity=0.7,
                    stroke_width=0
                )
                bar.move_to(axes.c2p(bar_center, hist[j]/2))
                new_bars.add(bar)

            new_ratio_text = Text(f"p/n = {ratio:.1f}", font_size=22, color=YELLOW)
            new_ratio_text.to_corner(UR)

            if current_bars is None:
                self.play(
                    *[GrowFromEdge(bar, DOWN) for bar in new_bars],
                    Transform(ratio_text, new_ratio_text),
                    run_time=0.5
                )
                current_bars = new_bars
            else:
                self.play(
                    ReplacementTransform(current_bars, new_bars),
                    Transform(ratio_text, new_ratio_text),
                    run_time=0.4
                )
                current_bars = new_bars

        # 警告标志
        warning = Text("Dimension Curse!", font_size=24, color=RED)
        warning.to_edge(DOWN)
        self.play(Write(warning))

        self.wait(1)
