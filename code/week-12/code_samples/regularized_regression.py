"""
Week 12 - 正则化回归
岭回归、LASSO、弹性网络与因子选择

包含：
- demonstrate_regularization(): 演示正则化回归方法对比
- factor_selection_lasso(): 使用LASSO进行因子选择
"""

import numpy as np
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression, LassoCV
import matplotlib.pyplot as plt


def demonstrate_regularization(show_plot=True):
    """
    演示正则化回归

    比较OLS、Ridge、LASSO、ElasticNet在多重共线性数据上的表现
    """
    np.random.seed(42)

    # 生成数据：多重共线性
    n_samples, n_features = 100, 50
    n_informative = 10  # 只有10个真正有用的特征

    # 真实系数
    true_coef = np.zeros(n_features)
    true_coef[:n_informative] = np.random.randn(n_informative)

    # 生成特征（有共线性）
    X = np.random.randn(n_samples, n_features)
    # 添加共线性
    for i in range(n_informative, n_features):
        X[:, i] = X[:, i % n_informative] + np.random.randn(n_samples) * 0.1

    # 生成目标
    y = X @ true_coef + np.random.randn(n_samples) * 0.5

    # 普通最小二乘
    ols = LinearRegression().fit(X, y)

    # 岭回归
    ridge = Ridge(alpha=1.0).fit(X, y)

    # LASSO
    lasso = Lasso(alpha=0.1).fit(X, y)

    # 弹性网络
    enet = ElasticNet(alpha=0.1, l1_ratio=0.5).fit(X, y)

    if show_plot:
        # 比较系数
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        methods = [
            ('OLS', ols.coef_),
            ('Ridge (λ=1)', ridge.coef_),
            ('LASSO (λ=0.1)', lasso.coef_),
            ('ElasticNet', enet.coef_)
        ]

        for ax, (name, coef) in zip(axes.flat, methods):
            # 估计系数
            markerline, stemlines, baseline = ax.stem(
                range(n_features), coef,
                linefmt='b-', markerfmt='bo', basefmt='k-'
            )
            plt.setp(stemlines, alpha=0.7)
            plt.setp(markerline, markersize=4)

            # 真实系数
            markerline2, stemlines2, baseline2 = ax.stem(
                range(n_features), true_coef,
                linefmt='r--', markerfmt='r^', basefmt='k-'
            )
            plt.setp(stemlines2, alpha=0.5)
            plt.setp(markerline2, markersize=4)

            ax.set_xlabel('特征索引')
            ax.set_ylabel('系数值')
            ax.set_title(f'{name}\n非零系数: {np.sum(np.abs(coef) > 0.01)}, '
                        f'MSE: {np.mean((coef - true_coef)**2):.4f}')
            ax.legend(['估计', '真实'], loc='upper right')

        plt.tight_layout()
        plt.show()

    # 打印统计
    print("系数估计误差 (MSE):")
    print(f"  OLS: {np.mean((ols.coef_ - true_coef)**2):.4f}")
    print(f"  Ridge: {np.mean((ridge.coef_ - true_coef)**2):.4f}")
    print(f"  LASSO: {np.mean((lasso.coef_ - true_coef)**2):.4f}")
    print(f"  ElasticNet: {np.mean((enet.coef_ - true_coef)**2):.4f}")

    print("\n非零系数数量:")
    print(f"  真实: {n_informative}")
    print(f"  LASSO: {np.sum(np.abs(lasso.coef_) > 0.01)}")
    print(f"  ElasticNet: {np.sum(np.abs(enet.coef_) > 0.01)}")

    return {
        'ols': ols.coef_,
        'ridge': ridge.coef_,
        'lasso': lasso.coef_,
        'elasticnet': enet.coef_,
        'true': true_coef
    }


def factor_selection_lasso(returns, factor_returns, factor_names):
    """
    使用LASSO进行因子选择

    参数：
    - returns: 资产收益率序列
    - factor_returns: 因子收益率矩阵 (n_samples, n_factors)
    - factor_names: 因子名称列表

    返回：
    - lasso_cv: 训练好的LassoCV模型
    - selected_factors: 选中的因子名称列表
    """
    # 使用交叉验证选择最优λ
    lasso_cv = LassoCV(cv=5, random_state=42)
    lasso_cv.fit(factor_returns, returns)

    # 获取选中的因子
    selected_mask = np.abs(lasso_cv.coef_) > 1e-6
    selected_factors = [name for name, selected in zip(factor_names, selected_mask) if selected]

    print(f"最优正则化参数: {lasso_cv.alpha_:.4f}")
    print(f"选中的因子 ({len(selected_factors)}/{len(factor_names)}):")
    for name, coef in zip(factor_names, lasso_cv.coef_):
        if abs(coef) > 1e-6:
            print(f"  {name}: {coef:.4f}")

    return lasso_cv, selected_factors


if __name__ == "__main__":
    # 示例1：正则化回归对比
    print("=" * 60)
    print("正则化回归方法对比")
    print("=" * 60)
    results = demonstrate_regularization(show_plot=False)

    # 示例2：LASSO因子选择
    print("\n" + "=" * 60)
    print("LASSO因子选择")
    print("=" * 60)

    np.random.seed(42)
    n_days = 500
    factor_names = ['市场', '规模', '价值', '动量', '质量',
                    '波动率', '流动性', '噪声1', '噪声2', '噪声3']
    n_factors = len(factor_names)

    # 生成因子收益（前5个是真实因子）
    factor_returns = np.random.randn(n_days, n_factors) * 0.01

    # 真实的因子暴露
    true_exposures = np.array([1.0, 0.5, -0.3, 0.2, 0.4, 0, 0, 0, 0, 0])

    # 生成资产收益
    asset_returns = factor_returns @ true_exposures + np.random.randn(n_days) * 0.005

    # LASSO因子选择
    lasso_model, selected = factor_selection_lasso(asset_returns, factor_returns, factor_names)

    print(f"\n真实有效因子: {factor_names[:5]}")
    print(f"LASSO选中因子: {selected}")
