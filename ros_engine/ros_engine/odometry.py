import time
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

odometry_position = Odometry()
x = 0.0
y = 0.0
th = 0.0

vx = 0.0
vth = 0.0
current_time = 0.0
last_time = 0.0

def estimateOdom(node):
    global x, y, th, current_time, last_time
    current_time = node.get_clock().now().nanoseconds / 1e9
    
    dt = current_time - last_time
    delta_x = (vx * math.cos(th)) * dt
    delta_y = (vx * math.sin(th)) * dt
    delta_th = vth * dt

    x = x + delta_x
    y = y + delta_y
    th = th + delta_th
    
    odometry_position.pose.pose.position.x = x
    odometry_position.pose.pose.position.y = y
    odometry_position.pose.pose.position.z = 0.0
    
    last_time = current_time

  
def setup():
    global last_time
    print('--> ODOM node')
    rclpy.init()
    node = rclpy.create_node('odometry')
    node.create_subscription(Twist, '/cmd_vel', set_vels, 10)
    odom_pub = node.create_publisher(Odometry, '/odom', 10)
    last_time = node.get_clock().now().nanoseconds / 1e9
    def odom_callback():
        estimateOdom(node)
        odom_pub.publish(odometry_position)
    node.create_timer(1.0, odom_callback)
    
    rclpy.spin(node)
    

def set_vels(twistMsg):
    global vx
    global vth
    vx = twistMsg.linear.x
    vth = twistMsg.angular.z
    
    odometry_position.twist.twist = twistMsg
    

if __name__ == '__main__':
    setup()
