#pragma once

#include <string>
#include <vector>
#include <memory>

// 事件类型枚举
enum class EventType
{
    STRATEGY_PROPOSED,
    CODE_REVIEW_REQUESTED,
    MARKET_UPDATE,
    RISK_ALERT,
    PERFORMANCE_REVIEW,
    COMPLIANCE_CHECK,
    DATA_READY
};

// 事件类
class TeamEvent
{
private:
    EventType type;
    std::string sender;
    std::string message;
    std::vector<std::string> data;

public:
    TeamEvent(EventType t, const std::string &sender, const std::string &msg);
    TeamEvent(EventType t, const std::string &sender, const std::string &msg,
              const std::vector<std::string> &data);

    EventType get_type() const { return type; }
    std::string get_sender() const { return sender; }
    std::string get_message() const { return message; }
    const std::vector<std::string> &get_data() const { return data; }
};