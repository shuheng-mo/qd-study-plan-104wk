"""
Cholesky分解动画
展示协方差矩阵的Cholesky分解过程
"""
from manim import *
import numpy as np

class CholeskyDecomposition(Scene):
    def construct(self):
        # 标题
        title = Text("Cholesky分解", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 协方差矩阵
        sigma_matrix = MathTex(
            r"\Sigma = \begin{bmatrix} 1 & 0.7 \\ 0.7 & 1 \end{bmatrix}",
            font_size=36
        )
        sigma_matrix.shift(UP * 1.5)
        self.play(Write(sigma_matrix))
        self.wait(0.5)

        # 分解公式
        decomp = MathTex(r"\Sigma = L L^T", font_size=36)
        decomp.next_to(sigma_matrix, DOWN, buff=0.5)
        self.play(Write(decomp))
        self.wait(0.5)

        # L矩阵
        l_matrix = MathTex(
            r"L = \begin{bmatrix} 1 & 0 \\ 0.7 & 0.714 \end{bmatrix}",
            font_size=36
        )
        l_matrix.next_to(decomp, DOWN, buff=0.5)
        self.play(Write(l_matrix))

        # L^T矩阵
        lt_matrix = MathTex(
            r"L^T = \begin{bmatrix} 1 & 0.7 \\ 0 & 0.714 \end{bmatrix}",
            font_size=36
        )
        lt_matrix.next_to(l_matrix, DOWN, buff=0.5)
        self.play(Write(lt_matrix))

        self.wait(1)

        # 清除并展示应用
        self.play(
            FadeOut(sigma_matrix),
            FadeOut(decomp),
            FadeOut(l_matrix),
            FadeOut(lt_matrix)
        )

        # 应用：生成相关随机数
        application_title = Text("应用：生成相关随机数", font_size=32)
        application_title.to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(application_title))

        # 步骤
        step1 = MathTex(r"z \sim N(0, I)", r"\quad \text{独立标准正态}", font_size=28)
        step1.shift(UP * 1)

        step2 = MathTex(r"x = Lz", font_size=28)
        step2.next_to(step1, DOWN, buff=0.5)

        step3 = MathTex(r"x \sim N(0, \Sigma)", r"\quad \text{相关正态}", font_size=28)
        step3.next_to(step2, DOWN, buff=0.5)

        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step2))
        self.wait(0.5)
        self.play(Write(step3))

        # 验证
        verify = MathTex(
            r"\text{验证: } E[xx^T] = E[Lzz^TL^T] = LE[zz^T]L^T = LIL^T = LL^T = \Sigma",
            font_size=24
        )
        verify.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(verify), run_time=2)

        self.wait(2)


class CholeskySimple(Scene):
    """简化版Cholesky分解动画"""
    def construct(self):
        # 公式展示
        eq1 = MathTex(r"\Sigma = LL^T", font_size=48)
        self.play(Write(eq1))
        self.wait(0.5)

        # 移动到上方
        self.play(eq1.animate.to_edge(UP))

        # 具体矩阵
        sigma = MathTex(
            r"\begin{bmatrix} 1 & 0.7 \\ 0.7 & 1 \end{bmatrix}",
            font_size=36
        ).shift(LEFT * 3)

        equals = MathTex("=", font_size=36)

        l_mat = MathTex(
            r"\begin{bmatrix} 1 & 0 \\ 0.7 & 0.71 \end{bmatrix}",
            font_size=36
        ).next_to(equals, RIGHT)

        lt_mat = MathTex(
            r"\begin{bmatrix} 1 & 0.7 \\ 0 & 0.71 \end{bmatrix}",
            font_size=36
        ).next_to(l_mat, RIGHT, buff=0.1)

        # 标签
        sigma_label = MathTex(r"\Sigma", color=BLUE, font_size=28).next_to(sigma, DOWN)
        l_label = MathTex(r"L", color=GREEN, font_size=28).next_to(l_mat, DOWN)
        lt_label = MathTex(r"L^T", color=GREEN, font_size=28).next_to(lt_mat, DOWN)

        self.play(Write(sigma), Write(sigma_label))
        self.wait(0.3)
        self.play(Write(equals))
        self.play(Write(l_mat), Write(l_label))
        self.play(Write(lt_mat), Write(lt_label))

        self.wait(0.5)

        # 应用说明
        application = MathTex(
            r"z \sim N(0,I) \;\rightarrow\; Lz \sim N(0,\Sigma)",
            font_size=32
        ).to_edge(DOWN).shift(UP * 0.5)

        box = SurroundingRectangle(application, color=YELLOW, buff=0.2)

        self.play(Write(application), Create(box))
        self.wait(1)


class CircleToEllipse(Scene):
    """圆形变换为椭圆 - 展示Cholesky变换的几何效果"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
        )
        self.add(axes)

        # 标题（使用Text避免LaTeX）
        title = Text("Cholesky: Circle to Ellipse", font_size=28).to_edge(UP)
        self.add(title)

        # 单位圆上的点
        n_points = 50
        angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        circle_points = np.array([[np.cos(a), np.sin(a)] for a in angles])

        # 绘制圆
        circle_dots = VGroup(*[
            Dot(axes.c2p(*p), color=BLUE, radius=0.06)
            for p in circle_points
        ])

        circle = Circle(radius=1 * 6/6, color=BLUE, stroke_width=2).move_to(axes.c2p(0, 0))

        self.play(Create(circle), Create(circle_dots))

        # 标签（使用Text避免LaTeX）
        formula1 = Text("z: Independent", font_size=20, color=BLUE).to_corner(UL)
        self.play(Write(formula1))

        self.wait(0.5)

        # Cholesky矩阵
        Sigma = np.array([[1, 0.7], [0.7, 1]])
        L = np.linalg.cholesky(Sigma)

        # 变换后的点
        ellipse_points = np.array([L @ p for p in circle_points])

        ellipse_dots = VGroup(*[
            Dot(axes.c2p(*p), color=RED, radius=0.06)
            for p in ellipse_points
        ])

        # 椭圆
        eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
        angle = np.degrees(np.arctan2(eigenvectors[1, 1], eigenvectors[0, 1]))
        ellipse = Ellipse(
            width=2*np.sqrt(eigenvalues[1]) * 6/6,
            height=2*np.sqrt(eigenvalues[0]) * 6/6,
            color=RED,
            stroke_width=2
        ).rotate(angle * DEGREES).move_to(axes.c2p(0, 0))

        # 变换动画
        self.play(
            Transform(circle, ellipse),
            Transform(circle_dots, ellipse_dots),
            run_time=2
        )

        formula2 = Text("Lz: Correlated", font_size=20, color=RED).next_to(formula1, DOWN)
        self.play(Write(formula2))

        self.wait(2)
