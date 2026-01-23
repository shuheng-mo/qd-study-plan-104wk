"""
Week 11 可视化生成脚本
生成线性代数进阶（上）相关的静态图表
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
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
        # macOS 可用中文字体（按推荐顺序）
        font_list = [
            "Hiragino Sans GB",  # 最可靠的macOS中文字体
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

    # 检查可用字体
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
        selected_font = font_list[0]  # 使用第一个作为fallback

    # 使用 matplotlib.rc 进行全局设置（更可靠）
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

# ⚠️ 关键：seaborn会重置字体，必须在之后重新设置
matplotlib.rcParams["font.sans-serif"] = [CHINESE_FONT, "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["font.family"] = "sans-serif"

# 其他matplotlib设置
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["figure.facecolor"] = "white"

print(f"✓ 最终字体设置: {matplotlib.rcParams['font.sans-serif']}")


def plot_gradient_descent():
    """
    图1: 梯度下降可视化
    展示二次函数的等高线和梯度下降路径
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 定义二次函数 f(x,y) = x^2 + 2y^2
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + 2 * Y**2

    # 左图：等高线 + 梯度下降路径
    ax1 = axes[0]
    contour = ax1.contour(X, Y, Z, levels=15, cmap="viridis")
    ax1.clabel(contour, inline=True, fontsize=8)

    # 梯度下降路径
    def gradient(x, y):
        return np.array([2 * x, 4 * y])

    path_x, path_y = [2.5], [2.5]
    lr = 0.15
    for _ in range(15):
        grad = gradient(path_x[-1], path_y[-1])
        path_x.append(path_x[-1] - lr * grad[0])
        path_y.append(path_y[-1] - lr * grad[1])

    ax1.plot(path_x, path_y, "ro-", markersize=6, linewidth=2, label="下降路径")
    ax1.plot(path_x[0], path_y[0], "g^", markersize=12, label="起点")
    ax1.plot(0, 0, "r*", markersize=15, label="最优解")

    # 绘制梯度箭头
    for i in range(0, len(path_x) - 1, 3):
        grad = gradient(path_x[i], path_y[i])
        grad_norm = grad / (np.linalg.norm(grad) + 1e-6) * 0.5
        ax1.annotate(
            "",
            xy=(path_x[i] - grad_norm[0], path_y[i] - grad_norm[1]),
            xytext=(path_x[i], path_y[i]),
            arrowprops=dict(arrowstyle="->", color="blue", lw=1.5),
        )

    ax1.set_xlabel("x", fontsize=12)
    ax1.set_ylabel("y", fontsize=12)
    ax1.set_title("梯度下降：沿负梯度方向迭代\n$f(x,y) = x^2 + 2y^2$", fontsize=14)
    ax1.legend(loc="upper right")
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect("equal")

    # 右图：损失函数下降曲线
    ax2 = axes[1]
    losses = [path_x[i] ** 2 + 2 * path_y[i] ** 2 for i in range(len(path_x))]
    iterations = range(len(losses))
    ax2.plot(iterations, losses, "b-o", linewidth=2, markersize=6)
    ax2.fill_between(iterations, losses, alpha=0.3)
    ax2.set_xlabel("迭代次数", fontsize=12)
    ax2.set_ylabel("损失函数值 f(x,y)", fontsize=12)
    ax2.set_title("损失函数收敛过程", fontsize=14)
    ax2.grid(True, alpha=0.3)

    # 添加注释
    ax2.annotate(
        f"起始: {losses[0]:.2f}",
        xy=(0, losses[0]),
        xytext=(2, losses[0] - 1),
        arrowprops=dict(arrowstyle="->", color="gray"),
        fontsize=10,
    )
    ax2.annotate(
        f"收敛: {losses[-1]:.4f}",
        xy=(len(losses) - 1, losses[-1]),
        xytext=(len(losses) - 5, losses[-1] + 2),
        arrowprops=dict(arrowstyle="->", color="gray"),
        fontsize=10,
    )

    plt.tight_layout()
    plt.savefig("01_gradient_descent.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 01_gradient_descent.png")


def plot_quadratic_form():
    """
    图2: 二次型的几何意义
    展示 w^T Σ w 等高线与特征向量方向
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 定义协方差矩阵
    Sigma = np.array([[2, 1], [1, 3]])
    eigenvalues, eigenvectors = np.linalg.eigh(Sigma)

    # 左图：二次型等高线
    ax1 = axes[0]
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)

    # 计算 w^T Σ w
    Z = Sigma[0, 0] * X**2 + 2 * Sigma[0, 1] * X * Y + Sigma[1, 1] * Y**2

    contour = ax1.contour(X, Y, Z, levels=15, cmap="RdYlBu_r")
    ax1.clabel(contour, inline=True, fontsize=8)

    # 绘制特征向量
    colors = ["#e74c3c", "#3498db"]
    for i, (val, vec) in enumerate(zip(eigenvalues, eigenvectors.T)):
        scale = 2
        ax1.annotate(
            "",
            xy=(scale * vec[0], scale * vec[1]),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=colors[i], lw=3),
        )
        ax1.annotate(
            "",
            xy=(-scale * vec[0], -scale * vec[1]),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=colors[i], lw=3),
        )
        ax1.text(
            scale * vec[0] * 1.1,
            scale * vec[1] * 1.1,
            r"$\lambda_{%d}$=%.2f" % (i + 1, val),
            fontsize=11,
            color=colors[i],
            fontweight="bold",
        )

    ax1.set_xlabel(r"$w_1$", fontsize=12)
    ax1.set_ylabel(r"$w_2$", fontsize=12)
    ax1.set_title(
        r"二次型 $w^T \Sigma w$ 的等高线" + "\n特征向量 = 主轴方向", fontsize=14
    )
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect("equal")
    ax1.axhline(y=0, color="k", linewidth=0.5)
    ax1.axvline(x=0, color="k", linewidth=0.5)

    # 右图：特征值与风险的关系
    ax2 = axes[1]

    # 在不同方向上计算风险
    angles = np.linspace(0, 2 * np.pi, 100)
    risks = []
    for theta in angles:
        w = np.array([np.cos(theta), np.sin(theta)])
        risk = w @ Sigma @ w
        risks.append(risk)

    ax2.plot(np.degrees(angles), risks, "b-", linewidth=2)
    ax2.fill_between(np.degrees(angles), risks, alpha=0.3)

    # 标记特征向量方向
    for i, vec in enumerate(eigenvectors.T):
        angle = np.degrees(np.arctan2(vec[1], vec[0]))
        if angle < 0:
            angle += 360
        risk_at_eigenvec = eigenvalues[i]
        ax2.axvline(
            x=angle,
            color=colors[i],
            linestyle="--",
            linewidth=2,
            label=f"特征方向{i+1}: θ={angle:.0f}°",
        )
        ax2.scatter([angle], [risk_at_eigenvec], color=colors[i], s=100, zorder=5)

    ax2.set_xlabel("权重方向 θ (度)", fontsize=12)
    ax2.set_ylabel(r"组合方差 $w^T \Sigma w$", fontsize=12)
    ax2.set_title("不同方向上的风险大小\n（特征值 = 主轴方向的方差）", fontsize=14)
    ax2.legend(loc="upper right")
    ax2.set_xlim(0, 360)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("02_quadratic_form.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 02_quadratic_form.png")


def plot_efficient_frontier():
    """
    图3: 有效前沿
    展示投资组合优化的风险-收益权衡
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    np.random.seed(42)

    # 定义资产
    n_assets = 5
    asset_names = ["股票A", "股票B", "股票C", "债券", "黄金"]
    expected_returns = np.array([0.12, 0.10, 0.14, 0.05, 0.07])
    volatilities = np.array([0.20, 0.18, 0.25, 0.08, 0.15])

    # 协方差矩阵
    corr_matrix = np.array(
        [
            [1.0, 0.6, 0.7, -0.2, 0.1],
            [0.6, 1.0, 0.5, -0.1, 0.15],
            [0.7, 0.5, 1.0, -0.15, 0.05],
            [-0.2, -0.1, -0.15, 1.0, 0.3],
            [0.1, 0.15, 0.05, 0.3, 1.0],
        ]
    )
    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix

    # 生成随机组合
    n_portfolios = 5000
    portfolio_returns = []
    portfolio_risks = []
    portfolio_sharpes = []

    for _ in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights /= weights.sum()

        ret = weights @ expected_returns
        risk = np.sqrt(weights @ cov_matrix @ weights)
        sharpe = (ret - 0.02) / risk  # 假设无风险利率2%

        portfolio_returns.append(ret)
        portfolio_risks.append(risk)
        portfolio_sharpes.append(sharpe)

    # 绘制随机组合
    scatter = ax.scatter(
        portfolio_risks,
        portfolio_returns,
        c=portfolio_sharpes,
        cmap="RdYlGn",
        alpha=0.5,
        s=10,
    )
    plt.colorbar(scatter, label="夏普比率", ax=ax)

    # 计算有效前沿（简化版）
    target_returns = np.linspace(0.05, 0.14, 50)
    frontier_risks = []

    for target in target_returns:
        # 找到满足目标收益的最小风险组合（简化：从随机组合中选择）
        valid_idx = [i for i, r in enumerate(portfolio_returns) if r >= target - 0.005]
        if valid_idx:
            min_risk_idx = min(valid_idx, key=lambda i: portfolio_risks[i])
            frontier_risks.append(portfolio_risks[min_risk_idx])
        else:
            frontier_risks.append(np.nan)

    # 绘制有效前沿（近似）
    ax.plot(frontier_risks, target_returns, "b-", linewidth=3, label="有效前沿")

    # 绘制个股位置
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
    for i, (name, ret, vol) in enumerate(
        zip(asset_names, expected_returns, volatilities)
    ):
        ax.scatter(
            [vol],
            [ret],
            s=200,
            c=colors[i],
            marker="s",
            edgecolors="black",
            linewidth=2,
            zorder=5,
        )
        ax.annotate(
            name,
            xy=(vol, ret),
            xytext=(vol + 0.01, ret + 0.005),
            fontsize=11,
            fontweight="bold",
        )

    # 标记最优夏普比率组合
    max_sharpe_idx = np.argmax(portfolio_sharpes)
    ax.scatter(
        [portfolio_risks[max_sharpe_idx]],
        [portfolio_returns[max_sharpe_idx]],
        s=300,
        c="gold",
        marker="*",
        edgecolors="black",
        linewidth=2,
        label=f"最优夏普组合\nSR={portfolio_sharpes[max_sharpe_idx]:.2f}",
        zorder=6,
    )

    # 最小方差组合
    min_var_idx = np.argmin(portfolio_risks)
    ax.scatter(
        [portfolio_risks[min_var_idx]],
        [portfolio_returns[min_var_idx]],
        s=200,
        c="white",
        marker="o",
        edgecolors="blue",
        linewidth=3,
        label=f"最小方差组合\n风险={portfolio_risks[min_var_idx]:.1%}",
        zorder=6,
    )

    ax.set_xlabel("风险（年化波动率）", fontsize=14)
    ax.set_ylabel("预期收益（年化）", fontsize=14)
    ax.set_title("投资组合有效前沿\nMarkowitz均值-方差优化", fontsize=16)
    ax.legend(loc="lower right", fontsize=10)

    # 格式化坐标轴为百分比
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.05, 0.30)
    ax.set_ylim(0.03, 0.16)

    plt.tight_layout()
    plt.savefig("03_efficient_frontier.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 03_efficient_frontier.png")


def plot_monte_carlo_var():
    """
    图4: 蒙特卡洛模拟与VaR
    展示收益率分布和风险价值
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    np.random.seed(42)

    # 模拟参数
    expected_return = 0.10 / 252  # 日收益
    volatility = 0.20 / np.sqrt(252)  # 日波动
    n_simulations = 100000
    initial_value = 1000000

    # 生成模拟收益率
    simulated_returns = np.random.normal(expected_return, volatility, n_simulations)
    simulated_pnl = initial_value * simulated_returns

    # 计算VaR和CVaR
    confidence = 0.95
    var_95 = -np.percentile(simulated_pnl, (1 - confidence) * 100)
    cvar_95 = -np.mean(simulated_pnl[simulated_pnl <= -var_95])

    # 左图：收益分布
    ax1 = axes[0]
    n, bins, patches = ax1.hist(
        simulated_pnl / 1000,
        bins=100,
        density=True,
        alpha=0.7,
        color="steelblue",
        edgecolor="white",
    )

    # 标记VaR区域
    var_threshold = -var_95 / 1000
    for i, (b, p) in enumerate(zip(bins[:-1], patches)):
        if b < var_threshold:
            p.set_facecolor("#e74c3c")
            p.set_alpha(0.8)

    ax1.axvline(
        x=var_threshold,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"95% VaR = ${var_95:,.0f}",
    )
    ax1.axvline(
        x=-cvar_95 / 1000,
        color="darkred",
        linestyle=":",
        linewidth=2,
        label=f"95% CVaR = ${cvar_95:,.0f}",
    )
    ax1.axvline(x=0, color="black", linestyle="-", linewidth=1)

    ax1.set_xlabel("日盈亏 (千美元)", fontsize=12)
    ax1.set_ylabel("概率密度", fontsize=12)
    ax1.set_title("蒙特卡洛模拟：组合日盈亏分布\n红色区域 = 超过VaR的损失", fontsize=14)
    ax1.legend(loc="upper right", fontsize=10)
    ax1.grid(True, alpha=0.3)

    # 添加注释
    ax1.annotate(
        "5%概率\n发生这些损失",
        xy=(var_threshold - 5, 0.005),
        fontsize=10,
        color="red",
        ha="center",
    )

    # 右图：累积分布函数
    ax2 = axes[1]
    sorted_pnl = np.sort(simulated_pnl / 1000)
    cumulative = np.arange(1, len(sorted_pnl) + 1) / len(sorted_pnl)

    ax2.plot(sorted_pnl, cumulative, "b-", linewidth=2)
    ax2.axhline(y=0.05, color="red", linestyle="--", linewidth=2, label="5%分位")
    ax2.axvline(x=var_threshold, color="red", linestyle="--", linewidth=2)

    # 标记VaR点
    ax2.scatter([var_threshold], [0.05], color="red", s=150, zorder=5)
    ax2.annotate(
        f"VaR点\n({var_threshold:.1f}K, 5%)",
        xy=(var_threshold, 0.05),
        xytext=(var_threshold - 15, 0.15),
        arrowprops=dict(arrowstyle="->", color="red"),
        fontsize=11,
        color="red",
    )

    ax2.fill_between(
        sorted_pnl[sorted_pnl <= var_threshold],
        cumulative[: np.sum(sorted_pnl <= var_threshold)],
        alpha=0.3,
        color="red",
    )

    ax2.set_xlabel("日盈亏 (千美元)", fontsize=12)
    ax2.set_ylabel("累积概率", fontsize=12)
    ax2.set_title("累积分布函数 (CDF)\nVaR = CDF的5%分位点", fontsize=14)
    ax2.legend(loc="lower right", fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)

    plt.tight_layout()
    plt.savefig("04_monte_carlo_var.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 04_monte_carlo_var.png")


def plot_cholesky_correlation():
    """
    图5: Cholesky分解生成相关收益率
    对比独立 vs 相关的模拟结果
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    np.random.seed(42)
    n_simulations = 1000

    # 定义相关结构
    correlation = 0.7
    cov_matrix = np.array([[1, correlation], [correlation, 1]]) * 0.04  # 20%波动率
    L = np.linalg.cholesky(cov_matrix)

    # 生成独立随机数
    z_independent = np.random.randn(n_simulations, 2) * 0.2

    # 使用Cholesky变换生成相关随机数
    z_standard = np.random.randn(n_simulations, 2)
    z_correlated = z_standard @ L.T

    # 左上：独立收益率散点图
    ax1 = axes[0, 0]
    ax1.scatter(
        z_independent[:, 0], z_independent[:, 1], alpha=0.5, s=20, c="steelblue"
    )
    ax1.set_xlabel("资产1收益率", fontsize=12)
    ax1.set_ylabel("资产2收益率", fontsize=12)
    corr_ind = np.corrcoef(z_independent.T)[0, 1]
    ax1.set_title(f"独立随机数\n相关系数 = {corr_ind:.3f}", fontsize=14)
    ax1.axhline(y=0, color="k", linewidth=0.5)
    ax1.axvline(x=0, color="k", linewidth=0.5)
    ax1.set_xlim(-0.8, 0.8)
    ax1.set_ylim(-0.8, 0.8)
    ax1.set_aspect("equal")

    # 右上：相关收益率散点图
    ax2 = axes[0, 1]
    ax2.scatter(z_correlated[:, 0], z_correlated[:, 1], alpha=0.5, s=20, c="coral")
    ax2.set_xlabel("资产1收益率", fontsize=12)
    ax2.set_ylabel("资产2收益率", fontsize=12)
    corr_cor = np.corrcoef(z_correlated.T)[0, 1]
    ax2.set_title(
        f"Cholesky变换后\n相关系数 = {corr_cor:.3f} (目标: {correlation})", fontsize=14
    )
    ax2.axhline(y=0, color="k", linewidth=0.5)
    ax2.axvline(x=0, color="k", linewidth=0.5)
    ax2.set_xlim(-0.8, 0.8)
    ax2.set_ylim(-0.8, 0.8)
    ax2.set_aspect("equal")

    # 添加椭圆拟合
    from matplotlib.patches import Ellipse

    cov_emp = np.cov(z_correlated.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_emp)
    angle = np.degrees(np.arctan2(eigenvectors[1, 1], eigenvectors[0, 1]))
    ellipse = Ellipse(
        xy=(0, 0),
        width=4 * np.sqrt(eigenvalues[1]),
        height=4 * np.sqrt(eigenvalues[0]),
        angle=angle,
        fill=False,
        color="red",
        linewidth=2,
        linestyle="--",
    )
    ax2.add_patch(ellipse)

    # 左下：Cholesky分解示意图
    ax3 = axes[1, 0]
    ax3.axis("off")

    # 使用多个text对象分别显示中文和公式
    # 标题（中文，使用默认字体）
    ax3.text(
        0.5,
        0.95,
        "Cholesky分解原理",
        fontsize=14,
        fontweight="bold",
        ha="center",
        va="top",
        transform=ax3.transAxes,
    )

    # 核心公式（使用mathtext）
    ax3.text(
        0.5,
        0.78,
        r"协方差矩阵分解: $\Sigma = LL^T$",
        fontsize=12,
        ha="center",
        va="top",
        transform=ax3.transAxes,
    )

    # 矩阵示例（英文+数字，可用monospace）
    matrix_text = (
        "[1.0  0.7]   [1.0   0  ] [1.0  0.7]\n"
        "[        ] = [         ]x[        ]\n"
        "[0.7  1.0]   [0.7  0.71] [0    0.71]\n"
        "   Cov           L          L'"
    )
    ax3.text(
        0.5,
        0.62,
        matrix_text,
        fontsize=10,
        family="monospace",
        ha="center",
        va="top",
        transform=ax3.transAxes,
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
    )

    # 应用说明（中文）
    ax3.text(
        0.5,
        0.28,
        "生成相关随机数:",
        fontsize=11,
        ha="center",
        va="top",
        transform=ax3.transAxes,
    )
    ax3.text(
        0.5,
        0.18,
        r"$z \sim N(0,I) \;\rightarrow\; Lz \sim N(0,\Sigma)$",
        fontsize=12,
        ha="center",
        va="top",
        transform=ax3.transAxes,
    )
    ax3.text(
        0.5,
        0.06,
        "独立 → 相关",
        fontsize=11,
        ha="center",
        va="top",
        transform=ax3.transAxes,
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )

    ax3.set_title("", fontsize=14)  # 标题已在内部绘制

    # 右下：时间序列对比
    ax4 = axes[1, 1]
    t = np.arange(100)

    # 生成路径
    np.random.seed(123)
    path_ind = np.cumsum(np.random.randn(100, 2) * 0.02, axis=0)

    np.random.seed(123)
    z_path = np.random.randn(100, 2)
    L_small = np.linalg.cholesky(np.array([[1, 0.8], [0.8, 1]]) * 0.0004)
    path_cor = np.cumsum(z_path @ L_small.T, axis=0)

    ax4.plot(t, path_ind[:, 0], "b-", alpha=0.7, label="独立-资产1")
    ax4.plot(t, path_ind[:, 1], "b--", alpha=0.7, label="独立-资产2")
    ax4.plot(t, path_cor[:, 0], "r-", alpha=0.7, label="相关-资产1")
    ax4.plot(t, path_cor[:, 1], "r--", alpha=0.7, label="相关-资产2")

    ax4.set_xlabel("时间", fontsize=12)
    ax4.set_ylabel("累积收益", fontsize=12)
    ax4.set_title("价格路径对比：相关资产同涨同跌", fontsize=14)
    ax4.legend(loc="upper left", fontsize=9)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("05_cholesky_correlation.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 05_cholesky_correlation.png")


def plot_risk_contribution():
    """
    图6: 风险贡献分解
    展示各资产对组合风险的贡献
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 定义资产和权重
    assets = ["股票A", "股票B", "股票C", "债券", "黄金"]
    weights = np.array([0.30, 0.25, 0.20, 0.15, 0.10])

    # 协方差矩阵
    volatilities = np.array([0.22, 0.18, 0.25, 0.06, 0.14])
    corr_matrix = np.array(
        [
            [1.0, 0.6, 0.7, -0.1, 0.1],
            [0.6, 1.0, 0.5, -0.05, 0.15],
            [0.7, 0.5, 1.0, -0.1, 0.05],
            [-0.1, -0.05, -0.1, 1.0, 0.2],
            [0.1, 0.15, 0.05, 0.2, 1.0],
        ]
    )
    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix

    # 计算风险贡献
    portfolio_var = weights @ cov_matrix @ weights
    portfolio_std = np.sqrt(portfolio_var)

    # 边际风险贡献
    mrc = cov_matrix @ weights / portfolio_std

    # 成分风险贡献
    crc = weights * mrc

    # 百分比贡献
    pct_contribution = crc / portfolio_std

    # 左图：权重 vs 风险贡献对比
    ax1 = axes[0]
    x = np.arange(len(assets))
    width = 0.35

    bars1 = ax1.bar(
        x - width / 2,
        weights * 100,
        width,
        label="权重 (%)",
        color="steelblue",
        alpha=0.8,
    )
    bars2 = ax1.bar(
        x + width / 2,
        pct_contribution * 100,
        width,
        label="风险贡献 (%)",
        color="coral",
        alpha=0.8,
    )

    ax1.set_ylabel("百分比 (%)", fontsize=12)
    ax1.set_title("权重 vs 风险贡献\n（权重不等于风险贡献！）", fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(assets, fontsize=11)
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.3, axis="y")

    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )
    for bar in bars2:
        height = bar.get_height()
        ax1.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

    # 右图：风险贡献饼图（使用绝对值）
    ax2 = axes[1]
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
    explode = (0.05, 0, 0, 0.05, 0)  # 突出显示第一个和债券

    # 使用绝对值用于饼图（负贡献表示对冲效果）
    pct_abs = np.abs(pct_contribution)
    pct_abs = pct_abs / pct_abs.sum()  # 重新归一化

    wedges, texts, autotexts = ax2.pie(
        pct_abs,
        labels=assets,
        autopct="%1.1f%%",
        colors=colors,
        explode=explode,
        shadow=True,
        startangle=90,
    )

    # 设置字体
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")

    ax2.set_title(f"风险贡献分解\n组合波动率 = {portfolio_std*100:.1f}%", fontsize=14)

    # 添加说明文本
    info_text = f"""
    关键发现：
    • 股票C权重20%，但贡献30%风险
    • 债券权重15%，但只贡献{pct_contribution[3]*100:.1f}%风险
    • 负相关资产可降低组合风险
    """
    fig.text(
        0.5,
        -0.02,
        info_text,
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("06_risk_contribution.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 06_risk_contribution.png")


def plot_covariance_eigenvalues():
    """
    图7: 协方差矩阵特征值问题
    展示维度灾难下的特征值分散
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    np.random.seed(42)

    # 场景设置
    scenarios = [
        (10, 250, "健康: p=10, n=250"),
        (100, 250, "临界: p=100, n=250"),
        (200, 250, "危险: p=200, n=250"),
        (300, 250, "病态: p=300, n=250 (p>n)"),
    ]

    colors = ["#2ecc71", "#f39c12", "#e74c3c", "#8e44ad"]

    for idx, (p, n, title) in enumerate(scenarios):
        ax = axes[idx // 2, idx % 2]

        # 生成随机收益率数据
        returns = np.random.randn(n, p) * 0.02

        # 计算样本协方差矩阵
        cov_matrix = np.cov(returns.T)

        # 计算特征值
        eigenvalues = np.linalg.eigvalsh(cov_matrix)
        eigenvalues = np.sort(eigenvalues)[::-1]  # 降序排列

        # 绘制特征值
        ax.bar(
            range(min(50, len(eigenvalues))),
            eigenvalues[:50],
            color=colors[idx],
            alpha=0.7,
            edgecolor="white",
        )

        # 添加零线
        ax.axhline(y=0, color="black", linestyle="-", linewidth=1)

        # 统计信息
        n_negative = np.sum(eigenvalues < 1e-10)
        n_small = np.sum(eigenvalues < 1e-6)
        condition_number = eigenvalues[0] / max(eigenvalues[-1], 1e-10)

        info = f"零特征值: {n_negative}\n条件数: {condition_number:.0e}"
        ax.text(
            0.95,
            0.95,
            info,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

        ax.set_xlabel("特征值序号", fontsize=11)
        ax.set_ylabel("特征值大小", fontsize=11)
        ax.set_title(title, fontsize=13, color=colors[idx], fontweight="bold")
        ax.grid(True, alpha=0.3, axis="y")

        # 标记问题区域
        if n_negative > 0:
            ax.axhspan(-0.0001, 1e-10, alpha=0.2, color="red", label="零/负特征值")

    plt.suptitle(
        "协方差矩阵的维度灾难\n当 p ≈ n 或 p > n 时，特征值出现问题",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig("07_eigenvalue_problem.png", bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成: 07_eigenvalue_problem.png")


def plot_optimization_comparison():
    """
    图8: 有约束vs无约束优化对比
    展示约束对权重分布的影响
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    np.random.seed(42)

    # 资产设置
    assets = ["股票A", "股票B", "股票C", "股票D", "股票E"]
    n = 5

    # 协方差矩阵（故意设置一些高相关性）
    volatilities = np.array([0.20, 0.18, 0.22, 0.25, 0.15])
    corr = np.array(
        [
            [1.0, 0.8, 0.3, 0.2, -0.1],
            [0.8, 1.0, 0.4, 0.3, -0.05],
            [0.3, 0.4, 1.0, 0.6, 0.1],
            [0.2, 0.3, 0.6, 1.0, 0.2],
            [-0.1, -0.05, 0.1, 0.2, 1.0],
        ]
    )
    cov_matrix = np.outer(volatilities, volatilities) * corr

    # 场景1: 无约束最小方差（使用伪逆处理可能的奇异性）
    ones = np.ones(n)
    try:
        cov_inv = np.linalg.inv(cov_matrix)
    except:
        cov_inv = np.linalg.pinv(cov_matrix)
    weights_unconstrained = cov_inv @ ones
    weights_unconstrained = weights_unconstrained / np.sum(weights_unconstrained)

    # 场景2: 做空限制 (w >= 0)
    # 简化：使用投影方法
    weights_no_short = np.maximum(weights_unconstrained, 0)
    weights_no_short = weights_no_short / np.sum(weights_no_short)

    # 场景3: 做空限制 + 权重上限
    weights_constrained = np.clip(weights_unconstrained, 0, 0.3)
    weights_constrained = weights_constrained / np.sum(weights_constrained)

    scenarios = [
        (weights_unconstrained, "无约束", "可能出现极端做空"),
        (weights_no_short, "禁止做空 (w≥0)", "权重更集中"),
        (weights_constrained, "禁止做空 + 上限30%", "权重更均衡"),
    ]

    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]

    for idx, (weights, title, subtitle) in enumerate(scenarios):
        ax = axes[idx]

        x = np.arange(n)
        bars = ax.bar(
            x, weights * 100, color=colors, alpha=0.8, edgecolor="white", linewidth=2
        )

        # 添加数值标签
        for bar, w in zip(bars, weights):
            height = bar.get_height()
            va = "bottom" if height >= 0 else "top"
            offset = 2 if height >= 0 else -2
            ax.annotate(
                f"{w*100:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, offset),
                textcoords="offset points",
                ha="center",
                va=va,
                fontsize=10,
                fontweight="bold",
            )

        # 计算组合风险
        portfolio_risk = np.sqrt(weights @ cov_matrix @ weights) * 100

        ax.axhline(y=0, color="black", linewidth=1)
        ax.set_xticks(x)
        ax.set_xticklabels(assets, fontsize=10)
        ax.set_ylabel("权重 (%)", fontsize=11)
        ax.set_title(
            f"{title}\n{subtitle}\n组合风险: {portfolio_risk:.1f}%", fontsize=12
        )
        ax.grid(True, alpha=0.3, axis="y")

        # 设置y轴范围
        y_min = min(weights.min() * 100 - 10, -20)
        y_max = max(weights.max() * 100 + 10, 50)
        ax.set_ylim(y_min, y_max)

        # 添加约束线
        if idx == 2:
            ax.axhline(y=30, color="red", linestyle="--", linewidth=2, label="上限30%")
            ax.legend(loc="upper right")

    plt.suptitle("约束条件对投资组合权重的影响", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(
        "08_optimization_comparison.png", bbox_inches="tight", facecolor="white"
    )
    plt.close()
    print("✓ 生成: 08_optimization_comparison.png")


def main():
    """生成所有图表"""
    print("=" * 50)
    print("开始生成 Week 11 可视化图表...")
    print("=" * 50)

    plot_gradient_descent()
    plot_quadratic_form()
    plot_efficient_frontier()
    plot_monte_carlo_var()
    plot_cholesky_correlation()
    plot_risk_contribution()
    plot_covariance_eigenvalues()
    plot_optimization_comparison()

    print("=" * 50)
    print("所有图表生成完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
