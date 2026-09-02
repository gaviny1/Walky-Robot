#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from rclpy.qos import qos_profile_sensor_data

class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector')

        # 1. The "Camera" (Subscriber)
        self.subscription_ = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, qos_profile_sensor_data
        )

        # 2. The "Walkie-Talkie" (Publisher)
        self.publisher_ = self.create_publisher(Bool, '/obstacle_alert', 10)

        self.danger_threshold = 1.5 # We consider anything closer than 1.5m a threat

    def scan_callback(self, msg):
        front_cone = msg.ranges[150:210]
        closest_distance = min(front_cone)
        alert_msg = Bool() # Create an empty boolean message

        if closest_distance < self.danger_threshold:
            alert_msg.data = True
            self.get_logger().warn(f"OBSTACLE AHEAD! DISTANCE: {closest_distance:.2f}m")
        else:
            alert_msg.data = False
            self.get_logger().info("Path clear.")
        
        self.publisher_.publish(alert_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
