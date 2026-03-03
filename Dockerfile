FROM osrf/ros:humble-desktop

RUN apt-get update && apt-get install -y \
    ros-humble-tf-transformations \
    python3-transforms3d \
    && rm -rf /var/lib/apt/lists/*
