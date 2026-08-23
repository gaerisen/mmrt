#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <odrive_can/msg/control_message.hpp>

class JoyToOdriveNode : public rclcpp::Node {
public:
  JoyToOdriveNode()
    : Node("joy_to_odrive")
  {
    scale_ = declare_parameter<double>("scale", 10.0);

    joy_sub_ = create_subscription<sensor_msgs::msg::Joy>(
      "/joy", 10,
      std::bind(&JoyToOdriveNode::joyCallback, this, std::placeholders::_1));

    pub_ = create_publisher<odrive_can::msg::ControlMessage>(
      "/odrive_axis0/control_message", 10);
  }

private:
  void joyCallback(const sensor_msgs::msg::Joy::SharedPtr msg) {
    // Axis 1 (left stick vertical) → velocity
    // Invert so pushing forward = positive velocity
    float vel = -msg->axes[1] * scale_;

    auto cmd = odrive_can::msg::ControlMessage();
    cmd.control_mode = 0x2;   // velocity control
    cmd.input_mode   = 0x2;   // velocity ramp
    cmd.input_pos    = 0.0f;
    cmd.input_vel    = vel;
    cmd.input_torque = 0.0f;

    pub_->publish(cmd);
  }

  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
  rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr pub_;
  double scale_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<JoyToOdriveNode>());
  rclcpp::shutdown();
  return 0;
}
