"""
矩阵作为变换
- 矩阵乘法的本质：线性变换
- 旋转、缩放、剪切、投影的几何意义
- 矩阵乘法在神经网络中的角色

运行方式：
manim -pql matrix_transform.py Scene名称
"""

from manim import *
import numpy as np


class LinearTransformIntro(LinearTransformationScene):
    """展示矩阵如何变换整个空间"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("矩阵变换：[[2,1],[1,2]]", font_size=38)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        vectors = VGroup(
            self.get_vector([1, 0], color=YELLOW),
            self.get_vector([0, 1], color=ORANGE),
            self.get_vector([1, 1], color=PURPLE),
        )
        
        self.play(Create(vectors))
        self.wait()
        
        matrix = [[2, 1], [1, 2]]
        self.apply_matrix(matrix)
        self.wait(2)


class MatrixAsFunction(Scene):
    """矩阵作为函数的理解"""
    
    def construct(self):
        title = Text("矩阵：向量的函数", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        input_vec = MathTex(
            r"\vec{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}",
            font_size=36
        ).shift(LEFT * 4)
        
        matrix = MathTex(
            r"A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}",
            font_size=36
        )
        
        output_vec = MathTex(
            r"\vec{y} = \begin{bmatrix} ax_1 + bx_2 \\ cx_1 + dx_2 \end{bmatrix}",
            font_size=36
        ).shift(RIGHT * 4)
        
        arrow1 = Arrow(LEFT * 2.5, LEFT * 0.8, color=YELLOW)
        arrow2 = Arrow(RIGHT * 0.8, RIGHT * 2.5, color=YELLOW)
        
        self.play(Write(input_vec))
        self.play(GrowArrow(arrow1))
        self.play(Write(matrix))
        self.play(GrowArrow(arrow2))
        self.play(Write(output_vec))
        self.wait()
        
        simple = MathTex(r"\vec{y} = A\vec{x}", font_size=48, color=YELLOW)
        simple.shift(DOWN * 2)
        box = SurroundingRectangle(simple, color=YELLOW)
        
        self.play(Write(simple), Create(box))
        self.wait(2)


class BasisVectorTransform(LinearTransformationScene):
    """基向量决定了整个变换"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            i_hat_color=GREEN,
            j_hat_color=RED,
            **kwargs
        )
    
    def construct(self):
        title = Text("基向量决定变换", font_size=36)
        title.to_corner(UL)
        self.add_foreground_mobjects(title)
        
        self.wait()
        
        self.apply_matrix([[2, 0], [0, 1]])
        self.wait(2)


class ScalingTransform(LinearTransformationScene):
    """缩放变换"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("缩放变换", font_size=42)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        square = Square(side_length=1, color=YELLOW, fill_opacity=0.3)
        square.move_to(self.plane.c2p(1.5, 1.5))
        self.add_transformable_mobject(square)
        
        self.wait()
        self.apply_matrix([[2, 0], [0, 0.5]])
        self.wait(2)


class RotationTransform(LinearTransformationScene):
    """旋转变换"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("旋转变换 45°", font_size=42)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        theta = 45
        theta_rad = theta * DEGREES
        
        triangle = Triangle(color=YELLOW, fill_opacity=0.3)
        triangle.scale(0.8)
        triangle.move_to(self.plane.c2p(1.5, 1))
        self.add_transformable_mobject(triangle)
        
        self.wait()
        
        rotation_matrix = [
            [np.cos(theta_rad), -np.sin(theta_rad)],
            [np.sin(theta_rad), np.cos(theta_rad)]
        ]
        self.apply_matrix(rotation_matrix)
        self.wait(2)


class ShearTransform(LinearTransformationScene):
    """剪切变换"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("剪切变换（水平）", font_size=42)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        square = Square(side_length=1.5, color=YELLOW, fill_opacity=0.3)
        square.move_to(self.plane.c2p(1, 1))
        self.add_transformable_mobject(square)
        
        self.wait()
        self.apply_matrix([[1, 1], [0, 1]])
        self.wait(2)


class ProjectionTransform(LinearTransformationScene):
    """投影变换 - 降维"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("投影变换（投影到x轴）", font_size=38)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        dots = VGroup(*[
            Dot(self.plane.c2p(x, y), color=YELLOW)
            for x, y in [(1, 2), (2, 1), (-1, 1.5), (0.5, -1), (1.5, 0.5)]
        ])
        self.add_transformable_mobject(dots)
        
        self.wait()
        self.apply_matrix([[1, 0], [0, 0]])
        
        note = Text("2D → 1D：信息丢失！", font_size=28, color=RED)
        note.to_edge(DOWN)
        self.add_foreground_mobject(note)
        self.play(Write(note))
        self.wait(2)


class CompositeTransform(LinearTransformationScene):
    """复合变换：矩阵乘法的顺序"""
    
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            show_basis_vectors=True,
            **kwargs
        )
    
    def construct(self):
        title = Text("复合变换 = 矩阵相乘", font_size=36)
        title.to_corner(UL)
        self.add_foreground_mobject(title)
        
        square = Square(side_length=1, color=YELLOW, fill_opacity=0.3)
        square.move_to(self.plane.c2p(1, 0.5))
        self.add_transformable_mobject(square)
        
        self.wait()
        
        theta = 45 * DEGREES
        rot_matrix = [[np.cos(theta), -np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]]
        self.apply_matrix(rot_matrix)
        self.wait()
        
        scale_matrix = [[2, 0], [0, 0.5]]
        self.apply_matrix(scale_matrix)
        self.wait(2)


class NeuralNetworkMatrix(Scene):
    """神经网络中的矩阵运算"""
    
    def construct(self):
        title = Text("神经网络中的矩阵", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        input_neurons = VGroup(*[
            Circle(radius=0.3, color=BLUE, fill_opacity=0.5)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.5)
        input_neurons.shift(LEFT * 4)
        
        input_labels = VGroup(
            MathTex("x_1"), MathTex("x_2"), MathTex("x_3")
        )
        for label, neuron in zip(input_labels, input_neurons):
            label.next_to(neuron, LEFT)
        
        output_neurons = VGroup(*[
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5)
            for _ in range(2)
        ]).arrange(DOWN, buff=0.8)
        output_neurons.shift(RIGHT * 4)
        
        output_labels = VGroup(
            MathTex("y_1"), MathTex("y_2")
        )
        for label, neuron in zip(output_labels, output_neurons):
            label.next_to(neuron, RIGHT)
        
        connections = VGroup()
        for i_neuron in input_neurons:
            for o_neuron in output_neurons:
                line = Line(
                    i_neuron.get_right(),
                    o_neuron.get_left(),
                    color=GRAY,
                    stroke_width=1
                )
                connections.add(line)
        
        self.play(Create(input_neurons), Write(input_labels))
        self.play(Create(connections))
        self.play(Create(output_neurons), Write(output_labels))
        self.wait()
        
        matrix_text = MathTex(
            r"W = \begin{bmatrix} w_{11} & w_{12} & w_{13} \\ w_{21} & w_{22} & w_{23} \end{bmatrix}",
            font_size=32
        )
        matrix_text.shift(DOWN * 2)
        
        operation = MathTex(
            r"\vec{y} = W\vec{x} + \vec{b}",
            font_size=36,
            color=YELLOW
        )
        operation.next_to(matrix_text, DOWN)
        
        self.play(Write(matrix_text))
        self.play(Write(operation))
        self.wait(2)


class MatrixMultiplicationVisualized(Scene):
    """矩阵乘法的可视化理解"""
    
    def construct(self):
        title = Text("矩阵乘法：行与列的点积", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        matA = MathTex(
            r"A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}",
            font_size=36
        ).shift(LEFT * 4 + UP * 1)
        
        matB = MathTex(
            r"B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}",
            font_size=36
        ).shift(UP * 1)
        
        matC = MathTex(
            r"C = \begin{bmatrix} ? & ? \\ ? & ? \end{bmatrix}",
            font_size=36
        ).shift(RIGHT * 4 + UP * 1)
        
        self.play(Write(matA), Write(matB), Write(matC))
        self.wait()
        
        calc1 = MathTex(
            r"C_{11} = \begin{bmatrix} 1 & 2 \end{bmatrix} \cdot \begin{bmatrix} 5 \\ 7 \end{bmatrix} = 1 \times 5 + 2 \times 7 = 19",
            font_size=28,
            color=YELLOW
        ).shift(DOWN * 1)
        
        self.play(Write(calc1))
        self.wait()
        
        calc2 = MathTex(
            r"C_{12} = \begin{bmatrix} 1 & 2 \end{bmatrix} \cdot \begin{bmatrix} 6 \\ 8 \end{bmatrix} = 1 \times 6 + 2 \times 8 = 22",
            font_size=28,
            color=GREEN
        ).shift(DOWN * 2)
        
        self.play(Write(calc2))
        self.wait()
        
        final = MathTex(
            r"C = \begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}",
            font_size=36
        ).shift(DOWN * 3)
        
        self.play(Transform(matC, final.copy().shift(RIGHT * 4 + UP * 4)))
        self.play(Write(final))
        self.wait(2)


class TransformationGallery(Scene):
    """变换效果画廊"""
    
    def construct(self):
        title = Text("常见变换一览", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        transforms = [
            ("单位矩阵", [[1, 0], [0, 1]], "不变"),
            ("缩放", [[2, 0], [0, 2]], "均匀放大"),
            ("旋转90°", [[0, -1], [1, 0]], "逆时针"),
            ("水平翻转", [[-1, 0], [0, 1]], "镜像"),
            ("剪切", [[1, 0.5], [0, 1]], "倾斜"),
            ("投影", [[1, 0], [0, 0]], "降维"),
        ]
        
        grid = VGroup()
        for i, (name, matrix, desc) in enumerate(transforms):
            plane = NumberPlane(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=2,
                y_length=2,
                background_line_style={"stroke_opacity": 0.3}
            )
            
            square = Square(side_length=0.8, color=BLUE, fill_opacity=0.3)
            
            matrix_np = np.array(matrix)
            transformed_points = []
            for corner in [[-0.4, -0.4], [0.4, -0.4], [0.4, 0.4], [-0.4, 0.4]]:
                new_point = matrix_np @ np.array(corner)
                transformed_points.append([new_point[0], new_point[1], 0])
            
            transformed = Polygon(*transformed_points, color=YELLOW, fill_opacity=0.3)
            
            label = Text(name, font_size=18)
            label.next_to(plane, DOWN, buff=0.1)
            
            group = VGroup(plane, square, transformed, label)
            grid.add(group)
        
        grid.arrange_in_grid(rows=2, cols=3, buff=0.5)
        grid.shift(DOWN * 0.3)
        
        self.play(Create(grid), run_time=3)
        self.wait(3)


if __name__ == "__main__":
    print("矩阵变换动画脚本")
    print("运行示例: manim -pql matrix_transform.py RotationTransform")
