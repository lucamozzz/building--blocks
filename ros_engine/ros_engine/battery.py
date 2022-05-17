from os import stat
import rclpy
from sensor_msgs.msg import BatteryState


def setup():
    rclpy.init()
    state = BatteryState()
    state.voltage = 5.0
    state.percentage = 1.0 # Charge percentage on 0 to 1 range
    node = rclpy.create_node('battery')
    charge_pub = node.create_publisher(BatteryState, 'charge', 10)

    def timer_callback():
        charge_pub.publish(state)
        state.percentage = state.percentage - 0.1
    timer = node.create_timer(300, timer_callback)
    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    setup()
