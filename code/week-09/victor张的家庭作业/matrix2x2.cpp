#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>
#include <fstream>

// ============================================================================
// 2×2 矩阵类(仅参考非最佳实践)
// ============================================================================
class Matrix2x2
{
public:
    double data[2][2];

    // 默认构造函数 - 单位矩阵
    Matrix2x2()
    {
        data[0][0] = 1;
        data[0][1] = 0;
        data[1][0] = 0;
        data[1][1] = 1;
    }

    // 参数构造函数
    Matrix2x2(double a, double b, double c, double d)
    {
        data[0][0] = a;
        data[0][1] = b;
        data[1][0] = c;
        data[1][1] = d;
    }

    // 矩阵乘法
    Matrix2x2 operator*(const Matrix2x2 &other) const
    {
        Matrix2x2 result;
        result.data[0][0] = data[0][0] * other.data[0][0] + data[0][1] * other.data[1][0];
        result.data[0][1] = data[0][0] * other.data[0][1] + data[0][1] * other.data[1][1];
        result.data[1][0] = data[1][0] * other.data[0][0] + data[1][1] * other.data[1][0];
        result.data[1][1] = data[1][0] * other.data[0][1] + data[1][1] * other.data[1][1];
        return result;
    }

    // 矩阵-向量乘法
    std::pair<double, double> transform(double x, double y) const
    {
        return {
            data[0][0] * x + data[0][1] * y,
            data[1][0] * x + data[1][1] * y};
    }

    // 行列式
    double determinant() const
    {
        return data[0][0] * data[1][1] - data[0][1] * data[1][0];
    }

    // 逆矩阵
    Matrix2x2 inverse() const
    {
        double det = determinant();
        if (std::abs(det) < 1e-10)
        {
            throw std::runtime_error("Matrix is singular, cannot invert");
        }
        return Matrix2x2(
            data[1][1] / det, -data[0][1] / det,
            -data[1][0] / det, data[0][0] / det);
    }

    // 转置
    Matrix2x2 transpose() const
    {
        return Matrix2x2(data[0][0], data[1][0], data[0][1], data[1][1]);
    }

    // 特征值（返回pair，可能是复数但这里简化处理实数情况）
    std::pair<double, double> eigenvalues() const
    {
        double trace = data[0][0] + data[1][1];
        double det = determinant();
        double discriminant = trace * trace - 4 * det;

        if (discriminant >= 0)
        {
            double sqrt_disc = std::sqrt(discriminant);
            return {(trace + sqrt_disc) / 2, (trace - sqrt_disc) / 2};
        }
        else
        {
            // 复数特征值，返回实部
            return {trace / 2, trace / 2};
        }
    }

    // 打印矩阵
    void print(const std::string &name = "") const
    {
        if (!name.empty())
        {
            std::cout << name << " = ";
        }
        std::cout << std::fixed << std::setprecision(3);
        std::cout << "[ " << data[0][0] << "  " << data[0][1] << " ]\n";
        std::cout << "  [ " << data[1][0] << "  " << data[1][1] << " ]\n";
    }
};

// ============================================================================
// 变换矩阵工厂函数
// ============================================================================

// 旋转矩阵 (角度为弧度)
Matrix2x2 rotation(double theta)
{
    return Matrix2x2(
        std::cos(theta), -std::sin(theta),
        std::sin(theta), std::cos(theta));
}

// 缩放矩阵
Matrix2x2 scaling(double sx, double sy)
{
    return Matrix2x2(sx, 0, 0, sy);
}

// 均匀缩放
Matrix2x2 uniformScaling(double s)
{
    return scaling(s, s);
}

// 水平剪切 (shear along x-axis)
Matrix2x2 shearX(double k)
{
    return Matrix2x2(1, k, 0, 1);
}

// 垂直剪切 (shear along y-axis)
Matrix2x2 shearY(double k)
{
    return Matrix2x2(1, 0, k, 1);
}

// 反射矩阵 (沿过原点的直线反射，角度为直线与x轴夹角)
Matrix2x2 reflection(double theta)
{
    double c2 = std::cos(2 * theta);
    double s2 = std::sin(2 * theta);
    return Matrix2x2(c2, s2, s2, -c2);
}

// 投影矩阵 (投影到过原点的直线，角度为直线与x轴夹角)
Matrix2x2 projection(double theta)
{
    double c = std::cos(theta);
    double s = std::sin(theta);
    return Matrix2x2(c * c, c * s, c * s, s * s);
}

// ============================================================================
// 向量类（辅助）
// ============================================================================
struct Vec2
{
    double x, y;
    Vec2(double x = 0, double y = 0) : x(x), y(y) {}

    Vec2 operator+(const Vec2 &v) const { return Vec2(x + v.x, y + v.y); }
    Vec2 operator-(const Vec2 &v) const { return Vec2(x - v.x, y - v.y); }
    Vec2 operator*(double s) const { return Vec2(x * s, y * s); }
    double dot(const Vec2 &v) const { return x * v.x + y * v.y; }
    double length() const { return std::sqrt(x * x + y * y); }

    void print() const
    {
        std::cout << "(" << x << ", " << y << ")";
    }
};

// ============================================================================
// 生成单位圆上的点
// ============================================================================
std::vector<Vec2> generateUnitCircle(int numPoints = 100)
{
    std::vector<Vec2> points;
    for (int i = 0; i <= numPoints; i++)
    {
        double theta = 2 * M_PI * i / numPoints;
        points.emplace_back(std::cos(theta), std::sin(theta));
    }
    return points;
}

// 应用矩阵变换到点集
std::vector<Vec2> transformPoints(const std::vector<Vec2> &points, const Matrix2x2 &m)
{
    std::vector<Vec2> result;
    for (const auto &p : points)
    {
        auto [x, y] = m.transform(p.x, p.y);
        result.emplace_back(x, y);
    }
    return result;
}

// ============================================================================
// 导出SVG格式（用于可视化）
// ============================================================================
void exportSVG(const std::string &filename,
               const std::vector<std::pair<std::vector<Vec2>, std::string>> &shapes)
{
    std::ofstream file(filename);

    file << R"(<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -4 8 8" width="400" height="400">
  <style>
    .grid { stroke: #ddd; stroke-width: 0.02; }
    .axis { stroke: #999; stroke-width: 0.03; }
  </style>
  
  <!-- Grid -->
  <g class="grid">
)";

    for (int i = -3; i <= 3; i++)
    {
        file << "    <line x1=\"-4\" y1=\"" << i << "\" x2=\"4\" y2=\"" << i << "\"/>\n";
        file << "    <line x1=\"" << i << "\" y1=\"-4\" x2=\"" << i << "\" y2=\"4\"/>\n";
    }

    file << R"(  </g>
  
  <!-- Axes -->
  <line class="axis" x1="-4" y1="0" x2="4" y2="0"/>
  <line class="axis" x1="0" y1="-4" x2="0" y2="4"/>
  
  <!-- Shapes -->
)";

    for (const auto &[points, color] : shapes)
    {
        file << "  <path d=\"M";
        for (size_t i = 0; i < points.size(); i++)
        {
            // SVG的y轴是反的
            file << points[i].x << " " << -points[i].y;
            if (i < points.size() - 1)
                file << " L";
        }
        file << " Z\" fill=\"" << color << "\" fill-opacity=\"0.3\" "
             << "stroke=\"" << color << "\" stroke-width=\"0.05\"/>\n";
    }

    file << "</svg>\n";
    file.close();
    std::cout << "SVG exported to: " << filename << std::endl;
}

// ============================================================================
// 演示程序
// ============================================================================
int main()
{
    std::cout << "╔══════════════════════════════════════════════════════════════╗\n";
    std::cout << "║           2×2 矩阵变换演示 (Matrix Transformations)          ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════════╝\n\n";

    // 1. 基本矩阵运算演示
    std::cout << "【1. 基本矩阵运算】\n";
    std::cout << "─────────────────────────────────────────\n";

    Matrix2x2 A(2, 1, 1, 3);
    Matrix2x2 B(1, 2, 0, 1);

    A.print("A");
    std::cout << std::endl;
    B.print("B");
    std::cout << std::endl;

    Matrix2x2 C = A * B;
    C.print("A × B");
    std::cout << std::endl;

    std::cout << "det(A) = " << A.determinant() << std::endl;
    auto [e1, e2] = A.eigenvalues();
    std::cout << "eigenvalues(A) = " << e1 << ", " << e2 << std::endl;

    A.inverse().print("\nA⁻¹");

    // 2. 变换矩阵演示
    std::cout << "\n\n【2. 变换矩阵】\n";
    std::cout << "─────────────────────────────────────────\n";

    double angle = M_PI / 4; // 45度

    Matrix2x2 R = rotation(angle);
    R.print("旋转 45°");
    std::cout << std::endl;

    Matrix2x2 S = scaling(2, 0.5);
    S.print("缩放 (2, 0.5)");
    std::cout << std::endl;

    Matrix2x2 Hx = shearX(0.5);
    Hx.print("水平剪切 k=0.5");
    std::cout << std::endl;

    Matrix2x2 Hy = shearY(0.5);
    Hy.print("垂直剪切 k=0.5");
    std::cout << std::endl;

    Matrix2x2 Ref = reflection(M_PI / 6); // 沿30度线反射
    Ref.print("沿30°线反射");

    // 3. 向量变换演示
    std::cout << "\n\n【3. 向量变换演示】\n";
    std::cout << "─────────────────────────────────────────\n";

    Vec2 v(1, 0);
    std::cout << "原始向量: ";
    v.print();
    std::cout << std::endl;

    auto [rx, ry] = R.transform(v.x, v.y);
    std::cout << "旋转45°后: (" << rx << ", " << ry << ")" << std::endl;

    auto [sx, sy] = S.transform(v.x, v.y);
    std::cout << "缩放后: (" << sx << ", " << sy << ")" << std::endl;

    // 4. 复合变换
    std::cout << "\n\n【4. 复合变换】\n";
    std::cout << "─────────────────────────────────────────\n";

    // 先缩放再旋转
    Matrix2x2 composite = R * S; // 注意：先应用S，再应用R
    composite.print("先缩放(2,0.5)再旋转45°");

    std::cout << "\n对向量(1,1)应用复合变换:\n";
    auto [cx, cy] = composite.transform(1, 1);
    std::cout << "(1,1) → (" << cx << ", " << cy << ")" << std::endl;

    // 5. 生成可视化数据
    std::cout << "\n\n【5. 生成SVG可视化】\n";
    std::cout << "─────────────────────────────────────────\n";

    auto circle = generateUnitCircle(100);

    // 各种变换后的形状
    auto rotated = transformPoints(circle, rotation(M_PI / 6));
    auto scaled = transformPoints(circle, scaling(2, 1));
    auto sheared = transformPoints(circle, shearX(0.8));
    auto combined = transformPoints(circle, rotation(M_PI / 4) * scaling(1.5, 0.7));

    exportSVG("circle_original.svg", {{circle, "#3498db"}});
    exportSVG("circle_scaled.svg", {{circle, "#ccc"}, {scaled, "#e74c3c"}});
    exportSVG("circle_sheared.svg", {{circle, "#ccc"}, {sheared, "#2ecc71"}});
    exportSVG("circle_combined.svg", {{circle, "#ccc"}, {combined, "#9b59b6"}});

    // 6. 验证矩阵性质
    std::cout << "\n\n【6. 矩阵性质验证】\n";
    std::cout << "─────────────────────────────────────────\n";

    // 旋转矩阵是正交矩阵
    Matrix2x2 R_T = R.transpose();
    Matrix2x2 R_RT = R * R_T;
    std::cout << "旋转矩阵正交性验证 (R × Rᵀ = I):\n";
    R_RT.print("R × Rᵀ");

    // 行列式等于面积缩放因子
    std::cout << "\n缩放矩阵的行列式 = " << S.determinant();
    std::cout << " (即面积缩放为原来的 " << S.determinant() << " 倍)\n";

    std::cout << "\n程序执行完成！\n";

    return 0;
}
