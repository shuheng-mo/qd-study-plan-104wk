## 104周转行Quant | W12 - 线性代数进阶（下）

> 上周Victor留下的"协方差矩阵估计"难题，本周终于迎来破解之道。从Ledoit-Wolf收缩估计到随机矩阵理论的噪声过滤，从卡尔曼滤波的递归优雅到正则化回归的几何直觉，SigmaX团队第一次感受到"高维统计"的魅力。当Carol用Marchenko-Pastur分布识别出协方差矩阵中的噪声特征值，当Eric用卡尔曼滤波捕捉到时变的市场贝塔，量化研究的视野正在向更深处延伸。

> 本期关键词：收缩估计、Ledoit-Wolf、因子模型、随机矩阵理论、Marchenko-Pastur分布、协方差去噪、卡尔曼滤波、状态空间模型、岭回归、LASSO、弹性网络

## 🎯收缩估计：在样本与结构之间平衡

周一早上，Victor带着一本厚厚的论文走进培训室。

> "上周我们看到了样本协方差矩阵的灾难性问题。今天，我要介绍一个优雅的解决方案——**收缩估计**。"

他在白板上画了一个示意图：

```
收缩估计的直觉：

样本协方差 Σ_sample ←――收缩――→ 结构化目标 F
      ↓                           ↓
   信息丰富                    稳定但有偏
   但噪声大
      ↓                           ↓
      └―――→ 最优组合 Σ_shrink ←―――┘
           = αF + (1-α)Σ_sample
```

Alice问："结构化目标是什么意思？"

> "好问题。结构化目标是一个我们**假设**的协方差结构，它参数少、稳定，但可能不够准确。常见的选择有："

```
常见的收缩目标 F：

1. 单位矩阵：F = σ²I
   - 假设所有资产波动率相同、不相关
   - 最简单但最不准确

2. 对角矩阵：F = diag(σ₁², σ₂², ..., σₙ²)
   - 保留个体波动率，假设不相关
   - 比单位矩阵更准确

3. 单因子模型：F = βββᵀσ_m² + D
   - 假设所有相关性来自市场因子
   - 金融中最常用
```

### Ledoit-Wolf收缩估计

Victor继续讲解：

> "2004年，Ledoit和Wolf提出了一个**自动确定收缩强度**的方法，被称为Ledoit-Wolf估计器。"

```
Ledoit-Wolf收缩估计：

Σ_LW = α*F + (1-α)*Σ_sample

其中收缩强度α由以下公式确定（最小化预期损失）：

α = min(1, max(0, (κ - n/p) / ((n+1-2/p)(κ-1) + n)))

κ是样本四阶矩与协方差的比值

直觉：
- 样本量n越小 → α越大（更多收缩）
- 资产数p越大 → α越大（更多收缩）
- 数据越不正态 → 收缩强度自动调整
```

Bob问："这个公式看起来很复杂，实际中怎么用？"

> "sklearn已经帮我们实现好了。"

```python
# 完整代码: code/week-12/code_samples/ledoit_wolf_estimator.py

from sklearn.covariance import LedoitWolf, ShrunkCovariance

def compare_covariance_estimators(returns, true_cov=None):
    """比较不同协方差估计方法"""
    # 1. 样本协方差
    sample_cov = np.cov(returns.T)

    # 2. Ledoit-Wolf收缩估计
    lw = LedoitWolf().fit(returns)
    lw_cov = lw.covariance_
    lw_shrinkage = lw.shrinkage_

    # 3. 固定收缩（向单位矩阵收缩）
    shrunk = ShrunkCovariance(shrinkage=0.2).fit(returns)
    shrunk_cov = shrunk.covariance_

    # 比较特征值分布和误差...
    return {'sample': sample_cov, 'ledoit_wolf': lw_cov, 'shrinkage': lw_shrinkage}
```

Carol惊讶地说："Ledoit-Wolf估计器自动把条件数从几千降到了几十！"

> "对。收缩的本质是**正则化**——通过牺牲一点准确性，换取巨大的稳定性提升。"

### 因子模型协方差

Victor继续介绍另一种方法：

> "收缩估计是**事后**修正样本协方差。另一种思路是**事先**假设协方差有因子结构。"

```
因子模型协方差：

假设收益率由因子驱动：
r = Bf + ε

其中：
- r: n×1 资产收益向量
- B: n×k 因子载荷矩阵
- f: k×1 因子收益向量
- ε: n×1 特异性收益（假设不相关）

则协方差矩阵为：
Σ = BΣ_f B' + D

其中：
- Σ_f: k×k 因子协方差
- D: n×n 对角矩阵（特异性方差）

参数数量对比：
- 完整协方差: n(n+1)/2 ≈ n²/2
- 因子模型: nk + k(k+1)/2 + n ≈ nk

当n=500, k=10：
- 完整: 125,250个参数
- 因子: 5,055个参数（减少96%！）
```

```python
# 完整代码: code/week-12/code_samples/ledoit_wolf_estimator.py

from sklearn.decomposition import PCA

def factor_model_covariance(returns, n_factors=5):
    """使用PCA构建因子模型协方差"""
    # PCA提取因子
    pca = PCA(n_components=n_factors)
    factors = pca.fit_transform(returns)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    
    # 因子协方差 + 特异性方差
    factor_cov = np.cov(factors.T)
    systematic_cov = loadings @ factor_cov @ loadings.T
    residuals = returns - factors @ loadings.T
    specific_var = np.diag(np.var(residuals, axis=0))
    
    return systematic_cov + specific_var, loadings, factor_cov
```

## 📊随机矩阵理论：区分信号与噪声

周二，Victor的课进入了更深的水域。

> "今天的内容有点数学，但非常powerful——**随机矩阵理论**（Random Matrix Theory, RMT）。它告诉我们如何识别协方差矩阵中的**真实结构**和**纯粹噪声**。"

他在白板上写下一个著名的定理：

```
Marchenko-Pastur定律：

设X是一个n×p的随机矩阵，每个元素独立同分布，均值0，方差σ²。
样本协方差矩阵 S = X'X/n

当n, p → ∞，p/n → γ（0 < γ < 1）时，
S的特征值分布收敛到Marchenko-Pastur分布：

           1
f(λ) = ――――――――― √[(λ₊-λ)(λ-λ₋)]
        2πσ²γλ

特征值的边界：
λ₊ = σ²(1 + √γ)²   （最大特征值）
λ₋ = σ²(1 - √γ)²   （最小特征值）
```

Eric皱眉："这在说什么？"

> "简单说：如果数据是**纯噪声**（没有任何结构），那么协方差矩阵的特征值分布有一个**确定的形状**。任何超出这个分布的特征值，才可能代表**真实的信号**。"

![Marchenko-Pastur分布](code/week-12/visualizations/01_marchenko_pastur.png)

```python
# 完整代码: code/week-12/code_samples/rmt_denoising.py

def marchenko_pastur_pdf(x, gamma, sigma=1.0):
    """Marchenko-Pastur分布的概率密度函数"""
    lambda_plus = sigma**2 * (1 + np.sqrt(gamma))**2
    lambda_minus = sigma**2 * (1 - np.sqrt(gamma))**2
    
    pdf = np.zeros_like(x)
    mask = (x >= lambda_minus) & (x <= lambda_plus)
    pdf[mask] = (1 / (2 * np.pi * sigma**2 * gamma * x[mask])) * \
                np.sqrt((lambda_plus - x[mask]) * (x[mask] - lambda_minus))
    
    return pdf, lambda_minus, lambda_plus

def visualize_mp_distribution(n_samples=500, n_assets=200, n_factors=0):
    """可视化特征值分布与MP理论预测"""
    gamma = n_assets / n_samples
    
    # 生成数据（纯噪声或因子+噪声）
    if n_factors == 0:
        X = np.random.randn(n_samples, n_assets)
    else:
        F = np.random.randn(n_samples, n_factors)
        B = np.random.randn(n_assets, n_factors) * 0.5
        E = np.random.randn(n_samples, n_assets)
        X = F @ B.T + E
    
    # 计算特征值并与MP理论对比
    cov_matrix = np.cov(X.T)
    eigenvalues = np.linalg.eigvalsh(cov_matrix)
    # ...绘图代码
```

Alice恍然大悟："所以超出MP边界的特征值才是真正的'信号'，边界内的都是噪声！"

> "完全正确。这给了我们一个**科学的方法**来决定保留多少特征值。"

### 协方差矩阵去噪

Victor接着讲解如何利用RMT对协方差矩阵去噪：

```
协方差矩阵去噪策略：

1. 计算样本协方差的特征分解：Σ = VΛV'
2. 确定MP边界：λ₊ = σ²(1 + √(p/n))²
3. 处理噪声特征值：
   - 方法A：截断（删除λ < λ₊的特征向量）
   - 方法B：收缩（将λ < λ₊的特征值收缩到均值）
   - 方法C：保持迹不变的调整
4. 重构：Σ_denoised = VΛ_adjusted V'
```

```python
# 完整代码: code/week-12/code_samples/rmt_denoising.py

def denoise_covariance_rmt(cov_matrix, n_samples, method='shrink'):
    """使用随机矩阵理论对协方差矩阵去噪"""
    n_assets = cov_matrix.shape[0]
    gamma = n_assets / n_samples
    
    # 特征分解
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # MP边界
    sigma_sq = np.median(eigenvalues)
    lambda_plus = sigma_sq * (1 + np.sqrt(gamma))**2
    
    # 识别并处理噪声特征值
    n_signal = np.sum(eigenvalues > lambda_plus)
    eigenvalues_denoised = eigenvalues.copy()
    if method == 'shrink' and n_signal < n_assets:
        noise_mean = eigenvalues[n_signal:].mean()
        eigenvalues_denoised[n_signal:] = 0.5 * noise_mean + 0.5 * eigenvalues[n_signal:]
    
    # 重构协方差矩阵
    return eigenvectors @ np.diag(eigenvalues_denoised) @ eigenvectors.T, n_signal
```

## 🔄卡尔曼滤波：递归估计的优雅

周三，Victor开始讲解一个全新的话题。

> "之前我们讨论的都是**静态**估计。但金融市场是**动态**的——相关性在变化，贝塔在漂移。今天我们学习一个处理动态系统的强大工具：**卡尔曼滤波**。"

他在白板上写下状态空间模型：

```
状态空间模型：

状态方程（系统如何演化）：
x_t = A·x_{t-1} + w_t,  w_t ~ N(0, Q)

观测方程（我们能观察到什么）：
y_t = C·x_t + v_t,      v_t ~ N(0, R)

其中：
- x_t: 隐藏状态（我们想估计的）
- y_t: 观测值（我们能看到的）
- A: 状态转移矩阵
- C: 观测矩阵
- Q: 过程噪声协方差
- R: 观测噪声协方差
```

Bob问："这和投资有什么关系？"

> "太多了！比如：
>
> - **时变贝塔**：股票对市场的敏感度在变化
> - **配对交易**：两只股票的价差是均值回复的
> - **动态因子**：因子暴露随时间变化"

![卡尔曼滤波示意](code/week-12/visualizations/02_kalman_filter.png)

```
卡尔曼滤波的两步递归：

=== 预测步（Predict）===
状态预测：x̂_t|t-1 = A·x̂_{t-1|t-1}
协方差预测：P_t|t-1 = A·P_{t-1|t-1}·A' + Q

=== 更新步（Update）===
创新（预测误差）：ε_t = y_t - C·x̂_t|t-1
创新协方差：S_t = C·P_t|t-1·C' + R
卡尔曼增益：K_t = P_t|t-1·C'·S_t⁻¹
状态更新：x̂_t|t = x̂_t|t-1 + K_t·ε_t
协方差更新：P_t|t = (I - K_t·C)·P_t|t-1

关键洞察：
- 卡尔曼增益K是"信任"数据vs"信任模型"的权衡
- K大：更信任新观测
- K小：更信任预测
```

Carol问："为什么叫'增益'？"

> "因为K决定了新观测对估计的'增益'或影响程度。如果观测噪声很大（R大），K就小，新观测的影响就小；如果模型不确定性大（P大），K就大，我们更愿意相信数据。"

### 时变贝塔估计

Victor用一个具体例子来说明：

```python
# 完整代码: code/week-12/code_samples/kalman_filter.py

class KalmanFilter:
    """通用卡尔曼滤波器"""
    def __init__(self, A, C, Q, R, x0, P0):
        self.A = np.atleast_2d(A)
        self.C = np.atleast_2d(C)
        self.Q = np.atleast_2d(Q)
        self.R = np.atleast_2d(R)
        self.x = np.atleast_1d(x0).reshape(-1, 1)
        self.P = np.atleast_2d(P0)

    def predict(self):
        """预测步"""
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q
        return self.x.flatten()

    def update(self, y):
        """更新步"""
        y = np.atleast_1d(y).reshape(-1, 1)
        innovation = y - self.C @ self.x
        S = self.C @ self.P @ self.C.T + self.R
        K = self.P @ self.C.T @ np.linalg.inv(S)
        self.x = self.x + K @ innovation
        self.P = (np.eye(self.n_states) - K @ self.C) @ self.P
        return self.x.flatten(), K

def estimate_time_varying_beta(stock_returns, market_returns):
    """使用卡尔曼滤波估计时变贝塔"""
    n_obs = len(stock_returns)
    A = np.eye(2)  # 随机游走
    Q = np.diag([0.0001, 0.001])  # 过程噪声
    R = np.array([[np.var(stock_returns) * 0.5]])
    x, P = np.array([0.0, 1.0]).reshape(-1, 1), np.eye(2)
    
    alphas, betas = np.zeros(n_obs), np.zeros(n_obs)
    for t in range(n_obs):
        C = np.array([[1, market_returns[t]]])
        # 预测和更新步骤...
        alphas[t], betas[t] = x[0, 0], x[1, 0]
    return alphas, betas
```

Eric看着结果说："卡尔曼滤波的跟踪比滚动窗口平滑多了，而且误差更小！"

> "对。卡尔曼滤波的优势是：
>
> 1. **自适应平滑**：根据数据噪声自动调整
> 2. **无需选择窗口**：避免了窗口长度的trade-off
> 3. **实时估计**：每个时刻都有最优估计"

## 📐正则化回归：另一个视角

周四，Victor转向正则化回归。

> "我们讲了协方差矩阵的正则化（收缩估计）。现在来看回归问题中的正则化。核心思想是一样的——**约束复杂度，换取稳定性**。"

```
正则化回归家族：

1. 岭回归（Ridge）: ||y - Xβ||² + λ||β||²
   - L2惩罚
   - 解：β = (X'X + λI)⁻¹X'y
   - 特点：系数收缩但不会变成0

2. LASSO: ||y - Xβ||² + λ||β||₁
   - L1惩罚
   - 无闭式解，需迭代算法
   - 特点：产生稀疏解（部分系数为0）

3. 弹性网络（Elastic Net）: ||y - Xβ||² + λ₁||β||₁ + λ₂||β||²
   - L1 + L2惩罚
   - 结合两者优点
```

![正则化几何](code/week-12/visualizations/03_regularization_geometry.png)

```python
# 完整代码: code/week-12/code_samples/regularized_regression.py

from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression

def demonstrate_regularization():
    """演示正则化回归"""
    # 生成多重共线性数据
    n_samples, n_features = 100, 50
    n_informative = 10
    true_coef = np.zeros(n_features)
    true_coef[:n_informative] = np.random.randn(n_informative)
    
    X = np.random.randn(n_samples, n_features)
    for i in range(n_informative, n_features):
        X[:, i] = X[:, i % n_informative] + np.random.randn(n_samples) * 0.1
    y = X @ true_coef + np.random.randn(n_samples) * 0.5

    # 比较不同方法
    ols = LinearRegression().fit(X, y)
    ridge = Ridge(alpha=1.0).fit(X, y)
    lasso = Lasso(alpha=0.1).fit(X, y)
    enet = ElasticNet(alpha=0.1, l1_ratio=0.5).fit(X, y)
    
    # 打印误差和稀疏性...
```

Alice问："岭回归和协方差收缩有什么联系？"

> "好问题！它们在数学上是等价的。"

```
岭回归与协方差收缩的联系：

岭回归解：β = (X'X + λI)⁻¹X'y

注意到 X'X 正是（未归一化的）样本协方差结构！

(X'X + λI)⁻¹ 本质上是在对 X'X 做"对角加扰"：
- λI 把 X'X 向单位矩阵收缩
- λ 越大，收缩越强，解越稳定

协方差收缩版本：
Σ_shrunk = (1-α)Σ_sample + α·diag(Σ_sample)

岭回归版本：
(X'X)_ridge = X'X + λI

两者都是在解决同一个问题：
高维情况下矩阵求逆的不稳定性！
```

### 因子选择中的LASSO应用

Victor展示了LASSO在量化研究中的应用：

```python
# 完整代码: code/week-12/code_samples/regularized_regression.py

from sklearn.linear_model import LassoCV

def factor_selection_lasso(returns, factor_returns, factor_names):
    """使用LASSO进行因子选择"""
    # 交叉验证选择最优λ
    lasso_cv = LassoCV(cv=5, random_state=42)
    lasso_cv.fit(factor_returns, returns)
    
    # 获取选中的因子
    selected_mask = np.abs(lasso_cv.coef_) > 1e-6
    selected_factors = [name for name, selected in zip(factor_names, selected_mask) if selected]
    
    print(f"最优正则化参数: {lasso_cv.alpha_:.4f}")
    print(f"选中的因子: {selected_factors}")
    return lasso_cv, selected_factors
```

## 💼综合实战：稳健投资组合构建

周五，Victor带大家做最后的综合项目。

> "我们把这两周学的东西都用上：收缩估计、去噪协方差、动态估计...构建一个**稳健的投资组合**。"

```python
# 完整代码: code/week-12/code_samples/robust_portfolio_manager.py

import cvxpy as cp
from sklearn.covariance import LedoitWolf

class RobustPortfolioManager:
    """稳健投资组合管理器"""
    
    def __init__(self, returns_data, cov_method='ledoit_wolf'):
        self.returns = returns_data.values
        self.n_assets = len(returns_data.columns)
        self.cov_method = cov_method
        self.expected_returns = self.returns.mean(axis=0) * 252
        self._estimate_covariance()
    
    def _estimate_covariance(self):
        """支持sample/ledoit_wolf/factor/rmt_denoise四种方法"""
        if self.cov_method == 'ledoit_wolf':
            lw = LedoitWolf().fit(self.returns)
            self.cov_matrix = lw.covariance_ * 252
        # ...其他方法
    
    def optimize(self, target_return=None, max_weight=0.2):
        """最小方差优化"""
        w = cp.Variable(self.n_assets)
        objective = cp.Minimize(cp.quad_form(w, self.cov_matrix))
        constraints = [cp.sum(w) == 1, w >= 0, w <= max_weight]
        problem = cp.Problem(objective, constraints)
        problem.solve()
        return w.value
    
    def backtest(self, test_returns, weights):
        """计算样本外表现"""
        portfolio_returns = test_returns @ weights
        annual_return = portfolio_returns.mean() * 252
        annual_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe = annual_return / annual_vol
        # ...计算最大回撤等指标
```

![不同协方差估计方法比较](code/week-12/visualizations/04_cov_comparison.png)

Carol看着结果说："Ledoit-Wolf和RMT去噪的夏普比率明显更高！"

> "是的。样本协方差在样本外表现最差，因为它**过拟合**了训练数据中的噪声。正则化方法通过牺牲一点样本内准确性，获得了更好的泛化能力。"

## 📒本周总结

本周是线性代数进阶的第二周，重点从协方差估计到动态建模，完成了量化投资中线性代数应用的完整闭环。

我们跟随Victor完成了以下核心内容：

1. **协方差矩阵的正则化估计**
   - 收缩估计的直觉：在样本信息与结构约束之间平衡
   - Ledoit-Wolf：自动确定最优收缩强度
   - 因子模型：通过降维大幅减少参数
   - 参数数量从n²降到nk

2. **随机矩阵理论初步**
   - Marchenko-Pastur分布：纯噪声矩阵的特征值分布
   - MP边界：λ± = σ²(1 ± √(p/n))²
   - 识别信号vs噪声：超出边界的特征值才是信号
   - 协方差矩阵去噪：截断或收缩噪声特征值

3. **卡尔曼滤波**
   - 状态空间模型：隐藏状态 + 观测方程
   - 两步递归：预测 + 更新
   - 卡尔曼增益：数据vs模型的信任权衡
   - 应用：时变贝塔估计、配对交易

4. **正则化回归**
   - 岭回归：L2惩罚，系数收缩但不为零
   - LASSO：L1惩罚，产生稀疏解
   - 弹性网络：结合两者优点
   - 与协方差收缩的数学联系

**稳健性是量化研究的核心**。这两周我们学会了如何应对高维统计的挑战：收缩、去噪、正则化，本质上都是在**约束复杂度、换取稳定性**。在金融数据普遍噪声大、样本少的背景下，这些工具是构建稳健策略的基石。

本周的代码实现和练习已上传至Github仓库：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)

**下周预告：W13 - C++ STL容器基础（上）**

下周我们将重返C++的世界，深度解析C++的标准模板库（STL）容器，争取用两周的时间就打下一个坚实的基础。

各位下周五见👋！
