# SigmaX's 线性代数摸底测验参考答案

## 1. 给定向量a=(2,3), b=(4,1)，求

### a) a·b的值及其几何意义

$$\mathbf{a} \cdot \mathbf{b} = 2 \times 4 + 3 \times 1 = 8 + 3 = 11$$

**几何意义：**
点积衡量两个向量的"协同程度"：

- **正值(11>0)**：两向量夹角为锐角，方向大致相同
- 点积 = |a||b|cosθ，即"a的长度 × b的长度 × 方向一致性"
- 可理解为：a在b方向上的投影长度 × b的长度

---

### b) a在b方向上的投影长度

$$\text{proj}_{\mathbf{b}}\mathbf{a} = \frac{\mathbf{a} \cdot \mathbf{b}}{|\mathbf{b}|}$$

$$|\mathbf{b}| = \sqrt{4^2 + 1^2} = \sqrt{17}$$

$$\text{投影长度} = \frac{11}{\sqrt{17}} = \frac{11\sqrt{17}}{17} \approx 2.67$$

---

### c) 夹角余弦值

$$\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{|\mathbf{a}||\mathbf{b}|}$$

$$|\mathbf{a}| = \sqrt{2^2 + 3^2} = \sqrt{13}$$

$$\cos\theta = \frac{11}{\sqrt{13} \times \sqrt{17}} = \frac{11}{\sqrt{221}} \approx 0.74$$

对应夹角 θ ≈ 42.3°

---

## 2. 为什么在高维空间中，随机向量几乎总是正交的？

设两个n维随机向量 $\mathbf{x}, \mathbf{y}$，各分量独立同分布。

**夹角余弦：**
$$\cos\theta = \frac{\mathbf{x} \cdot \mathbf{y}}{|\mathbf{x}||\mathbf{y}|} = \frac{\sum_{i=1}^n x_i y_i}{\sqrt{\sum x_i^2}\sqrt{\sum y_i^2}}$$

| 项 | 行为 | 原因 |
|---|---|---|
| 分子 $\sum x_i y_i$ | ～ $O(\sqrt{n})$ | 中心极限定理，正负抵消 |
| 分母 $\|x\|\|y\|$ | ～ $O(n)$ | 大数定律，稳定增长 |
| cosθ | ～ $O(1/\sqrt{n})$ → 0 | 分子增长慢于分母 |

当 n → ∞ 时，cosθ → 0，即 θ → 90°。

**直观理解：** 高维空间"几乎所有方向都是垂直的"——可用的正交方向数量随维度指数增长。

### 这对推荐系统有什么启示？

1. **嵌入维度选择**
   - 维度太高：所有用户/物品向量都近似正交，相似度计算失去区分度
   - 维度太低：表达能力不足
   - 需要平衡：通常选择 50-300 维

2. **冷启动问题**
   - 新用户/物品的随机初始化向量与所有现有向量几乎正交
   - 点积推荐得分趋近于零，解释了冷启动困难的数学本质

3. **稀疏性诅咒**
   - 用户行为向量在高维空间中极度稀疏
   - 传统距离度量失效，需要降维或使用专门的相似度度量

---

## 3. 给定一个2×2矩阵A = ((2,0),(0,3)), 它对向量(1,1)做了什么几何变换？

$$A \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \begin{pmatrix} 2 & 0 \\ 0 & 3 \end{pmatrix} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \begin{pmatrix} 2 \\ 3 \end{pmatrix}$$

这是一个**各向异性缩放(Anisotropic Scaling)**：

```
    y                      y
    |                      |
    |  • (1,1)            |      • (2,3)
    |   \                  |       \
    |    \                 |        \
    +--------- x    →      +-------------- x
    
   原向量                  变换后
```

| 特性 | 说明 |
|-----|------|
| x方向 | 拉伸2倍 |
| y方向 | 拉伸3倍 |
| 长度变化 | $\sqrt{2}$ → $\sqrt{13}$ |
| 方向变化 | 45° → arctan(3/2) ≈ 56.3° |

**本质：** 对角矩阵沿坐标轴方向独立缩放，不改变坐标轴方向，但会改变非坐标轴方向向量的角度。

---

## 4. 什么样的矩阵能把一个圆变成椭圆？写出通解

### 通解

任何**可逆的2×2实矩阵**都能把圆变成椭圆（含特例：圆→圆）。

**标准形式（使用SVD分解）：**

$$A = U \Sigma V^T$$

其中：

- $U, V$ 是正交矩阵（旋转/反射）
- $\Sigma = \begin{pmatrix} \sigma_1 & 0 \\ 0 & \sigma_2 \end{pmatrix}$，$\sigma_1, \sigma_2 > 0$ 是奇异值

### 参数化通解

$$A = \begin{pmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{pmatrix} \begin{pmatrix} a & 0 \\ 0 & b \end{pmatrix} \begin{pmatrix} \cos\psi & -\sin\psi \\ \sin\psi & \cos\psi \end{pmatrix}^T$$

**参数意义：**

| 参数 | 意义 | 范围 |
|-----|------|------|
| a, b | 椭圆的半长轴、半短轴 | a, b > 0 |
| ψ | 输入空间旋转角 | [0, 2π) |
| φ | 输出椭圆主轴方向 | [0, 2π) |

### 具体例子

**最简形式（椭圆轴与坐标轴对齐）：**
$$A = \begin{pmatrix} a & 0 \\ 0 & b \end{pmatrix}, \quad a \neq b$$

单位圆 $x^2 + y^2 = 1$ → 椭圆 $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$

---

## 5. 为什么协方差矩阵一定是对称半正定的？从线性代数的角度证明(拔高题)

### 定义回顾

设随机向量 $\mathbf{X} = (X_1, ..., X_n)^T$，协方差矩阵：
$$\Sigma_{ij} = \text{Cov}(X_i, X_j) = E[(X_i - \mu_i)(X_j - \mu_j)]$$

### 证明对称性

$$\Sigma_{ij} = E[(X_i - \mu_i)(X_j - \mu_j)] = E[(X_j - \mu_j)(X_i - \mu_i)] = \Sigma_{ji}$$

乘法交换律直接保证 $\Sigma = \Sigma^T$。 ∎

### 证明半正定性

**方法一：直接证明**

对任意非零向量 $\mathbf{v} \in \mathbb{R}^n$：

$$\mathbf{v}^T \Sigma \mathbf{v} = \mathbf{v}^T E[(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^T] \mathbf{v}$$

$$= E[\mathbf{v}^T(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^T\mathbf{v}]$$

$$= E[(\mathbf{v}^T(\mathbf{X}-\boldsymbol{\mu}))^2]$$

设 $Y = \mathbf{v}^T(\mathbf{X}-\boldsymbol{\mu})$，这是一个标量随机变量，则：

$$\mathbf{v}^T \Sigma \mathbf{v} = E[Y^2] \geq 0$$

因为任何实数的平方的期望非负。 ∎

**方法二：Gram矩阵视角**

协方差矩阵可写成：
$$\Sigma = E[(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^T]$$

对于样本协方差矩阵：
$$S = \frac{1}{n-1}\sum_{k=1}^n (\mathbf{x}_k - \bar{\mathbf{x}})(\mathbf{x}_k - \bar{\mathbf{x}})^T = \frac{1}{n-1}BB^T$$

其中 $B$ 是中心化后的数据矩阵。

**关键定理：** 任何形如 $BB^T$ 的矩阵都是半正定的：
$$\mathbf{v}^T(BB^T)\mathbf{v} = (B^T\mathbf{v})^T(B^T\mathbf{v}) = \|B^T\mathbf{v}\|^2 \geq 0$$

### 物理意义

| 性质 | 意义 |
|-----|------|
| 对称性 | Cov(X,Y) = Cov(Y,X)，协变关系无方向 |
| 半正定 | 任何线性组合的方差 ≥ 0（方差不能为负） |
| 正定 | 变量间无完全线性相关（满秩） |
| 奇异(有0特征值) | 存在完全线性相关的变量组合 |
