# ROS2 launch file for elevation map demo world
# Invokes mvsim/launch/launch_world.launch.py
# See: https://mvsimulator.readthedocs.io/en/latest/mvsim_node.html

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    mapfile = os.path.join(get_package_share_directory('mvsim_demo'),
                              "launch/demo_map.yaml")
    worldfile = os.path.join(get_package_share_directory('mvsim_demo'),
                              "launch/demo.world.xml")
    paramsfile = os.path.join(get_package_share_directory('mvsim_demo'),
                              "launch/nav2_params.yaml")

    ld = LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('mvsim'),
                    'launch',
                    'launch_world.launch.py'
                ])
            ]),
            launch_arguments={
                'world_file': worldfile,
                'use_rviz': 'False',
                'headless': 'True',
                'do_fake_localization': 'False'
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('nav2_bringup'),
                    'launch',
                    'bringup_launch.py'
                ])
            ]),
            launch_arguments={
                'map': mapfile,
                'use_sim_time': 'True',
                'params_file': paramsfile
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('nav2_bringup'),
                    'launch',
                    'rviz_launch.py'
                ])
            ]),
            launch_arguments={
                'map': mapfile,
                'use_sim_time': 'True',
                'params_file': paramsfile
            }.items()
        ),
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            remappings=[
                ('/cloud_in', '/lidar1_points')
            ],
            parameters=[{
                'target_frame': 'base_link',
                'min_height': 0.1
            }]
        )
    ])

    return ld
