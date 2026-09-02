import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Get the directories of your packages and Nav2
    desc_dir = get_package_share_directory('walkway_description')
    nav_dir = get_package_share_directory('walkway_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 2. Include the Display Launch
    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(desc_dir, 'launch', 'display.launch.py')
        )
    )

    # 3. Include AMCL Launch
    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav_dir, 'launch', 'localization.launch.py')
        )
    )

    # 4. Include the Nav2 Planners and Controllers
    nav2_params_file = os.path.join(nav_dir, 'config', 'nav2_params_1_3.yaml')
    path_planning_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'params_file': nav2_params_file
        }.items()
    )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(nav_dir, 'config', 'ekf.yaml'),
                    {'use_sim_time': True}]
    )

    # 5. Return the Master Launch Description
    return LaunchDescription([
        display_launch,
        localization_launch,
        path_planning_launch,
        ekf_node
    ])