"""
有效前沿构建动画
展示随着目标收益率变化，最优组合点如何描绘出有效前沿
"""
from manim import *
import numpy as np


class EfficientFrontierConstruction(Scene):
    """有效前沿逐点构建动画"""
    def construct(self):
        # 标题
        title = Text("Efficient Frontier Construction", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 坐标系
        axes = Axes(
            x_range=[0, 0.35, 0.05],
            y_range=[0, 0.20, 0.02],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(DOWN * 0.3)

        x_label = Text("Risk", font_size=20).next_to(axes.x_axis, RIGHT)
        y_label = Text("Return", font_size=20).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 模拟5只资产
        np.random.seed(42)
        n_assets = 5
        expected_returns = np.array([0.08, 0.12, 0.10, 0.15, 0.07])
        volatilities = np.array([0.15, 0.22, 0.18, 0.28, 0.12])

        # 相关矩阵 -> 协方差矩阵
        corr = np.array([
            [1.0, 0.3, 0.2, 0.4, 0.1],
            [0.3, 1.0, 0.5, 0.6, 0.2],
            [0.2, 0.5, 1.0, 0.4, 0.3],
            [0.4, 0.6, 0.4, 1.0, 0.2],
            [0.1, 0.2, 0.3, 0.2, 1.0]
        ])
        cov_matrix = np.outer(volatilities, volatilities) * corr

        # 绘制个股位置
        asset_dots = VGroup()
        asset_labels = VGroup()
        colors = [BLUE, GREEN, ORANGE, RED, PURPLE]

        for i in range(n_assets):
            dot = Dot(
                axes.c2p(volatilities[i], expected_returns[i]),
                color=colors[i],
                radius=0.1
            )
            label = Text(f"Asset {i+1}", font_size=14, color=colors[i])
            label.next_to(dot, RIGHT, buff=0.1)
            asset_dots.add(dot)
            asset_labels.add(label)

        self.play(Create(asset_dots), Write(asset_labels))
        self.wait(0.5)

        # 计算有效前沿点
        def portfolio_stats(weights):
            ret = weights @ expected_returns
            risk = np.sqrt(weights @ cov_matrix @ weights)
            return risk, ret

        def optimize_for_return(target_ret, cov_matrix, expected_returns):
            """简单的二次规划求解"""
            from scipy.optimize import minimize

            n = len(expected_returns)

            def objective(w):
                return w @ cov_matrix @ w

            constraints = [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                {'type': 'eq', 'fun': lambda w: w @ expected_returns - target_ret}
            ]
            bounds = [(0, 1) for _ in range(n)]

            result = minimize(objective, np.ones(n)/n, method='SLSQP',
                            bounds=bounds, constraints=constraints)
            if result.success:
                return result.x
            return None

        # 生成有效前沿点
        target_returns = np.linspace(0.07, 0.15, 30)
        frontier_points = []

        for target in target_returns:
            weights = optimize_for_return(target, cov_matrix, expected_returns)
            if weights is not None:
                risk, ret = portfolio_stats(weights)
                if risk < 0.35:
                    frontier_points.append((risk, ret))

        # 动画：逐点绘制有效前沿
        frontier_dots = VGroup()
        frontier_line = VMobject(color=YELLOW, stroke_width=3)

        # 目标收益指示器
        target_line = DashedLine(
            axes.c2p(0, target_returns[0]),
            axes.c2p(0.35, target_returns[0]),
            color=WHITE,
            stroke_width=1
        )
        target_label = Text(f"Target: {target_returns[0]:.1%}", font_size=16)
        target_label.next_to(target_line, LEFT)

        self.play(Create(target_line), Write(target_label))

        points_for_line = []
        for i, (risk, ret) in enumerate(frontier_points):
            # 更新目标线
            new_target_line = DashedLine(
                axes.c2p(0, ret),
                axes.c2p(0.35, ret),
                color=WHITE,
                stroke_width=1
            )
            new_label = Text(f"Target: {ret:.1%}", font_size=16)
            new_label.next_to(new_target_line, LEFT)

            # 创建新点
            dot = Dot(axes.c2p(risk, ret), color=YELLOW, radius=0.06)
            frontier_dots.add(dot)
            points_for_line.append(axes.c2p(risk, ret))

            # 更新曲线
            if len(points_for_line) >= 2:
                new_line = VMobject(color=YELLOW, stroke_width=3)
                new_line.set_points_smoothly(points_for_line)

                self.play(
                    Transform(target_line, new_target_line),
                    Transform(target_label, new_label),
                    Create(dot),
                    Transform(frontier_line, new_line),
                    run_time=0.15
                )
            else:
                self.play(
                    Transform(target_line, new_target_line),
                    Transform(target_label, new_label),
                    Create(dot),
                    run_time=0.15
                )

        self.play(FadeOut(target_line), FadeOut(target_label))

        # 标注有效前沿
        frontier_label = Text("Efficient Frontier", font_size=20, color=YELLOW)
        frontier_label.next_to(frontier_line, UP)
        self.play(Write(frontier_label))

        self.wait(2)


class EfficientFrontierSimple(Scene):
    """简化版有效前沿动画，适合GIF"""
    def construct(self):
        # 坐标系
        axes = Axes(
            x_range=[0, 0.35, 0.05],
            y_range=[0, 0.18, 0.02],
            x_length=7,
            y_length=5,
        )

        x_label = Text("Risk", font_size=18).next_to(axes.x_axis, RIGHT)
        y_label = Text("Return", font_size=18).next_to(axes.y_axis, UP)
        title = Text("Efficient Frontier", font_size=28).to_edge(UP)

        self.add(axes, x_label, y_label, title)

        # 资产数据
        np.random.seed(42)
        expected_returns = np.array([0.08, 0.12, 0.10, 0.15, 0.07])
        volatilities = np.array([0.15, 0.22, 0.18, 0.28, 0.12])
        corr = np.array([
            [1.0, 0.3, 0.2, 0.4, 0.1],
            [0.3, 1.0, 0.5, 0.6, 0.2],
            [0.2, 0.5, 1.0, 0.4, 0.3],
            [0.4, 0.6, 0.4, 1.0, 0.2],
            [0.1, 0.2, 0.3, 0.2, 1.0]
        ])
        cov_matrix = np.outer(volatilities, volatilities) * corr

        # 绘制个股
        colors = [BLUE, GREEN, ORANGE, RED, PURPLE]
        for i in range(5):
            dot = Dot(axes.c2p(volatilities[i], expected_returns[i]),
                     color=colors[i], radius=0.08)
            self.add(dot)

        # 预计算有效前沿
        def optimize_for_return(target_ret):
            from scipy.optimize import minimize
            n = 5
            def objective(w):
                return w @ cov_matrix @ w
            constraints = [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                {'type': 'eq', 'fun': lambda w: w @ expected_returns - target_ret}
            ]
            bounds = [(0, 1) for _ in range(n)]
            result = minimize(objective, np.ones(n)/n, method='SLSQP',
                            bounds=bounds, constraints=constraints)
            if result.success:
                return np.sqrt(result.fun), target_ret
            return None

        frontier_points = []
        for target in np.linspace(0.07, 0.15, 40):
            result = optimize_for_return(target)
            if result and result[0] < 0.35:
                frontier_points.append(result)

        # 动画绘制
        moving_dot = Dot(axes.c2p(frontier_points[0][0], frontier_points[0][1]),
                        color=YELLOW, radius=0.1)
        trace = VMobject(color=YELLOW, stroke_width=4)
        trace_points = [axes.c2p(frontier_points[0][0], frontier_points[0][1])]
        trace.set_points_as_corners(trace_points)

        self.add(moving_dot, trace)

        for risk, ret in frontier_points[1:]:
            new_pos = axes.c2p(risk, ret)
            trace_points.append(new_pos)
            new_trace = VMobject(color=YELLOW, stroke_width=4)
            new_trace.set_points_smoothly(trace_points)

            self.play(
                moving_dot.animate.move_to(new_pos),
                Transform(trace, new_trace),
                run_time=0.08
            )

        # 最终标记
        self.play(moving_dot.animate.set_color(GREEN).scale(1.5))
        self.wait(1)
