#include "../include/CoreMembers.hpp"
#include "../include/WorkStrategy.hpp"
#include <iostream>

// ========== QuantResearcher ==========
QuantResearcher::QuantResearcher(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::QUANT_RESEARCHER), work_strategy(std::make_unique<ResearchStrategy>()) {}

void QuantResearcher::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string QuantResearcher::get_skills() const
{
    return "Python, R, 统计学, 机器学习, 金融理论, 数据挖掘";
}

void QuantResearcher::propose_strategy() const
{
    std::cout << "[策略提议] " << name << " 提出新的量化策略: 基于深度学习的动量因子!" << std::endl;
}

void QuantResearcher::conduct_backtest() const
{
    std::cout << "[回测] " << name << " 正在进行历史数据回测，夏普比率达到了 2.8!" << std::endl;
}

void QuantResearcher::execute_main_task() const
{
    work_strategy->execute(name);
    propose_strategy();
    conduct_backtest();
}

// ========== QuantDeveloper ==========
QuantDeveloper::QuantDeveloper(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::QUANT_DEVELOPER), work_strategy(std::make_unique<DevelopmentStrategy>()) {}

void QuantDeveloper::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string QuantDeveloper::get_skills() const
{
    return "C++, Python, 系统架构, 低延迟交易, 数据库优化, Linux";
}

void QuantDeveloper::review_code() const
{
    std::cout << "[代码审查] " << name << " 发现了性能瓶颈，建议使用内存池优化!" << std::endl;
}

void QuantDeveloper::optimize_system() const
{
    std::cout << "[系统优化] " << name << " 成功将延迟降低了15微秒!" << std::endl;
}

void QuantDeveloper::execute_main_task() const
{
    work_strategy->execute(name);
    review_code();
    optimize_system();
}

// ========== Trader ==========
Trader::Trader(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::TRADER), work_strategy(std::make_unique<TradingStrategy>()) {}

void Trader::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string Trader::get_skills() const
{
    return "市场分析, 风险控制, 交易执行, 衍生品, 套利策略";
}

void Trader::execute_orders() const
{
    std::cout << "[订单执行] " << name << " 成功执行了100万美元的交易订单!" << std::endl;
}

void Trader::monitor_positions() const
{
    std::cout << "[仓位监控] " << name << " 当前投资组合的Beta值为0.95，风险可控。" << std::endl;
}

void Trader::execute_main_task() const
{
    work_strategy->execute(name);
    execute_orders();
    monitor_positions();
}

// ========== RiskManager ==========
RiskManager::RiskManager(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::RISK_MANAGER), work_strategy(std::make_unique<RiskManagementStrategy>()) {}

void RiskManager::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string RiskManager::get_skills() const
{
    return "风险建模, VaR计算, 压力测试, 监管合规, 风险报告";
}

void RiskManager::calculate_var() const
{
    std::cout << "[风险计算] " << name << " 计算得出今日VaR为250万美元 (95%置信度)。" << std::endl;
}

void RiskManager::check_limits() const
{
    std::cout << "[限额检查] " << name << " 检查发现所有仓位均在风险限额内。" << std::endl;
}

void RiskManager::generate_risk_report() const
{
    std::cout << "[风险报告] " << name << " 生成了详细的风险评估报告。" << std::endl;
}

void RiskManager::execute_main_task() const
{
    work_strategy->execute(name);
    calculate_var();
    check_limits();
    generate_risk_report();
}

// ========== PortfolioManager ==========
PortfolioManager::PortfolioManager(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::PORTFOLIO_MANAGER), work_strategy(std::make_unique<RiskManagementStrategy>()) {}

void PortfolioManager::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string PortfolioManager::get_skills() const
{
    return "资产配置, 投资组合理论, 业绩归因, 再平衡策略, 客户管理";
}

void PortfolioManager::rebalance_portfolio() const
{
    std::cout << "[组合再平衡] " << name << " 调整了资产配置，股票/债券比例优化至70/30。" << std::endl;
}

void PortfolioManager::optimize_allocation() const
{
    std::cout << "[配置优化] " << name << " 使用马科维茨模型优化了投资组合权重。" << std::endl;
}

void PortfolioManager::execute_main_task() const
{
    work_strategy->execute(name);
    rebalance_portfolio();
    optimize_allocation();
}

// ========== DataScientist ==========
DataScientist::DataScientist(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::DATA_SCIENTIST), work_strategy(std::make_unique<DataAnalysisStrategy>()) {}

void DataScientist::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string DataScientist::get_skills() const
{
    return "机器学习, 深度学习, 大数据处理, 特征工程, TensorFlow, PyTorch";
}

void DataScientist::clean_data() const
{
    std::cout << "[数据清洗] " << name << " 处理了500GB的市场数据，清除了异常值。" << std::endl;
}

void DataScientist::build_models() const
{
    std::cout << "[模型构建] " << name << " 构建了LSTM预测模型，准确率达到78%。" << std::endl;
}

void DataScientist::execute_main_task() const
{
    work_strategy->execute(name);
    clean_data();
    build_models();
}

// ========== ComplianceOfficer ==========
ComplianceOfficer::ComplianceOfficer(const std::string &n, double s, EmployeeLevel lvl)
    : Employee(n, s, lvl, EmployeeType::COMPLIANCE_OFFICER), work_strategy(std::make_unique<ComplianceStrategy>()) {}

void ComplianceOfficer::do_work() const
{
    prepare_work();
    execute_main_task();
    wrap_up_work();
}

std::string ComplianceOfficer::get_skills() const
{
    return "金融法规, 合规监管, 内部审计, 风险评估, 报告撰写";
}

void ComplianceOfficer::review_trades() const
{
    std::cout << "[交易审查] " << name << " 审查了今日所有交易，未发现违规行为。" << std::endl;
}

void ComplianceOfficer::check_regulations() const
{
    std::cout << "[监管检查] " << name << " 确认所有操作符合SEC和CFTC要求。" << std::endl;
}

void ComplianceOfficer::execute_main_task() const
{
    work_strategy->execute(name);
    review_trades();
    check_regulations();
}