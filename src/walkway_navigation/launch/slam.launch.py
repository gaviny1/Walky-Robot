#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node 

def generate_launch_description():
    # 1. Find our package and the slam_toolbox package
    pkg_dir = get_package_share_directory('walkway_navigation')
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    # 2. Define the paths to the launch and config files
    slam_launch_file = os.path.join(slam_toolbox_dir, 'launch','online_async_launch.py')
    slam_config_file = os.path.join(pkg_dir, 'config', 'mapper_params_online_async.yaml')

    # 3. Include the SLAM launch file with our specific arguments
    slam_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch_file),
            launch_arguments={
                'slam_params_file': slam_config_file,
                'use_sim_time': 'true',
            }.items()
        )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(pkg_dir, 'config', 'ekf.yaml'),
                    {'use_sim_time': True}]
    )

    return LaunchDescription([
        slam_launch,
        ekf_node
        ])