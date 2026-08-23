cmake_minimum_required(VERSION 3.8)
project(joy_to_odrive)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(odrive_can REQUIRED)

add_executable(joy_to_odrive src/joy_to_odrive.cpp)
ament_target_dependencies(joy_to_odrive
  rclcpp
  sensor_msgs
  odrive_can
)

install(TARGETS
  joy_to_odrive
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
