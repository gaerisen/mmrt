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
    ld = LaunchDescription([
        Node(
            package='topic_tools',
            executable='relay',
            arguments=['/cmd_vel_nav', '/cmd_vel']
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('mvsim'),
                    'mvsim_tutorial',
                    'demo_elevation_map.launch.py'
                ])
            ])
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
                'map': 'demo_map.yaml'
            }.items()
        )
    ])

    return ld
