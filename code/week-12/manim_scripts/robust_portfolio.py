"""
稳健投资组合动画
展示不同协方差估计方法的有效前沿对比
"""
from manim import *
import numpy as np


class RobustPortfolio(Scene):
    """完整版：稳健组合对比"""

    def construct(self):
        # 标题
        title = Text("不同协方差估计方法的有效前沿", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[0, 0.3, 0.05],
            y_range=[0, 0.15, 0.03],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)

        x_label = Text("风险 (波动率)", font_size=18).next_to(axes, DOWN)
        y_label = Text("收益", font_size=18).next_to(axes, LEFT).rotate(PI/2)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 模拟不同方法的有效前沿
        # 样本协方差（不稳定，锯齿状）
        np.random.seed(42)
        risks_sample = np.linspace(0.08, 0.25, 20)
        returns_sample = 0.02 + 0.4 * risks_sample + np.random.randn(20) * 0.01

        # Ledoit-Wolf（更平滑）
        risks_lw = np.linspace(0.07, 0.22, 20)
        returns_lw = 0.025 + 0.45 * risks_lw

        # RMT去噪（最优）
        risks_rmt = np.linspace(0.06, 0.20, 20)
        returns_rmt = 0.03 + 0.5 * risks_rmt

        # 绘制有效前沿
        # 样本协方差
        sample_frontier = axes.plot_line_graph(
            x_values=risks_sample,
            y_values=returns_sample,
            line_color=RED,
            stroke_width=2,
            add_vertex_dots=False
        )
        sample_label = Text("样本协方差", font_size=16, color=RED)
        sample_label.to_corner(UR).shift(DOWN * 2)

        self.play(Create(sample_frontier["line_graph"]), Write(sample_label))

        # Ledoit-Wolf
        lw_frontier = axes.plot_line_graph(
            x_values=risks_lw,
            y_values=returns_lw,
            line_color=BLUE,
            stroke_width=2,
            add_vertex_dots=False
        )
        lw_label = Text("Ledoit-Wolf", font_size=16, color=BLUE)
        lw_label.next_to(sample_label, DOWN)

        self.play(Create(lw_frontier["line_graph"]), Write(lw_label))

        # RMT去噪
        rmt_frontier = axes.plot_line_graph(
            x_values=risks_rmt,
            y_values=returns_rmt,
            line_color=GREEN,
            stroke_width=2,
            add_vertex_dots=False
        )
        rmt_label = Text("RMT去噪", font_size=16, color=GREEN)
        rmt_label.next_to(lw_label, DOWN)

        self.play(Create(rmt_frontier["line_graph"]), Write(rmt_label))

        # 标注最优点
        optimal_risk = 0.12
        optimal_return_sample = 0.02 + 0.4 * optimal_risk
        optimal_return_lw = 0.025 + 0.45 * optimal_risk
        optimal_return_rmt = 0.03 + 0.5 * optimal_risk

        opt_sample = Dot(axes.c2p(optimal_risk + 0.02, optimal_return_sample), color=RED, radius=0.08)
        opt_lw = Dot(axes.c2p(optimal_risk, optimal_return_lw), color=BLUE, radius=0.08)
        opt_rmt = Dot(axes.c2p(optimal_risk - 0.02, optimal_return_rmt), color=GREEN, radius=0.08)

        self.play(Create(opt_sample), Create(opt_lw), Create(opt_rmt))

        # 说明文字
        note1 = Text("样本协方差：不稳定，过拟合", font_size=16, color=RED)
        note2 = Text("正则化方法：更平滑，泛化更好", font_size=16, color=GREEN)
        notes = VGroup(note1, note2).arrange(DOWN, buff=0.2)
        notes.to_edge(DOWN)

        self.play(Write(notes))
        self.wait(2)


class PortfolioSimple(Scene):
    """简化版：用于GIF"""

    def construct(self):
        title = Text("协方差估计方法对比", font_size=28)
        title.to_edge(UP)
        self.add(title)

        # 简化坐标
        axes = Axes(
            x_range=[0, 1, 0.5],
            y_range=[0, 1, 0.5],
            x_length=6,
            y_length=4,
        ).shift(DOWN * 0.3)

        x_label = Text("风险", font_size=16).next_to(axes, DOWN)
        y_label = Text("收益", font_size=16).next_to(axes, LEFT)
        self.add(axes, x_label, y_label)

        # 三条有效前沿
        # 样本：锯齿
        sample_points = [
            axes.c2p(0.3, 0.2),
            axes.c2p(0.4, 0.35),
            axes.c2p(0.5, 0.4),
            axes.c2p(0.6, 0.55),
            axes.c2p(0.7, 0.5),
            axes.c2p(0.8, 0.7)
        ]
        sample_curve = VMobject(color=RED, stroke_width=2)
        sample_curve.set_points_smoothly(sample_points)

        # LW：平滑
        lw_points = [
            axes.c2p(0.25, 0.25),
            axes.c2p(0.35, 0.4),
            axes.c2p(0.45, 0.55),
            axes.c2p(0.55, 0.65),
            axes.c2p(0.65, 0.75)
        ]
        lw_curve = VMobject(color=BLUE, stroke_width=2)
        lw_curve.set_points_smoothly(lw_points)

        # RMT：更优
        rmt_points = [
            axes.c2p(0.2, 0.3),
            axes.c2p(0.3, 0.45),
            axes.c2p(0.4, 0.6),
            axes.c2p(0.5, 0.75),
            axes.c2p(0.6, 0.85)
        ]
        rmt_curve = VMobject(color=GREEN, stroke_width=2)
        rmt_curve.set_points_smoothly(rmt_points)

        # 动画
        self.play(Create(sample_curve), run_time=1)
        sample_label = Text("样本", font_size=14, color=RED).move_to(axes.c2p(0.85, 0.65))
        self.add(sample_label)

        self.play(Create(lw_curve), run_time=1)
        lw_label = Text("收缩", font_size=14, color=BLUE).move_to(axes.c2p(0.7, 0.8))
        self.add(lw_label)

        self.play(Create(rmt_curve), run_time=1)
        rmt_label = Text("去噪", font_size=14, color=GREEN).move_to(axes.c2p(0.55, 0.9))
        self.add(rmt_label)

        # 最优标记
        best_dot = Dot(axes.c2p(0.4, 0.6), color=YELLOW, radius=0.1)
        best_text = Text("更优", font_size=12, color=YELLOW).next_to(best_dot, UR, buff=0.1)
        self.play(Create(best_dot), Write(best_text))

        self.wait(2)
