"""
行列式与秩
- 行列式：变换后的体积缩放比（含正负号的意义）
- 秩：信息的有效维度
- 满秩、降秩与线性相关性
- 为什么低秩矩阵在推荐系统和压缩中很重要

运行方式：
manim -pql determinant_rank.py Scene名称
"""

from manim import *
import numpy as np


class DeterminantAsArea(Scene):
    """2D行列式：面积的缩放"""
    
    def construct(self):
        title = Text("行列式 = 面积缩放因子", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        plane = NumberPlane(
            x_range=[-1, 4, 1],
            y_range=[-1, 4, 1],
            x_length=5,
            y_length=5
        ).shift(LEFT * 2)
        
        self.play(Create(plane))
        
        unit_square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE
        )
        
        area1 = Text("面积 = 1", font_size=28, color=BLUE)
        area1.move_to(plane.c2p(0.5, 0.5))
        
        self.play(Create(unit_square), Write(area1))
        self.wait()
        
        matrix_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}",
            font_size=32
        ).shift(RIGHT * 3 + UP * 2)
        
        det_tex = MathTex(
            r"\det(A) = 2 \times 3 - 1 \times 0 = 6",
            font_size=28
        ).next_to(matrix_tex, DOWN)
        
        self.play(Write(matrix_tex), Write(det_tex))
        self.wait()
        
        transformed = Polygon(
            plane.c2p(0, 0),
            plane.c2p(2, 0),
            plane.c2p(3, 3),
            plane.c2p(1, 3),
            fill_color=YELLOW,
            fill_opacity=0.5,
            stroke_color=YELLOW
        )
        
        area2 = Text("面积 = 6", font_size=28, color=YELLOW)
        area2.move_to(plane.c2p(1.5, 1.5))
        
        self.play(
            Transform(unit_square, transformed),
            Transform(area1, area2)
        )
        self.wait()
        
        conclusion = Text(
            "新面积 = |det(A)| × 原面积",
            font_size=32,
            color=GREEN
        ).to_edge(DOWN)
        
        self.play(Write(conclusion))
        self.wait(2)


class DeterminantSign(LinearTransformationScene):
    """行列式的符号：方向的翻转"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("行列式符号：方向翻转", font_size=36)
        title.to_corner(UL)
        self.add(title)
        
        info = VGroup(
            Text("det > 0: 保持方向", font_size=24, color=GREEN),
            Text("det < 0: 翻转方向", font_size=24, color=RED),
        ).arrange(DOWN)
        info.to_corner(UR)
        self.add(info)
        
        square = Square(side_length=1, color=YELLOW, fill_opacity=0.3)
        square.move_to(self.plane.c2p(1, 0.5))
        self.add_transformable_mobject(square)
        
        arrow = CurvedArrow(
            self.plane.c2p(1.6, 0.8),
            self.plane.c2p(1.6, 0.2),
            color=GREEN
        )
        self.add_transformable_mobject(arrow)
        
        self.wait()
        
        flip_matrix = [[-1, 0], [0, 1]]
        
        step = MathTex(r"\det = -1", font_size=28, color=RED)
        step.to_edge(DOWN)
        self.add(step)
        
        self.apply_matrix(flip_matrix)
        self.wait(2)


class DeterminantZero(LinearTransformationScene):
    """行列式为零：降维"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("det = 0：空间被压缩", font_size=36)
        title.to_corner(UL)
        self.add(title)
        
        matrix_tex = MathTex(
            r"\begin{bmatrix} 2 & 1 \\ 4 & 2 \end{bmatrix}",
            r"\det = 2 \times 2 - 1 \times 4 = 0",
            font_size=24
        )
        matrix_tex.to_corner(UR)
        self.add(matrix_tex)
        
        dots = VGroup(*[
            Dot(self.plane.c2p(x, y), color=YELLOW)
            for x, y in [(0.5, 0.5), (1, 1), (0.5, 1.5), (1.5, 0.5), (1, 0)]
        ])
        self.add_transformable_mobject(dots)
        
        self.wait()
        
        singular_matrix = [[2, 1], [4, 2]]
        self.apply_matrix(singular_matrix)
        
        note = Text("2D平面 → 1D直线", font_size=28, color=RED)
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)


class Determinant3D(ThreeDScene):
    """3D行列式：体积缩放"""
    
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        title = Text("3D行列式 = 体积缩放", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        axes = ThreeDAxes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            z_range=[-1, 3, 1],
            x_length=4,
            y_length=4,
            z_length=4
        )
        self.play(Create(axes))
        
        cube = Cube(side_length=1, fill_opacity=0.3, fill_color=BLUE)
        cube.move_to(axes.c2p(0.5, 0.5, 0.5))
        
        self.play(Create(cube))
        
        vol_label = MathTex(r"V = 1", font_size=28)
        vol_label.to_corner(UR)
        self.add_fixed_in_frame_mobjects(vol_label)
        
        self.wait()
        
        new_vol_label = MathTex(r"V = 2 \times 1.5 \times 1 = 3", font_size=28).to_corner(UR)
        self.add_fixed_in_frame_mobjects(new_vol_label)
        self.play(
            cube.animate.apply_matrix([[2, 0, 0], [0, 1.5, 0], [0, 0, 1]]),
            Transform(vol_label, new_vol_label)
        )
        
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class RankIntro(Scene):
    """秩的直观理解"""
    
    def construct(self):
        title = Text("秩：信息的有效维度", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        definition = VGroup(
            Text("秩 = 矩阵中「真正独立」的行/列数", font_size=28),
            Text("= 线性变换的输出空间维度", font_size=28, color=YELLOW),
        ).arrange(DOWN)
        definition.shift(UP * 1)
        
        self.play(Write(definition))
        self.wait()
        
        example1 = VGroup(
            MathTex(
                r"A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}",
                font_size=32
            ),
            Text("rank(A) = 2", font_size=28, color=GREEN),
            Text("满秩", font_size=24, color=GREEN)
        ).arrange(DOWN)
        example1.shift(LEFT * 3 + DOWN * 1.5)
        
        example2 = VGroup(
            MathTex(
                r"B = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}",
                font_size=32
            ),
            Text("rank(B) = 1", font_size=28, color=RED),
            Text("降秩（第二行=2×第一行）", font_size=24, color=RED)
        ).arrange(DOWN)
        example2.shift(RIGHT * 3 + DOWN * 1.5)
        
        self.play(Write(example1))
        self.play(Write(example2))
        self.wait(2)


class RankVisualization(LinearTransformationScene):
    """秩的几何可视化"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("秩 = 输出空间的维度", font_size=36)
        title.to_corner(UL)
        self.add(title)
        
        dots = VGroup(*[
            Dot(self.plane.c2p(x, y), color=YELLOW, radius=0.05)
            for x in np.arange(-2, 2.5, 0.5)
            for y in np.arange(-2, 2.5, 0.5)
        ])
        self.add_transformable_mobject(dots)
        
        info1 = Text("rank = 2: 输出是2D", font_size=24)
        info1.to_corner(UR)
        self.add(info1)
        
        self.wait()
        self.apply_matrix([[1, 1], [0, 1]])
        self.wait(2)


class LinearDependence(Scene):
    """线性相关与线性无关"""
    
    def construct(self):
        title = Text("线性相关 vs 线性无关", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        plane1 = NumberPlane(
            x_range=[-2, 3, 1], y_range=[-2, 3, 1],
            x_length=4, y_length=4
        ).shift(LEFT * 3)
        
        vec1a = Arrow(plane1.c2p(0, 0), plane1.c2p(2, 0), buff=0, color=BLUE, stroke_width=4)
        vec1b = Arrow(plane1.c2p(0, 0), plane1.c2p(0, 2), buff=0, color=RED, stroke_width=4)
        
        label1 = Text("线性无关", font_size=24, color=GREEN)
        label1.next_to(plane1, DOWN)
        sublabel1 = Text("能张成整个2D平面", font_size=18, color=GRAY)
        sublabel1.next_to(label1, DOWN, buff=0.1)
        
        plane2 = NumberPlane(
            x_range=[-2, 3, 1], y_range=[-2, 3, 1],
            x_length=4, y_length=4
        ).shift(RIGHT * 3)
        
        vec2a = Arrow(plane2.c2p(0, 0), plane2.c2p(2, 1), buff=0, color=BLUE, stroke_width=4)
        vec2b = Arrow(plane2.c2p(0, 0), plane2.c2p(1, 0.5), buff=0, color=RED, stroke_width=4)
        
        label2 = Text("线性相关", font_size=24, color=RED)
        label2.next_to(plane2, DOWN)
        sublabel2 = Text("只能张成一条直线", font_size=18, color=GRAY)
        sublabel2.next_to(label2, DOWN, buff=0.1)
        
        self.play(Create(plane1), Create(plane2))
        self.play(
            GrowArrow(vec1a), GrowArrow(vec1b),
            GrowArrow(vec2a), GrowArrow(vec2b)
        )
        self.play(
            Write(label1), Write(sublabel1),
            Write(label2), Write(sublabel2)
        )
        self.wait(2)


class LowRankApproximation(Scene):
    """低秩近似：压缩的核心"""
    
    def construct(self):
        title = Text("低秩近似：数据压缩的秘密", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        original = VGroup(
            Text("原始矩阵 (1000×1000)", font_size=24),
            MathTex(r"A \in \mathbb{R}^{1000 \times 1000}", font_size=28),
            Text("存储：1,000,000 个数", font_size=20, color=GRAY)
        ).arrange(DOWN)
        original.shift(LEFT * 4 + UP * 0.5)
        
        self.play(Write(original))
        self.wait()
        
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=YELLOW)
        arrow_label = Text("低秩近似", font_size=24, color=YELLOW)
        arrow_label.next_to(arrow, UP)
        
        self.play(GrowArrow(arrow), Write(arrow_label))
        
        decomposed = VGroup(
            Text("秩-r 近似", font_size=24),
            MathTex(r"A \approx UV^T", font_size=28),
            MathTex(r"U \in \mathbb{R}^{1000 \times r}, V \in \mathbb{R}^{1000 \times r}", font_size=22),
            Text("存储：2000r 个数", font_size=20, color=GREEN)
        ).arrange(DOWN)
        decomposed.shift(RIGHT * 4 + UP * 0.5)
        
        self.play(Write(decomposed))
        self.wait()
        
        ratio = VGroup(
            Text("如果 r = 50：", font_size=24),
            Text("压缩比 = 1,000,000 / 100,000 = 10×", font_size=28, color=GREEN)
        ).arrange(DOWN)
        ratio.shift(DOWN * 2)
        
        self.play(Write(ratio))
        self.wait(2)


class ImageCompression(Scene):
    """图像压缩示例"""
    
    def construct(self):
        title = Text("SVD图像压缩", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        
        original = VGroup(
            Rectangle(width=2, height=2, fill_color=BLUE, fill_opacity=0.8),
            Text("原图", font_size=20),
            Text("秩 = 100", font_size=16, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        original.shift(LEFT * 4)
        
        rank50 = VGroup(
            Rectangle(width=2, height=2, fill_color=BLUE, fill_opacity=0.7),
            Text("秩-50", font_size=20),
            Text("质量 95%", font_size=16, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        rank50.shift(LEFT * 1.3)
        
        rank20 = VGroup(
            Rectangle(width=2, height=2, fill_color=BLUE, fill_opacity=0.5),
            Text("秩-20", font_size=20),
            Text("质量 85%", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.2)
        rank20.shift(RIGHT * 1.3)
        
        rank5 = VGroup(
            Rectangle(width=2, height=2, fill_color=BLUE, fill_opacity=0.2),
            Text("秩-5", font_size=20),
            Text("质量 60%", font_size=16, color=RED)
        ).arrange(DOWN, buff=0.2)
        rank5.shift(RIGHT * 4)
        
        self.play(Create(original))
        self.play(Create(rank50))
        self.play(Create(rank20))
        self.play(Create(rank5))
        
        note = Text("保留最重要的r个奇异值，丢弃其余", font_size=24, color=YELLOW)
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)


class RecommendationSystem(Scene):
    """推荐系统中的低秩假设"""
    
    def construct(self):
        title = Text("推荐系统：用户-物品矩阵", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        matrix_visual = VGroup()
        
        header_row = VGroup(
            Text("", font_size=18),
            Text("电影1", font_size=18),
            Text("电影2", font_size=18),
            Text("电影3", font_size=18),
            Text("...", font_size=18),
        ).arrange(RIGHT, buff=0.3)
        
        row1 = VGroup(
            Text("用户A", font_size=18),
            Text("5", font_size=18, color=GREEN),
            Text("?", font_size=18, color=RED),
            Text("4", font_size=18, color=GREEN),
            Text("...", font_size=18),
        ).arrange(RIGHT, buff=0.3)
        
        row2 = VGroup(
            Text("用户B", font_size=18),
            Text("?", font_size=18, color=RED),
            Text("3", font_size=18, color=GREEN),
            Text("?", font_size=18, color=RED),
            Text("...", font_size=18),
        ).arrange(RIGHT, buff=0.3)
        
        row3 = VGroup(
            Text("用户C", font_size=18),
            Text("4", font_size=18, color=GREEN),
            Text("4", font_size=18, color=GREEN),
            Text("?", font_size=18, color=RED),
            Text("...", font_size=18),
        ).arrange(RIGHT, buff=0.3)
        
        matrix_visual = VGroup(header_row, row1, row2, row3)
        matrix_visual.arrange(DOWN, buff=0.2)
        matrix_visual.shift(UP * 1)
        
        self.play(Write(matrix_visual))
        self.wait()
        
        assumption = VGroup(
            Text("核心假设：用户偏好由少数「隐因子」决定", font_size=24),
            MathTex(r"R \approx U \times V^T", font_size=32),
            Text("U: 用户-隐因子    V: 物品-隐因子", font_size=20, color=GRAY)
        ).arrange(DOWN)
        assumption.shift(DOWN * 1.5)
        
        self.play(Write(assumption))
        self.wait()
        
        prediction = Text("填补 ? = 预测评分！", font_size=28, color=YELLOW)
        prediction.to_edge(DOWN)
        self.play(Write(prediction))
        self.wait(2)


class RankSummary(Scene):
    """秩的总结"""
    
    def construct(self):
        title = Text("秩的关键要点", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        points = VGroup(
            VGroup(
                Text("1. 秩 = 有效信息维度", font_size=28, color=BLUE),
                Text("矩阵中真正独立的行/列数", font_size=22, color=GRAY),
            ).arrange(DOWN, aligned_edge=LEFT),
            
            VGroup(
                Text("2. 满秩 ⟺ 可逆", font_size=28, color=GREEN),
                Text("rank(A) = n ⟺ det(A) ≠ 0", font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT),
            
            VGroup(
                Text("3. 低秩 = 冗余/压缩机会", font_size=28, color=YELLOW),
                Text("推荐系统、图像压缩、降噪", font_size=22, color=GRAY),
            ).arrange(DOWN, aligned_edge=LEFT),
            
            VGroup(
                Text("4. 矩阵分解利用低秩结构", font_size=28, color=PURPLE),
                Text("A ≈ UVᵀ (秩-r近似)", font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        points.shift(DOWN * 0.3)
        
        for point in points:
            self.play(Write(point))
            self.wait(0.5)
        
        self.wait(2)


if __name__ == "__main__":
    print("行列式与秩动画脚本")
    print("运行示例: manim -pql determinant_rank.py DeterminantAsArea")
