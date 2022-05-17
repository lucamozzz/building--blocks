#!/usr/bin/env python3

import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3, Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion


class GoTo():
    def __init__(self, node: Node, vector: Vector3):
        self.destination = vector
        self.node = node
        self.obstacle = False
    
    def start(self):
        self.velocity = Twist()
        self.position = Odometry()
        self.is_rotating = False
        self.ang_vel = 0.0
        self.lin_vel = 0.8
        self.roll = self.pitch = self.yaw = 0.0
        self.reached = False

        self.odom_sub = self.node.create_subscription(
            Odometry, 'odom', self.get_position, 10)
        self.velocity_pub = self.node.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.5
        self.timer = self.node.create_timer(timer_period, self.velocity_callback)

    def destroy_activity(self):
        self.node.destroy_publisher(self.velocity_pub)
        self.node.destroy_subscription(self.odom_sub)

    def velocity_callback(self):
        self.obstacle = self.node.get_parameter('obstacle').get_parameter_value().bool_value
        self.node.get_logger().info(str(self.obstacle))
        
        if not self.obstacle:
            self.velocity_pub.publish(self.velocity)

    def rotate(self, angle):
        self.is_rotating = True
        check = angle - self.yaw
        self.velocity.angular.z = self.ang_vel * (check)
        if check < 0.002 and check > -0.002:
            self.is_rotating = False

    def get_position(self, odometry: Odometry):
        self.position = odometry.pose.pose
        x = self.position.position.x
        y = self.position.position.y

        orientation_q = odometry.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y,
                            orientation_q.z, orientation_q.w]
        (self.roll, self.pitch, self.yaw) = euler_from_quaternion(orientation_list)

        diff_x = self.destination.x - x
        diff_y = self.destination.y - y
        angle_to_goal = math.atan2(diff_y, diff_x)

        if abs(diff_x) < 0.65 and abs(diff_y) < 0.65:
            if not self.reached:
                self.velocity.linear.x = 0.0
                self.velocity.angular.z = 0.0
                self.velocity_pub.publish(self.velocity)
                time.sleep(0.2)
                self.reached = True
        else:
            self.rotate(angle_to_goal)
            if not self.is_rotating and not self.obstacle:
                self.velocity.linear.x = self.lin_vel
                self.velocity.angular.z = 0.0
        
        if not self.obstacle:
            self.velocity_pub.publish(self.velocity)


def setup():
    GoTo(rclpy.create_node('go_to'))

if __name__ == '__main__':
    setup()