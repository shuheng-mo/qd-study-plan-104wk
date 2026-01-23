## 104周转行Quant | W11 - 线性代数进阶（上）

> 矩阵分解告一段落，Victor开始传授"优化的艺术"。从矩阵微积分的链式法则到拉格朗日乘数的约束优化，从Cholesky分解的蒙特卡洛魔法到协方差矩阵的维度诅咒，这周的内容让SigmaX团队第一次感受到数学**优化**的艺术。当Alice用cvxpy自动求解带约束的组合优化，当Carol用Cholesky分解模拟出1万条相关资产路径，量化研究的大门正在缓缓打开。

> 本期关键词：矩阵微积分、梯度向量、Hessian矩阵、二次规划、拉格朗日乘数法、KKT条件、Cholesky分解、蒙特卡洛模拟、VaR、协方差矩阵正定性

## 🧮矩阵求导：优化的语言

周一早上，Victor准时出现在培训室。

他看了一眼每个人桌上的笔记本，满意地点点头——上周的投资组合优化作业，大家都认真完成了。

> "上周我们推导了最小方差组合的解析解。谁还记得那个公式？"

Alice举手：

> "w* = Σ⁻¹1 / (1ᵀΣ⁻¹1)，最优权重等于协方差矩阵的逆乘以全1向量，再归一化。"

> "对。但你们有没有想过，这个公式是怎么**推导**出来的？"

Bob挠头："不是直接给的吗？"

Victor摇头：

> "任何优化问题的解析解，都是通过**求导**得到的。这周我们要学的，就是如何对**矩阵和向量**求导。"

他在白板上写下：

```
标量求导 vs 矩阵求导

标量：df/dx，一个数
向量：∂f/∂x = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]ᵀ，一个向量
矩阵：∂f/∂X，一个矩阵

这个向量叫做梯度（gradient），记作∇f
```

> "梯度的几何意义是什么？"

Carol回答："函数增长最快的方向？"

> "对！在高维空间中，梯度指向函数值增加最快的方向。如果你想最小化一个函数，就沿着**负梯度方向**走。"

![梯度下降可视化](code/week-11/visualizations/01_gradient_descent.png)

Victor继续写：

```
常用的矩阵求导公式：

1. 线性项：∂(aᵀx)/∂x = a

2. 二次型：∂(xᵀAx)/∂x = (A + Aᵀ)x
   如果A是对称矩阵：∂(xᵀAx)/∂x = 2Ax

3. 链式法则：∂f(g(x))/∂x = (∂f/∂g)(∂g/∂x)
```

Eric皱眉："等等，为什么二次型的导数是2Ax？这和标量的d(ax²)/dx = 2ax很像，但维度对吗？"

> "好问题！"Victor在白板上详细展开：

```
展开二次型：
xᵀAx = Σᵢ Σⱼ xᵢ aᵢⱼ xⱼ

对xₖ求偏导：
∂(xᵀAx)/∂xₖ = Σⱼ aₖⱼ xⱼ + Σᵢ xᵢ aᵢₖ
             = (Ax)ₖ + (Aᵀx)ₖ
             = ((A + Aᵀ)x)ₖ

组合起来：
∂(xᵀAx)/∂x = (A + Aᵀ)x

如果A是对称的（Aᵀ = A）：
∂(xᵀAx)/∂x = 2Ax
```

> "协方差矩阵就是对称的，所以在投资组合优化中，我们总是能用2Σw这个简洁形式。"

### 推导投资组合优化的解析解

Victor在白板上写下完整推导：

```
问题：最小化 wᵀΣw（组合方差）
约束：wᵀ1 = 1（权重之和为1）

构建拉格朗日函数：
L(w, λ) = wᵀΣw - λ(wᵀ1 - 1)

对w求导并令其为0：
∂L/∂w = 2Σw - λ1 = 0
=> w = (λ/2)Σ⁻¹1

代入约束条件：
wᵀ1 = (λ/2)(Σ⁻¹1)ᵀ1 = (λ/2)(1ᵀΣ⁻¹1) = 1
=> λ = 2/(1ᵀΣ⁻¹1)

最终解：
w* = Σ⁻¹1 / (1ᵀΣ⁻¹1)
```

Alice恍然大悟："原来那个公式是这样推出来的！2Σw = λ1，所以最优权重正比于Σ⁻¹1。"

> "现在你知道为什么说**矩阵微积分是优化的语言**了吧。没有它，你只能用数值方法盲目搜索；有了它，你能直接算出解析解。"

Bob问："那如果没有解析解怎么办？"

> "那就用**梯度下降**。沿着负梯度方向一步一步走，最终会走到极小值点。"

```python
def gradient_descent(f, grad_f, x0, learning_rate=0.01, max_iter=1000, tol=1e-6):
    """
    梯度下降算法
    f: 目标函数
    grad_f: 梯度函数
    x0: 初始点
    """
    x = x0.copy()

    for i in range(max_iter):
        g = grad_f(x)  # 计算梯度
        x_new = x - learning_rate * g  # 更新

        if np.linalg.norm(x_new - x) < tol:
            print(f"收敛于第{i}次迭代")
            break
        x = x_new

    return x

# 示例：最小化投资组合方差
def portfolio_variance(w, cov_matrix):
    return w @ cov_matrix @ w

def portfolio_gradient(w, cov_matrix):
    return 2 * cov_matrix @ w
```

## 🎯二次规划：带约束的优化艺术

周二，Victor深入讲解约束优化。

> "上周我们只处理了一个等式约束。实际中，投资组合优化有大量约束：不能做空、单个股票不能超过10%、行业暴露限制...今天我们学习如何系统处理这些约束。"

他在白板上画了一个图：

![二次型等高线](code/week-11/visualizations/02_quadratic_form.png)

```
二次规划（Quadratic Programming）的标准形式：

最小化：(1/2)xᵀQx + cᵀx
约束：  Ax = b        （等式约束）
       Gx ≤ h        （不等式约束）

其中Q是正定矩阵（保证问题是凸的）
```

Carol问："为什么要求Q正定？"

> "因为只有Q正定时，目标函数才是**凸函数**，才有唯一的全局最小值。如果Q不正定，可能有多个局部极小值，优化会变得非常困难。"

Victor继续讲解KKT条件：

```
KKT条件（Karush-Kuhn-Tucker）：

对于约束优化问题，最优解x*必须满足：

1. 原问题可行：Ax* = b, Gx* ≤ h
2. 对偶可行：λ ≥ 0（不等式约束的乘子非负）
3. 互补松弛：λᵢ(gᵢ(x*) - hᵢ) = 0
4. 驻点条件：∇f(x*) + Aᵀν + Gᵀλ = 0

互补松弛的意义：
- 如果约束不紧（gᵢ(x*) < hᵢ），则λᵢ = 0
- 如果λᵢ > 0，则约束必紧（gᵢ(x*) = hᵢ）
```

Eric问："这太抽象了，能举个具体例子吗？"

> "好，我们来看一个带做空限制的投资组合优化。"

```python
import cvxpy as cp
import numpy as np

def portfolio_optimization_with_constraints(expected_returns, cov_matrix,
                                            target_return=None,
                                            max_weight=0.3,
                                            allow_short=False):
    """
    带约束的投资组合优化

    参数：
    - expected_returns: 预期收益向量
    - cov_matrix: 协方差矩阵
    - target_return: 目标收益（可选）
    - max_weight: 单个资产最大权重
    - allow_short: 是否允许做空
    """
    n = len(expected_returns)
    w = cp.Variable(n)  # 权重变量

    # 目标：最小化组合方差
    portfolio_variance = cp.quad_form(w, cov_matrix)
    objective = cp.Minimize(portfolio_variance)

    # 约束条件
    constraints = [
        cp.sum(w) == 1,  # 权重之和为1
        w <= max_weight,  # 单个资产不超过30%
    ]

    if not allow_short:
        constraints.append(w >= 0)  # 不允许做空

    if target_return is not None:
        constraints.append(w @ expected_returns >= target_return)

    # 求解
    problem = cp.Problem(objective, constraints)
    problem.solve()

    if problem.status == 'optimal':
        return w.value, np.sqrt(problem.value)
    else:
        raise ValueError(f"优化失败：{problem.status}")

# 示例
np.random.seed(42)
n_assets = 5
expected_returns = np.array([0.10, 0.12, 0.08, 0.15, 0.09])
cov_matrix = np.array([
    [0.04, 0.01, 0.005, 0.02, 0.01],
    [0.01, 0.05, 0.01, 0.015, 0.008],
    [0.005, 0.01, 0.03, 0.01, 0.005],
    [0.02, 0.015, 0.01, 0.06, 0.02],
    [0.01, 0.008, 0.005, 0.02, 0.035]
])

weights, risk = portfolio_optimization_with_constraints(
    expected_returns, cov_matrix,
    target_return=0.11,
    max_weight=0.4,
    allow_short=False
)

print("最优权重:", weights.round(4))
print("组合风险(标准差):", round(risk, 4))
print("预期收益:", round(weights @ expected_returns, 4))
```

Alice兴奋地说："cvxpy真方便！定义好目标和约束，它就自动帮我们求解了。"

> Victor点点头。"没错。但你要理解背后的数学原理。cvxpy内部就是在检验KKT条件，找到满足所有条件的解。"

### 有效前沿的构建

Victor接着讲解如何构建有效前沿：

```python
def compute_efficient_frontier(expected_returns, cov_matrix, n_points=50):
    """计算有效前沿"""
    min_ret = 0.05
    max_ret = max(expected_returns)
    target_returns = np.linspace(min_ret, max_ret, n_points)

    frontier_risks = []
    frontier_weights = []

    for target in target_returns:
        try:
            weights, risk = portfolio_optimization_with_constraints(
                expected_returns, cov_matrix,
                target_return=target,
                max_weight=0.5,
                allow_short=False
            )
            frontier_risks.append(risk)
            frontier_weights.append(weights)
        except:
            continue

    return np.array(frontier_risks), target_returns[:len(frontier_risks)], frontier_weights

# 绘制有效前沿
import matplotlib.pyplot as plt

risks, returns, _ = compute_efficient_frontier(expected_returns, cov_matrix)

plt.figure(figsize=(10, 6))
plt.plot(risks, returns, 'b-', linewidth=2, label='有效前沿')
plt.scatter([np.sqrt(cov_matrix[i,i]) for i in range(5)], expected_returns,
            c='red', s=100, label='个股')
plt.xlabel('风险（标准差）')
plt.ylabel('预期收益')
plt.title('投资组合有效前沿')
plt.legend()
plt.grid(True)
plt.show()
```

![有效前沿](code/week-11/visualizations/03_efficient_frontier.png)

## 🔺Cholesky分解：正定矩阵的优雅分解

周三，Victor进入本周的另一个重点。

> "今天我们学习一个非常实用的矩阵分解——**Cholesky分解**。它比特征分解快一倍，而且是蒙特卡洛模拟的核心工具。"

他在白板上写下定义：

```
Cholesky分解：

对于正定矩阵Σ，存在唯一的下三角矩阵L，使得：
    Σ = LLᵀ

其中L的对角元素都是正数。

为什么有用？
1. 计算效率：O(n³/3)，比特征分解快
2. 数值稳定：不需要求特征值
3. 蒙特卡洛模拟的关键工具
```

Bob问："正定矩阵是什么来着？"

> "好问题。复习一下："

```
正定矩阵的定义：
对于所有非零向量x，都有 xᵀΣx > 0

等价条件（任选其一）：
1. 所有特征值都是正数
2. 所有顺序主子式都是正数
3. 存在Cholesky分解
4. 存在可逆矩阵A使得Σ = AᵀA

协方差矩阵的性质：
- 对称：Σᵀ = Σ
- 半正定：xᵀΣx ≥ 0（特征值非负）
- 如果没有完美共线性，则正定（特征值都为正）
```

> "半正定和正定的区别很重要。样本协方差矩阵可能只是半正定——如果样本数小于资产数，一定会有零特征值。"

### 蒙特卡洛模拟：从独立到相关

Victor开始讲解Cholesky分解最重要的应用：

> "假设你要模拟5只相关股票的未来收益率。如果它们是独立的，很简单：分别生成5个正态随机数。但现实中，股票收益率是**相关**的！"

![Cholesky分解与相关性](code/week-11/visualizations/05_cholesky_correlation.png)

```
问题：如何生成服从N(μ, Σ)的随机向量？

解决方案：Cholesky分解！

步骤：
1. 对Σ做Cholesky分解：Σ = LLᵀ
2. 生成独立标准正态向量：z ~ N(0, I)
3. 变换：x = μ + Lz

验证：
E[x] = μ + L·E[z] = μ
Cov(x) = L·Cov(z)·Lᵀ = L·I·Lᵀ = LLᵀ = Σ ✓
```

Carol恍然大悟："原来是这样！L把独立的随机数变换成相关的。"

> "对！L可以理解为一个**着色矩阵**，把白噪声（独立同分布）变成彩色噪声（相关结构）。"

```python
import numpy as np

def simulate_correlated_returns(expected_returns, cov_matrix, n_simulations=10000):
    """
    使用Cholesky分解模拟相关资产收益率

    参数：
    - expected_returns: 预期收益向量
    - cov_matrix: 协方差矩阵
    - n_simulations: 模拟次数

    返回：
    - 模拟收益率矩阵 (n_simulations, n_assets)
    """
    n_assets = len(expected_returns)

    # Cholesky分解
    L = np.linalg.cholesky(cov_matrix)

    # 生成独立标准正态随机数
    z = np.random.standard_normal((n_simulations, n_assets))

    # 变换为相关收益率
    # x = μ + Lz （注意：z是行向量，所以用L的转置）
    simulated_returns = expected_returns + z @ L.T

    return simulated_returns

# 验证：检查模拟结果的统计性质
np.random.seed(42)
simulated = simulate_correlated_returns(expected_returns, cov_matrix, n_simulations=100000)

print("理论均值:", expected_returns)
print("模拟均值:", simulated.mean(axis=0).round(4))
print()
print("理论协方差矩阵:")
print(cov_matrix.round(4))
print()
print("模拟协方差矩阵:")
print(np.cov(simulated.T).round(4))
```

### VaR计算：风险管理的核心

Victor继续讲解蒙特卡洛模拟在风险管理中的应用：

> "有了模拟收益率，我们就能计算**VaR**（Value at Risk，风险价值）了。VaR回答的问题是：在给定置信水平下，最大可能损失是多少？"

```python
def calculate_var_cvar(portfolio_weights, expected_returns, cov_matrix,
                       confidence_level=0.95, n_simulations=100000,
                       initial_value=1000000):
    """
    使用蒙特卡洛模拟计算VaR和CVaR

    参数：
    - portfolio_weights: 投资组合权重
    - confidence_level: 置信水平（如0.95表示95%）
    - initial_value: 初始投资金额

    返回：
    - VaR: 风险价值
    - CVaR: 条件风险价值（Expected Shortfall）
    """
    # 模拟资产收益率
    simulated_returns = simulate_correlated_returns(
        expected_returns, cov_matrix, n_simulations
    )

    # 计算组合收益率
    portfolio_returns = simulated_returns @ portfolio_weights

    # 计算组合价值变化
    portfolio_pnl = initial_value * portfolio_returns

    # VaR: 损失分布的分位数
    var_percentile = (1 - confidence_level) * 100
    var = -np.percentile(portfolio_pnl, var_percentile)

    # CVaR: 超过VaR的平均损失
    losses = -portfolio_pnl
    cvar = losses[losses >= var].mean()

    return var, cvar, portfolio_pnl

# 计算等权组合的VaR
equal_weights = np.ones(5) / 5
var_95, cvar_95, pnl = calculate_var_cvar(
    equal_weights, expected_returns, cov_matrix,
    confidence_level=0.95
)

print(f"投资组合初始价值: $1,000,000")
print(f"95% VaR: ${var_95:,.2f}")
print(f"95% CVaR: ${cvar_95:,.2f}")
print(f"\n解读：在95%的置信水平下，")
print(f"- 每日最大损失不超过 ${var_95:,.2f}")
print(f"- 如果发生超过VaR的损失，平均损失为 ${cvar_95:,.2f}")
```

Alice问："VaR和CVaR有什么区别？为什么要用CVaR？"

> "好问题！VaR只告诉你'最坏情况下损失多少'，但没说如果超过这个阈值会怎样。CVaR告诉你'如果真的发生极端损失，平均会亏多少'。在风险管理中，CVaR更加保守，也更符合监管要求。"

```
VaR vs CVaR

VaR的问题：
1. 不满足次可加性：VaR(A+B) 可能 > VaR(A) + VaR(B)
2. 忽略尾部风险：只关心分位点，不关心更极端的情况

CVaR的优点：
1. 满足次可加性：分散化总是降低CVaR
2. 考虑尾部风险：是尾部损失的期望值
3. 是凸函数：可以用凸优化求解最小CVaR组合
```

![蒙特卡洛VaR分布](code/week-11/visualizations/04_monte_carlo_var.png)

## 🚨协方差矩阵的维度诅咒

周四，Victor表情严肃地走进培训室。

> "今天讲一个让很多量化基金栽过跟头的问题——**协方差矩阵估计**。"

他在白板上写下一个惊人的数字：

```
问题规模：

假设你要投资500只股票
协方差矩阵大小：500 × 500 = 250,000个参数

假设你有250个交易日的数据
样本数：250

问题：用250个样本估计250,000个参数，靠谱吗？
```

开发团队大伙面面相觑。

> "这就是**维度灾难**。当资产数p接近甚至超过样本数n时，样本协方差矩阵会出现严重问题。"

![协方差矩阵特征值问题](code/week-11/visualizations/07_eigenvalue_problem.png)

Victor详细解释问题：

```
样本协方差矩阵的问题：

1. 奇异性
   - 当 p > n 时，矩阵秩最多为n-1
   - 矩阵奇异，无法求逆
   - Cholesky分解失败

2. 特征值分散
   - 最大特征值被高估
   - 最小特征值被低估（甚至为负/零）
   - 导致优化结果不稳定

3. 极端权重
   - 基于有偏协方差的优化会产生极端权重
   - 大量做空、高换手率
   - 样本内表现好，样本外崩溃
```

Eric问："那怎么解决这个问题？"

> "下周我们会详细讲。今天先给你们看看问题有多严重。"

```python
def demonstrate_covariance_problems():
    """演示协方差矩阵估计问题"""
    np.random.seed(42)

    # 场景1：p < n（理想情况）
    print("=" * 50)
    print("场景1：p=10资产, n=250天 (p < n)")
    print("=" * 50)

    p1, n1 = 10, 250
    returns1 = np.random.randn(n1, p1) * 0.02  # 模拟日收益率
    cov1 = np.cov(returns1.T)
    eigenvalues1 = np.linalg.eigvalsh(cov1)

    print(f"最小特征值: {eigenvalues1.min():.6f}")
    print(f"最大特征值: {eigenvalues1.max():.6f}")
    print(f"条件数: {eigenvalues1.max()/eigenvalues1.min():.2f}")
    print(f"矩阵正定: {np.all(eigenvalues1 > 0)}")

    # 场景2：p ≈ n（临界情况）
    print("\n" + "=" * 50)
    print("场景2：p=200资产, n=250天 (p ≈ n)")
    print("=" * 50)

    p2, n2 = 200, 250
    returns2 = np.random.randn(n2, p2) * 0.02
    cov2 = np.cov(returns2.T)
    eigenvalues2 = np.linalg.eigvalsh(cov2)

    print(f"最小特征值: {eigenvalues2.min():.6f}")
    print(f"最大特征值: {eigenvalues2.max():.6f}")
    print(f"条件数: {eigenvalues2.max()/max(eigenvalues2.min(), 1e-10):.2f}")
    print(f"矩阵正定: {np.all(eigenvalues2 > 1e-10)}")
    print(f"接近零的特征值数量: {np.sum(eigenvalues2 < 1e-6)}")

    # 场景3：p > n（病态情况）
    print("\n" + "=" * 50)
    print("场景3：p=500资产, n=250天 (p > n)")
    print("=" * 50)

    p3, n3 = 500, 250
    returns3 = np.random.randn(n3, p3) * 0.02
    cov3 = np.cov(returns3.T)
    eigenvalues3 = np.linalg.eigvalsh(cov3)

    print(f"最小特征值: {eigenvalues3.min():.6f}")
    print(f"最大特征值: {eigenvalues3.max():.6f}")
    print(f"零特征值数量: {np.sum(np.abs(eigenvalues3) < 1e-10)}")
    print(f"矩阵秩: {np.linalg.matrix_rank(cov3)}")
    print(f"理论最大秩: {min(n3-1, p3)}")

    # 尝试Cholesky分解
    try:
        L = np.linalg.cholesky(cov3)
        print("Cholesky分解: 成功")
    except np.linalg.LinAlgError:
        print("Cholesky分解: 失败（矩阵不正定）")

demonstrate_covariance_problems()
```

### 正定性修复的临时方案

Victor给出一些应急方法：

```python
def make_positive_definite(cov_matrix, method='eigenvalue', epsilon=1e-6):
    """
    将半正定/非正定矩阵修复为正定矩阵

    方法：
    1. eigenvalue: 将负/零特征值替换为小正数
    2. diagonal: 对角线加小量
    3. nearest: 找最近的正定矩阵
    """
    if method == 'eigenvalue':
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        eigenvalues = np.maximum(eigenvalues, epsilon)
        return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

    elif method == 'diagonal':
        min_eig = np.min(np.linalg.eigvalsh(cov_matrix))
        if min_eig < epsilon:
            cov_matrix = cov_matrix + (epsilon - min_eig) * np.eye(len(cov_matrix))
        return cov_matrix

    elif method == 'nearest':
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

print("原始矩阵特征值范围:",
      np.linalg.eigvalsh(cov_singular).min(),
      "到",
      np.linalg.eigvalsh(cov_singular).max())

cov_fixed = make_positive_definite(cov_singular, method='eigenvalue')
print("修复后特征值范围:",
      np.linalg.eigvalsh(cov_fixed).min(),
      "到",
      np.linalg.eigvalsh(cov_fixed).max())

# 验证Cholesky分解
try:
    L = np.linalg.cholesky(cov_fixed)
    print("Cholesky分解成功！")
except:
    print("Cholesky分解失败")
```

> "但要记住，这些只是**应急方案**。真正的解决办法是使用**收缩估计**或**因子模型**，我们下周会详细讲。"

## 💼实战：完整的风险管理流程

周五，Victor带大家做一个完整的实战项目。

> "我们把这周学的东西串起来：从数据到协方差估计，到投资组合优化，再到风险评估。"

```python
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

    def optimize_portfolio(self, target_return=None, max_weight=0.3,
                          min_weight=0.0, risk_aversion=None):
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
            objective = cp.Maximize(portfolio_return - (risk_aversion/2) * portfolio_variance)
        else:
            # 最小方差优化
            objective = cp.Minimize(portfolio_variance)

        constraints = [
            cp.sum(w) == 1,
            w >= min_weight,
            w <= max_weight
        ]

        if target_return is not None:
            constraints.append(self.expected_returns @ w >= target_return)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        if problem.status == 'optimal':
            self.optimal_weights = w.value
            self.optimal_risk = np.sqrt(self.optimal_weights @ self.cov_matrix @ self.optimal_weights)
            self.optimal_return = self.optimal_weights @ self.expected_returns
            return self.optimal_weights
        else:
            raise ValueError(f"优化失败: {problem.status}")

    def calculate_risk_metrics(self, weights, confidence_level=0.95,
                               n_simulations=100000, holding_period=1):
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
        var = -np.percentile(portfolio_returns, (1-confidence_level)*100)
        cvar = -np.mean(portfolio_returns[portfolio_returns <= -var])

        # 组合统计
        portfolio_std = np.sqrt(weights @ daily_cov @ weights)
        portfolio_mean = weights @ daily_returns
        sharpe = (portfolio_mean * 252) / (portfolio_std * np.sqrt(252))  # 年化夏普

        return {
            'VaR': var,
            'CVaR': cvar,
            'daily_volatility': portfolio_std,
            'annual_volatility': portfolio_std * np.sqrt(252),
            'expected_daily_return': portfolio_mean,
            'expected_annual_return': portfolio_mean * 252,
            'sharpe_ratio': sharpe,
            'confidence_level': confidence_level,
            'holding_period': holding_period
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
            'portfolio_volatility': portfolio_std,
            'marginal_risk_contribution': mrc,
            'component_risk_contribution': crc,
            'percentage_contribution': pct_contribution
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
        for i, (name, pct) in enumerate(zip(self.asset_names, risk_decomp['percentage_contribution'])):
            print(f"  {name}: {pct*100:.2f}%")

# 使用示例
import pandas as pd

# 创建模拟数据
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=500, freq='B')
assets = ['股票A', '股票B', '股票C', '债券', '黄金']

# 模拟收益率（带相关性）
true_cov = np.array([
    [0.04, 0.02, 0.015, -0.005, 0.001],
    [0.02, 0.05, 0.02, -0.003, 0.002],
    [0.015, 0.02, 0.045, -0.002, 0.001],
    [-0.005, -0.003, -0.002, 0.01, 0.003],
    [0.001, 0.002, 0.001, 0.003, 0.015]
]) / 252  # 日度协方差

L = np.linalg.cholesky(true_cov)
returns_data = pd.DataFrame(
    np.random.randn(500, 5) @ L.T + np.array([0.10, 0.12, 0.11, 0.04, 0.06])/252,
    index=dates,
    columns=assets
)

# 初始化风险管理器
rm = PortfolioRiskManager(returns_data)

# 优化组合
optimal_weights = rm.optimize_portfolio(target_return=0.08, max_weight=0.4)

# 打印摘要
rm.print_portfolio_summary(optimal_weights)
```

![风险贡献分解](code/week-11/visualizations/06_risk_contribution.png)

![约束优化对比](code/week-11/visualizations/08_optimization_comparison.png)

## 📒本周总结

本周是线性代数进阶的第一周，重点从矩阵运算转向矩阵优化。

我们跟随Victor完成了以下核心内容：

1. **矩阵微积分基础**
   - 梯度向量∇f：函数增长最快的方向
   - 二次型求导：∂(xᵀAx)/∂x = 2Ax
   - 链式法则在矩阵中的应用
   - 推导了Markowitz组合的解析解

2. **二次规划与约束优化**
   - 拉格朗日乘数法处理等式约束
   - KKT条件处理不等式约束
   - cvxpy实现带约束的组合优化
   - 有效前沿的构建方法

3. **Cholesky分解与蒙特卡洛模拟**
   - Cholesky分解：Σ = LLᵀ，仅适用于正定矩阵
   - 核心应用：从独立随机数生成相关收益率
   - VaR与CVaR的计算
   - 风险归因与成分贡献分析

4. **协方差矩阵的挑战**
   - 维度灾难：当p > n时矩阵奇异
   - 特征值分散：最大被高估，最小被低估
   - 正定性修复的临时方案
   - 应急方法：特征值截断、对角加扰

**优化是数学的艺术**。这周我们学会了如何用数学语言描述约束、如何求导找到最优解、如何用模拟评估风险。但这只是开始——协方差矩阵的估计问题，需要更高级的工具来解决，这些问题我们将在下周继续讨论。

本周的代码实现和练习已上传至Github仓库：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)

**下周预告：W12 - 线性代数进阶（下）**

下周我们将学习更高级的协方差矩阵估计方法：收缩估计、随机矩阵理论、卡尔曼滤波，以及正则化回归。这些工具将帮助我们构建更稳健的投资组合。

各位下周五见！👋
