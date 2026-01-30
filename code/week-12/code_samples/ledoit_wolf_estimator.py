"""
Week 12 - 协方差矩阵收缩估计
Ledoit-Wolf收缩估计器和因子模型协方差

包含：
- compare_covariance_estimators(): 比较不同协方差估计方法
- factor_model_covariance(): 使用PCA构建因子模型协方差
"""

import numpy as np
from sklearn.covariance import LedoitWolf, ShrunkCovariance
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def compare_covariance_estimators(returns, true_cov=None):
    """
    比较不同协方差估计方法

    参数：
    - returns: 收益率数据 (n_samples, n_assets)
    - true_cov: 真实协方差（如果已知，用于评估）

    返回：
    - dict: 包含各估计方法的协方差矩阵和收缩参数
    """
    n_samples, n_assets = returns.shape

    # 1. 样本协方差
    sample_cov = np.cov(returns.T)

    # 2. Ledoit-Wolf收缩估计
    lw = LedoitWolf().fit(returns)
    lw_cov = lw.covariance_
    lw_shrinkage = lw.shrinkage_

    # 3. 固定收缩（向单位矩阵收缩）
    shrunk = ShrunkCovariance(shrinkage=0.2).fit(returns)
    shrunk_cov = shrunk.covariance_

    print(f"数据维度: {n_samples}样本 × {n_assets}资产")
    print(f"p/n比率: {n_assets/n_samples:.2f}")
    print(f"\nLedoit-Wolf最优收缩强度: {lw_shrinkage:.4f}")

    # 比较特征值分布
    eig_sample = np.linalg.eigvalsh(sample_cov)
    eig_lw = np.linalg.eigvalsh(lw_cov)

    print(f"\n特征值范围:")
    print(f"  样本协方差: [{eig_sample.min():.6f}, {eig_sample.max():.6f}]")
    print(f"  Ledoit-Wolf: [{eig_lw.min():.6f}, {eig_lw.max():.6f}]")
    print(f"\n条件数:")
    print(f"  样本协方差: {eig_sample.max()/max(eig_sample.min(), 1e-10):.2f}")
    print(f"  Ledoit-Wolf: {eig_lw.max()/eig_lw.min():.2f}")

    if true_cov is not None:
        # 计算Frobenius范数误差
        err_sample = np.linalg.norm(sample_cov - true_cov, 'fro')
        err_lw = np.linalg.norm(lw_cov - true_cov, 'fro')
        print(f"\nFrobenius范数误差:")
        print(f"  样本协方差: {err_sample:.4f}")
        print(f"  Ledoit-Wolf: {err_lw:.4f}")
        print(f"  改进: {(err_sample-err_lw)/err_sample*100:.1f}%")

    return {
        'sample': sample_cov,
        'ledoit_wolf': lw_cov,
        'shrinkage': lw_shrinkage
    }


def factor_model_covariance(returns, n_factors=5):
    """
    使用PCA构建因子模型协方差

    步骤：
    1. 对收益率做PCA提取因子
    2. 计算因子载荷和因子协方差
    3. 估计特异性方差

    参数：
    - returns: 收益率数据 (n_samples, n_assets)
    - n_factors: 因子数量

    返回：
    - factor_model_cov: 因子模型协方差矩阵
    - loadings: 因子载荷矩阵
    - factor_cov: 因子协方差矩阵
    """
    n_samples, n_assets = returns.shape

    # PCA提取因子
    pca = PCA(n_components=n_factors)
    factors = pca.fit_transform(returns)  # n_samples × n_factors

    # 因子载荷（还原到原始空间的系数）
    # 注意：sklearn的components_是V'，载荷需要乘以奇异值
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)  # n_assets × n_factors

    # 因子协方差
    factor_cov = np.cov(factors.T)  # n_factors × n_factors

    # 系统性协方差
    systematic_cov = loadings @ factor_cov @ loadings.T

    # 特异性方差（残差方差）
    residuals = returns - factors @ loadings.T
    specific_var = np.diag(np.var(residuals, axis=0))

    # 因子模型协方差
    factor_model_cov = systematic_cov + specific_var

    # 解释方差比例
    explained_var_ratio = pca.explained_variance_ratio_.sum()

    print(f"因子数: {n_factors}")
    print(f"累计解释方差: {explained_var_ratio*100:.1f}%")
    print(f"参数数量: {n_assets*n_factors + n_factors*(n_factors+1)//2 + n_assets}")
    print(f"完整协方差参数: {n_assets*(n_assets+1)//2}")

    return factor_model_cov, loadings, factor_cov


if __name__ == "__main__":
    # 模拟实验
    np.random.seed(42)
    n_assets, n_samples = 100, 150  # p/n = 0.67

    # 生成真实协方差矩阵（因子结构）
    n_factors = 5
    factor_loadings = np.random.randn(n_assets, n_factors) * 0.1
    specific_var = np.diag(np.random.uniform(0.01, 0.05, n_assets))
    true_cov = factor_loadings @ factor_loadings.T + specific_var

    # 生成模拟数据
    L = np.linalg.cholesky(true_cov)
    returns = np.random.randn(n_samples, n_assets) @ L.T

    # 比较估计方法
    print("=" * 60)
    print("协方差估计方法比较")
    print("=" * 60)
    results = compare_covariance_estimators(returns, true_cov)

    # 测试因子模型
    print("\n" + "=" * 60)
    print("因子模型协方差")
    print("=" * 60)
    factor_cov, loadings, f_cov = factor_model_covariance(returns, n_factors=5)

    # 验证正定性
    eigenvalues = np.linalg.eigvalsh(factor_cov)
    print(f"\n因子模型协方差特征值范围: [{eigenvalues.min():.6f}, {eigenvalues.max():.6f}]")
    print(f"条件数: {eigenvalues.max()/eigenvalues.min():.2f}")

    # 计算误差
    err_factor = np.linalg.norm(factor_cov - true_cov, 'fro')
    err_sample = np.linalg.norm(results['sample'] - true_cov, 'fro')
    print(f"\nFrobenius范数误差:")
    print(f"  样本协方差: {err_sample:.4f}")
    print(f"  因子模型: {err_factor:.4f}")
