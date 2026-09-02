#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped

class PoseTracker(Node):
    def __init__(self):
        super().__init__('pose_tracker')
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.get_logger.info(f'Walkway Humanoid is currently at: X: {x:.2f}, Y: {y:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = PoseTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()