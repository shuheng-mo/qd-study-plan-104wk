"""
Week 10 - 为小红书文章生成静态图示（修复版）
解决中文字体显示问题
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
from matplotlib.font_manager import FontProperties

# 直接指定系统中文字体文件
FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'
CN_FONT = FontProperties(fname=FONT_PATH)

print(f"✓ 加载中文字体: {FONT_PATH}")

# 设置负号正确显示
plt.rcParams['axes.unicode_minus'] = False

# 输出目录
output_dir = "rednote_figures"
import os
os.makedirs(output_dir, exist_ok=True)

def save_fig(name):
    """保存图表"""
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png", dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 已生成: {name}.png")
    plt.close()


# ============================================================
# 图1: 特征向量 vs 普通向量
# ============================================================
def fig1_eigenvector_comparison():
    """特征向量只被拉伸，普通向量方向会改变"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 左图：普通向量
    ax1.set_xlim(-0.5, 3)
    ax1.set_ylim(-0.5, 2)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('普通向量：方向改变', fontproperties=CN_FONT, fontsize=16, fontweight='bold')
    
    # 原向量
    ax1.arrow(0, 0, 1, 0, head_width=0.15, head_length=0.15, fc='blue', ec='blue', linewidth=2)
    ax1.text(0.5, -0.3, 'v', fontsize=14, color='blue', ha='center')
    
    # 变换后的向量
    ax1.arrow(0, 0, 2, 1, head_width=0.15, head_length=0.15, fc='red', ec='red', linewidth=2)
    ax1.text(1.3, 0.8, 'Av', fontsize=14, color='red', ha='center')
    
    # 右图：特征向量
    ax2.set_xlim(-0.5, 3)
    ax2.set_ylim(-0.5, 2)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('特征向量：只拉伸不旋转', fontproperties=CN_FONT, fontsize=16, fontweight='bold')
    
    # 原向量
    ax2.arrow(0, 0, 0.7, 0.7, head_width=0.15, head_length=0.15, fc='blue', ec='blue', linewidth=2)
    ax2.text(0.35, 0.2, 'v', fontsize=14, color='blue', ha='center')
    
    # 变换后的向量（同方向，3倍长度）
    ax2.arrow(0, 0, 2.1, 2.1, head_width=0.15, head_length=0.15, fc='green', ec='green', linewidth=2)
    ax2.text(1.5, 1.5, 'λv (λ=3)', fontsize=14, color='green', ha='center')
    
    save_fig('01_eigenvector_comparison')


# ============================================================
# 图2: 单位圆变椭圆
# ============================================================
def fig2_circle_to_ellipse():
    """矩阵变换：单位圆→椭圆"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 单位圆
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)
    ax.plot(circle_x, circle_y, 'b-', linewidth=2, label='原始单位圆')
    
    # 变换矩阵 A = [[3, 0], [0, 2]]
    A = np.array([[3, 0], [0, 2]])
    points = np.array([circle_x, circle_y])
    transformed = A @ points
    
    ax.plot(transformed[0], transformed[1], 'orange', linewidth=2, label='变换后椭圆')
    
    # 特征向量（主轴方向）
    ax.arrow(0, 0, 3, 0, head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=2)
    ax.text(1.5, -0.5, 'v₁ (λ₁=3)', fontproperties=CN_FONT, fontsize=13, color='red')
    
    ax.arrow(0, 0, 0, 2, head_width=0.2, head_length=0.2, fc='green', ec='green', linewidth=2)
    ax.text(-0.8, 1, 'v₂ (λ₂=2)', fontproperties=CN_FONT, fontsize=13, color='green')
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    # 图例
    legend = ax.legend(fontsize=12, prop=CN_FONT)
    ax.set_title('单位圆 → 椭圆：特征向量是主轴方向', fontproperties=CN_FONT, fontsize=14, fontweight='bold')
    
    save_fig('02_circle_to_ellipse')


# ============================================================
# 图3: PageRank网络图
# ============================================================
def fig3_pagerank_network():
    """PageRank: 网页链接网络"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 节点位置
    positions = {
        'A': (1, 3),
        'B': (4, 3),
        'C': (1, 1),
        'D': (4, 1)
    }
    
    # 绘制节点
    for name, (x, y) in positions.items():
        circle = Circle((x, y), 0.35, color='skyblue', ec='navy', linewidth=2, zorder=10)
        ax.add_patch(circle)
        ax.text(x, y, name, fontsize=20, ha='center', va='center', fontweight='bold', zorder=11)
    
    # 绘制边（箭头）
    edges = [
        ('B', 'A'), ('C', 'A'), ('D', 'B'),
        ('A', 'C'), ('B', 'D'), ('C', 'D')
    ]
    
    for src, dst in edges:
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        
        # 计算箭头位置（避开圆形节点）
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        dx /= dist
        dy /= dist
        
        start = (x1 + dx*0.4, y1 + dy*0.4)
        end = (x2 - dx*0.4, y2 - dy*0.4)
        
        arrow = FancyArrowPatch(start, end, arrowstyle='->', mutation_scale=20,
                               linewidth=2, color='gray', zorder=5)
        ax.add_patch(arrow)
    
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('PageRank：网页链接网络\n重要性通过链接传递', fontproperties=CN_FONT, fontsize=14, fontweight='bold')
    
    # 添加说明
    ax.text(2.5, 0.3, 'PageRank = 转移矩阵M的特征向量 (λ=1)', 
            fontproperties=CN_FONT, fontsize=12, ha='center', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    save_fig('03_pagerank_network')


# ============================================================
# 图4: SVD分解示意
# ============================================================
def fig4_svd_decomposition():
    """SVD分解：A = UΣVᵀ"""
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # A矩阵
    rect_A = FancyBboxPatch((0.5, 1), 1.5, 2, boxstyle="round,pad=0.1", 
                            ec='blue', fc='lightblue', linewidth=2)
    ax.add_patch(rect_A)
    ax.text(1.25, 2, 'A', fontsize=24, ha='center', va='center', fontweight='bold')
    ax.text(1.25, 0.5, 'm×n', fontsize=12, ha='center')
    
    # 等号
    ax.text(2.5, 2, '=', fontsize=24, ha='center', va='center')
    
    # U矩阵
    rect_U = FancyBboxPatch((3.2, 1), 1.2, 2, boxstyle="round,pad=0.1", 
                            ec='red', fc='lightcoral', linewidth=2)
    ax.add_patch(rect_U)
    ax.text(3.8, 2, 'U', fontsize=24, ha='center', va='center', fontweight='bold')
    ax.text(3.8, 0.5, 'm×m', fontsize=12, ha='center')
    
    # 乘号
    ax.text(4.8, 2, '×', fontsize=20, ha='center', va='center')
    
    # Σ矩阵
    rect_S = FancyBboxPatch((5.3, 1.3), 1.5, 1.4, boxstyle="round,pad=0.1", 
                            ec='green', fc='lightgreen', linewidth=2)
    ax.add_patch(rect_S)
    ax.text(6.05, 2, 'Σ', fontsize=24, ha='center', va='center', fontweight='bold')
    ax.text(6.05, 0.5, 'm×n', fontsize=12, ha='center')
    
    # 乘号
    ax.text(7.2, 2, '×', fontsize=20, ha='center', va='center')
    
    # Vᵀ矩阵
    rect_V = FancyBboxPatch((7.7, 1.5), 1.8, 1, boxstyle="round,pad=0.1", 
                            ec='purple', fc='plum', linewidth=2)
    ax.add_patch(rect_V)
    ax.text(8.6, 2, 'Vᵀ', fontsize=24, ha='center', va='center', fontweight='bold')
    ax.text(8.6, 0.5, 'n×n', fontsize=12, ha='center')
    
    # 说明文字（使用中文字体）
    ax.text(1.25, 3.5, '原矩阵', fontproperties=CN_FONT, fontsize=11, ha='center', color='blue')
    ax.text(3.8, 3.5, '左奇异向量', fontproperties=CN_FONT, fontsize=11, ha='center', color='red')
    ax.text(6.05, 3.5, '奇异值(对角)', fontproperties=CN_FONT, fontsize=11, ha='center', color='green')
    ax.text(8.6, 3.5, '右奇异向量', fontproperties=CN_FONT, fontsize=11, ha='center', color='purple')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title('SVD：万能的矩阵分解', fontproperties=CN_FONT, fontsize=14, fontweight='bold', pad=20)
    
    save_fig('04_svd_decomposition')


# ============================================================
# 图5: PCA降维
# ============================================================
def fig5_pca_dimension_reduction():
    """PCA：找到方差最大的方向"""
    np.random.seed(42)
    
    # 生成2D数据（修复协方差矩阵为正定）
    mean = [0, 0]
    cov = [[2, 1.2], [1.2, 1]]
    data = np.random.multivariate_normal(mean, cov, 200)
    
    # 计算主成分
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    pca.fit(data)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 散点图
    ax.scatter(data[:, 0], data[:, 1], alpha=0.5, s=50, c='steelblue', edgecolor='navy')
    
    # 主成分方向
    for i, (comp, var) in enumerate(zip(pca.components_, pca.explained_variance_)):
        comp = comp * np.sqrt(var) * 3  # 缩放以便可视化
        ax.arrow(0, 0, comp[0], comp[1], head_width=0.3, head_length=0.3,
                fc=['red', 'green'][i], ec=['red', 'green'][i], linewidth=3, alpha=0.8)
        ax.text(comp[0]*1.2, comp[1]*1.2, f'PC{i+1}\n({pca.explained_variance_ratio_[i]*100:.0f}%)',
                fontproperties=CN_FONT, fontsize=12, ha='center', fontweight='bold', color=['red', 'green'][i])
    
    ax.set_xlabel('特征1', fontproperties=CN_FONT, fontsize=12)
    ax.set_ylabel('特征2', fontproperties=CN_FONT, fontsize=12)
    ax.set_title('PCA：找到方差最大的方向\n(箭头长度 ∝ 方差大小)', fontproperties=CN_FONT, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_aspect('equal')
    
    save_fig('05_pca_dimension_reduction')


# ============================================================
# 图6: 推荐系统评分矩阵
# ============================================================
def fig6_recommendation_matrix():
    """推荐系统：用户-商品评分矩阵"""
    # 评分矩阵（NaN表示未评分）
    ratings = np.array([
        [5, 3, np.nan, 1],
        [4, np.nan, np.nan, 1],
        [1, 1, np.nan, 5],
        [np.nan, np.nan, 4, 4]
    ])
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 创建mask用于显示
    mask = np.isnan(ratings)
    display_data = np.where(mask, 0, ratings)
    
    # 绘制热力图
    im = ax.imshow(display_data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=5)
    
    # 设置刻度
    users = ['Alice', 'Bob', 'Carol', 'Dave']
    movies = ['电影1', '电影2', '电影3', '电影4']
    ax.set_xticks(np.arange(len(movies)))
    ax.set_yticks(np.arange(len(users)))
    ax.set_xticklabels(movies, fontproperties=CN_FONT, fontsize=12)
    ax.set_yticklabels(users, fontsize=12)
    
    # 添加文本
    for i in range(len(users)):
        for j in range(len(movies)):
            if mask[i, j]:
                text = '?'
                color = 'red'
                weight = 'bold'
            else:
                text = f'{int(ratings[i, j])}'
                color = 'white' if ratings[i, j] > 2.5 else 'black'
                weight = 'normal'
            ax.text(j, i, text, ha='center', va='center', 
                   color=color, fontsize=18, fontweight=weight)
    
    ax.set_title('推荐系统：用户-商品评分矩阵\n目标：预测 ? 处的评分', 
                fontproperties=CN_FONT, fontsize=14, fontweight='bold')
    
    # 添加colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('评分', fontproperties=CN_FONT, rotation=270, labelpad=15, fontsize=11)
    
    # 添加说明
    ax.text(1.5, 4.5, 'R ≈ P × Qᵀ  (矩阵分解)', fontproperties=CN_FONT,
           fontsize=12, ha='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    save_fig('06_recommendation_matrix')


# ============================================================
# 图7: 有效前沿
# ============================================================
def fig7_efficient_frontier():
    """投资组合优化：有效前沿"""
    np.random.seed(42)
    
    # 生成随机投资组合
    n_portfolios = 1000
    returns = []
    risks = []
    
    for _ in range(n_portfolios):
        # 随机权重
        weights = np.random.random(5)
        weights /= weights.sum()
        
        # 假设的收益和风险
        portfolio_risk = np.random.uniform(8, 25)
        
        # 引入相关性（风险高收益也倾向于高）
        portfolio_return = 5 + 0.4 * portfolio_risk + np.random.randn() * 2
        
        returns.append(portfolio_return)
        risks.append(portfolio_risk)
    
    returns = np.array(returns)
    risks = np.array(risks)
    
    # 计算有效前沿（找每个风险水平的最高收益）
    risk_bins = np.linspace(risks.min(), risks.max(), 50)
    frontier_returns = []
    frontier_risks = []
    
    for i in range(len(risk_bins)-1):
        mask = (risks >= risk_bins[i]) & (risks < risk_bins[i+1])
        if mask.any():
            max_return = returns[mask].max()
            frontier_returns.append(max_return)
            frontier_risks.append(risk_bins[i])
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 散点图：所有投资组合
    ax.scatter(risks, returns, alpha=0.3, s=20, c='steelblue', label='可行组合')
    
    # 有效前沿
    ax.plot(frontier_risks, frontier_returns, 'r-', linewidth=3, label='有效前沿')
    
    # 最小方差点
    min_risk_idx = np.argmin(risks)
    ax.scatter(risks[min_risk_idx], returns[min_risk_idx], 
              s=200, c='green', marker='*', edgecolor='darkgreen', 
              linewidth=2, label='最小方差组合', zorder=10)
    
    ax.set_xlabel('风险 (标准差 %)', fontproperties=CN_FONT, fontsize=12)
    ax.set_ylabel('预期收益 (%)', fontproperties=CN_FONT, fontsize=12)
    ax.set_title('Markowitz有效前沿\n相同风险下，前沿上的组合收益最高', 
                fontproperties=CN_FONT, fontsize=14, fontweight='bold')
    
    # 图例
    legend = ax.legend(fontsize=11, loc='lower right', prop=CN_FONT)
    ax.grid(True, alpha=0.3)
    
    save_fig('07_efficient_frontier')


# ============================================================
# 图8: 条件数比较
# ============================================================
def fig8_condition_number():
    """数值稳定性：条件数的影响"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 左图：良态矩阵（圆形）
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)
    ax1.plot(circle_x, circle_y, 'g-', linewidth=3)
    ax1.fill(circle_x, circle_y, alpha=0.2, color='green')
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.set_title('良态矩阵\nκ(A) ≈ 1', fontproperties=CN_FONT, fontsize=14, fontweight='bold', color='green')
    ax1.text(0, -1.8, '误差不会被放大\n数值计算稳定', fontproperties=CN_FONT,
            ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax1.grid(True, alpha=0.3)
    
    # 右图：病态矩阵（扁椭圆）
    ellipse_x = circle_x * 1.2
    ellipse_y = circle_y * 0.15
    ax2.plot(ellipse_x, ellipse_y, 'r-', linewidth=3)
    ax2.fill(ellipse_x, ellipse_y, alpha=0.2, color='red')
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect('equal')
    ax2.set_title('病态矩阵\nκ(A) >> 1', fontproperties=CN_FONT, fontsize=14, fontweight='bold', color='red')
    ax2.text(0, -1.8, '微小误差被放大\n数值计算不稳定', fontproperties=CN_FONT,
            ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle('条件数 κ(A) = 最大奇异值 / 最小奇异值', fontproperties=CN_FONT, fontsize=15, fontweight='bold', y=1.02)
    
    save_fig('08_condition_number')


# ============================================================
# 图9: 矩阵分解对比
# ============================================================
def fig9_decomposition_comparison():
    """矩阵分解三剑客对比"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    
    # 表格数据
    methods = ['SVD', 'PCA', 'LU', 'QR']
    properties = ['公式', '适用范围', '主要用途', '数值特点']
    
    data = {
        'SVD': ['A = UΣVᵀ', '任意矩阵', '降维/压缩/推荐', '万能但较慢'],
        'PCA': ['协方差矩阵\n特征分解', '数据矩阵', '特征提取/因子', '找主成分'],
        'LU': ['A = LU', '方阵', '解方程组', '效率高O(n²)'],
        'QR': ['A = QR', '任意矩阵', '最小二乘', '数值稳定'],
    }
    
    # 绘制表格
    cell_height = 0.8
    cell_width = 2.5
    
    # 表头
    for i, prop in enumerate(['方法'] + properties):
        rect = FancyBboxPatch((0, 4.2 - i*cell_height), cell_width*0.8, cell_height*0.9,
                              boxstyle="round,pad=0.05", ec='black', fc='lightgray', linewidth=2)
        ax.add_patch(rect)
        ax.text(cell_width*0.4, 4.6 - i*cell_height, prop, fontproperties=CN_FONT,
               ha='center', va='center', fontsize=11, fontweight='bold')
    
    # 表格内容
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
    for j, method in enumerate(methods):
        for i, values in enumerate([method] + data[method]):
            x = (j + 1) * cell_width
            y = 4.2 - i * cell_height
            
            color = colors[j] if i == 0 else 'white'
            rect = FancyBboxPatch((x, y), cell_width*0.9, cell_height*0.9,
                                 boxstyle="round,pad=0.05", ec='gray', fc=color, linewidth=1)
            ax.add_patch(rect)
            ax.text(x + cell_width*0.45, y + cell_height*0.45, values, fontproperties=CN_FONT,
                   ha='center', va='center', fontsize=10)
    
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 5.5)
    ax.set_title('矩阵分解方法对比', fontproperties=CN_FONT, fontsize=15, fontweight='bold', pad=20)
    
    save_fig('09_decomposition_comparison')


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 60)
    print("生成Week 10小红书配图（中文字体修复版）")
    print("=" * 60)
    
    fig1_eigenvector_comparison()
    fig2_circle_to_ellipse()
    fig3_pagerank_network()
    fig4_svd_decomposition()
    fig5_pca_dimension_reduction()
    fig6_recommendation_matrix()
    fig7_efficient_frontier()
    fig8_condition_number()
    fig9_decomposition_comparison()
    
    print("=" * 60)
    print(f"✓ 所有图表已生成在 {output_dir}/ 目录")
    print(f"✓ 中文字体使用: STHeiti Medium")
    print("=" * 60)


if __name__ == "__main__":
    main()
