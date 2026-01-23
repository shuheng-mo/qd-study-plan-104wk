import pandas as pd
import cvxpy as cp
import numpy as np


class PortfolioRiskManager:
    """投资组合风险管理器"""

    def __init__(self, returns_data):
        """

        初始化风险管理器

        returns_data: DataFrame，行是日期，列是资产

        """

        self.returns = returns_data.values

        self.asset_names = returns_data.columns.tolist()

        self.n_assets = len(self.asset_names)

        self.expected_returns = self.returns.mean(axis=0) * 252  # 年化

        self._estimate_covariance()

    def _estimate_covariance(self):
        """估计协方差矩阵"""

        # 样本协方差（年化）

        self.cov_sample = np.cov(self.returns.T) * 252

        # 检查正定性

        eigenvalues = np.linalg.eigvalsh(self.cov_sample)

        self.is_positive_definite = np.all(eigenvalues > 1e-10)

        if not self.is_positive_definite:

            print("警告：样本协方差矩阵不正定，正在修复...")

            self.cov_matrix = make_positive_definite(self.cov_sample)

        else:

            self.cov_matrix = self.cov_sample

    def optimize_portfolio(
        self, target_return=None, max_weight=0.3, min_weight=0.0, risk_aversion=None
    ):
        """

        优化投资组合

        参数：

        - target_return: 目标年化收益

        - max_weight: 单资产最大权重

        - min_weight: 单资产最小权重（0表示不做空）

        - risk_aversion: 风险厌恶系数（用于均值-方差优化）

        """

        w = cp.Variable(self.n_assets)

        # 组合方差

        portfolio_variance = cp.quad_form(w, self.cov_matrix)

        if risk_aversion is not None:

            # 均值-方差优化: max μᵀw - (λ/2)wᵀΣw

            portfolio_return = self.expected_returns @ w

            objective = cp.Maximize(
                portfolio_return - (risk_aversion / 2) * portfolio_variance
            )

        else:

            # 最小方差优化

            objective = cp.Minimize(portfolio_variance)

        constraints = [cp.sum(w) == 1, w >= min_weight, w <= max_weight]

        if target_return is not None:

            constraints.append(self.expected_returns @ w >= target_return)

        problem = cp.Problem(objective, constraints)

        problem.solve()

        if problem.status == "optimal":

            self.optimal_weights = w.value

            self.optimal_risk = np.sqrt(
                self.optimal_weights @ self.cov_matrix @ self.optimal_weights
            )

            self.optimal_return = self.optimal_weights @ self.expected_returns

            return self.optimal_weights

        else:

            raise ValueError(f"优化失败: {problem.status}")

    def calculate_risk_metrics(
        self, weights, confidence_level=0.95, n_simulations=100000, holding_period=1
    ):
        """

        计算风险指标

        参数：

        - weights: 投资组合权重

        - confidence_level: VaR置信水平

        - n_simulations: 蒙特卡洛模拟次数

        - holding_period: 持有期（天）

        """

        # 日度参数

        daily_returns = self.expected_returns / 252

        daily_cov = self.cov_matrix / 252

        # Cholesky分解

        L = np.linalg.cholesky(daily_cov)

        # 蒙特卡洛模拟

        z = np.random.standard_normal((n_simulations, self.n_assets))

        simulated_returns = daily_returns + z @ L.T

        # 多期收益（假设收益率可加）

        if holding_period > 1:

            multi_period_returns = np.zeros(n_simulations)

            for _ in range(holding_period):

                z = np.random.standard_normal((n_simulations, self.n_assets))

                daily_ret = daily_returns + z @ L.T

                multi_period_returns += daily_ret @ weights

            portfolio_returns = multi_period_returns

        else:

            portfolio_returns = simulated_returns @ weights

        # 计算VaR和CVaR

        var = -np.percentile(portfolio_returns, (1 - confidence_level) * 100)

        cvar = -np.mean(portfolio_returns[portfolio_returns <= -var])

        # 组合统计

        portfolio_std = np.sqrt(weights @ daily_cov @ weights)

        portfolio_mean = weights @ daily_returns

        sharpe = (portfolio_mean * 252) / (portfolio_std * np.sqrt(252))  # 年化夏普

        return {
            "VaR": var,
            "CVaR": cvar,
            "daily_volatility": portfolio_std,
            "annual_volatility": portfolio_std * np.sqrt(252),
            "expected_daily_return": portfolio_mean,
            "expected_annual_return": portfolio_mean * 252,
            "sharpe_ratio": sharpe,
            "confidence_level": confidence_level,
            "holding_period": holding_period,
        }

    def risk_decomposition(self, weights):
        """

        风险分解：计算每个资产对组合风险的贡献

        """

        portfolio_var = weights @ self.cov_matrix @ weights

        portfolio_std = np.sqrt(portfolio_var)

        # 边际风险贡献 (MRC)

        mrc = self.cov_matrix @ weights / portfolio_std

        # 成分风险贡献 (CRC)

        crc = weights * mrc

        # 百分比贡献

        pct_contribution = crc / portfolio_std

        return {
            "portfolio_volatility": portfolio_std,
            "marginal_risk_contribution": mrc,
            "component_risk_contribution": crc,
            "percentage_contribution": pct_contribution,
        }

    def print_portfolio_summary(self, weights):
        """打印投资组合摘要"""

        risk_metrics = self.calculate_risk_metrics(weights)

        risk_decomp = self.risk_decomposition(weights)

        print("=" * 60)

        print("投资组合摘要")

        print("=" * 60)

        print("\n资产配置:")

        for i, (name, w) in enumerate(zip(self.asset_names, weights)):

            print(f"  {name}: {w*100:.2f}%")

        print(f"\n预期收益与风险:")

        print(f"  预期年化收益: {risk_metrics['expected_annual_return']*100:.2f}%")

        print(f"  年化波动率: {risk_metrics['annual_volatility']*100:.2f}%")

        print(f"  夏普比率: {risk_metrics['sharpe_ratio']:.3f}")

        print(f"\n风险指标 (95%置信度):")

        print(f"  日度VaR: {risk_metrics['VaR']*100:.2f}%")

        print(f"  日度CVaR: {risk_metrics['CVaR']*100:.2f}%")

        print(f"\n风险贡献:")

        for i, (name, pct) in enumerate(
            zip(self.asset_names, risk_decomp["percentage_contribution"])
        ):

            print(f"  {name}: {pct*100:.2f}%")


# 创建模拟数据

np.random.seed(42)

dates = pd.date_range("2020-01-01", periods=500, freq="B")

assets = ["股票A", "股票B", "股票C", "债券", "黄金"]

# 模拟收益率（带相关性）

true_cov = (
    np.array(
        [
            [0.04, 0.02, 0.015, -0.005, 0.001],
            [0.02, 0.05, 0.02, -0.003, 0.002],
            [0.015, 0.02, 0.045, -0.002, 0.001],
            [-0.005, -0.003, -0.002, 0.01, 0.003],
            [0.001, 0.002, 0.001, 0.003, 0.015],
        ]
    )
    / 252
)  # 日度协方差

L = np.linalg.cholesky(true_cov)

returns_data = pd.DataFrame(
    np.random.randn(500, 5) @ L.T + np.array([0.10, 0.12, 0.11, 0.04, 0.06]) / 252,
    index=dates,
    columns=assets,
)

# 初始化风险管理器

rm = PortfolioRiskManager(returns_data)

# 优化组合

optimal_weights = rm.optimize_portfolio(target_return=0.08, max_weight=0.4)

# 打印摘要

rm.print_portfolio_summary(optimal_weights)
