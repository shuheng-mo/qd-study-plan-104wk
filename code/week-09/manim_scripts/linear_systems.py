"""
线性方程组与逆矩阵
- 线性方程组的几何解释：平面/直线的交点
- 何时有解？何时无解？何时有无穷多解？
- 逆矩阵的几何意义与计算代价
- 伪逆（Moore-Penrose）：当逆不存在时的最优近似

运行方式：
manim -pql linear_systems.py Scene名称
"""

from manim import *
import numpy as np


class LinearSystemGeometry(Scene):
    """2D线性方程组：两条直线的交点"""
    
    def construct(self):
        title = Text("线性方程组 = 直线的交点", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        eq1 = MathTex(r"2x + y = 5", font_size=32, color=BLUE)
        eq2 = MathTex(r"x - y = 1", font_size=32, color=RED)
        equations = VGroup(eq1, eq2).arrange(DOWN, aligned_edge=LEFT)
        equations.to_corner(UL).shift(DOWN * 1)
        
        self.play(Write(eq1))
        self.play(Write(eq2))
        
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-2, 6, 1],
            x_length=6,
            y_length=6
        ).shift(RIGHT * 1.5)
        
        self.play(Create(plane))
        
        line1 = plane.plot(lambda x: 5 - 2*x, x_range=[0, 4], color=BLUE, stroke_width=3)
        label1 = MathTex(r"2x + y = 5", font_size=24, color=BLUE)
        label1.next_to(line1, UR)
        
        self.play(Create(line1), Write(label1))
        
        line2 = plane.plot(lambda x: x - 1, x_range=[0, 4.5], color=RED, stroke_width=3)
        label2 = MathTex(r"x - y = 1", font_size=24, color=RED)
        label2.next_to(line2, DR)
        
        self.play(Create(line2), Write(label2))
        
        intersection = Dot(plane.c2p(2, 1), color=YELLOW, radius=0.15)
        int_label = MathTex(r"(2, 1)", font_size=28, color=YELLOW)
        int_label.next_to(intersection, UR)
        
        self.play(Create(intersection), Write(int_label))
        
        solution = MathTex(r"\text{解: } x=2, y=1", font_size=32, color=YELLOW)
        solution.to_edge(DOWN)
        self.play(Write(solution))
        self.wait(2)


class LinearSystemMatrix(Scene):
    """线性方程组的矩阵形式"""
    
    def construct(self):
        title = Text("方程组 → 矩阵形式", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        eq_form = MathTex(
            r"\begin{cases} 2x + y = 5 \\ x - y = 1 \end{cases}",
            font_size=36
        ).shift(LEFT * 3 + UP * 1)
        
        self.play(Write(eq_form))
        self.wait()
        
        arrow = Arrow(LEFT * 1, RIGHT * 1, color=YELLOW)
        self.play(GrowArrow(arrow))
        
        matrix_form = MathTex(
            r"\begin{bmatrix} 2 & 1 \\ 1 & -1 \end{bmatrix}",
            r"\begin{bmatrix} x \\ y \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} 5 \\ 1 \end{bmatrix}",
            font_size=36
        ).shift(RIGHT * 2 + UP * 1)
        
        self.play(Write(matrix_form))
        self.wait()
        
        abstract = MathTex(r"A\vec{x} = \vec{b}", font_size=48, color=YELLOW)
        abstract.shift(DOWN * 1.5)
        
        labels = VGroup(
            MathTex(r"A: \text{系数矩阵}", font_size=28),
            MathTex(r"\vec{x}: \text{未知向量}", font_size=28),
            MathTex(r"\vec{b}: \text{常数向量}", font_size=28)
        ).arrange(RIGHT, buff=1)
        labels.shift(DOWN * 2.5)
        
        self.play(Write(abstract))
        self.play(Write(labels))
        self.wait(2)


class ThreeSolutionCases(Scene):
    """三种解的情况"""
    
    def construct(self):
        title = Text("线性方程组的三种情况", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        plane1 = NumberPlane(
            x_range=[-2, 3, 1], y_range=[-2, 3, 1],
            x_length=3, y_length=3
        ).shift(LEFT * 4)
        
        line1a = plane1.plot(lambda x: 2 - x, x_range=[-1, 2.5], color=BLUE, stroke_width=3)
        line1b = plane1.plot(lambda x: 0.5*x, x_range=[-1, 2.5], color=RED, stroke_width=3)
        dot1 = Dot(plane1.c2p(4/3, 2/3), color=YELLOW, radius=0.1)
        
        case1_label = Text("唯一解", font_size=24, color=GREEN)
        case1_label.next_to(plane1, DOWN)
        case1_sub = Text("两线相交", font_size=18, color=GRAY)
        case1_sub.next_to(case1_label, DOWN, buff=0.1)
        
        plane2 = NumberPlane(
            x_range=[-2, 3, 1], y_range=[-2, 3, 1],
            x_length=3, y_length=3
        )
        
        line2a = plane2.plot(lambda x: 1 - x, x_range=[-1, 2.5], color=BLUE, stroke_width=3)
        line2b = plane2.plot(lambda x: 2 - x, x_range=[-1, 2.5], color=RED, stroke_width=3)
        
        case2_label = Text("无解", font_size=24, color=RED)
        case2_label.next_to(plane2, DOWN)
        case2_sub = Text("两线平行", font_size=18, color=GRAY)
        case2_sub.next_to(case2_label, DOWN, buff=0.1)
        
        plane3 = NumberPlane(
            x_range=[-2, 3, 1], y_range=[-2, 3, 1],
            x_length=3, y_length=3
        ).shift(RIGHT * 4)
        
        line3a = plane3.plot(lambda x: 1 - x, x_range=[-1, 2.5], color=PURPLE, stroke_width=5)
        
        case3_label = Text("无穷多解", font_size=24, color=YELLOW)
        case3_label.next_to(plane3, DOWN)
        case3_sub = Text("两线重合", font_size=18, color=GRAY)
        case3_sub.next_to(case3_label, DOWN, buff=0.1)
        
        self.play(Create(plane1), Create(plane2), Create(plane3))
        self.play(
            Create(line1a), Create(line1b), Create(dot1),
            Create(line2a), Create(line2b),
            Create(line3a)
        )
        self.play(
            Write(case1_label), Write(case1_sub),
            Write(case2_label), Write(case2_sub),
            Write(case3_label), Write(case3_sub)
        )
        self.wait(2)


class ThreeDLinearSystem(ThreeDScene):
    """3D线性方程组：平面的交点"""
    
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        title = Text("3D: 三个平面的交点", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        self.play(Create(axes))
        
        plane1 = Surface(
            lambda u, v: axes.c2p(u, v, 3 - u - v),
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_color=BLUE,
            fill_opacity=0.3,
            resolution=(10, 10)
        )
        
        plane2 = Surface(
            lambda u, v: axes.c2p(u, u, v),
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_color=RED,
            fill_opacity=0.3,
            resolution=(10, 10)
        )
        
        plane3 = Surface(
            lambda u, v: axes.c2p(v, u, 2 - u),
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_color=GREEN,
            fill_opacity=0.3,
            resolution=(10, 10)
        )
        
        self.play(Create(plane1))
        self.play(Create(plane2))
        self.play(Create(plane3))
        
        intersection = Sphere(radius=0.15, color=YELLOW)
        intersection.move_to(axes.c2p(1, 1, 1))
        
        self.play(Create(intersection))
        
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()


class InverseMatrixIntro(Scene):
    """逆矩阵概念介绍"""
    
    def construct(self):
        title = Text("逆矩阵：撤销变换", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        problem = MathTex(r"A\vec{x} = \vec{b}", font_size=48)
        problem.shift(UP * 1)
        self.play(Write(problem))
        
        question = Text("如何求 x？", font_size=32, color=YELLOW)
        question.next_to(problem, DOWN)
        self.play(Write(question))
        self.wait()
        
        solution = MathTex(
            r"A^{-1}A\vec{x} &= A^{-1}\vec{b}\\",
            r"I\vec{x} &= A^{-1}\vec{b}\\",
            r"\vec{x} &= A^{-1}\vec{b}",
            font_size=36
        ).shift(DOWN * 1)
        
        self.play(Write(solution))
        self.wait()
        
        box = SurroundingRectangle(solution[2], color=YELLOW)
        self.play(Create(box))
        self.wait(2)


class InverseMatrixGeometry(LinearTransformationScene):
    """逆矩阵的几何意义：逆变换"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("逆矩阵 = 逆变换", font_size=36)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        square = Square(side_length=1, color=YELLOW, fill_opacity=0.3)
        self.add_transformable_mobject(square)
        
        matrix_A = [[2, 1], [1, 1]]
        
        self.wait()
        self.apply_matrix(matrix_A)
        self.wait()
        
        matrix_A_inv = [[1, -1], [-1, 2]]
        
        self.apply_matrix(matrix_A_inv)
        self.wait(2)


class WhenInverseExists(Scene):
    """何时逆矩阵存在"""
    
    def construct(self):
        title = Text("逆矩阵何时存在？", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        conditions = VGroup(
            Text("逆矩阵存在的等价条件：", font_size=28, color=YELLOW),
            MathTex(r"\det(A) \neq 0", font_size=32),
            MathTex(r"\text{rank}(A) = n \text{ (满秩)}", font_size=32),
            MathTex(r"\text{列向量线性无关}", font_size=32),
            MathTex(r"A\vec{x} = \vec{0} \text{ 只有零解}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        conditions.shift(LEFT * 2)
        
        self.play(Write(conditions[0]))
        for i in range(1, 5):
            self.play(Write(conditions[i]))
            self.wait(0.5)
        
        self.wait()
        
        geo_title = Text("几何意义：", font_size=28, color=GREEN)
        geo_title.shift(RIGHT * 3 + UP * 1)
        
        geo_text = VGroup(
            Text("变换不会", font_size=24),
            Text("「压缩维度」", font_size=24, color=RED),
        ).arrange(DOWN)
        geo_text.next_to(geo_title, DOWN)
        
        self.play(Write(geo_title), Write(geo_text))
        self.wait(2)


class SingularMatrixDemo(LinearTransformationScene):
    """奇异矩阵：无法逆转的变换"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("奇异矩阵：投影到x轴 (det=0)", font_size=32)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        dots = VGroup(*[
            Dot(self.plane.c2p(x, y), color=YELLOW)
            for x, y in [(1, 1), (1, -1), (2, 0.5), (2, -0.5)]
        ])
        self.add_transformable_mobject(dots)
        
        self.wait()
        self.apply_matrix([[1, 0], [0, 0]])
        self.wait(2)


class PseudoInverseIntro(Scene):
    """伪逆的概念"""
    
    def construct(self):
        title = Text("伪逆：当逆不存在时", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        problem = VGroup(
            Text("超定方程组（方程比未知数多）：", font_size=28),
            MathTex(
                r"\begin{bmatrix} 1 & 1 \\ 2 & 1 \\ 3 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 2 \\ 3 \\ 5 \end{bmatrix}",
                font_size=32
            )
        ).arrange(DOWN)
        problem.shift(UP * 1)
        
        self.play(Write(problem))
        self.wait()
        
        no_solution = Text("通常无精确解！", font_size=32, color=RED)
        no_solution.next_to(problem, DOWN)
        self.play(Write(no_solution))
        self.wait()
        
        pseudo = VGroup(
            Text("伪逆给出「最优近似」：", font_size=28, color=GREEN),
            MathTex(r"\vec{x}^* = A^+ \vec{b}", font_size=36),
            Text("最小化 ‖Ax - b‖²", font_size=24, color=YELLOW)
        ).arrange(DOWN)
        pseudo.shift(DOWN * 1.5)
        
        self.play(Write(pseudo))
        self.wait(2)


class LeastSquaresVisualization(Scene):
    """最小二乘拟合可视化"""
    
    def construct(self):
        title = Text("最小二乘法：最优拟合直线", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 6, 1],
            x_length=7,
            y_length=5
        ).shift(DOWN * 0.5)
        
        self.play(Create(plane))
        
        points_data = [(1, 2.1), (2, 2.9), (3, 4.2), (4, 5.1)]
        dots = VGroup(*[
            Dot(plane.c2p(x, y), color=YELLOW, radius=0.1)
            for x, y in points_data
        ])
        
        self.play(Create(dots))
        
        best_line = plane.plot(
            lambda x: 1.03 * x + 0.95,
            x_range=[0, 4.5],
            color=GREEN,
            stroke_width=3
        )
        
        self.play(Create(best_line))
        
        residuals = VGroup()
        for x, y in points_data:
            y_pred = 1.03 * x + 0.95
            line = DashedLine(
                plane.c2p(x, y),
                plane.c2p(x, y_pred),
                color=RED,
                stroke_width=2
            )
            residuals.add(line)
        
        self.play(Create(residuals))
        
        formula = MathTex(
            r"\min_{\vec{x}} \|A\vec{x} - \vec{b}\|^2",
            font_size=32
        ).to_corner(UR)
        
        solution = MathTex(
            r"\vec{x}^* = (A^T A)^{-1} A^T \vec{b}",
            font_size=28,
            color=YELLOW
        ).next_to(formula, DOWN)
        
        self.play(Write(formula))
        self.play(Write(solution))
        self.wait(2)


class PseudoInverseFormula(Scene):
    """伪逆的计算公式"""
    
    def construct(self):
        title = Text("Moore-Penrose 伪逆", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        case1 = VGroup(
            Text("1. 超定（m > n，行多）：", font_size=28, color=BLUE),
            MathTex(r"A^+ = (A^T A)^{-1} A^T", font_size=32),
            Text("最小二乘解", font_size=22, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT)
        case1.shift(UP * 1 + LEFT * 2)
        
        case2 = VGroup(
            Text("2. 欠定（m < n，列多）：", font_size=28, color=GREEN),
            MathTex(r"A^+ = A^T (A A^T)^{-1}", font_size=32),
            Text("最小范数解", font_size=22, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT)
        case2.shift(DOWN * 1.5 + LEFT * 2)
        
        self.play(Write(case1))
        self.wait()
        self.play(Write(case2))
        self.wait()
        
        svd = VGroup(
            Text("通用方法：SVD分解", font_size=28, color=YELLOW),
            MathTex(r"A = U\Sigma V^T \Rightarrow A^+ = V\Sigma^+ U^T", font_size=32)
        ).arrange(DOWN)
        svd.shift(DOWN * 3.5)
        
        self.play(Write(svd))
        self.wait(2)


class WhyNotInvert(Scene):
    """为什么不直接求逆"""
    
    def construct(self):
        title = Text("工程实践：为什么不直接求逆？", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        problems = VGroup(
            Text("❌ 直接求 A⁻¹ 的问题：", font_size=28, color=RED),
            Text("• 计算代价高：O(n³)", font_size=24),
            Text("• 数值不稳定", font_size=24),
            Text("• 对奇异矩阵无能为力", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problems.shift(LEFT * 3 + UP * 0.5)
        
        solutions = VGroup(
            Text("✓ 更好的方法：", font_size=28, color=GREEN),
            Text("• LU分解：求解 Ax=b", font_size=24),
            Text("• QR分解：最小二乘", font_size=24),
            Text("• SVD：通用、稳定", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        solutions.shift(RIGHT * 3 + UP * 0.5)
        
        self.play(Write(problems))
        self.wait()
        self.play(Write(solutions))
        self.wait()
        
        code = Code(
            code_string="""# Python实践
import numpy as np

x = np.linalg.inv(A) @ b

x = np.linalg.solve(A, b)

x = np.linalg.lstsq(A, b)[0]""",
            language="python",
            background="window"
        ).scale(0.7).shift(DOWN * 2)
        
        self.play(Create(code))
        self.wait(2)


if __name__ == "__main__":
    print("线性方程组与逆矩阵动画脚本")
    print("运行示例: manim -pql linear_systems.py LinearSystemGeometry")
