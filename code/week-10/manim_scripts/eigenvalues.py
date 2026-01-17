"""
Week 10 - Part 1: 特征值与特征向量
- Av = λv 的几何意义
- 特征向量只被拉伸不被旋转
- 单位圆变椭圆：特征方向就是长短轴
- PageRank应用
- 幂迭代法

运行方式：
manim -pql eigenvalues.py Scene名称
例如：manim -pql eigenvalues.py CircleToEllipse
"""

from manim import *
import numpy as np


# ============================================================
# Scene 1: 单位圆变椭圆
# ============================================================
class CircleToEllipse(Scene):
    """单位圆变椭圆，展示特征向量是长短轴方向"""

    def construct(self):
        title = Text("单位圆 → 椭圆：特征向量是主轴方向", font_size=36)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 矩阵 A = [[3, 0], [0, 2]]，特征值3和2
        # 特征向量是 (1,0) 和 (0,1)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            background_line_style={"stroke_opacity": 0.3}
        ).shift(DOWN * 0.5)
        self.play(Create(plane))

        # 单位圆
        circle = Circle(radius=1, color=BLUE, stroke_width=3)
        circle.move_to(plane.c2p(0, 0))
        circle_label = Text("单位圆", font_size=24, color=BLUE)
        circle_label.next_to(circle, UR)

        self.play(Create(circle), Write(circle_label))
        self.wait()

        # 特征向量
        eigen1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color=RED, stroke_width=4)
        eigen2 = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), buff=0, color=GREEN, stroke_width=4)

        eigen1_label = MathTex(r"\vec{v}_1", color=RED, font_size=28).next_to(eigen1, DOWN)
        eigen2_label = MathTex(r"\vec{v}_2", color=GREEN, font_size=28).next_to(eigen2, LEFT)

        self.play(
            GrowArrow(eigen1), Write(eigen1_label),
            GrowArrow(eigen2), Write(eigen2_label)
        )
        self.wait()

        # 变换信息
        matrix_info = MathTex(
            r"A = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}",
            r"\quad \lambda_1 = 3, \lambda_2 = 2",
            font_size=28
        ).to_edge(LEFT).shift(UP * 2.2)
        self.play(Write(matrix_info))

        # 变换后的椭圆和特征向量
        ellipse = Ellipse(width=6, height=4, color=YELLOW, stroke_width=3)
        ellipse.move_to(plane.c2p(0, 0))

        eigen1_new = Arrow(plane.c2p(0, 0), plane.c2p(3, 0), buff=0, color=RED, stroke_width=4)
        eigen2_new = Arrow(plane.c2p(0, 0), plane.c2p(0, 2), buff=0, color=GREEN, stroke_width=4)

        # 动画变换
        self.play(
            Transform(circle, ellipse),
            Transform(eigen1, eigen1_new),
            Transform(eigen2, eigen2_new),
            FadeOut(circle_label),
            run_time=2
        )

        ellipse_label = Text("椭圆", font_size=24, color=YELLOW)
        ellipse_label.next_to(ellipse, UR)
        self.play(Write(ellipse_label))

        # 解释
        explanation = VGroup(
            Text("• 特征向量方向 = 椭圆的主轴方向", font_size=24),
            Text("• 特征值大小 = 对应轴的长度", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation.to_edge(DOWN)

        self.play(Write(explanation))
        self.wait(2)


class EigenvectorVsNormal(Scene):
    """对比普通向量与特征向量的变换效果"""

    def construct(self):
        title = Text("普通向量 vs 特征向量", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 定义变换矩阵 A = [[2, 1], [1, 2]]
        # 特征值: 3, 1
        # 特征向量: (1,1), (1,-1)
        A = np.array([[2, 1], [1, 2]])

        # 左边：普通向量
        plane_left = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            background_line_style={"stroke_opacity": 0.3}
        ).shift(LEFT * 3.5 + DOWN * 0.3)

        label_left = Text("普通向量", font_size=24).next_to(plane_left, DOWN)

        # 普通向量 (1, 0)
        v_normal = np.array([1, 0])
        Av_normal = A @ v_normal  # = [2, 1]

        vec_normal = Arrow(
            plane_left.c2p(0, 0),
            plane_left.c2p(1, 0),
            buff=0,
            color=BLUE,
            stroke_width=4
        )
        vec_normal_transformed = Arrow(
            plane_left.c2p(0, 0),
            plane_left.c2p(2, 1),
            buff=0,
            color=RED,
            stroke_width=4
        )

        # 右边：特征向量
        plane_right = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            background_line_style={"stroke_opacity": 0.3}
        ).shift(RIGHT * 3.5 + DOWN * 0.3)

        label_right = Text("特征向量", font_size=24).next_to(plane_right, DOWN)

        # 特征向量 (1, 1) 归一化
        v_eigen = np.array([1, 1]) / np.sqrt(2)
        Av_eigen = A @ v_eigen  # = 3 * v_eigen

        vec_eigen = Arrow(
            plane_right.c2p(0, 0),
            plane_right.c2p(v_eigen[0], v_eigen[1]),
            buff=0,
            color=BLUE,
            stroke_width=4
        )
        vec_eigen_transformed = Arrow(
            plane_right.c2p(0, 0),
            plane_right.c2p(Av_eigen[0], Av_eigen[1]),
            buff=0,
            color=GREEN,
            stroke_width=4
        )

        # 动画
        self.play(Create(plane_left), Create(plane_right))
        self.play(Write(label_left), Write(label_right))

        self.play(GrowArrow(vec_normal), GrowArrow(vec_eigen))
        self.wait()

        # 展示变换
        transform_text = Text("应用矩阵变换 A", font_size=28, color=YELLOW)
        transform_text.shift(UP * 2.0)
        self.play(Write(transform_text))

        self.play(
            Transform(vec_normal.copy(), vec_normal_transformed),
            Transform(vec_eigen.copy(), vec_eigen_transformed)
        )
        self.play(
            GrowArrow(vec_normal_transformed),
            GrowArrow(vec_eigen_transformed)
        )
        self.wait()

        # 结论
        result_left = Text("方向改变了!", font_size=22, color=RED)
        result_left.next_to(plane_left, UP).shift(UP * 0.2)

        result_right = Text("方向没变,只是变长了3倍!", font_size=22, color=GREEN)
        result_right.next_to(plane_right, UP).shift(UP * 0.2)

        self.play(Write(result_left), Write(result_right))
        self.wait(2)


# ============================================================
# Scene 2: PageRank应用
# ============================================================
class PageRankIntro(Scene):
    """PageRank的基本思想"""

    def construct(self):
        title = Text("PageRank: 特征向量的商业奇迹", font_size=38)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 网页链接图
        # A <- B, A <- C, B <- D, C <- A, D <- B, D <- C

        # 节点位置
        pos_A = LEFT * 3.5 + UP * 0.5
        pos_B = RIGHT * 0.5 + UP * 0.5
        pos_C = LEFT * 3.5 + DOWN * 1.5
        pos_D = RIGHT * 0.5 + DOWN * 1.5

        # 创建节点
        nodes = VGroup()
        labels = VGroup()

        for name, pos, color in [
            ("A", pos_A, BLUE),
            ("B", pos_B, GREEN),
            ("C", pos_C, ORANGE),
            ("D", pos_D, PURPLE)
        ]:
            node = Circle(radius=0.4, color=color, fill_opacity=0.7)
            node.move_to(pos)
            label = Text(name, font_size=28, color=WHITE)
            label.move_to(pos)
            nodes.add(node)
            labels.add(label)

        self.play(Create(nodes), Write(labels))
        self.wait()

        # 创建链接箭头
        arrows = VGroup()
        # B -> A
        arrows.add(Arrow(pos_B + LEFT * 0.5, pos_A + RIGHT * 0.5, buff=0.1, color=GRAY))
        # C -> A
        arrows.add(Arrow(pos_C + UP * 0.5, pos_A + DOWN * 0.5, buff=0.1, color=GRAY))
        # D -> B
        arrows.add(Arrow(pos_D + UP * 0.5, pos_B + DOWN * 0.5, buff=0.1, color=GRAY))
        # A -> C
        arrows.add(Arrow(pos_A + DOWN * 0.5, pos_C + UP * 0.5, buff=0.1, color=GRAY))
        # B -> D (曲线)
        arrows.add(Arrow(pos_B + DOWN * 0.5, pos_D + UP * 0.5, buff=0.1, color=GRAY))
        # C -> D
        arrows.add(Arrow(pos_C + RIGHT * 0.5, pos_D + LEFT * 0.5, buff=0.1, color=GRAY))

        self.play(Create(arrows))
        self.wait()

        # 核心思想
        idea = VGroup(
            Text("核心思想:", font_size=28, color=YELLOW),
            Text("• 被重要网页链接的网页也重要", font_size=24),
            Text("• 重要性可以「传递」", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT)
        idea.to_edge(RIGHT).shift(RIGHT * 0.5 + DOWN * 0.8)

        self.play(Write(idea))
        self.wait(2)


class PowerIteration(Scene):
    """幂迭代法可视化"""

    def construct(self):
        title = Text("幂迭代法：找主特征向量", font_size=38)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 公式
        formula = MathTex(
            r"\vec{x}_{k+1} = \frac{A\vec{x}_k}{\|A\vec{x}_k\|}",
            font_size=36
        ).shift(UP * 2.2)
        self.play(Write(formula))

        # 矩阵 A
        A = np.array([[2, 1], [1, 2]])
        # 主特征向量是 (1, 1)/sqrt(2)，特征值为3

        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
            background_line_style={"stroke_opacity": 0.3}
        ).shift(DOWN * 0.8)

        self.play(Create(plane))

        # 初始向量
        x = np.array([1.0, 0.2])
        x = x / np.linalg.norm(x)

        # 目标特征向量
        target = np.array([1, 1]) / np.sqrt(2)
        target_arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(target[0], target[1]),
            buff=0,
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5
        )
        target_label = MathTex(r"\vec{v}_1", color=GREEN, font_size=24)
        target_label.next_to(target_arrow.get_end(), UR, buff=0.1)

        self.play(Create(target_arrow), Write(target_label))

        # 迭代过程
        current_arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(x[0], x[1]),
            buff=0,
            color=YELLOW,
            stroke_width=4
        )
        iteration_label = Text("k=0", font_size=24)
        iteration_label.to_corner(DR).shift(UP * 0.5)

        self.play(GrowArrow(current_arrow), Write(iteration_label))
        self.wait()

        # 进行几次迭代
        for k in range(1, 6):
            # 计算 Ax
            Ax = A @ x
            # 归一化
            x_new = Ax / np.linalg.norm(Ax)

            new_arrow = Arrow(
                plane.c2p(0, 0),
                plane.c2p(x_new[0], x_new[1]),
                buff=0,
                color=YELLOW,
                stroke_width=4
            )
            new_label = Text(f"k={k}", font_size=24)
            new_label.to_corner(DR).shift(UP * 0.5)

            self.play(
                Transform(current_arrow, new_arrow),
                Transform(iteration_label, new_label),
                run_time=0.8
            )

            x = x_new

        # 收敛说明
        converge_text = Text(
            "收敛到主特征向量！",
            font_size=28,
            color=GREEN
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(converge_text))
        self.wait(2)


# ============================================================
# Scene 3: 协方差矩阵的特征分解
# ============================================================
class CovarianceEigen(Scene):
    """协方差矩阵的特征分解与风险因子"""

    def construct(self):
        title = Text("协方差矩阵的特征分解", font_size=38)
        title.to_edge(UP).shift(DOWN * 0.1)
        subtitle = Text("发现隐藏的风险因子", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 数据点云
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_opacity": 0.2}
        ).shift(LEFT * 2 + DOWN * 0.5)

        self.play(Create(plane))

        # 生成椭圆分布的点
        np.random.seed(42)
        n_points = 30
        # 协方差矩阵
        cov = np.array([[2, 0.8], [0.8, 0.5]])
        points_data = np.random.multivariate_normal([0, 0], cov, n_points)

        dots = VGroup()
        for x, y in points_data:
            dot = Dot(plane.c2p(x, y), color=BLUE, radius=0.05)
            dots.add(dot)

        self.play(Create(dots))
        self.wait()

        # 特征向量（主成分方向）
        eigenvalues, eigenvectors = np.linalg.eig(cov)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # 第一主成分
        v1 = eigenvectors[:, 0] * np.sqrt(eigenvalues[0]) * 1.5
        pc1 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(v1[0], v1[1]),
            buff=0,
            color=RED,
            stroke_width=4
        )
        pc1_neg = Arrow(
            plane.c2p(0, 0),
            plane.c2p(-v1[0], -v1[1]),
            buff=0,
            color=RED,
            stroke_width=4
        )
        pc1_label = Text("PC1 (主风险方向)", font_size=20, color=RED)
        pc1_label.next_to(pc1.get_end(), UR, buff=0.1)

        # 第二主成分
        v2 = eigenvectors[:, 1] * np.sqrt(eigenvalues[1]) * 1.5
        pc2 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(v2[0], v2[1]),
            buff=0,
            color=GREEN,
            stroke_width=4
        )
        pc2_neg = Arrow(
            plane.c2p(0, 0),
            plane.c2p(-v2[0], -v2[1]),
            buff=0,
            color=GREEN,
            stroke_width=4
        )
        pc2_label = Text("PC2", font_size=20, color=GREEN)
        pc2_label.next_to(pc2.get_end(), UL, buff=0.1)

        self.play(
            GrowArrow(pc1), GrowArrow(pc1_neg), Write(pc1_label),
            GrowArrow(pc2), GrowArrow(pc2_neg), Write(pc2_label)
        )
        self.wait()

        # 右侧说明
        # First block
        info_eigen = VGroup(
            Text("特征值 = 方差", font_size=22, color=YELLOW),
            MathTex(r"\lambda_1 = " + f"{eigenvalues[0]:.2f}", font_size=24),
            MathTex(r"\lambda_2 = " + f"{eigenvalues[1]:.2f}", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        info_eigen.shift(RIGHT * 4 + UP * 1.5)

        # Second block below first
        info_variance = VGroup(
            Text("方差占比:", font_size=20, color=YELLOW),
            Text(f"PC1: {eigenvalues[0]/sum(eigenvalues)*100:.1f}%", font_size=18),
            Text(f"PC2: {eigenvalues[1]/sum(eigenvalues)*100:.1f}%", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        info_variance.shift(RIGHT * 4 + DOWN * 0.5)

        self.play(Write(info_eigen), Write(info_variance))
        self.wait()

        # 结论
        conclusion = Text(
            "风险主要集中在PC1方向！",
            font_size=26,
            color=ORANGE
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(conclusion))
        self.wait(2)


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    print("Week 10 - Part 1: 特征值与特征向量动画")
    print("运行示例: manim -pql eigenvalues.py CircleToEllipse")
    print("\n可用场景:")
    print("  - CircleToEllipse: 单位圆变椭圆")
    print("  - CovarianceEigen: 协方差矩阵特征分解")
    print("  - EigenvectorVsNormal: 普通向量vs特征向量")
    print("  - PageRankIntro: PageRank介绍")
    print("  - PowerIteration: 幂迭代法")
