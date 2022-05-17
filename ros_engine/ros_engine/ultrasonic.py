# Lettore distanza

import rclpy
from sensor_msgs.msg import Range, LaserScan
from .hardware.ultrasonic_sensor import UltrasonicSensor

ultrasonic = UltrasonicSensor()
dist = 0


def setup():
    print('--> ULTRASONIC node')
    rclpy.init()
    node = rclpy.create_node('ultrasonic_sensor')
    distance_pub = node.create_publisher(Range, 'range', 10)
    laser_pub = node.create_publisher(LaserScan, 'scan', 10)
    

    distance_data = Range()
    laser_data = LaserScan()

    def timer_callback():  # definition of a timer function that manages all the publications
        dist = ultrasonic.check_distance()
        print(dist)
        distance_data.range = dist
        laser_data.ranges = [dist]
        #node.get_logger().info('Publishing: "%s"' % distance_data.range)
        distance_pub.publish(distance_data)
        laser_pub.publish(laser_data)

    timer_period = 0.5  # seconds
    timer = node.create_timer(timer_period, timer_callback)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    setup()
