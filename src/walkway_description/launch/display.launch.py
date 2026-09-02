import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # 1. Find the exact path to our package and the xacro file
    pkg_name = 'walkway_description'
    pkg_path = get_package_share_directory(pkg_name)
    xacro_file = os.path.join(pkg_path, 'urdf', 'humanoid.urdf.xacro')
    #world_sdf_path = os.path.join(pkg_path, 'worlds', 'test_world_1.sdf')
    world_sdf_path = os.path.join(pkg_path, 'worlds', 'sidewalk_1_1.sdf')

    # 2. Tell xacro to process the file and turn it into standard XML
    robot_description_xml = xacro.process_file(xacro_file).toxml()

    # 3. Create the Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_xml,
                    'use_sim_time': True}]
    )

    gazebo_pkg_path = get_package_share_directory('ros_gz_sim')
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg_path, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'{world_sdf_path} -r'}.items()
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'walkway_humanoid',
            '-x', '-14.0',
            '-y', '0.0',
            '-z', '0.5' # Spawn it 0.5 meters in the air so it drops into the world
        ],
        output='screen'
    )

    # 4. Joint State Publisher GUI
    #node_joint_state_publisher_gui = Node(
    #    package='joint_state_publisher_gui',
    #    executable='joint_state_publisher_gui',
    #    name='joint_state_publisher_gui'
    #)

    # 4. The Bridge: Translate Gazebo physics data into ROS 2 topics
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Syntax: /topic@ROS_MESSAGE_TYPE]GAZEBO_MESSAGE_TYPE
            # The ']' means one-way communication: ROS 2 -> Gazebo
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/gazebo_joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            #'/model/walkway_humanoid/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/camera/rgbd/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/rgbd/depth_image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/rgbd/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/camera/rgbd/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked'
        ],
        remappings=[
            #('/model/walkway_humanoid/tf', '/tf'),
            ('/gazebo_joint_states', '/joint_states')
        ],
        output='screen'
    )

    # 5. Configure Rviz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_path, 'config', 'walkway1_3.rviz')],
        parameters=[{'use_sim_time': True}]
    )

    # 6. Return the LaunchDescription so ROS 2 knows what to run
    return LaunchDescription([
        node_robot_state_publisher,
        #node_joint_state_publisher_gui
        gazebo_launch,
        spawn_robot,
        bridge_node,
        rviz_node
    ])