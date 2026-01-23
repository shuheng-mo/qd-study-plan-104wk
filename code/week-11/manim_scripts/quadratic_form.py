"""
二次型可视化动画
展示 w^T Σ w 的几何意义和特征向量方向
"""
from manim import *
import numpy as np

class QuadraticFormVisualization(Scene):
    def construct(self):
        # 标题
        title = Text("二次型的几何意义", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.3)

        x_label = MathTex("w_1").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("w_2").next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 协方差矩阵
        Sigma = np.array([[2, 1], [1, 3]])
        eigenvalues, eigenvectors = np.linalg.eigh(Sigma)

        # 公式
        formula = MathTex(r"\Sigma = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}", font_size=28)
        formula.to_corner(UR).shift(DOWN * 0.5)
        self.play(Write(formula))

        # 绘制等高线 w^T Σ w = c
        contours = VGroup()
        for level in [1, 2, 4, 6, 8]:
            # 椭圆的参数需要从特征值计算
            # w^T Σ w = level 定义了一个椭圆
            # 在特征向量坐标系下，这是 λ1*u1^2 + λ2*u2^2 = level
            points = []
            for theta in np.linspace(0, 2*np.pi, 100):
                # 在特征向量坐标系下的点
                r1 = np.sqrt(level / eigenvalues[0])
                r2 = np.sqrt(level / eigenvalues[1])
                u = np.array([r1 * np.cos(theta), r2 * np.sin(theta)])
                # 转换回原坐标系
                w = eigenvectors @ u
                points.append(axes.c2p(*w))

            ellipse = VMobject(color=BLUE, stroke_width=1.5, stroke_opacity=0.6)
            ellipse.set_points_smoothly(points + [points[0]])
            contours.add(ellipse)

        self.play(Create(contours), run_time=2)

        # 绘制特征向量
        colors = [RED, GREEN]
        eigenvector_arrows = VGroup()
        eigenvector_labels = VGroup()

        for i, (val, vec) in enumerate(zip(eigenvalues, eigenvectors.T)):
            # 正向箭头
            arrow = Arrow(
                axes.c2p(0, 0),
                axes.c2p(*(vec * 2)),
                color=colors[i],
                buff=0,
                stroke_width=4
            )
            # 反向箭头
            arrow_neg = Arrow(
                axes.c2p(0, 0),
                axes.c2p(*(-vec * 2)),
                color=colors[i],
                buff=0,
                stroke_width=4
            )

            label = MathTex(rf"\lambda_{i+1}={val:.1f}", font_size=24, color=colors[i])
            label.next_to(arrow, RIGHT if vec[0] > 0 else LEFT)

            eigenvector_arrows.add(arrow, arrow_neg)
            eigenvector_labels.add(label)

        self.play(Create(eigenvector_arrows), run_time=1.5)
        self.play(Write(eigenvector_labels))

        # 说明文字
        explanation = VGroup(
            Text("特征向量 = 主轴方向", font_size=24),
            Text("特征值 = 该方向的方差", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DL)

        self.play(Write(explanation))

        # 动画：旋转向量显示不同方向的风险
        rotating_arrow = Arrow(
            axes.c2p(0, 0),
            axes.c2p(1.5, 0),
            color=YELLOW,
            buff=0,
            stroke_width=3
        )

        # 风险值显示
        risk_text = Text("方差: ", font_size=24).to_edge(DOWN).shift(UP * 0.5)
        risk_value = DecimalNumber(Sigma[0, 0], num_decimal_places=2, font_size=24)
        risk_value.next_to(risk_text, RIGHT)
        risk_group = VGroup(risk_text, risk_value)

        self.play(Create(rotating_arrow), Write(risk_group))

        # 旋转一圈
        def update_arrow(mob, alpha):
            theta = alpha * 2 * np.pi
            w = np.array([np.cos(theta), np.sin(theta)])
            risk = w @ Sigma @ w
            end_point = axes.c2p(*(w * 1.5))
            mob.put_start_and_end_on(axes.c2p(0, 0), end_point)

        def update_risk(mob):
            # 获取当前箭头方向
            end = rotating_arrow.get_end()
            start = rotating_arrow.get_start()
            direction = end - start
            w = np.array([direction[0], direction[1]])
            w = w / np.linalg.norm(w)
            # 转换回数据坐标
            w_data = np.array([
                w[0] * 6 / axes.x_length,
                w[1] * 6 / axes.y_length
            ])
            w_data = w_data / np.linalg.norm(w_data)
            risk = w_data @ Sigma @ w_data
            mob.set_value(risk)

        risk_value.add_updater(update_risk)

        self.play(
            UpdateFromAlphaFunc(rotating_arrow, update_arrow),
            run_time=4,
            rate_func=linear
        )

        risk_value.remove_updater(update_risk)

        self.wait(2)


class QuadraticFormSimple(Scene):
    """简化版，适合GIF"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
        )

        # 协方差矩阵
        Sigma = np.array([[2, 1], [1, 3]])
        eigenvalues, eigenvectors = np.linalg.eigh(Sigma)

        # 等高线
        contours = VGroup()
        for level in [1, 2, 4, 6]:
            points = []
            for theta in np.linspace(0, 2*np.pi, 100):
                r1 = np.sqrt(level / eigenvalues[0])
                r2 = np.sqrt(level / eigenvalues[1])
                u = np.array([r1 * np.cos(theta), r2 * np.sin(theta)])
                w = eigenvectors @ u
                points.append(axes.c2p(*w))
            ellipse = VMobject(color=BLUE, stroke_width=2, stroke_opacity=0.6)
            ellipse.set_points_smoothly(points + [points[0]])
            contours.add(ellipse)

        self.add(axes, contours)

        # 标题
        title = MathTex(r"w^T \Sigma w", font_size=36).to_edge(UP)
        self.add(title)

        # 特征向量
        colors = [RED, GREEN]
        for i, (val, vec) in enumerate(zip(eigenvalues, eigenvectors.T)):
            arrow = Arrow(axes.c2p(0, 0), axes.c2p(*(vec * 2)), color=colors[i], buff=0, stroke_width=4)
            arrow_neg = Arrow(axes.c2p(0, 0), axes.c2p(*(-vec * 2)), color=colors[i], buff=0, stroke_width=4)
            self.add(arrow, arrow_neg)

        # 旋转向量动画
        rotating_arrow = Arrow(axes.c2p(0, 0), axes.c2p(1.5, 0), color=YELLOW, buff=0, stroke_width=4)
        self.add(rotating_arrow)

        def update_arrow(mob, alpha):
            theta = alpha * 2 * np.pi
            w = np.array([np.cos(theta), np.sin(theta)])
            end_point = axes.c2p(*(w * 1.5))
            mob.put_start_and_end_on(axes.c2p(0, 0), end_point)

        self.play(
            UpdateFromAlphaFunc(rotating_arrow, update_arrow),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)
