#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid

class MapMonitor(Node):
    def __init__(self):
        super().__init__('map_monitor')
        self.subscription = self.create_subscription(
            OccupancyGrid, '/map', self.map_callback,10
        )

    def map_callback(self, msg):
        self.get_logger().info(
            f'Received map! Size: {msg.info.width}x{msg.info.height}, '
            f'Resolution: {msg.info.resolution} m/cell'
        )

def main(args=None):
    rclpy.init(args=args)
    node = MapMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()