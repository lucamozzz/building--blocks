from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg = 'ros_engine'

    return LaunchDescription([
        Node(package=pkg, executable='move'),
        Node(package=pkg, executable='ultrasonic'),
        Node(package=pkg, executable='led'),
        Node(package=pkg, executable='battery'),
        Node(package=pkg, executable='odometry'),
        
    ])
