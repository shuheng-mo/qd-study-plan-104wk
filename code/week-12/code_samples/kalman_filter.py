"""
Week 12 - 卡尔曼滤波
通用卡尔曼滤波器和时变贝塔估计

包含：
- KalmanFilter: 通用卡尔曼滤波器类
- estimate_time_varying_beta(): 使用卡尔曼滤波估计时变贝塔
"""

import numpy as np
import matplotlib.pyplot as plt


class KalmanFilter:
    """
    通用卡尔曼滤波器

    状态方程：x_t = A·x_{t-1} + w_t,  w_t ~ N(0, Q)
    观测方程：y_t = C·x_t + v_t,      v_t ~ N(0, R)
    """

    def __init__(self, A, C, Q, R, x0, P0):
        """
        初始化卡尔曼滤波器

        参数：
        - A: 状态转移矩阵
        - C: 观测矩阵
        - Q: 过程噪声协方差
        - R: 观测噪声协方差
        - x0: 初始状态估计
        - P0: 初始协方差估计
        """
        self.A = np.atleast_2d(A)
        self.C = np.atleast_2d(C)
        self.Q = np.atleast_2d(Q)
        self.R = np.atleast_2d(R)
        self.x = np.atleast_1d(x0).reshape(-1, 1)
        self.P = np.atleast_2d(P0)

        self.n_states = self.A.shape[0]
        self.n_obs = self.C.shape[0]

    def predict(self):
        """
        预测步

        返回：
        - 预测状态向量
        """
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q
        return self.x.flatten()

    def update(self, y):
        """
        更新步

        参数：
        - y: 观测值

        返回：
        - 更新后的状态向量
        - 卡尔曼增益
        """
        y = np.atleast_1d(y).reshape(-1, 1)

        # 创新（预测误差）
        innovation = y - self.C @ self.x

        # 创新协方差
        S = self.C @ self.P @ self.C.T + self.R

        # 卡尔曼增益
        K = self.P @ self.C.T @ np.linalg.inv(S)

        # 状态更新
        self.x = self.x + K @ innovation

        # 协方差更新
        I = np.eye(self.n_states)
        self.P = (I - K @ self.C) @ self.P

        return self.x.flatten(), K

    def filter(self, observations):
        """
        对整个序列进行滤波

        参数：
        - observations: 观测序列

        返回：
        - 状态估计序列
        """
        n_obs = len(observations)
        states = np.zeros((n_obs, self.n_states))

        for t, y in enumerate(observations):
            self.predict()
            state, _ = self.update(y)
            states[t] = state

        return states


def estimate_time_varying_beta(stock_returns, market_returns):
    """
    使用卡尔曼滤波估计时变贝塔

    模型：
    r_stock,t = alpha_t + beta_t * r_market,t + epsilon_t

    状态：x_t = [alpha_t, beta_t]'
    状态方程：x_t = x_{t-1} + w_t  （随机游走）
    观测方程：r_stock,t = [1, r_market,t] @ x_t + v_t

    参数：
    - stock_returns: 股票收益率序列
    - market_returns: 市场收益率序列

    返回：
    - alphas: alpha估计序列
    - betas: beta估计序列
    """
    n_obs = len(stock_returns)

    # 状态转移矩阵（随机游走）
    A = np.eye(2)

    # 过程噪声协方差（参数漂移速度）
    Q = np.diag([0.0001, 0.001])  # beta的漂移大于alpha

    # 观测噪声方差
    R = np.array([[np.var(stock_returns) * 0.5]])

    # 初始状态
    x0 = np.array([0.0, 1.0])  # alpha=0, beta=1
    P0 = np.eye(2) * 1.0

    # 存储结果
    alphas = np.zeros(n_obs)
    betas = np.zeros(n_obs)

    # 初始化
    x = x0.reshape(-1, 1)
    P = P0

    for t in range(n_obs):
        # 观测矩阵随时间变化
        C = np.array([[1, market_returns[t]]])

        # 预测步
        x_pred = A @ x
        P_pred = A @ P @ A.T + Q

        # 更新步
        y = stock_returns[t]
        innovation = y - C @ x_pred
        S = C @ P_pred @ C.T + R
        K = P_pred @ C.T / S[0, 0]

        x = x_pred + K * innovation
        P = (np.eye(2) - K @ C) @ P_pred

        alphas[t] = x[0, 0]
        betas[t] = x[1, 0]

    return alphas, betas


def rolling_ols_beta(stock_returns, market_returns, window=60):
    """
    滚动窗口OLS估计贝塔（用于比较）

    参数：
    - stock_returns: 股票收益率序列
    - market_returns: 市场收益率序列
    - window: 滚动窗口大小

    返回：
    - rolling_beta: 滚动贝塔估计序列
    """
    n_obs = len(stock_returns)
    rolling_beta = np.zeros(n_obs)

    for t in range(window, n_obs):
        X = market_returns[t-window:t]
        y = stock_returns[t-window:t]
        rolling_beta[t] = np.cov(X, y)[0, 1] / np.var(X)

    # 填充前window个值
    rolling_beta[:window] = rolling_beta[window]

    return rolling_beta


if __name__ == "__main__":
    # 模拟时变贝塔的股票
    np.random.seed(42)
    n_days = 500

    # 市场收益
    market_returns = np.random.randn(n_days) * 0.01

    # 真实的时变贝塔（正弦变化 + 趋势）
    true_beta = 1.0 + 0.3 * np.sin(2 * np.pi * np.arange(n_days) / 250) + \
                0.002 * np.arange(n_days)
    true_alpha = 0.0002  # 微小的超额收益

    # 生成股票收益
    stock_returns = true_alpha + true_beta * market_returns + np.random.randn(n_days) * 0.005

    # 卡尔曼滤波估计
    est_alpha, est_beta = estimate_time_varying_beta(stock_returns, market_returns)

    # 滚动窗口OLS作为对比
    window = 60
    rolling_beta = rolling_ols_beta(stock_returns, market_returns, window)

    # 绘图
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # 贝塔估计对比
    axes[0].plot(true_beta, 'k-', label='真实Beta', linewidth=2)
    axes[0].plot(est_beta, 'b-', label='卡尔曼滤波估计', alpha=0.8)
    axes[0].plot(rolling_beta, 'r--', label=f'{window}日滚动OLS', alpha=0.6)
    axes[0].set_xlabel('时间')
    axes[0].set_ylabel('Beta')
    axes[0].set_title('时变Beta估计：卡尔曼滤波 vs 滚动OLS')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 估计误差
    axes[1].plot(np.abs(est_beta - true_beta), 'b-', label='卡尔曼滤波误差')
    axes[1].plot(np.abs(rolling_beta - true_beta), 'r-', label='滚动OLS误差', alpha=0.6)
    axes[1].set_xlabel('时间')
    axes[1].set_ylabel('绝对误差')
    axes[1].set_title('估计误差对比')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # 打印统计
    print(f"\n均方根误差(RMSE):")
    print(f"  卡尔曼滤波: {np.sqrt(np.mean((est_beta - true_beta)**2)):.4f}")
    print(f"  滚动OLS: {np.sqrt(np.mean((rolling_beta - true_beta)**2)):.4f}")
