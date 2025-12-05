#include "../include/WorkStrategy.hpp"
#include <iostream>

// ResearchStrategy 实现
void ResearchStrategy::execute(const std::string &employee_name) const
{
    std::cout << "[研究策略] " << employee_name
              << " 正在阅读最新论文，挖掘Alpha因子，构建量化模型..." << std::endl;
}

// DevelopmentStrategy 实现
void DevelopmentStrategy::execute(const std::string &employee_name) const
{
    std::cout << "[开发策略] " << employee_name
              << " 正在优化交易系统，减少延迟，提升系统性能..." << std::endl;
}

// TradingStrategy 实现
void TradingStrategy::execute(const std::string &employee_name) const
{
    std::cout << "[交易策略] " << employee_name
              << " 正在监控市场，执行交易策略，管理风险敞口..." << std::endl;
}

// RiskManagementStrategy 实现
void RiskManagementStrategy::execute(const std::string &employee_name) const
{
    std::cout << "[风险管理策略] " << employee_name
              << " 正在计算VaR，监控仓位，评估市场风险..." << std::endl;
}

// DataAnalysisStrategy 实现
void DataAnalysisStrategy::execute(const std::string &employee_name) const
{
    std::cout << "[数据分析策略] " << employee_name
              << " 正在清洗数据，构建机器学习模型，进行特征工程..." << std::endl;
}

// ComplianceStrategy 实现
void ComplianceStrategy::execute(const std::string &employee_name) const
{
    std::cout << "[合规策略] " << employee_name
              << " 正在审查交易记录，检查监管合规性，生成合规报告..." << std::endl;
}