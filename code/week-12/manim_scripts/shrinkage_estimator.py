"""
收缩估计动画
展示协方差矩阵从样本协方差向结构化目标收缩的过程
"""
from manim import *
import numpy as np


class ShrinkageEstimator(Scene):
    """完整版：收缩估计过程动画"""

    def construct(self):
        # 标题
        title = Text("协方差矩阵收缩估计", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 公式
        formula = MathTex(
            r"\Sigma_{shrink} = \alpha F + (1-\alpha) \Sigma_{sample}",
            font_size=32
        )
        formula.next_to(title, DOWN, buff=0.5)
        self.play(Write(formula))

        # 创建三个矩阵的可视化
        # 样本协方差
        sample_label = Text("样本协方差 Σ_sample", font_size=24)
        sample_label.to_edge(LEFT).shift(UP * 1.5 + RIGHT * 1.5)

        # 收缩目标
        target_label = Text("收缩目标 F", font_size=24)
        target_label.to_edge(RIGHT).shift(UP * 1.5 + LEFT * 1.5)

        # 收缩结果
        result_label = Text("收缩结果 Σ_shrink", font_size=24)
        result_label.move_to(DOWN * 2.5)

        self.play(
            Write(sample_label),
            Write(target_label),
            Write(result_label)
        )

        # 创建矩阵热力图
        np.random.seed(42)
        n = 5

        # 样本协方差（有噪声）
        sample_data = np.random.randn(n, n)
        sample_cov = sample_data @ sample_data.T / n
        sample_cov = sample_cov / np.max(np.abs(sample_cov))

        # 收缩目标（单位矩阵缩放）
        target = np.eye(n) * np.mean(np.diag(sample_cov))
        target = target / np.max(np.abs(target))

        def create_matrix_visual(data, position, scale=0.8):
            """创建矩阵的可视化"""
            squares = VGroup()
            n = data.shape[0]
            for i in range(n):
                for j in range(n):
                    val = data[i, j]
                    color = interpolate_color(BLUE, RED, (val + 1) / 2)
                    sq = Square(side_length=0.4 * scale)
                    sq.set_fill(color, opacity=0.8)
                    sq.set_stroke(WHITE, width=1)
                    sq.move_to(position + RIGHT * j * 0.4 * scale + DOWN * i * 0.4 * scale)
                    squares.add(sq)
            # 居中
            squares.move_to(position)
            return squares

        sample_visual = create_matrix_visual(sample_cov, LEFT * 3.5 + UP * 0)
        target_visual = create_matrix_visual(target, RIGHT * 3.5 + UP * 0)

        self.play(Create(sample_visual), Create(target_visual))

        # Alpha滑块
        alpha_tracker = ValueTracker(0)

        alpha_label = always_redraw(
            lambda: Text(
                f"α = {alpha_tracker.get_value():.2f}",
                font_size=28
            ).move_to(DOWN * 1)
        )
        self.play(Write(alpha_label))

        # 结果矩阵
        def get_shrunk_matrix(alpha):
            return alpha * target + (1 - alpha) * sample_cov

        result_visual = always_redraw(
            lambda: create_matrix_visual(
                get_shrunk_matrix(alpha_tracker.get_value()),
                DOWN * 2.5 + LEFT * 0.5,
                scale=1.0
            )
        )

        self.add(result_visual)

        # 动画：改变alpha
        self.play(alpha_tracker.animate.set_value(0.3), run_time=2)
        self.wait(0.5)
        self.play(alpha_tracker.animate.set_value(0.7), run_time=2)
        self.wait(0.5)
        self.play(alpha_tracker.animate.set_value(0.5), run_time=1)

        # 说明文字
        note = Text(
            "α越大，越接近结构化目标（更稳定）\nα越小，越接近样本协方差（更精确）",
            font_size=20
        ).to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)


class ShrinkageSimple(Scene):
    """简化版：用于GIF"""

    def construct(self):
        title = Text("收缩估计", font_size=32)
        title.to_edge(UP)

        formula = MathTex(
            r"\Sigma_{shrink} = \alpha F + (1-\alpha) \Sigma_{sample}",
            font_size=28
        )
        formula.next_to(title, DOWN)

        self.add(title, formula)

        # 简化的动画
        left_sq = Square(side_length=1.5, color=BLUE, fill_opacity=0.5)
        left_sq.move_to(LEFT * 3)
        left_label = Text("Σ_sample", font_size=20).next_to(left_sq, DOWN)

        right_sq = Square(side_length=1.5, color=GREEN, fill_opacity=0.5)
        right_sq.move_to(RIGHT * 3)
        right_label = Text("F (目标)", font_size=20).next_to(right_sq, DOWN)

        self.play(Create(left_sq), Create(right_sq))
        self.add(left_label, right_label)

        # 结果
        result_sq = Square(side_length=1.5, fill_opacity=0.5)
        result_sq.move_to(DOWN * 1.5)
        result_label = Text("Σ_shrink", font_size=20).next_to(result_sq, DOWN)

        alpha_tracker = ValueTracker(0)

        def update_result(sq):
            alpha = alpha_tracker.get_value()
            color = interpolate_color(BLUE, GREEN, alpha)
            sq.set_fill(color, opacity=0.5)

        result_sq.add_updater(update_result)
        self.add(result_sq, result_label)

        # 动画
        self.play(alpha_tracker.animate.set_value(1), run_time=3)
        self.play(alpha_tracker.animate.set_value(0.5), run_time=1.5)
        self.wait(1)
