"""
向量的几何直觉
- 向量不只是数组：方向与大小的理解
- 点积：投影与相似度
- 叉积：面积与法向量
- 向量范数：L1、L2、无穷范数

运行方式：
manim -pql vectors.py Scene名称
例如：manim -pql vectors.py VectorIntro
"""

from manim import *
import numpy as np


class VectorIntro(Scene):
    """向量的基本概念：从数组到几何对象"""
    
    def construct(self):
        title = Text("向量：不只是数组", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        array_text = MathTex(r"\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}")
        array_text.shift(LEFT * 4)
        self.play(Write(array_text))
        self.wait()
        
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=6,
            y_length=4,
            background_line_style={"stroke_opacity": 0.4}
        ).shift(RIGHT * 2)
        
        self.play(Create(plane))
        
        vector = Arrow(
            plane.c2p(0, 0), 
            plane.c2p(3, 2), 
            buff=0,
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(GrowArrow(vector))
        self.wait()
        
        magnitude_text = MathTex(r"|\vec{v}| = \sqrt{3^2 + 2^2} = \sqrt{13}")
        magnitude_text.next_to(array_text, DOWN, buff=0.5)
        
        direction_text = Text("方向：从原点指向 (3, 2)", font_size=24)
        direction_text.next_to(magnitude_text, DOWN, buff=0.3)
        
        self.play(Write(magnitude_text))
        self.play(Write(direction_text))
        self.wait()
        
        shift_text = Text("向量可以平移，本质不变", font_size=28, color=GREEN)
        shift_text.to_edge(DOWN)
        self.play(Write(shift_text))
        
        vector_copy = vector.copy().set_color(GREEN)
        self.play(vector_copy.animate.shift(RIGHT * 1 + UP * 1))
        self.wait()
        
        vector_copy2 = vector.copy().set_color(BLUE)
        self.play(vector_copy2.animate.shift(LEFT * 0.5 + DOWN * 0.5))
        self.wait(2)


class VectorAsDisplacement(Scene):
    """向量作为位移的理解"""
    
    def construct(self):
        title = Text("向量 = 位移", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        plane = NumberPlane(
            x_range=[-2, 6, 1],
            y_range=[-2, 5, 1],
            x_length=8,
            y_length=6
        )
        self.play(Create(plane))
        
        dot_start = Dot(plane.c2p(1, 1), color=BLUE, radius=0.15)
        label_start = Text("起点", font_size=24).next_to(dot_start, DOWN)
        
        self.play(Create(dot_start), Write(label_start))
        
        vector = Arrow(
            plane.c2p(1, 1),
            plane.c2p(4, 3),
            buff=0,
            color=YELLOW,
            stroke_width=5
        )
        
        vector_label = MathTex(r"\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}")
        vector_label.next_to(vector, UP)
        
        self.play(GrowArrow(vector), Write(vector_label))
        self.wait()
        
        dot_end = Dot(plane.c2p(4, 3), color=GREEN, radius=0.15)
        label_end = Text("终点", font_size=24).next_to(dot_end, UP)
        
        self.play(Create(dot_end), Write(label_end))
        
        explanation = Text(
            "向量描述的是「怎么走」，而不是「在哪里」",
            font_size=28,
            color=ORANGE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)


class DotProductIntro(Scene):
    """点积的几何意义"""
    
    def construct(self):
        title = Text("点积：投影与相似度", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        formula = MathTex(
            r"\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta",
            font_size=36
        )
        formula.next_to(title, DOWN)
        self.play(Write(formula))
        
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=6,
            y_length=4
        ).shift(DOWN * 0.5)
        
        self.play(Create(plane))
        
        vec_a = Arrow(plane.c2p(0, 0), plane.c2p(4, 0), buff=0, color=BLUE, stroke_width=4)
        vec_b = Arrow(plane.c2p(0, 0), plane.c2p(3, 2), buff=0, color=RED, stroke_width=4)
        
        label_a = MathTex(r"\vec{a}", color=BLUE).next_to(vec_a, DOWN)
        label_b = MathTex(r"\vec{b}", color=RED).next_to(vec_b, UP)
        
        self.play(GrowArrow(vec_a), Write(label_a))
        self.play(GrowArrow(vec_b), Write(label_b))
        
        angle = Angle(vec_a, vec_b, radius=0.8, color=YELLOW)
        angle_label = MathTex(r"\theta", color=YELLOW).next_to(angle, RIGHT, buff=0.1)
        
        self.play(Create(angle), Write(angle_label))
        self.wait()
        
        proj_point = plane.c2p(3, 0)
        proj_line = DashedLine(plane.c2p(3, 2), proj_point, color=GREEN)
        proj_vec = Arrow(plane.c2p(0, 0), proj_point, buff=0, color=GREEN, stroke_width=4)
        
        proj_label = Text("b在a上的投影", font_size=24, color=GREEN)
        proj_label.next_to(proj_vec, DOWN, buff=0.3)
        
        self.play(Create(proj_line))
        self.play(GrowArrow(proj_vec), Write(proj_label))
        self.wait(2)


class DotProductSimilarity(Scene):
    """点积衡量相似度 - 推荐系统应用"""
    
    def construct(self):
        title = Text("点积衡量相似度", font_size=42).to_edge(UP)
        subtitle = Text("推荐系统的核心思想", font_size=28, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait()
        
        user_text = Text("用户偏好:", font_size=28).shift(UP * 1.5 + LEFT * 4)
        user_vec = MathTex(
            r"\vec{u} = \begin{bmatrix} 0.8 \\ 0.6 \\ 0.1 \end{bmatrix}",
            font_size=32
        ).next_to(user_text, RIGHT)
        
        labels = VGroup(
            Text("动作", font_size=20),
            Text("科幻", font_size=20),
            Text("爱情", font_size=20)
        ).arrange(DOWN, buff=0.3).next_to(user_vec, RIGHT, buff=0.5)
        
        self.play(Write(user_text), Write(user_vec), Write(labels))
        self.wait()
        
        movie1_text = Text("电影A:", font_size=28).shift(DOWN * 0.5 + LEFT * 4)
        movie1_vec = MathTex(
            r"\vec{m_1} = \begin{bmatrix} 0.9 \\ 0.7 \\ 0.0 \end{bmatrix}",
            font_size=32
        ).next_to(movie1_text, RIGHT)
        
        movie2_text = Text("电影B:", font_size=28).shift(DOWN * 2 + LEFT * 4)
        movie2_vec = MathTex(
            r"\vec{m_2} = \begin{bmatrix} 0.1 \\ 0.2 \\ 0.9 \end{bmatrix}",
            font_size=32
        ).next_to(movie2_text, RIGHT)
        
        self.play(Write(movie1_text), Write(movie1_vec))
        self.play(Write(movie2_text), Write(movie2_vec))
        self.wait()
        
        calc1 = MathTex(
            r"\vec{u} \cdot \vec{m_1} = 0.8 \times 0.9 + 0.6 \times 0.7 + 0.1 \times 0.0 = 1.14",
            font_size=28,
            color=GREEN
        ).shift(RIGHT * 2 + UP * 0.5)
        
        calc2 = MathTex(
            r"\vec{u} \cdot \vec{m_2} = 0.8 \times 0.1 + 0.6 \times 0.2 + 0.1 \times 0.9 = 0.29",
            font_size=28,
            color=RED
        ).shift(RIGHT * 2 + DOWN * 1)
        
        self.play(Write(calc1))
        self.play(Write(calc2))
        self.wait()
        
        conclusion = Text("推荐电影A！（相似度更高）", font_size=32, color=YELLOW)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)


class DotProductAngleCases(Scene):
    """点积与角度的三种情况"""
    
    def construct(self):
        title = Text("点积与夹角的关系", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        cases = VGroup()
        
        plane1 = NumberPlane(
            x_range=[-1, 3, 1], y_range=[-1, 3, 1],
            x_length=3, y_length=3
        ).shift(LEFT * 4)
        vec1a = Arrow(plane1.c2p(0, 0), plane1.c2p(2, 0), buff=0, color=BLUE)
        vec1b = Arrow(plane1.c2p(0, 0), plane1.c2p(1.5, 1.5), buff=0, color=RED)
        label1 = Text("θ < 90°\n点积 > 0\n同向", font_size=20, color=GREEN)
        label1.next_to(plane1, DOWN)
        
        plane2 = NumberPlane(
            x_range=[-1, 3, 1], y_range=[-1, 3, 1],
            x_length=3, y_length=3
        )
        vec2a = Arrow(plane2.c2p(0, 0), plane2.c2p(2, 0), buff=0, color=BLUE)
        vec2b = Arrow(plane2.c2p(0, 0), plane2.c2p(0, 2), buff=0, color=RED)
        label2 = Text("θ = 90°\n点积 = 0\n垂直", font_size=20, color=YELLOW)
        label2.next_to(plane2, DOWN)
        
        plane3 = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-1, 3, 1],
            x_length=3, y_length=3
        ).shift(RIGHT * 4)
        vec3a = Arrow(plane3.c2p(0, 0), plane3.c2p(1.5, 0), buff=0, color=BLUE)
        vec3b = Arrow(plane3.c2p(0, 0), plane3.c2p(-1, 1.5), buff=0, color=RED)
        label3 = Text("θ > 90°\n点积 < 0\n反向", font_size=20, color=RED)
        label3.next_to(plane3, DOWN)
        
        self.play(Create(plane1), Create(plane2), Create(plane3))
        self.play(
            GrowArrow(vec1a), GrowArrow(vec1b),
            GrowArrow(vec2a), GrowArrow(vec2b),
            GrowArrow(vec3a), GrowArrow(vec3b)
        )
        self.play(Write(label1), Write(label2), Write(label3))
        self.wait(2)


class CrossProductIntro(ThreeDScene):
    """叉积的几何意义（3D）"""
    
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        title = Text("叉积：面积与法向量", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        axes = ThreeDAxes(
            x_range=[-1, 4, 1],
            y_range=[-1, 4, 1],
            z_range=[-1, 4, 1],
            x_length=5,
            y_length=5,
            z_length=5
        )
        self.play(Create(axes))
        
        vec_a = Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(2, 0, 0),
            color=BLUE
        )
        vec_b = Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(1, 2, 0),
            color=RED
        )
        
        self.play(Create(vec_a), Create(vec_b))
        self.wait()
        
        vec_cross = Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(0, 0, 3),
            color=GREEN
        )
        
        self.play(Create(vec_cross))
        
        parallelogram = Polygon(
            axes.c2p(0, 0, 0),
            axes.c2p(2, 0, 0),
            axes.c2p(3, 2, 0),
            axes.c2p(1, 2, 0),
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_color=YELLOW
        )
        
        self.play(Create(parallelogram))
        
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        formula = MathTex(
            r"\vec{a} \times \vec{b} = |\vec{a}||\vec{b}|\sin\theta \cdot \hat{n}",
            font_size=28
        )
        formula.to_corner(DR)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(2)


class CrossProduct2DArea(Scene):
    """2D中叉积计算平行四边形面积"""
    
    def construct(self):
        title = Text("叉积计算面积", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=5
        ).shift(DOWN * 0.5)
        
        self.play(Create(plane))
        
        vec_a = Arrow(plane.c2p(0, 0), plane.c2p(3, 0), buff=0, color=BLUE, stroke_width=4)
        vec_b = Arrow(plane.c2p(0, 0), plane.c2p(2, 2), buff=0, color=RED, stroke_width=4)
        
        label_a = MathTex(r"\vec{a} = (3, 0)", color=BLUE, font_size=28)
        label_a.next_to(vec_a, DOWN)
        label_b = MathTex(r"\vec{b} = (2, 2)", color=RED, font_size=28)
        label_b.next_to(vec_b, UL)
        
        self.play(GrowArrow(vec_a), Write(label_a))
        self.play(GrowArrow(vec_b), Write(label_b))
        
        parallelogram = Polygon(
            plane.c2p(0, 0),
            plane.c2p(3, 0),
            plane.c2p(5, 2),
            plane.c2p(2, 2),
            fill_color=YELLOW,
            fill_opacity=0.4,
            stroke_color=YELLOW
        )
        
        self.play(Create(parallelogram))
        
        formula = MathTex(
            r"|\vec{a} \times \vec{b}| = |a_x b_y - a_y b_x| = |3 \times 2 - 0 \times 2| = 6",
            font_size=28
        ).to_edge(DOWN)
        
        area_label = Text("面积 = 6", font_size=32, color=YELLOW)
        area_label.move_to(plane.c2p(2.5, 1))
        
        self.play(Write(formula))
        self.play(Write(area_label))
        self.wait(2)


class VectorNorms(Scene):
    """L1、L2、无穷范数的可视化"""
    
    def construct(self):
        title = Text("向量范数：度量「长度」的多种方式", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        vec_text = MathTex(r"\vec{v} = (3, 4)", font_size=32)
        vec_text.next_to(title, DOWN)
        self.play(Write(vec_text))
        
        plane_l2 = NumberPlane(
            x_range=[-1, 5, 1], y_range=[-1, 5, 1],
            x_length=3.5, y_length=3.5
        ).shift(LEFT * 4 + DOWN * 0.5)
        
        vec_l2 = Arrow(plane_l2.c2p(0, 0), plane_l2.c2p(3, 4), buff=0, color=YELLOW)
        circle = Circle(radius=plane_l2.c2p(5, 0)[0] - plane_l2.c2p(0, 0)[0], color=BLUE)
        circle.move_to(plane_l2.c2p(0, 0))
        
        l2_label = MathTex(r"\|v\|_2 = \sqrt{3^2+4^2} = 5", font_size=24)
        l2_label.next_to(plane_l2, DOWN)
        l2_title = Text("L2范数(欧氏)", font_size=20, color=BLUE)
        l2_title.next_to(l2_label, DOWN)
        
        plane_l1 = NumberPlane(
            x_range=[-1, 8, 1], y_range=[-1, 8, 1],
            x_length=3.5, y_length=3.5
        ).shift(DOWN * 0.5)
        
        vec_l1 = Arrow(plane_l1.c2p(0, 0), plane_l1.c2p(3, 4), buff=0, color=YELLOW)
        diamond = Polygon(
            plane_l1.c2p(7, 0), plane_l1.c2p(0, 7),
            plane_l1.c2p(-7, 0), plane_l1.c2p(0, -7),
            color=GREEN, stroke_width=2
        ).scale(0.25).move_to(plane_l1.c2p(0, 0))
        
        path_l1 = VGroup(
            Line(plane_l1.c2p(0, 0), plane_l1.c2p(3, 0), color=RED, stroke_width=3),
            Line(plane_l1.c2p(3, 0), plane_l1.c2p(3, 4), color=RED, stroke_width=3)
        )
        
        l1_label = MathTex(r"\|v\|_1 = |3|+|4| = 7", font_size=24)
        l1_label.next_to(plane_l1, DOWN)
        l1_title = Text("L1范数(曼哈顿)", font_size=20, color=GREEN)
        l1_title.next_to(l1_label, DOWN)
        
        plane_linf = NumberPlane(
            x_range=[-1, 5, 1], y_range=[-1, 5, 1],
            x_length=3.5, y_length=3.5
        ).shift(RIGHT * 4 + DOWN * 0.5)
        
        vec_linf = Arrow(plane_linf.c2p(0, 0), plane_linf.c2p(3, 4), buff=0, color=YELLOW)
        square = Square(side_length=2 * (plane_linf.c2p(4, 0)[0] - plane_linf.c2p(0, 0)[0]), color=PURPLE)
        square.move_to(plane_linf.c2p(0, 0))
        
        linf_label = MathTex(r"\|v\|_\infty = \max(|3|,|4|) = 4", font_size=24)
        linf_label.next_to(plane_linf, DOWN)
        linf_title = Text("L∞范数(最大值)", font_size=20, color=PURPLE)
        linf_title.next_to(linf_label, DOWN)
        
        self.play(Create(plane_l2), Create(plane_l1), Create(plane_linf))
        self.play(
            GrowArrow(vec_l2), GrowArrow(vec_l1), GrowArrow(vec_linf)
        )
        self.play(
            Create(circle), Create(path_l1), Create(square)
        )
        self.play(
            Write(l2_label), Write(l1_label), Write(linf_label)
        )
        self.play(
            Write(l2_title), Write(l1_title), Write(linf_title)
        )
        self.wait(2)


class NormApplications(Scene):
    """范数在机器学习中的应用"""
    
    def construct(self):
        title = Text("范数的实际应用", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        l1_box = VGroup(
            Text("L1 正则化 (Lasso)", font_size=28, color=GREEN),
            Text("• 产生稀疏解", font_size=22),
            Text("• 特征选择", font_size=22),
            Text("• 部分权重变为0", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        l1_box.shift(LEFT * 3 + UP * 0.5)
        
        l2_box = VGroup(
            Text("L2 正则化 (Ridge)", font_size=28, color=BLUE),
            Text("• 权重整体缩小", font_size=22),
            Text("• 防止过拟合", font_size=22),
            Text("• 权重趋近于0但不为0", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        l2_box.shift(RIGHT * 3 + UP * 0.5)
        
        self.play(Write(l1_box), Write(l2_box))
        self.wait()
        
        formula = MathTex(
            r"\text{Loss} = \text{MSE} + \lambda \|\vec{w}\|",
            font_size=32
        ).shift(DOWN * 2)
        
        self.play(Write(formula))
        self.wait(2)


if __name__ == "__main__":
    print("向量动画脚本")
    print("运行单个场景: manim -pql vectors.py VectorIntro")
    print("运行全部场景: manim -pql vectors.py")
