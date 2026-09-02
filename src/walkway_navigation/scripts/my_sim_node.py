#!/usr/bin/env python3

import rclpy
from rclpy.node import node

class MySimNode(Node):
    def __init__(self):
        super().__init__('my_sim_node',
                        parameter_overrides=[rclpy.parameter.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])
        self.get_logger().info('Python Node started with simulation time enabled!')

def main(args=None):
    rclpy.init(args=args)
    node = MySimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    