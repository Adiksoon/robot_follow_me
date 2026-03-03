from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'follow_bot',
                '-file', '/home/zygar/ros2_ws/src/robot_description/urdf/robot.urdf',
                '-x', '0', '-y', '0', '-z', '0.1'
            ],
            output='screen'
        )
    ])
