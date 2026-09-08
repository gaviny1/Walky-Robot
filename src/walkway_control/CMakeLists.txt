cmake_minimum_required(VERSION 3.8)
project(walkway_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)

# 2. Build the C++ executable
add_executable(simple_driver_cpp src/simple_driver.cpp)
ament_target_dependencies(simple_driver_cpp rclcpp geometry_msgs)

# 3. Install the C++ executable so 'ros2 run' can find it
install(TARGETS
  simple_driver_cpp
  DESTINATION lib/${PROJECT_NAME}
)

# 4. Install the Python script so 'ros2 run' can find it
install(PROGRAMS
  scripts/simple_driver.py
  scripts/speed_tuner.py
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
