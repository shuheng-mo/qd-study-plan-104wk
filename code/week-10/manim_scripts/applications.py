"""
Week 10 - Part 3: 实战应用
- 推荐系统：矩阵分解
- 投资组合优化：Markowitz模型
- 有效前沿

运行方式：
manim -pql applications.py Scene名称
例如：manim -pql applications.py RecommendationMatrix
"""

from manim import *
import numpy as np


# ============================================================
# Scene 1: 推荐系统 - 矩阵分解
# ============================================================
class RecommendationMatrix(Scene):
    """用户-商品评分矩阵"""

    def construct(self):
        title = Text("推荐系统：用户-商品矩阵", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 评分矩阵 - 左侧，使用简单直接的定位
        matrix_content = [
            ["", "电影1", "电影2", "电影3", "电影4"],
            ["Alice", "5", "3", "?", "1"],
            ["Bob", "4", "?", "?", "1"],
            ["Carol", "1", "1", "?", "5"],
            ["Dave", "?", "?", "4", "4"],
        ]

        table = VGroup()
        for i, row in enumerate(matrix_content):
            row_group = VGroup()
            for j, cell in enumerate(row):
                if cell == "?":
                    text = Text(cell, font_size=24, color=RED)
                elif i == 0 or j == 0:
                    text = Text(cell, font_size=22, color=YELLOW if i == 0 else BLUE)
                else:
                    text = Text(cell, font_size=24)

                # 简单定位：从原点出发
                text.move_to(np.array([j * 1.2 - 2.4, 1.2 - i * 0.7, 0]))
                row_group.add(text)
            table.add(row_group)
        
        # 整体左移
        table.shift(LEFT * 3)

        self.play(Write(table))
        self.wait()

        # 问题说明 - 右侧，简洁清晰
        problem = VGroup(
            Text("目标：预测 ? 位置的评分", font_size=22, color=YELLOW),
            Text("", font_size=6),
            Text("假设：评分矩阵是低秩的", font_size=20),
            Text("（用户喜好可由少数", font_size=18, color=GRAY),
            Text("  因子来描述）", font_size=18, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        problem.shift(RIGHT * 3 + UP * 0.3)

        self.play(Write(problem))
        self.wait(2)


class MatrixFactorizationIdea(Scene):
    """矩阵分解的思想"""

    def construct(self):
        title = Text("矩阵分解：找到隐含因子", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 公式
        formula = MathTex(
            r"R \approx P \times Q^T",
            font_size=48
        ).shift(UP * 1.8)
        self.play(Write(formula))
        self.wait()

        # 矩阵形状示意
        R_rect = Rectangle(width=3, height=2, color=BLUE, fill_opacity=0.3)
        R_label = VGroup(
            Text("R", font_size=28),
            Text("m×n", font_size=20, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        R_label.move_to(R_rect)
        R_group = VGroup(R_rect, R_label).shift(LEFT * 4 + DOWN * 0.3)
        R_desc = Text("评分矩阵", font_size=20).next_to(R_group, DOWN)

        P_rect = Rectangle(width=1.5, height=2, color=RED, fill_opacity=0.3)
        P_label = VGroup(
            Text("P", font_size=28),
            Text("m×k", font_size=20, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        P_label.move_to(P_rect)
        P_group = VGroup(P_rect, P_label).shift(DOWN * 0.3)
        P_desc = Text("用户因子", font_size=20).next_to(P_group, DOWN)

        Q_rect = Rectangle(width=3, height=1, color=GREEN, fill_opacity=0.3)
        Q_label = VGroup(
            MathTex("Q^T", font_size=28),
            Text("k×n", font_size=20, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        Q_label.move_to(Q_rect)
        Q_group = VGroup(Q_rect, Q_label).shift(RIGHT * 3.5 + DOWN * 0.3)
        Q_desc = Text("商品因子", font_size=20).next_to(Q_group, DOWN)

        equal = MathTex(r"\approx", font_size=36).shift(LEFT * 2)
        times = MathTex(r"\times", font_size=36).shift(RIGHT * 1.0)

        self.play(Create(R_group), Write(R_desc))
        self.play(Write(equal))
        self.play(Create(P_group), Write(P_desc))
        self.play(Write(times))
        self.play(Create(Q_group), Write(Q_desc))
        self.wait()

        # k的含义
        k_explain = Text(
            "k = 隐含因子数量（如：科幻、动作、爱情...）",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(k_explain))
        self.wait(2)


class CollaborativeFiltering(Scene):
    """协同过滤示意"""

    def construct(self):
        title = Text("协同过滤：相似用户有相似喜好", font_size=38)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 向量空间示意
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_opacity": 0.2}
        ).shift(LEFT * 2 + DOWN * 0.3)

        x_label = Text("科幻偏好", font_size=20).next_to(plane, DOWN)
        y_label = Text("动作偏好", font_size=20).next_to(plane, LEFT).rotate(90 * DEGREES)

        self.play(Create(plane), Write(x_label))

        # 用户向量
        alice = Arrow(plane.c2p(0, 0), plane.c2p(4, 3), buff=0, color=BLUE, stroke_width=3)
        alice_label = Text("Alice", font_size=20, color=BLUE)
        alice_label.next_to(alice.get_end(), UR, buff=0.1)

        bob = Arrow(plane.c2p(0, 0), plane.c2p(3.5, 3.2), buff=0, color=GREEN, stroke_width=3)
        bob_label = Text("Bob", font_size=20, color=GREEN)
        bob_label.next_to(bob.get_end(), RIGHT, buff=0.1)

        carol = Arrow(plane.c2p(0, 0), plane.c2p(1, 4), buff=0, color=ORANGE, stroke_width=3)
        carol_label = Text("Carol", font_size=20, color=ORANGE)
        carol_label.next_to(carol.get_end(), UL, buff=0.1)

        self.play(GrowArrow(alice), Write(alice_label))
        self.play(GrowArrow(bob), Write(bob_label))
        self.play(GrowArrow(carol), Write(carol_label))
        self.wait()

        # 相似度说明
        similarity = VGroup(
            Text("向量夹角小 = 相似", font_size=24, color=YELLOW),
            Text("Alice ≈ Bob (夹角小)", font_size=22, color=GREEN),
            Text("Alice ≠ Carol (夹角大)", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        similarity.shift(RIGHT * 3.5 + DOWN * 0.3)

        self.play(Write(similarity))
        self.wait()

        # 推荐逻辑
        logic = Text(
            "如果Bob喜欢某电影，那Alice可能也喜欢！",
            font_size=24,
            color=GREEN
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(logic))
        self.wait(2)


# ============================================================
# Scene 2: 投资组合优化
# ============================================================
class EfficientFrontier(Scene):
    """有效前沿"""

    def construct(self):
        title = Text("有效前沿", font_size=42)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[0, 25, 5],
            y_range=[0, 20, 5],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.8)

        x_label = Text("风险 (标准差 %)", font_size=20)
        x_label.next_to(axes.x_axis, DOWN)

        y_label = Text("收益 (%)", font_size=20)
        y_label.next_to(axes.y_axis, LEFT).rotate(90 * DEGREES)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 随机投资组合点
        np.random.seed(789)
        n_points = 50
        risks = np.random.uniform(5, 20, n_points)
        returns = 0.5 * risks + np.random.randn(n_points) * 2

        random_dots = VGroup()
        for r, ret in zip(risks, returns):
            dot = Dot(axes.c2p(r, ret), color=BLUE, radius=0.05, fill_opacity=0.5)
            random_dots.add(dot)

        self.play(Create(random_dots))
        self.wait()

        # 有效前沿曲线
        frontier_risks = np.linspace(5, 20, 50)
        frontier_returns = 0.8 * frontier_risks - 0.01 * (frontier_risks - 12) ** 2 + 2

        frontier_points = [axes.c2p(r, ret) for r, ret in zip(frontier_risks, frontier_returns)]
        frontier = VMobject()
        frontier.set_points_smoothly(frontier_points)
        frontier.set_color(YELLOW)
        frontier.set_stroke(width=4)

        frontier_label = Text("有效前沿", font_size=22, color=YELLOW)
        frontier_label.next_to(frontier.get_end(), UR)

        self.play(Create(frontier), Write(frontier_label))
        self.wait()

        # 最小方差点
        min_var_point = Dot(axes.c2p(5, 6), color=GREEN, radius=0.15)
        min_var_label = Text("最小方差组合", font_size=18, color=GREEN)
        min_var_label.next_to(min_var_point, DOWN)

        self.play(Create(min_var_point), Write(min_var_label))
        self.wait()

        # 说明
        explanation = VGroup(
            Text("• 有效前沿上的组合：相同风险下收益最高", font_size=22),
            Text("• 前沿以下的点：可以被优化", font_size=22, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(explanation))
        self.wait(2)


class PortfolioVisualization(Scene):
    """投资组合风险可视化"""

    def construct(self):
        title = Text("投资组合在风险空间中的位置", font_size=36)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        # 创建坐标系（代表风险因子空间）
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_opacity": 0.2}
        ).shift(DOWN * 0.5)

        x_label = Text("风险因子1", font_size=20).next_to(plane, DOWN)
        y_label = Text("风险因子2", font_size=20).next_to(plane, LEFT).rotate(90 * DEGREES)

        self.play(Create(plane), Write(x_label), Write(y_label))

        # 风险椭圆（协方差矩阵的等高线）
        ellipse = Ellipse(width=4, height=2, color=BLUE, fill_opacity=0.2)
        ellipse.move_to(plane.get_center())
        ellipse_label = Text("等风险线", font_size=18, color=BLUE)
        ellipse_label.next_to(ellipse, UR)

        self.play(Create(ellipse), Write(ellipse_label))

        # 特征向量（风险主轴）
        eigen1 = Arrow(plane.c2p(-2, 0), plane.c2p(2, 0), buff=0, color=RED, stroke_width=3)
        eigen1_label = MathTex(r"v_1", color=RED, font_size=24)
        eigen1_label.next_to(eigen1.get_end(), RIGHT)

        eigen2 = Arrow(plane.c2p(0, -1), plane.c2p(0, 1), buff=0, color=GREEN, stroke_width=3)
        eigen2_label = MathTex(r"v_2", color=GREEN, font_size=24)
        eigen2_label.next_to(eigen2.get_end(), UP)

        self.play(GrowArrow(eigen1), Write(eigen1_label))
        self.play(GrowArrow(eigen2), Write(eigen2_label))
        self.wait()

        # 不同的投资组合
        portfolio1 = Dot(plane.c2p(1.5, 0.3), color=YELLOW, radius=0.15)
        p1_label = Text("高风险组合", font_size=16, color=YELLOW)
        p1_label.next_to(portfolio1, UR, buff=0.1)

        portfolio2 = Dot(plane.c2p(0.3, 0.8), color=PURPLE, radius=0.15)
        p2_label = Text("低风险组合", font_size=16, color=PURPLE)
        p2_label.next_to(portfolio2, UL, buff=0.1)

        self.play(Create(portfolio1), Write(p1_label))
        self.play(Create(portfolio2), Write(p2_label))
        self.wait()

        # 说明
        note = Text(
            "沿v1方向暴露越大，承担的风险越高",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(note))
        self.wait(2)


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    print("Week 10 - Part 3: 实战应用动画")
    print("运行示例: manim -pql applications.py RecommendationMatrix")
    print("\n可用场景:")
    print("  - CollaborativeFiltering: 协同过滤")
    print("  - EfficientFrontier: 有效前沿")
    print("  - MatrixFactorizationIdea: 矩阵分解思想")
    print("  - PortfolioVisualization: 风险空间可视化")
    print("  - RecommendationMatrix: 评分矩阵")
