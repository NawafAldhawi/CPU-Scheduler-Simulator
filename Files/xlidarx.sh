#!/bin/bash

python3 rec_Strim.py

cd ros2_ws

# Source ROS 2 Foxy setup
source /opt/ros/foxy/setup.bash

# Source your workspace
source ~/ros2_ws/install/setup.bash


# Launch the sllidar_ros2 package
ros2 launch sllidar_ros2 view_sllidar_a3_launch.py
