#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarReader(Node):
    def __init__(self):
        super().__init__('lidar_reader')
        
        self.subscriber_ = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10
        )
    
    def listener_callback(self, msg):
        # LiDAR sends 360 samples, the middle index (180) is usually straight ahead.
        center_index = len(msg.ranges) // 2
        distance_ahead = msg.ranges[center_index]

        closest_obs_distance = min(msg.ranges)
        closest_obs_index = msg.ranges.index(closest_obs_distance)


        self.get_logger().info(f"Distance straight ahead: {distance_ahead:.2f} meters")
        self.get_logger().info(f"Closest obstacle distance: {closest_obs_distance:.2f} meters, at: {closest_obs_index}.")

def main(args=None):
    rclpy.init(args=args)
    node = LidarReader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()