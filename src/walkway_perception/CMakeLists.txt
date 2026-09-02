cmake_minimum_required(VERSION 3.8)
cmake_policy(SET CMP0144 NEW)
project(walkway_perception)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(nav2_msgs REQUIRED)

add_executable(lidar_reader_cpp src/lidar_reader.cpp)
ament_target_dependencies(lidar_reader_cpp rclcpp sensor_msgs)

add_executable(obstacle_detector_cpp src/obstacle_detector.cpp)
ament_target_dependencies(obstacle_detector_cpp rclcpp sensor_msgs std_msgs)

add_executable(voxel_filter src/voxel_filter.cpp)
ament_target_dependencies(voxel_filter rclcpp sensor_msgs pcl_conversions)

add_executable(clear_costmap_client src/clear_costmap_client.cpp)
ament_target_dependencies(clear_costmap_client rclcpp nav2_msgs)

install(TARGETS
  lidar_reader_cpp
  obstacle_detector_cpp
  voxel_filter
  clear_costmap_client
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/lidar_reader.py
  scripts/obstacle_detector.py
  scripts/pointcloud_filter.py
  scripts/clear_costmap_client.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
