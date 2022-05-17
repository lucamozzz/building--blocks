# Gira o si muove

import rclpy
from geometry_msgs.msg import Twist
from .hardware.motors import Motors

motors = Motors()

def setup():  # Motor initialization
    print('--> MOTOR node')
    motors.motor_init()

    # initialization of ROS subscriber
    rclpy.init()
    node = rclpy.create_node('movement_actuator')
    node.create_subscription(Twist, 'cmd_vel', move, 10)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()
        print('Shutting down: stopping motors')
        motors.motor_stop()


# ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
def move(twistMsg):
    turn = ''
    direction=''
    lin_vel = 0
    lin_vel = twistMsg.linear.x
    ang_vel = twistMsg.angular.z
    if lin_vel < 0.8:
        speed = abs(0.8 * 100)
    else:
        speed = abs(lin_vel * 100)
    if lin_vel > 0:
        direction = 'forward'
    elif lin_vel < 0:
        direction = 'backward'
    if ang_vel > 0:
        turn = 'right'
    elif ang_vel < 0:
        turn = 'left'
    elif lin_vel == 0 and ang_vel == 0:
        direction = 'no'
    motors.movement(direction, turn, speed)

if __name__ == '__main__':
    setup()
