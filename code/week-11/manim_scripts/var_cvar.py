"""
VaR和CVaR可视化动画
展示蒙特卡洛模拟生成的损益分布和风险度量
"""
from manim import *
import numpy as np


class VaRCVaRVisualization(Scene):
    """VaR和CVaR的动态可视化"""
    def construct(self):
        # 标题
        title = Text("VaR & CVaR Visualization", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 坐标系 - 损益分布
        axes = Axes(
            x_range=[-0.15, 0.15, 0.05],
            y_range=[0, 1500, 300],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.5)

        x_label = Text("Portfolio Return", font_size=18).next_to(axes.x_axis, DOWN)
        y_label = Text("Frequency", font_size=18).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)

        self.play(Create(axes), Write(x_label))

        # 生成模拟数据
        np.random.seed(42)
        n_simulations = 10000
        portfolio_mean = 0.0005  # 日均收益
        portfolio_std = 0.02    # 日波动率

        returns = np.random.normal(portfolio_mean, portfolio_std, n_simulations)

        # 计算VaR和CVaR
        confidence = 0.95
        var_percentile = (1 - confidence) * 100
        var = -np.percentile(returns, var_percentile)
        cvar = -np.mean(returns[returns <= -var])

        # 创建直方图
        n_bins = 50
        hist, bin_edges = np.histogram(returns, bins=n_bins, range=(-0.15, 0.15))

        # 动画：逐步构建直方图
        bars = VGroup()
        bar_width = (bin_edges[1] - bin_edges[0]) * axes.x_length / 0.3

        for i in range(n_bins):
            bar_height = hist[i] * axes.y_length / 1500
            bar_center_x = (bin_edges[i] + bin_edges[i+1]) / 2

            # 根据是否在VaR左侧决定颜色
            if bin_edges[i+1] < -var:
                color = RED  # 尾部风险区域
            else:
                color = BLUE

            bar = Rectangle(
                width=bar_width * 0.9,
                height=max(bar_height, 0.01),
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=0.5
            )
            bar.move_to(axes.c2p(bar_center_x, hist[i]/2))
            bars.add(bar)

        # 分批显示直方图
        batch_size = 5
        for i in range(0, n_bins, batch_size):
            batch = bars[i:i+batch_size]
            self.play(*[GrowFromEdge(bar, DOWN) for bar in batch], run_time=0.2)

        self.wait(0.5)

        # VaR线
        var_line = DashedLine(
            axes.c2p(-var, 0),
            axes.c2p(-var, 1200),
            color=YELLOW,
            stroke_width=3
        )
        var_label = Text(f"95% VaR = {var*100:.2f}%", font_size=18, color=YELLOW)
        var_label.next_to(var_line, UP)

        self.play(Create(var_line), Write(var_label))
        self.wait(0.5)

        # 高亮尾部区域
        tail_region = Polygon(
            axes.c2p(-0.15, 0),
            axes.c2p(-var, 0),
            axes.c2p(-var, 800),
            axes.c2p(-0.15, 100),
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=0
        )
        self.play(FadeIn(tail_region))

        # CVaR标注
        cvar_line = Line(
            axes.c2p(-cvar, 0),
            axes.c2p(-cvar, 600),
            color=ORANGE,
            stroke_width=4
        )
        cvar_label = Text(f"CVaR = {cvar*100:.2f}%", font_size=18, color=ORANGE)
        cvar_label.next_to(cvar_line, LEFT)

        self.play(Create(cvar_line), Write(cvar_label))

        # 说明文字
        explanation = VGroup(
            Text("VaR: Maximum loss at 95% confidence", font_size=16),
            Text("CVaR: Expected loss in worst 5% cases", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DR)

        self.play(Write(explanation))

        self.wait(2)


class VaRCVaRSimple(Scene):
    """简化版VaR/CVaR动画"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[-0.12, 0.12, 0.04],
            y_range=[0, 1200, 400],
            x_length=9,
            y_length=5,
        ).shift(DOWN * 0.3)

        title = Text("VaR & CVaR", font_size=28).to_edge(UP)
        x_label = Text("Return", font_size=16).next_to(axes.x_axis, DOWN)

        self.add(axes, title, x_label)

        # 模拟数据
        np.random.seed(42)
        returns = np.random.normal(0.0005, 0.02, 10000)
        var = -np.percentile(returns, 5)
        cvar = -np.mean(returns[returns <= -var])

        # 直方图
        hist, bin_edges = np.histogram(returns, bins=40, range=(-0.12, 0.12))

        bars = VGroup()
        for i in range(40):
            bar_width = 0.006 * 9 / 0.24
            bar_height = hist[i] * 5 / 1200
            bar_center = (bin_edges[i] + bin_edges[i+1]) / 2

            color = RED if bin_edges[i+1] < -var else BLUE

            bar = Rectangle(
                width=bar_width * 0.9,
                height=max(bar_height, 0.01),
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=0
            )
            bar.move_to(axes.c2p(bar_center, hist[i]/2))
            bars.add(bar)

        # 动画显示直方图增长
        for bar in bars:
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)

        self.add(bars)

        self.play(
            *[bar.animate.restore() for bar in bars],
            run_time=1.5,
            lag_ratio=0.02
        )

        # VaR线
        var_line = DashedLine(
            axes.c2p(-var, 0),
            axes.c2p(-var, 1000),
            color=YELLOW,
            stroke_width=3
        )
        var_text = Text(f"VaR={var*100:.1f}%", font_size=16, color=YELLOW)
        var_text.next_to(var_line, UP)

        self.play(Create(var_line), Write(var_text))

        # CVaR线
        cvar_line = Line(
            axes.c2p(-cvar, 0),
            axes.c2p(-cvar, 500),
            color=ORANGE,
            stroke_width=4
        )
        cvar_text = Text(f"CVaR={cvar*100:.1f}%", font_size=16, color=ORANGE)
        cvar_text.next_to(cvar_line, LEFT)

        self.play(Create(cvar_line), Write(cvar_text))

        # 尾部区域高亮
        tail_highlight = VGroup()
        for i, bar in enumerate(bars):
            if bin_edges[i+1] < -var:
                highlight = bar.copy()
                highlight.set_fill(RED, opacity=0.9)
                tail_highlight.add(highlight)

        self.play(
            *[FadeIn(h, scale=1.1) for h in tail_highlight],
            run_time=0.5
        )

        self.wait(1.5)
