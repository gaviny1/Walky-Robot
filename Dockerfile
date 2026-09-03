# 1. Pull the official ROS 2 Jazzy image (contains Ubuntu and core ROS 2)
FROM osrf/ros:jazzy-desktop

# 2. Create your workspace directory inside the isolated container
RUN mkdir -p /rosdev_ws/src
WORKDIR /rosdev_ws

# 3. Copy your local human-written code into the container's src folder
COPY src/ ./src/

# 4. Use rosdep to read your package.xml files and install missing dependencies
RUN apt-get update && rosdep update && \
    rosdep install --from-paths src --ignore-src -y

# 5. Build the workspace (compiling your C++ nodes and linking Python)
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && colcon build"

# 6. Ensure the workspace is sourced automatically when the container is run
RUN echo "source /rosdev_ws/install/setup.bash" >> ~/.bashrc