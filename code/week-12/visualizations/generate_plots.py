"""
Week 12 可视化生成脚本
生成线性代数进阶（下）相关的静态图表
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.covariance import LedoitWolf
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
import seaborn as sns
from scipy.stats import norm
import warnings
import platform

warnings.filterwarnings("ignore")


def setup_chinese_font():
    """配置中文字体，支持macOS/Windows/Linux"""
    from matplotlib.font_manager import fontManager
    import matplotlib as mpl

    system = platform.system()

    if system == "Darwin":  # macOS
        font_list = [
            "Hiragino Sans GB",
            "Arial Unicode MS",
            "Songti SC",
            "STHeiti",
            "Heiti TC",
            "PingFang SC",
            "Apple LiGothic",
        ]
    elif system == "Windows":
        font_list = ["Microsoft YaHei", "SimHei", "SimSun", "KaiTi"]
    else:  # Linux
        font_list = ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "DejaVu Sans"]

    available_fonts = set([f.name for f in fontManager.ttflist])

    selected_font = None
    for font in font_list:
        if font in available_fonts:
            selected_font = font
            break

    if selected_font:
        print(f"✓ 使用中文字体: {selected_font}")
    else:
        print("⚠ 未找到预设中文字体")
        selected_font = font_list[0]

    mpl.rc("font", family="sans-serif")
    mpl.rcParams["font.sans-serif"] = [
        selected_font,
        "DejaVu Sans",
        "Bitstream Vera Sans",
    ]
    mpl.rcParams["axes.unicode_minus"] = False

    return selected_font


# 执行字体设置
CHINESE_FONT = setup_chinese_font()

# 设置seaborn风格
sns.set_style("whitegrid")
sns.set_palette("husl")

# 重新设置字体（seaborn会重置）
matplotlib.rcParams["font.sans-serif"] = [CHINESE_FONT, "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["font.family"] = "sans-serif"

# 其他matplotlib设置
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["figure.facecolor"] = "white"

print(f"✓ 最终字体设置: {matplotlib.rcParams['font.sans-serif']}")


def plot_marchenko_pastur():
    """
    图1: Marchenko-Pastur分布可视化
    展示特征值分布与MP理论预测
    """
    np.random.seed(42)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax_idx, n_factors in enumerate([0, 5]):
        ax = axes[ax_idx]
        n_samples, n_assets = 500, 200
        gamma = n_assets / n_samples

        if n_factors == 0:
            X = np.random.randn(n_samples, n_assets)
            title = f"纯噪声数据 (p={n_assets}, n={n_samples})"
        else:
            F = np.random.randn(n_samples, n_factors)
            B = np.random.randn(n_assets, n_factors) * 0.5
            E = np.random.randn(n_samples, n_assets)
            X = F @ B.T + E
            title = f"因子+噪声数据 ({n_factors}个因子)"

        cov_matrix = np.cov(X.T)
        eigenvalues = np.linalg.eigvalsh(cov_matrix)

        # MP理论
        sigma_sq = 1.0
        lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2
        lambda_minus = sigma_sq * (1 - np.sqrt(gamma))**2

        x = np.linspace(0.001, eigenvalues.max() * 1.1, 1000)
        mp_pdf = np.zeros_like(x)
        mask = (x >= lambda_minus) & (x <= lambda_plus)
        mp_pdf[mask] = (1 / (2 * np.pi * sigma_sq * gamma * x[mask])) * \
                       np.sqrt((lambda_plus - x[mask]) * (x[mask] - lambda_minus))

        # 绘图
        ax.hist(eigenvalues, bins=50, density=True, alpha=0.7,
                label='样本特征值', color='steelblue')
        ax.plot(x, mp_pdf, 'r-', linewidth=2.5, label='MP理论分布')
        ax.axvline(lambda_minus, color='green', linestyle='--', linewidth=2,
                   label=f'λ₋ = {lambda_minus:.2f}')
        ax.axvline(lambda_plus, color='orange', linestyle='--', linewidth=2,
                   label=f'λ₊ = {lambda_plus:.2f}')

        n_signal = np.sum(eigenvalues > lambda_plus)
        if n_signal > 0:
            ax.annotate(f'{n_signal}个信号特征值',
                       xy=(lambda_plus * 1.05, 0.4),
                       fontsize=11, color='red', fontweight='bold')

        ax.set_xlabel('特征值', fontsize=12)
        ax.set_ylabel('概率密度', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.legend(fontsize=10, loc='upper right')
        ax.set_xlim(0, eigenvalues.max() * 1.1)

    plt.tight_layout()
    plt.savefig('01_marchenko_pastur.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 01_marchenko_pastur.png")


def plot_kalman_filter():
    """
    图2: 卡尔曼滤波时变贝塔估计
    """
    np.random.seed(42)
    n_days = 500

    # 市场收益
    market_returns = np.random.randn(n_days) * 0.01

    # 真实时变贝塔
    true_beta = 1.0 + 0.3 * np.sin(2 * np.pi * np.arange(n_days) / 250) + \
                0.002 * np.arange(n_days)
    true_alpha = 0.0002

    # 生成股票收益
    stock_returns = true_alpha + true_beta * market_returns + np.random.randn(n_days) * 0.005

    # 卡尔曼滤波估计
    A = np.eye(2)
    Q = np.diag([0.0001, 0.001])
    R = np.array([[np.var(stock_returns) * 0.5]])

    x = np.array([[0.0], [1.0]])
    P = np.eye(2) * 1.0

    est_beta = np.zeros(n_days)

    for t in range(n_days):
        C = np.array([[1, market_returns[t]]])
        x_pred = A @ x
        P_pred = A @ P @ A.T + Q
        y = stock_returns[t]
        innovation = y - C @ x_pred
        S = C @ P_pred @ C.T + R
        K = P_pred @ C.T / S[0, 0]
        x = x_pred + K * innovation
        P = (np.eye(2) - K @ C) @ P_pred
        est_beta[t] = x[1, 0]

    # 滚动OLS
    window = 60
    rolling_beta = np.zeros(n_days)
    for t in range(window, n_days):
        X = market_returns[t-window:t]
        y = stock_returns[t-window:t]
        rolling_beta[t] = np.cov(X, y)[0, 1] / np.var(X)
    rolling_beta[:window] = rolling_beta[window]

    # 绘图
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    # 贝塔估计对比
    axes[0].plot(true_beta, 'k-', label='真实Beta', linewidth=2.5)
    axes[0].plot(est_beta, 'b-', label='卡尔曼滤波', linewidth=1.5, alpha=0.9)
    axes[0].plot(rolling_beta, 'r--', label=f'{window}日滚动OLS', linewidth=1.5, alpha=0.7)
    axes[0].set_xlabel('时间 (天)', fontsize=12)
    axes[0].set_ylabel('Beta', fontsize=12)
    axes[0].set_title('时变Beta估计：卡尔曼滤波 vs 滚动OLS', fontsize=14)
    axes[0].legend(fontsize=11, loc='upper left')
    axes[0].grid(True, alpha=0.3)

    # 估计误差
    axes[1].fill_between(range(n_days), np.abs(est_beta - true_beta),
                         alpha=0.5, label='卡尔曼滤波误差', color='blue')
    axes[1].fill_between(range(n_days), np.abs(rolling_beta - true_beta),
                         alpha=0.3, label='滚动OLS误差', color='red')
    axes[1].set_xlabel('时间 (天)', fontsize=12)
    axes[1].set_ylabel('绝对误差', fontsize=12)
    axes[1].set_title('估计误差对比', fontsize=14)
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3)

    # 添加RMSE统计
    rmse_kalman = np.sqrt(np.mean((est_beta - true_beta)**2))
    rmse_ols = np.sqrt(np.mean((rolling_beta - true_beta)**2))
    axes[1].text(0.98, 0.95, f'RMSE: 卡尔曼={rmse_kalman:.4f}, OLS={rmse_ols:.4f}',
                 transform=axes[1].transAxes, fontsize=11,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('02_kalman_filter.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 02_kalman_filter.png")


def plot_regularization_geometry():
    """
    图3: 正则化的几何解释
    L1 (菱形) vs L2 (圆形) 约束
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 目标函数等高线
    beta1 = np.linspace(-2, 2, 100)
    beta2 = np.linspace(-2, 2, 100)
    B1, B2 = np.meshgrid(beta1, beta2)

    # RSS等高线 (以(1.5, 1.5)为最优解)
    Z = (B1 - 1.5)**2 + (B2 - 1.5)**2

    # L2约束 (圆形)
    ax1 = axes[0]
    ax1.contour(B1, B2, Z, levels=15, cmap='Blues', alpha=0.8)

    theta = np.linspace(0, 2*np.pi, 100)
    for r in [0.5, 1.0, 1.5]:
        ax1.plot(r*np.cos(theta), r*np.sin(theta), 'g-', linewidth=2 if r == 1.0 else 1)

    # 标注切点
    ax1.plot(1.5/np.sqrt(2)*1, 1.5/np.sqrt(2)*1, 'ro', markersize=12, label='Ridge解')
    ax1.plot(1.5, 1.5, 'b*', markersize=15, label='OLS解')
    ax1.axhline(y=0, color='k', linewidth=0.5)
    ax1.axvline(x=0, color='k', linewidth=0.5)

    ax1.set_xlabel(r'$\beta_1$', fontsize=14)
    ax1.set_ylabel(r'$\beta_2$', fontsize=14)
    ax1.set_title(r'Ridge回归 (L2约束)' + '\n' + r'$\|\beta\|_2^2 \leq t$', fontsize=14)
    ax1.legend(fontsize=11, loc='upper left')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')

    # L1约束 (菱形)
    ax2 = axes[1]
    ax2.contour(B1, B2, Z, levels=15, cmap='Blues', alpha=0.8)

    # 菱形
    for t in [0.5, 1.0, 1.5]:
        diamond_x = [t, 0, -t, 0, t]
        diamond_y = [0, t, 0, -t, 0]
        ax2.plot(diamond_x, diamond_y, 'g-', linewidth=2 if t == 1.0 else 1)

    # LASSO解在角点
    ax2.plot(1.0, 0, 'ro', markersize=12, label='LASSO解')
    ax2.plot(1.5, 1.5, 'b*', markersize=15, label='OLS解')
    ax2.axhline(y=0, color='k', linewidth=0.5)
    ax2.axvline(x=0, color='k', linewidth=0.5)

    # 标注稀疏性
    ax2.annotate('稀疏解\n$\\beta_2 = 0$',
                xy=(1.0, 0), xytext=(1.5, -0.8),
                fontsize=11, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))

    ax2.set_xlabel(r'$\beta_1$', fontsize=14)
    ax2.set_ylabel(r'$\beta_2$', fontsize=14)
    ax2.set_title(r'LASSO回归 (L1约束)' + '\n' + r'$\|\beta\|_1 \leq t$', fontsize=14)
    ax2.legend(fontsize=11, loc='upper left')
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('03_regularization_geometry.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 03_regularization_geometry.png")


def plot_cov_comparison():
    """
    图4: 不同协方差估计方法的组合表现比较
    """
    np.random.seed(42)

    # 模拟数据
    n_train, n_test = 250, 250
    n_assets = 50
    n_factors = 5

    F = np.random.randn(n_assets, n_factors) * 0.2
    true_cov = F @ F.T + np.diag(np.random.uniform(0.01, 0.05, n_assets))

    L = np.linalg.cholesky(true_cov)
    mu = np.random.uniform(0.05, 0.15, n_assets) / 252

    train_returns = mu + np.random.randn(n_train, n_assets) @ L.T
    test_returns = mu + np.random.randn(n_test, n_assets) @ L.T

    # 估计不同协方差
    methods = {
        '样本协方差': np.cov(train_returns.T) * 252,
        'Ledoit-Wolf': LedoitWolf().fit(train_returns).covariance_ * 252,
    }

    # 因子模型
    pca = PCA(n_components=5)
    factors = pca.fit_transform(train_returns)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    factor_cov = np.cov(factors.T)
    systematic = loadings @ factor_cov @ loadings.T
    residuals = train_returns - factors @ loadings.T
    specific = np.diag(np.var(residuals, axis=0))
    methods['因子模型'] = (systematic + specific) * 252

    # RMT去噪
    sample_cov = np.cov(train_returns.T)
    eigenvalues, eigenvectors = np.linalg.eigh(sample_cov)
    gamma = n_assets / n_train
    sigma_sq = np.median(eigenvalues)
    lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2
    denoised_eigenvalues = eigenvalues.copy()
    noise_mask = eigenvalues <= lambda_plus
    if noise_mask.any():
        denoised_eigenvalues[noise_mask] = eigenvalues[noise_mask].mean()
    methods['RMT去噪'] = (eigenvectors @ np.diag(denoised_eigenvalues) @ eigenvectors.T) * 252

    # 简单优化和回测
    results = {}
    for name, cov in methods.items():
        # 确保正定
        eig = np.linalg.eigvalsh(cov)
        if eig.min() < 1e-6:
            eig_fixed = np.maximum(eig, 1e-6)
            V = np.linalg.eigh(cov)[1]
            cov = V @ np.diag(eig_fixed) @ V.T

        # 等风险贡献近似（简化为最小方差）
        inv_vol = 1 / np.sqrt(np.diag(cov))
        weights = inv_vol / inv_vol.sum()

        # 回测
        portfolio_returns = test_returns @ weights
        annual_return = portfolio_returns.mean() * 252
        annual_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe = annual_return / annual_vol if annual_vol > 0 else 0

        cumulative = (1 + portfolio_returns).cumprod()
        rolling_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - rolling_max) / rolling_max
        max_dd = abs(drawdown.min())

        results[name] = {
            'sharpe': sharpe,
            'volatility': annual_vol * 100,
            'return': annual_return * 100,
            'max_drawdown': max_dd * 100
        }

    # 绘图
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    method_names = list(results.keys())
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']

    # 夏普比率
    ax1 = axes[0, 0]
    sharpes = [results[m]['sharpe'] for m in method_names]
    bars1 = ax1.bar(method_names, sharpes, color=colors)
    ax1.set_ylabel('夏普比率', fontsize=12)
    ax1.set_title('夏普比率对比', fontsize=14)
    ax1.axhline(y=0, color='k', linewidth=0.5)
    for bar, val in zip(bars1, sharpes):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.3f}', ha='center', fontsize=10)

    # 年化波动率
    ax2 = axes[0, 1]
    vols = [results[m]['volatility'] for m in method_names]
    bars2 = ax2.bar(method_names, vols, color=colors)
    ax2.set_ylabel('年化波动率 (%)', fontsize=12)
    ax2.set_title('年化波动率对比', fontsize=14)
    for bar, val in zip(bars2, vols):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{val:.1f}%', ha='center', fontsize=10)

    # 年化收益
    ax3 = axes[1, 0]
    rets = [results[m]['return'] for m in method_names]
    bars3 = ax3.bar(method_names, rets, color=colors)
    ax3.set_ylabel('年化收益 (%)', fontsize=12)
    ax3.set_title('年化收益对比', fontsize=14)
    ax3.axhline(y=0, color='k', linewidth=0.5)
    for bar, val in zip(bars3, rets):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{val:.1f}%', ha='center', fontsize=10)

    # 最大回撤
    ax4 = axes[1, 1]
    dds = [results[m]['max_drawdown'] for m in method_names]
    bars4 = ax4.bar(method_names, dds, color=colors)
    ax4.set_ylabel('最大回撤 (%)', fontsize=12)
    ax4.set_title('最大回撤对比', fontsize=14)
    for bar, val in zip(bars4, dds):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{val:.1f}%', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('04_cov_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 04_cov_comparison.png")


def plot_shrinkage_concept():
    """
    图5: 收缩估计概念图
    """
    np.random.seed(42)

    n_samples, n_assets = 150, 100

    # 生成真实协方差
    n_factors = 5
    F = np.random.randn(n_assets, n_factors) * 0.1
    specific_var = np.diag(np.random.uniform(0.01, 0.05, n_assets))
    true_cov = F @ F.T + specific_var

    L = np.linalg.cholesky(true_cov)
    returns = np.random.randn(n_samples, n_assets) @ L.T

    # 样本协方差
    sample_cov = np.cov(returns.T)
    eig_sample = np.linalg.eigvalsh(sample_cov)

    # Ledoit-Wolf
    lw = LedoitWolf().fit(returns)
    eig_lw = np.linalg.eigvalsh(lw.covariance_)
    shrinkage = lw.shrinkage_

    # 真实协方差特征值
    eig_true = np.linalg.eigvalsh(true_cov)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 样本协方差特征值
    axes[0].hist(eig_sample, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    axes[0].axvline(eig_sample.mean(), color='red', linestyle='--', linewidth=2, label=f'均值={eig_sample.mean():.3f}')
    axes[0].set_xlabel('特征值', fontsize=12)
    axes[0].set_ylabel('频数', fontsize=12)
    axes[0].set_title(f'样本协方差特征值\n条件数: {eig_sample.max()/max(eig_sample.min(),1e-10):.0f}', fontsize=14)
    axes[0].legend(fontsize=10)

    # 收缩目标（单位矩阵缩放）
    target_eig = np.ones(n_assets) * np.mean(np.diag(sample_cov))
    axes[1].hist(target_eig, bins=30, alpha=0.7, color='green', edgecolor='black')
    axes[1].axvline(target_eig[0], color='red', linestyle='--', linewidth=2, label=f'目标={target_eig[0]:.3f}')
    axes[1].set_xlabel('特征值', fontsize=12)
    axes[1].set_ylabel('频数', fontsize=12)
    axes[1].set_title('收缩目标 (缩放单位矩阵)\n所有特征值相等', fontsize=14)
    axes[1].legend(fontsize=10)

    # 收缩后特征值
    axes[2].hist(eig_lw, bins=30, alpha=0.7, color='purple', edgecolor='black')
    axes[2].axvline(eig_lw.mean(), color='red', linestyle='--', linewidth=2, label=f'均值={eig_lw.mean():.3f}')
    axes[2].set_xlabel('特征值', fontsize=12)
    axes[2].set_ylabel('频数', fontsize=12)
    axes[2].set_title(f'Ledoit-Wolf收缩后\n收缩强度α={shrinkage:.3f}, 条件数: {eig_lw.max()/eig_lw.min():.0f}', fontsize=14)
    axes[2].legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('05_shrinkage_concept.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 05_shrinkage_concept.png")


def plot_eigenvalue_denoising():
    """
    图6: 协方差矩阵去噪效果
    """
    np.random.seed(42)

    n_samples, n_assets = 250, 100
    n_true_factors = 5

    # 生成真实协方差
    F = np.random.randn(n_assets, n_true_factors) * 0.3
    true_cov = F @ F.T + np.eye(n_assets) * 0.5

    L = np.linalg.cholesky(true_cov)
    returns = np.random.randn(n_samples, n_assets) @ L.T
    sample_cov = np.cov(returns.T)

    # 特征分解
    eigenvalues = np.linalg.eigvalsh(sample_cov)
    eigenvalues = np.sort(eigenvalues)[::-1]

    # MP边界
    gamma = n_assets / n_samples
    sigma_sq = np.median(eigenvalues)
    lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2

    # 去噪
    n_signal = np.sum(eigenvalues > lambda_plus)
    denoised_eigenvalues = eigenvalues.copy()
    noise_mean = eigenvalues[n_signal:].mean()
    denoised_eigenvalues[n_signal:] = noise_mean

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 去噪前
    ax1 = axes[0]
    colors = ['red' if e > lambda_plus else 'steelblue' for e in eigenvalues]
    ax1.bar(range(n_assets), eigenvalues, color=colors, alpha=0.7)
    ax1.axhline(y=lambda_plus, color='orange', linestyle='--', linewidth=2,
                label=f'MP上界 λ₊={lambda_plus:.3f}')
    ax1.axhline(y=sigma_sq, color='green', linestyle=':', linewidth=2,
                label=f'噪声方差 σ²={sigma_sq:.3f}')
    ax1.set_xlabel('特征值索引', fontsize=12)
    ax1.set_ylabel('特征值', fontsize=12)
    ax1.set_title(f'去噪前：样本协方差特征值\n{n_signal}个信号 + {n_assets-n_signal}个噪声', fontsize=14)
    ax1.legend(fontsize=10)

    # 去噪后
    ax2 = axes[1]
    colors_denoised = ['red' if i < n_signal else 'purple' for i in range(n_assets)]
    ax2.bar(range(n_assets), denoised_eigenvalues, color=colors_denoised, alpha=0.7)
    ax2.axhline(y=noise_mean, color='purple', linestyle='--', linewidth=2,
                label=f'噪声均值={noise_mean:.3f}')
    ax2.set_xlabel('特征值索引', fontsize=12)
    ax2.set_ylabel('特征值', fontsize=12)
    ax2.set_title(f'去噪后：噪声特征值收缩到均值\n保留{n_signal}个信号特征值', fontsize=14)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('06_eigenvalue_denoising.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 06_eigenvalue_denoising.png")


def plot_lasso_sparsity():
    """
    图7: LASSO稀疏性演示
    """
    np.random.seed(42)

    n_samples, n_features = 100, 50
    n_informative = 10

    true_coef = np.zeros(n_features)
    true_coef[:n_informative] = np.random.randn(n_informative)

    X = np.random.randn(n_samples, n_features)
    for i in range(n_informative, n_features):
        X[:, i] = X[:, i % n_informative] + np.random.randn(n_samples) * 0.1

    y = X @ true_coef + np.random.randn(n_samples) * 0.5

    # 各种回归
    ols = LinearRegression().fit(X, y)
    ridge = Ridge(alpha=1.0).fit(X, y)
    lasso = Lasso(alpha=0.1).fit(X, y)
    enet = ElasticNet(alpha=0.1, l1_ratio=0.5).fit(X, y)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    methods = [
        ('OLS', ols.coef_, 'blue'),
        ('Ridge (λ=1)', ridge.coef_, 'green'),
        ('LASSO (λ=0.1)', lasso.coef_, 'red'),
        ('ElasticNet', enet.coef_, 'purple')
    ]

    for ax, (name, coef, color) in zip(axes.flat, methods):
        # 柱状图
        bars = ax.bar(range(n_features), coef, color=color, alpha=0.7, label='估计')
        ax.scatter(range(n_features), true_coef, color='black', s=20, zorder=5, label='真实')

        # 标注稀疏性
        n_nonzero = np.sum(np.abs(coef) > 0.01)
        mse = np.mean((coef - true_coef)**2)

        ax.set_xlabel('特征索引', fontsize=11)
        ax.set_ylabel('系数值', fontsize=11)
        ax.set_title(f'{name}\n非零系数: {n_nonzero}, MSE: {mse:.4f}', fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.axhline(y=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('07_lasso_sparsity.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 07_lasso_sparsity.png")


def plot_factor_model():
    """
    图8: 因子模型协方差结构
    """
    np.random.seed(42)

    n_assets = 20
    n_factors = 3

    # 生成因子载荷
    loadings = np.random.randn(n_assets, n_factors) * 0.3
    loadings[:7, 0] += 0.5   # 行业1
    loadings[7:14, 1] += 0.5  # 行业2
    loadings[14:, 2] += 0.5   # 行业3

    # 因子协方差
    factor_cov = np.eye(n_factors)
    factor_cov[0, 1] = factor_cov[1, 0] = 0.3
    factor_cov[0, 2] = factor_cov[2, 0] = 0.1

    # 系统性协方差
    systematic = loadings @ factor_cov @ loadings.T

    # 特异性方差
    specific = np.diag(np.random.uniform(0.1, 0.3, n_assets))

    # 总协方差
    total_cov = systematic + specific

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 因子载荷热力图
    ax1 = axes[0, 0]
    im1 = ax1.imshow(loadings, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    ax1.set_xlabel('因子', fontsize=12)
    ax1.set_ylabel('资产', fontsize=12)
    ax1.set_title('因子载荷矩阵 B', fontsize=14)
    ax1.set_xticks(range(n_factors))
    ax1.set_xticklabels(['市场', '价值', '成长'])
    plt.colorbar(im1, ax=ax1)

    # 系统性协方差
    ax2 = axes[0, 1]
    im2 = ax2.imshow(systematic, cmap='viridis', aspect='auto')
    ax2.set_xlabel('资产', fontsize=12)
    ax2.set_ylabel('资产', fontsize=12)
    ax2.set_title('系统性协方差 BΣ_f B\'', fontsize=14)
    plt.colorbar(im2, ax=ax2)

    # 特异性方差
    ax3 = axes[1, 0]
    ax3.bar(range(n_assets), np.diag(specific), color='orange', alpha=0.7)
    ax3.set_xlabel('资产', fontsize=12)
    ax3.set_ylabel('特异性方差', fontsize=12)
    ax3.set_title('特异性方差 D (对角矩阵)', fontsize=14)

    # 总协方差
    ax4 = axes[1, 1]
    im4 = ax4.imshow(total_cov, cmap='viridis', aspect='auto')
    ax4.set_xlabel('资产', fontsize=12)
    ax4.set_ylabel('资产', fontsize=12)
    ax4.set_title('总协方差 Σ = BΣ_f B\' + D', fontsize=14)
    plt.colorbar(im4, ax=ax4)

    # 添加公式说明
    fig.text(0.5, 0.02, '因子模型：Σ = BΣ_f B\' + D，参数数量从 n²/2 降到 nk',
             ha='center', fontsize=12, style='italic')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig('08_factor_model.png', bbox_inches='tight')
    plt.close()
    print("✓ 生成 08_factor_model.png")


def main():
    """生成所有图表"""
    print("\n" + "=" * 50)
    print("Week 12 可视化生成")
    print("=" * 50 + "\n")

    plot_marchenko_pastur()     # 01
    plot_kalman_filter()        # 02
    plot_regularization_geometry()  # 03
    plot_cov_comparison()       # 04
    plot_shrinkage_concept()    # 05
    plot_eigenvalue_denoising() # 06
    plot_lasso_sparsity()       # 07
    plot_factor_model()         # 08

    print("\n" + "=" * 50)
    print("✓ 所有图表生成完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
