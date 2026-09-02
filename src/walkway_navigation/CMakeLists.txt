cmake_minimum_required(VERSION 3.8)
project(walkway_navigation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(action_msgs REQUIRED)

install(DIRECTORY 
  launch config maps rviz
  DESTINATION share/${PROJECT_NAME}
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


add_executable(map_saver_client_cpp src/map_saver_client.cpp)
ament_target_dependencies(map_saver_client_cpp rclcpp nav_msgs)

add_executable(pose_tracker_cpp src/pose_tracker.cpp)
ament_target_dependencies(pose_tracker_cpp rclcpp geometry_msgs)

add_executable(nav_client_cpp src/nav_client.cpp)
ament_target_dependencies(nav_client_cpp rclcpp rclcpp_action nav2_msgs)

add_executable(waypoint_patrol_cpp src/waypoint_patrol.cpp)
ament_target_dependencies(waypoint_patrol_cpp rclcpp rclcpp_action nav2_msgs)

add_executable(ekf_monitor src/ekf_monitor.cpp)
ament_target_dependencies(ekf_monitor rclcpp nav_msgs)

add_executable(stuck_monitor src/stuck_monitor.cpp)
ament_target_dependencies(stuck_monitor rclcpp nav2_msgs action_msgs)


install(TARGETS 
  map_saver_client_cpp
  pose_tracker_cpp
  nav_client_cpp
  waypoint_patrol_cpp
  ekf_monitor
  stuck_monitor
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS 
  scripts/map_saver_client.py
  scripts/pose_tracker.py
  scripts/nav_action_client.py
  scripts/waypoint_patrol.py
  scripts/ekf_monitor.py
  scripts/stuck_monitor.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
