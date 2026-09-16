# Walky Robot Navigation Stack

A ROS 2 Jazzy workspace developing perception, navigation, and control modules for a robot operating in simulated pedestrian sidewalk environments.

<img width="800" height="503" alt="Walky-Robot_demo" src="https://github.com/user-attachments/assets/b571de5f-1256-4683-8cac-7f70c0efec2b" />

## Package Architecture

### `walkway_description`
* Contains the robot URDF models and Gazebo SDF world files.
* Stores RViz configuration files for visualization.
* Provides `display.launch.py` for map scanning of the Gazebo world.

### `walkway_perception`
* Features a `voxel_filter` node to condense large arrays of 3D points.
* Includes `clear_costmap_client.py` to manually clear local and global costmaps, temporarily resolving obstacle ghosting issues.

### `walkway_navigation`
* Handles localization, path planning, and waypoint tracking using AMCL and Nav2.
* Stores the pre-generated `sidewalk_map` for simulation.
* Provides `slam.launch.py` for environment mapping and `master.launch.py` for one-command simulation spinning.
* Includes `map_saver_client.py` to save scanned maps and `waypoint_patrol.py` to initiate navigation tasks.

### `walkway_control`
* Handles hardware interfacing and motor command generation *(In Development)*.

---

## Quick Start (Docker)

This repository includes a fully containerized ROS 2 Jazzy environment. 
To build and run the simulation without installing ROS 2 locally:

1. Unlock the local display for the container:
   ```bash
   xhost +local:root
   ```

2. Build the Docker container:
    ```bash
    docker build -t walky-robot .
    ```

3. Run the container with the necessary graphical environment variables and socket volumes attached:
   ```bash
   docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device=/dev/dri walky-robot
   ```

4. Then, launch ROS:
    ```bash
    ros2 launch walkway_navigation master.launch.py
    ```

---

## Configuration & Usage

### 1. Generate a Map 
Launch the environment display and set the Fixed Frame to `map` in RViz:
```bash
ros2 launch walkway_description display.launch.py
```
In a new terminal, launch the SLAM module:
```bash
ros2 launch walkway_navigation slam.launch.py
```
In a third terminal, run the teleop node to drive the robot around and observe the map generating in RViz:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Once the entire map is scanned, save it to the workspace:
```bash
ros2 run nav2_map_server map_saver_cli -f src/walkway_navigation/maps/walkway_map_1_1
```

### 2. LiDAR Navigation
Before launching, ensure your configuration files are set for LiDAR:
* Inside `display.launch.py`, make sure `rviz_node` uses `walkway1.rviz` in arguments.
* Inside `bringup.launch.py`, make sure `nav2_params_file` uses `nav2_params_1_1.yaml`.

Run the stack:
```bash
ros2 launch walkway_navigation bringup.launch.py
```
In a new terminal,
```bash
ros2 run walkway_navigation waypoint_patrol.py
```

### 3. LiDAR + Camera Navigation
Before launching, ensure your configuration files are set for the depth camera:
* Inside `display.launch.py`, make sure `rviz_node` uses `walkway1_3.rviz` in arguments.
* Inside `bringup.launch.py`, make sure `nav2_params_file` uses `nav2_params_1_3.yaml`.

Run the stack in 3 different terminals,
```bash
ros2 launch walkway_navigation bringup.launch.py
ros2 run walkway_perception voxel_filter
ros2 run walkway_navigation waypoint_patrol.py
```
