#include "../include/TeamEvent.hpp"

TeamEvent::TeamEvent(EventType t, const std::string &sender, const std::string &msg)
    : type(t), sender(sender), message(msg) {}

TeamEvent::TeamEvent(EventType t, const std::string &sender, const std::string &msg,
                     const std::vector<std::string> &data)
    : type(t), sender(sender), message(msg), data(data) {}