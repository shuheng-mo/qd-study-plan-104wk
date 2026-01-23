import numpy as np


def make_positive_definite(cov_matrix, method="eigenvalue", epsilon=1e-6):
    """

    将半正定/非正定矩阵修复为正定矩阵

    方法：

    1. eigenvalue: 将负/零特征值替换为小正数

    2. diagonal: 对角线加小量

    3. nearest: 找最近的正定矩阵

    """

    if method == "eigenvalue":

        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        eigenvalues = np.maximum(eigenvalues, epsilon)

        return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

    elif method == "diagonal":

        min_eig = np.min(np.linalg.eigvalsh(cov_matrix))

        if min_eig < epsilon:

            cov_matrix = cov_matrix + (epsilon - min_eig) * np.eye(len(cov_matrix))

        return cov_matrix

    elif method == "nearest":

        # Higham算法的简化版本

        from scipy.linalg import sqrtm

        B = (cov_matrix + cov_matrix.T) / 2

        _, s, V = np.linalg.svd(B)

        H = V.T @ np.diag(s) @ V

        A2 = (B + H) / 2

        A3 = (A2 + A2.T) / 2

        # 确保正定

        min_eig = np.min(np.linalg.eigvalsh(A3))

        if min_eig < epsilon:

            A3 = A3 + (epsilon - min_eig) * np.eye(len(A3))

        return A3


# 测试修复方法

np.random.seed(42)

p, n = 100, 80  # p > n，矩阵奇异

returns = np.random.randn(n, p) * 0.02

cov_singular = np.cov(returns.T)

print(
    "原始矩阵特征值范围:",
    np.linalg.eigvalsh(cov_singular).min(),
    "到",
    np.linalg.eigvalsh(cov_singular).max(),
)

cov_fixed = make_positive_definite(cov_singular, method="eigenvalue")

print(
    "修复后特征值范围:",
    np.linalg.eigvalsh(cov_fixed).min(),
    "到",
    np.linalg.eigvalsh(cov_fixed).max(),
)

# 验证Cholesky分解

try:

    L = np.linalg.cholesky(cov_fixed)

    print("Cholesky分解成功！")

except:

    print("Cholesky分解失败")
