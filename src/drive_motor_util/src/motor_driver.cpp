#include <memory>
#include <rclcpp/rclcpp.hpp>
#include "geometry_msgs/msg/twist.hpp"
#include "std_msgs/msg/float32.hpp"

// Constant defines
const float PI = 3.14159265;
const float WHEEL_CIRC_METERS = (PI*0.029);
const float GEAR_RATIO = 20.0;
const float WHEELBASE_RAD_METERS = 1.67;

// Helper functions
float twist_to_lateral_vel(geometry_msgs::msg::Twist cmd)
{
	// m   wheel rev   motor rev     rad       rad
	// - x --------- x --------- x --------- = ---
	// s       m       wheel rev   motor rev    s
	
	float x = cmd.linear.x;
	x /= WHEEL_CIRC_METERS;
	x *= GEAR_RATIO;
	x *= 2*PI;
	return x;
}

float twist_to_angular_vel(geometry_msgs::msg::Twist cmd)
{
	float x = cmd.angular.z; // Yaw axis
	x *= WHEELBASE_RAD_METERS;
	x /= WHEEL_CIRC_METERS;
	x *= GEAR_RATIO;
	x *= 2*PI;
	return x;
}

// Node description; reads from `/cmd_vel`, maps those values to motor commands,
// and publishes the results
//
// TODO: Replace Float32 with a more semantically meaningful msg and/or a direct
// interface to odrive_can_node
class MotorDriver : public rclcpp::Node
{
public:
	MotorDriver() :
		Node("motor_driver")
	{
		RCLCPP_INFO(this->get_logger(), "Motor driver is up");

		r_vel_pub = create_publisher<std_msgs::msg::Float32>(
				"/r_mtr_vel", 10);

		l_vel_pub = create_publisher<std_msgs::msg::Float32>(
				"/l_mtl_vel", 10);

                cmd_vel_sub = create_subscription<geometry_msgs::msg::Twist>(
                    "/cmd_vel", 10,
                    std::bind(&MotorDriver::translate, this,
                              std::placeholders::_1)
		);
        }

        ~MotorDriver()
	{
		RCLCPP_INFO(this->get_logger(), "Motor driver destroyed");
	}

private:
	void translate(geometry_msgs::msg::Twist::UniquePtr msg)
	{
		float lin = twist_to_lateral_vel(*msg);
		float ang = twist_to_angular_vel(*msg);

		auto rvel = std_msgs::msg::Float32();
		auto lvel = std_msgs::msg::Float32();

		rvel.data = lin + ang;
		lvel.data = lin - ang;

		r_vel_pub->publish(rvel);
		l_vel_pub->publish(lvel);
	}

	rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr r_vel_pub;
	rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr l_vel_pub;
	rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub;
};

int main(int argc, char ** argv)
{
	rclcpp::init(argc, argv);

	try {
		rclcpp::spin(std::make_shared<MotorDriver>());
	} catch (std::runtime_error &e) {
		std::cerr << e.what();
		return 1;
	}

	rclcpp::shutdown();

	return 0;
}
