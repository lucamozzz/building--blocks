#!/usr/bin/env python3

from multiprocessing import Process
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import BatteryState
from std_msgs.msg import ColorRGBA

from tesi_mozzoni import GoTo
from tesi_mozzoni import CheckBattery
from tesi_mozzoni import DetectObstacle


class CarController(Node):
    def __init__(self):
        super().__init__('car_controller')
        self.create_subscription(Vector3, 'destination', self.move, 10)
        self.create_subscription(
            BatteryState, 'charge', self.battery_handler, 10)
        self.led_pub = self.create_publisher(ColorRGBA, 'led', 10)
        self.led = ColorRGBA()
        rclpy.spin(self)

    def move(self, destination: Vector3):
        self.get_logger().info('QUI')
        runInParallel(GoTo(self, destination).start(), DetectObstacle(self).start())
        self.set_led_color(0.0, 1.0, 0.0)

    def battery_handler(self, charge: BatteryState):
        runInParallel(CheckBattery(self, charge).start(),
                      self.set_led_color(1.0, 0.0, 0.0))
        self.set_led_color(0.0, 0.0, 0.0)

    def set_led_color(self, r, g, b):
        self.led.r = r
        self.led.g = g
        self.led.b = b
        self.led_pub.publish(self.led)


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def setup():
    rclpy.init()
    controller = CarController()
    rclpy.spin(controller)
    if KeyboardInterrupt:
        rclpy.shutdown()


if __name__ == '__main__':
    setup()
