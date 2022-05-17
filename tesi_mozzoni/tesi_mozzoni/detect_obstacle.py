#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import ColorRGBA
from sensor_msgs.msg import Range
from rclpy.parameter import Parameter

class DetectObstacle():
    def __init__(self, node: Node):
        self.node = node
        self.node.declare_parameter('obstacle', False)
    
    def start(self):
        self.velocity = Twist()
        self.led = ColorRGBA()
        self.led_pub = self.node.create_publisher(ColorRGBA, 'led', 10)
        self.range_sub = self.node.create_subscription(
            Range, 'range', self.avoid_obstacle, 10)
        self.velocity_pub = self.node.create_publisher(Twist, 'cmd_vel', 10)

    def avoid_obstacle(self, obstacle_distance: Range):        
        if obstacle_distance.range < 0.5:
            self.node.get_logger().info('Metto TRUE')
            
            my_new_param = Parameter(
                    'obstacle',
                    rclpy.Parameter.Type.BOOL,
                    True
                )
            self.node.set_parameters([my_new_param])
            self.set_led_color(1.0, 1.0, 0.0)
            self.velocity.linear.x = -0.5
            self.velocity.angular.z = 1.0
            self.velocity_pub.publish(self.velocity)
            #time.sleep(10)
            self.set_led_color(0.0, 0.0, 0.0)
        else:
            self.node.get_logger().info('Metto FALSE')
            my_new_param = Parameter(
                    'obstacle',
                    rclpy.Parameter.Type.BOOL,
                    False
                )
            self.node.set_parameters([my_new_param])
            self.set_led_color(0.0, 1.0, 0.0)
            self.velocity.angular.z = 0.0

    def set_led_color(self, r, g, b):
        self.led.r = r
        self.led.g = g
        self.led.b = b
        self.led_pub.publish(self.led)


def setup():
    DetectObstacle(rclpy.create_node('detect_obs'))

if __name__ == '__main__':
    setup()