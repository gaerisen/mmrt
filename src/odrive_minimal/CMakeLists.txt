cmake_minimum_required(VERSION 3.20)
project(odrive_minimal)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
	add_compile_options(-Wall -Wextra -Wpedantic -Iinclude)
endif()

set(CMAKE_CXX_STANDARD 20)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(listener src/odrive_node.cpp
			src/odrive.c
			src/can_util.c)

target_link_libraries(listener PUBLIC rclcpp::rclcpp std_msgs::std_msgs)

install(TARGETS
		listener
		DESTINATION lib/${PROJECT_NAME})

ament_package()

