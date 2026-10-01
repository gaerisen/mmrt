#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include "custom_interfaces/msg/fsm_event.hpp"

using FSMEvent = custom_interfaces::msg::FSMEvent;

enum class State 
{
    IDLE,
    MOVING,
    BLOCKED,
};

std::string to_string(State s) 
{
    switch (s) 
    {
        case State::IDLE: return "idle";
        case State::MOVING: return "moving";
        case State::BLOCKED: return "blocked";
    }
    return "unknown";
}

State next(State s) 
{
    switch (s) 
    {
        case State::IDLE: return State::MOVING;
        case State::MOVING: return State::BLOCKED;
        case State::BLOCKED: return State::IDLE;
    }
}

class EquipmentServicingFSM : public rclcpp::Node {
    public:
    EquipmentServicingFSM() : Node("equipment_servicing_fsm"), state_(State::IDLE) 
    {
        subscription_ = create_subscription<FSMEvent>(
            "fsm_events", 10,
            std::bind(&MissionFSM::on_event, this, std::placeholders::_1));

        publisher_ create_publisher<std_msg::String>("mission_state", 10);
    }

    private:
    void on_event(const FSMEvent::SharedPtr msg)
    {
        switch (state_)
        {
            case State::IDLE:
                if (msg->event == FSMEvent::START) 
                {
                    transition(next(state_));
                }
                break;
            case State:DONE:
            case State::FAILED:
                break;
            default:
                if (msg->source != to_string(state_)) 
                {
                    RCLCPP_WARN(get_logger(), "Ignoring event from '%s' while in '%s'",
                        msg->source.c_str(), to_string(state_).c_str());
                    return;
                }
                if (msg->event == FSMEvent::SUCCESS)
                {
                    transition(next(state_));
                }
                else if (msg->event == FSMEvent::FAILURE)
                {
                    transition(State::FAILED);
                }
                break;
        }
    }

    void transition(State s)
    {
        RCLCPP_INFO(get_logger(), "%s -> %s",
            to_string(state_).c_str(), to_string(s).c_str());
        state_ = s;

        std_msgs::msg::String out;
        out.data = to_string(state_);
        publisher_->publish(out);
    }

    State state_;
    rclcpp::Subscription<FSMEvent>::SharedPtr subscriber_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};

int main (int argc, char** argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<EquipmentServicingFSM>());
    rclcpp::shutdown();
}