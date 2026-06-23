#include <memory>

extern "C" {
	#include "odrive.h"
}

#include "rclcpp/rclcpp.hpp"
#include "rclcpp/logging.hpp"
#include "std_msgs/msg/float32.hpp"

class ODriveSubscriber : public rclcpp::Node
{
public:
	ODriveSubscriber() :
		Node("odrive_subscriber")
	{
		sock_ = init_can("can0");
		if (sock_ == -1) throw std::runtime_error(
				"Couldn't initialize CAN socket");

		if (set_axis_state(sock_, 42, 8))
			throw std::runtime_error(
				"Couldn't set axis state");

		if (set_controller_mode(sock_, 42, 2, 2))
			throw std::runtime_error(
				"Couldn't set controller mode");

		auto topic_callback = 
			[this](std_msgs::msg::Float32::UniquePtr msg) -> void
			{
				RCLCPP_INFO(	this->get_logger(),
						"Tgt velocity: '%.2f'\n",
						msg->data);
				set_input_vel(sock_, 42, msg->data, 0);
			};

		subscription_ =
			this->create_subscription<std_msgs::msg::Float32>(
					"motor_vel", 10, topic_callback);
	}

	~ODriveSubscriber()
	{
		RCLCPP_INFO(	this->get_logger(),
				"Reached destructor\n");
		set_axis_state(sock_, 42, 1);
		set_controller_mode(sock_, 42, 0, 0);
	}

private:
	rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr subscription_;
	int sock_;
};

int main(int argc, char *argv[])
{
	rclcpp::init(argc, argv);

	try {
		rclcpp::spin(std::make_shared<ODriveSubscriber>());
	} catch (std::runtime_error &e) {
		std::cerr << e.what();
		return 1;
	}

	rclcpp::shutdown();

	return 0;
}
