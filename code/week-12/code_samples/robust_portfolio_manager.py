"""
Week 12 - 稳健投资组合管理
稳健投资组合管理器和协方差方法比较

包含：
- RobustPortfolioManager: 稳健投资组合管理器类
- compare_covariance_methods(): 比较不同协方差估计方法的组合表现
"""

import numpy as np
import pandas as pd
import cvxpy as cp
from sklearn.covariance import LedoitWolf
from sklearn.decomposition import PCA


class RobustPortfolioManager:
    """稳健投资组合管理器"""

    def __init__(self, returns_data, cov_method='ledoit_wolf'):
        """
        初始化

        参数：
        - returns_data: DataFrame，收益率数据
        - cov_method: 协方差估计方法
          'sample': 样本协方差
          'ledoit_wolf': Ledoit-Wolf收缩
          'factor': 因子模型
          'rmt_denoise': 随机矩阵理论去噪
        """
        self.returns = returns_data.values
        self.asset_names = returns_data.columns.tolist()
        self.n_assets = len(self.asset_names)
        self.n_samples = len(returns_data)
        self.cov_method = cov_method

        # 估计预期收益
        self.expected_returns = self.returns.mean(axis=0) * 252

        # 估计协方差矩阵
        self._estimate_covariance()

    def _estimate_covariance(self):
        """根据选择的方法估计协方差矩阵"""

        if self.cov_method == 'sample':
            self.cov_matrix = np.cov(self.returns.T) * 252
            self.method_name = "样本协方差"

        elif self.cov_method == 'ledoit_wolf':
            lw = LedoitWolf().fit(self.returns)
            self.cov_matrix = lw.covariance_ * 252
            self.shrinkage = lw.shrinkage_
            self.method_name = f"Ledoit-Wolf (收缩={self.shrinkage:.3f})"

        elif self.cov_method == 'factor':
            self.cov_matrix = self._factor_model_cov() * 252
            self.method_name = "因子模型"

        elif self.cov_method == 'rmt_denoise':
            sample_cov = np.cov(self.returns.T)
            self.cov_matrix = self._rmt_denoise(sample_cov) * 252
            self.method_name = "RMT去噪"

        # 确保正定
        self._ensure_positive_definite()

    def _factor_model_cov(self, n_factors=5):
        """因子模型协方差"""
        pca = PCA(n_components=n_factors)
        factors = pca.fit_transform(self.returns)
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
        factor_cov = np.cov(factors.T)

        systematic = loadings @ factor_cov @ loadings.T
        residuals = self.returns - factors @ loadings.T
        specific = np.diag(np.var(residuals, axis=0))

        return systematic + specific

    def _rmt_denoise(self, cov_matrix):
        """RMT去噪"""
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        gamma = self.n_assets / self.n_samples
        sigma_sq = np.median(eigenvalues)
        lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2

        # 收缩噪声特征值
        denoised_eigenvalues = eigenvalues.copy()
        noise_mask = eigenvalues <= lambda_plus
        if noise_mask.any():
            noise_mean = eigenvalues[noise_mask].mean()
            denoised_eigenvalues[noise_mask] = noise_mean

        return eigenvectors @ np.diag(denoised_eigenvalues) @ eigenvectors.T

    def _ensure_positive_definite(self, epsilon=1e-6):
        """确保协方差矩阵正定"""
        eigenvalues = np.linalg.eigvalsh(self.cov_matrix)
        if eigenvalues.min() < epsilon:
            # 特征值修复
            eigenvalues_fixed = np.maximum(eigenvalues, epsilon)
            eigenvectors = np.linalg.eigh(self.cov_matrix)[1]
            self.cov_matrix = eigenvectors @ np.diag(eigenvalues_fixed) @ eigenvectors.T

    def optimize(self, target_return=None, max_weight=0.2, min_weight=0.0):
        """
        最小方差优化

        参数：
        - target_return: 目标年化收益
        - max_weight: 单资产最大权重
        - min_weight: 单资产最小权重

        返回：
        - 最优权重向量
        """
        w = cp.Variable(self.n_assets)

        objective = cp.Minimize(cp.quad_form(w, self.cov_matrix))

        constraints = [
            cp.sum(w) == 1,
            w >= min_weight,
            w <= max_weight
        ]

        if target_return is not None:
            constraints.append(w @ self.expected_returns >= target_return)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        if problem.status == 'optimal':
            return w.value
        else:
            raise ValueError(f"优化失败: {problem.status}")

    def backtest(self, test_returns, weights):
        """
        简单回测

        参数：
        - test_returns: 测试期收益率数据
        - weights: 投资组合权重

        返回：
        - 绩效指标字典
        """
        portfolio_returns = test_returns @ weights

        # 计算指标
        annual_return = portfolio_returns.mean() * 252
        annual_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe = annual_return / annual_vol if annual_vol > 0 else 0

        # 最大回撤
        cumulative = (1 + portfolio_returns).cumprod()
        rolling_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        return {
            'annual_return': annual_return,
            'annual_volatility': annual_vol,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown
        }


def compare_covariance_methods(n_train=250, n_test=250, n_assets=50):
    """
    比较不同协方差估计方法的组合表现

    参数：
    - n_train: 训练期样本数
    - n_test: 测试期样本数
    - n_assets: 资产数量

    返回：
    - 各方法绩效结果字典
    """
    np.random.seed(42)

    # 真实协方差（因子结构）
    n_factors = 5
    F = np.random.randn(n_assets, n_factors) * 0.2
    true_cov = F @ F.T + np.diag(np.random.uniform(0.01, 0.05, n_assets))

    # 生成训练和测试数据
    L = np.linalg.cholesky(true_cov)
    mu = np.random.uniform(0.05, 0.15, n_assets) / 252

    train_returns = mu + np.random.randn(n_train, n_assets) @ L.T
    test_returns = mu + np.random.randn(n_test, n_assets) @ L.T

    # 创建DataFrame
    train_df = pd.DataFrame(train_returns, columns=[f'Asset_{i}' for i in range(n_assets)])

    # 测试不同方法
    methods = ['sample', 'ledoit_wolf', 'factor', 'rmt_denoise']
    results = {}

    print("=" * 60)
    print("不同协方差估计方法的投资组合表现比较")
    print("=" * 60)

    for method in methods:
        pm = RobustPortfolioManager(train_df, cov_method=method)
        weights = pm.optimize(max_weight=0.1)
        perf = pm.backtest(test_returns, weights)
        results[method] = perf

        print(f"\n{pm.method_name}:")
        print(f"  年化收益: {perf['annual_return']*100:.2f}%")
        print(f"  年化波动: {perf['annual_volatility']*100:.2f}%")
        print(f"  夏普比率: {perf['sharpe_ratio']:.3f}")
        print(f"  最大回撤: {perf['max_drawdown']*100:.2f}%")

    return results


if __name__ == "__main__":
    # 运行比较
    results = compare_covariance_methods()

    # 绘制比较图
    import matplotlib.pyplot as plt

    methods = list(results.keys())
    sharpe_ratios = [results[m]['sharpe_ratio'] for m in methods]
    volatilities = [results[m]['annual_volatility'] * 100 for m in methods]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 夏普比率对比
    axes[0].bar(methods, sharpe_ratios, color=['#e74c3c', '#3498db', '#2ecc71', '#9b59b6'])
    axes[0].set_ylabel('夏普比率')
    axes[0].set_title('不同协方差估计方法的夏普比率')
    axes[0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)

    # 波动率对比
    axes[1].bar(methods, volatilities, color=['#e74c3c', '#3498db', '#2ecc71', '#9b59b6'])
    axes[1].set_ylabel('年化波动率 (%)')
    axes[1].set_title('不同协方差估计方法的年化波动率')

    plt.tight_layout()
    plt.show()
