#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tesi_mozzoni import GoTo
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import Vector3


class CheckBattery():
    def __init__(self, node: Node, charge: BatteryState):
        self.node = node
        self.charge = charge
    def start(self):
        if self.charge.percentage < 0.1:
            vector = Vector3()
            vector.x = 0.0
            vector.y = 0.0
            vector.z = 0.0
            # Ipoteticamente lecoordinate della base
            GoTo(self.node, vector)

def setup():
    CheckBattery(rclpy.create_node('battery'))

if __name__ == '__main__':
    setup()