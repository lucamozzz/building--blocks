# Sub -> cambia status del led

import pathlib
import os
import rclpy
from std_msgs.msg import ColorRGBA


# Get current working path
path = str(pathlib.Path(__file__).parent.absolute())

# LEDs need to be managed as super users
def call_script(R, G, B):
    cmd = 'python3 ' + path + '/hardware/led_strip.py ' + \
        str(R) + ' ' + str(G) + ' ' + str(B)
    os.popen("sudo -S %s" % (cmd), 'w')


def setup():
    print('--> LED node')
    rclpy.init()
    node = rclpy.create_node('led_actuator')
    node.create_subscription(ColorRGBA, 'led', manageLed, 10)

    rclpy.spin(node)

    if KeyboardInterrupt:
        call_script(0, 0, 0)
        node.destroy_node()
        rclpy.shutdown()
        print('Shutting down: stopping LEDs')
        

def manageLed(colorMsg):
    R = colorMsg.r
    G = colorMsg.g
    B = colorMsg.b

    call_script(R, G, B)


if __name__ == '__main__':
    setup()
