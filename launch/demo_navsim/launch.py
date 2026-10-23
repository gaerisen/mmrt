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
    worldfile = os.path.join("demo.world.xml")

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
                'world_file': 'demo.world.xml',
                'use_rviz': 'False',
                'headless': 'False',
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
                'map': 'demo_map.yaml',
                'use_sim_time': 'True',
                'params_file': 'nav2_params.yaml'
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
                'map': 'demo_map.yaml',
                'use_sim_time': 'True',
                'params_file': 'nav2_params.yaml'
            }.items()
        ),
        Node(
            package='topic_tools',
            executable='relay',
            parameters=[{
                'input_topic': '/laser1',
                'output_topic': '/scan'
            }]
        )
    ])

    return ld
