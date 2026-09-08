from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. Bringup launch file
    bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('walkway_navigation'), 'launch', 'bringup.launch.py')
        )
    )

    # 2. Voxel filter node
    voxel_filter_node = Node(
        package='walkway_perception',
        executable='voxel_filter',
        name='voxel_filter'
    )

    # 3. Waypoint patrol node
    waypoint_patrol_node = Node(
        package='walkway_navigation',
        executable='waypoint_patrol.py',
        name='waypoint_patrol'
    )

    return LaunchDescription([
        bringup_launch,
        voxel_filter_node,
        waypoint_patrol_node
    ])