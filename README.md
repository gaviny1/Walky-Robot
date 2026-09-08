# Walky Robot Navigation Stack

A ROS 2 Jazzy workspace developing perception, navigation, and control modules for a robot operating in simulated pedestrian sidewalk environments.

## Quick Start 

## Config Setting
1. Save a map 
    launch display.launch.py   
        set Fixed Frame to map
    
    Launch slam.launch.py 

    Run teleop_twist_keyboard
        drive the robot around and observe map generated in RViz 

    Scan the entire map, and run nav2_map_server map_saver_cli -f src/walkway_navigation/maps/walkway_map_1_1

2. LiDAR 
    Inside display.launch.py,
    make sure rviz_node uses walkway1.rviz

    Inside bringup.launch.py,
    make sure nav2_params_file uses nav2_params_1.yaml

    bringup.launch.py
    waypoint_patrol.py

3. Camera
    Inside display.launch.py,
    make sure rviz_node uses walkway1_1.rviz

    Inside bringup.launch.py,
    make sure nav2_params_file uses nav2_params_1_1.yaml
    
    bringup.launch.py
    voxel_filter
    waypoint_patrol.py

## Docker
This repository includes a fully containerized ROS 2 Jazzy environment. To build and run the simulation without installing ROS 2 locally:

1. Unlock local display for the container:
   ```bash
   xhost +local:root

2. Run the container with the necessary graphical environment variables and socket volumes attached:
   ```bash
   docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device=/dev/dri walky-robot

