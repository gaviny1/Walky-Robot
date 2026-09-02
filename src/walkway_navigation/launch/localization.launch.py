#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1. Get the path to the nav2_bringup package
    pkg_dir = get_package_share_directory('walkway_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 2. Get the path to the specific map file
    #map_yaml_file = os.path.join(pkg_dir, 'maps', 'test_world_1.yaml')
    map_yaml_file = os.path.join(pkg_dir, 'maps', 'sidewalk_map.yaml')
    nav2_params_file = os.path.join(pkg_dir, 'config', 'amcl_params.yaml')

    # 3. Create launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_dir = LaunchConfiguration('map', default=map_yaml_file)
    params_file = LaunchConfiguration('params_file', default=nav2_params_file)

    # 4. Include the official localization launch file from Nav2
    localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'localization_launch.py')
        ),
        launch_arguments={
            'map': map_dir,
            'use_sim_time': use_sim_time,
            'params_file': params_file
        }.items()
    )

    return LaunchDescription([localization_cmd])
