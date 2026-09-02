#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class SpeedTuner(Node):
    def __init__(self):
        super().__init__('speed_tuner')

        # 1. Declare the parameter with a default value of 1.5
        self.declare_parameter('max_walking_speed', 1.5)

        # 2. Retrieve the parameter's current value
        current_speed = self.get_parameter('max_walking_speed').value

        # 3. Print it to the console
        self.get_logger().info(f'Robot walking speed set to: {current_speed} m's')

def main(args=None):
    rclpy.init(args=args)
    node = SpeedTuner()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()