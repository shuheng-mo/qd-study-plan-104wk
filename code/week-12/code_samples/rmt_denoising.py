"""
Week 12 - 随机矩阵理论与协方差矩阵去噪
Marchenko-Pastur分布和基于RMT的协方差去噪

包含：
- marchenko_pastur_pdf(): 计算MP分布的概率密度函数
- visualize_mp_distribution(): 可视化特征值分布与MP理论预测
- denoise_covariance_rmt(): 使用RMT对协方差矩阵去噪
"""

import numpy as np
import matplotlib.pyplot as plt


def marchenko_pastur_pdf(x, gamma, sigma=1.0):
    """
    Marchenko-Pastur分布的概率密度函数

    参数：
    - x: 特征值数组
    - gamma: p/n 比率（资产数/样本数）
    - sigma: 噪声标准差

    返回：
    - pdf: 概率密度值
    - lambda_minus: MP分布下界
    - lambda_plus: MP分布上界
    """
    lambda_plus = sigma**2 * (1 + np.sqrt(gamma))**2
    lambda_minus = sigma**2 * (1 - np.sqrt(gamma))**2

    pdf = np.zeros_like(x, dtype=float)
    mask = (x >= lambda_minus) & (x <= lambda_plus)

    pdf[mask] = (1 / (2 * np.pi * sigma**2 * gamma * x[mask])) * \
                np.sqrt((lambda_plus - x[mask]) * (x[mask] - lambda_minus))

    return pdf, lambda_minus, lambda_plus


def visualize_mp_distribution(n_samples=500, n_assets=200, n_factors=0, show_plot=True):
    """
    可视化特征值分布与MP理论预测

    参数：
    - n_samples: 样本数
    - n_assets: 资产数
    - n_factors: 因子数（0表示纯噪声）
    - show_plot: 是否显示图表

    返回：
    - eigenvalues: 特征值数组
    - lambda_plus: MP上界
    """
    np.random.seed(42)
    gamma = n_assets / n_samples

    if n_factors == 0:
        # 纯噪声数据
        X = np.random.randn(n_samples, n_assets)
        title = f"纯噪声数据 (p={n_assets}, n={n_samples}, γ={gamma:.2f})"
    else:
        # 有因子结构的数据
        # 生成因子
        F = np.random.randn(n_samples, n_factors)
        # 因子载荷
        B = np.random.randn(n_assets, n_factors) * 0.5
        # 噪声
        E = np.random.randn(n_samples, n_assets)
        # 收益率 = 因子贡献 + 噪声
        X = F @ B.T + E
        title = f"因子+噪声数据 (p={n_assets}, n={n_samples}, {n_factors}因子)"

    # 计算样本协方差矩阵
    cov_matrix = np.cov(X.T)
    eigenvalues = np.linalg.eigvalsh(cov_matrix)

    # MP理论预测
    x = np.linspace(0.001, eigenvalues.max() * 1.1, 1000)
    mp_pdf, lambda_minus, lambda_plus = marchenko_pastur_pdf(x, gamma)

    if show_plot:
        # 绘图
        fig, ax = plt.subplots(figsize=(12, 6))

        # 特征值直方图
        ax.hist(eigenvalues, bins=50, density=True, alpha=0.7,
                label='样本特征值分布', color='steelblue')

        # MP理论分布
        ax.plot(x, mp_pdf, 'r-', linewidth=2, label='Marchenko-Pastur理论分布')

        # 标注边界
        ax.axvline(lambda_minus, color='green', linestyle='--',
                   label=f'λ₋ = {lambda_minus:.3f}')
        ax.axvline(lambda_plus, color='orange', linestyle='--',
                   label=f'λ₊ = {lambda_plus:.3f}')

        # 标注超出MP边界的特征值数量
        n_signal = np.sum(eigenvalues > lambda_plus)
        if n_signal > 0:
            ax.annotate(f'{n_signal}个特征值\n超出噪声边界',
                       xy=(lambda_plus * 1.1, 0.3),
                       fontsize=12, color='red')

        ax.set_xlabel('特征值', fontsize=12)
        ax.set_ylabel('概率密度', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.legend(fontsize=10)
        ax.set_xlim(0, eigenvalues.max() * 1.1)

        plt.tight_layout()
        plt.show()

    return eigenvalues, lambda_plus


def denoise_covariance_rmt(cov_matrix, n_samples, method='shrink'):
    """
    使用随机矩阵理论对协方差矩阵去噪

    参数：
    - cov_matrix: 样本协方差矩阵
    - n_samples: 样本数量
    - method: 去噪方法
        - 'truncate': 将噪声特征值设为均值
        - 'shrink': 将噪声特征值向均值收缩

    返回：
    - cov_denoised: 去噪后的协方差矩阵
    - n_signal: 识别的信号特征值数量
    """
    n_assets = cov_matrix.shape[0]
    gamma = n_assets / n_samples

    # 特征分解
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # 排序（从大到小）
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # 估计噪声方差σ²（使用中位数，更稳健）
    sigma_sq = np.median(eigenvalues)

    # MP边界
    lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2

    # 识别信号特征值
    n_signal = np.sum(eigenvalues > lambda_plus)
    print(f"识别到 {n_signal} 个信号特征值（共{n_assets}个）")

    # 去噪
    eigenvalues_denoised = eigenvalues.copy()

    if method == 'truncate':
        # 截断：将噪声特征值设为均值
        noise_mean = eigenvalues[n_signal:].mean() if n_signal < n_assets else eigenvalues[-1]
        eigenvalues_denoised[n_signal:] = noise_mean

    elif method == 'shrink':
        # 收缩：将噪声特征值向均值收缩
        if n_signal < n_assets:
            noise_eigenvalues = eigenvalues[n_signal:]
            noise_mean = noise_eigenvalues.mean()
            # 收缩公式
            shrinkage = 0.5
            eigenvalues_denoised[n_signal:] = shrinkage * noise_mean + \
                                              (1-shrinkage) * noise_eigenvalues

    # 保持矩阵迹不变（可选）
    trace_original = eigenvalues.sum()
    trace_denoised = eigenvalues_denoised.sum()
    eigenvalues_denoised *= trace_original / trace_denoised

    # 重构协方差矩阵
    cov_denoised = eigenvectors @ np.diag(eigenvalues_denoised) @ eigenvectors.T

    return cov_denoised, n_signal


if __name__ == "__main__":
    # 示例1：纯噪声情况
    print("=== 纯噪声数据 ===")
    eig_noise, lambda_plus_noise = visualize_mp_distribution(n_factors=0, show_plot=False)
    print(f"超出MP上界的特征值: {np.sum(eig_noise > lambda_plus_noise)}")

    # 示例2：有信号情况
    print("\n=== 有5个因子的数据 ===")
    eig_signal, lambda_plus_signal = visualize_mp_distribution(n_factors=5, show_plot=False)
    print(f"超出MP上界的特征值: {np.sum(eig_signal > lambda_plus_signal)}")

    # 示例3：测试去噪效果
    print("\n" + "=" * 60)
    print("协方差矩阵去噪测试")
    print("=" * 60)

    np.random.seed(42)
    n_samples, n_assets = 250, 100
    n_true_factors = 5

    # 生成真实协方差（因子结构）
    F = np.random.randn(n_assets, n_true_factors) * 0.3
    true_cov = F @ F.T + np.eye(n_assets) * 0.5

    # 生成样本数据
    L = np.linalg.cholesky(true_cov)
    returns = np.random.randn(n_samples, n_assets) @ L.T
    sample_cov = np.cov(returns.T)

    # 去噪
    denoised_cov, n_signal = denoise_covariance_rmt(sample_cov, n_samples, method='shrink')

    # 比较误差
    err_sample = np.linalg.norm(sample_cov - true_cov, 'fro')
    err_denoised = np.linalg.norm(denoised_cov - true_cov, 'fro')

    print(f"\n与真实协方差的Frobenius距离:")
    print(f"  样本协方差: {err_sample:.4f}")
    print(f"  去噪协方差: {err_denoised:.4f}")
    print(f"  改进: {(err_sample - err_denoised) / err_sample * 100:.1f}%")
