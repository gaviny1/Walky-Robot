#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class EKFMonitor(Node):
    def __init__(self):
        super().__init__('ekf_monitor')
        self.raw_sub = self.create_subscription(
            Odometry, '/odom', self.raw_odom_callback, 10)

        self.ekf_sub = self.create_subscription(
            Odometry, '/odometry/filtered', self.ekf_callback, 10)

        self.raw_x = 0.0
        self.raw_y = 0.0
        self.ekf_x = 0.0
        self.ekf_y = 0.0

        self.timer = self.create_timer(1.0, self.report_drift)

    def raw_odom_callback(self, msg):
        self.raw_x = msg.pose.pose.position.x 
        self.raw_y = msg.pose.pose.position.y 
    
    def ekf_callback(self, msg):
        self.ekf_x = msg.pose.pose.position.x
        self.ekf_y = msg.pose.pose.position.y

    def report_drift(self): 
        drift_x = abs(self.ekf_x - self.raw_x)
        drift_y = abs(self.ekf_y - self.raw_y)
        drift_2d = math.hypot(self.ekf_x - self.raw_x, self.ekf_y - self.raw_y)
        #self.get_logger().info(f'Current X drift between wheels and EKF: {drift_x:.4f} meters')
        #self.get_logger().info(f'Current Y drift between wheels and EKF: {drift_y:.4f} meters')
        self.get_logger().info(
            f'Drift -> X: {drift_x:.4f}m | Y: {drift_y:.4f}m'
        )

def main(args=None):
    rclpy.init(args=args)
    node = EKFMonitor()

    try:
        rclpy.spin(node)
    except (SystemExit, KeyboardInterrupt):
        node.get_logger().info('Spin broken. Cleaning up...')
    finally:
        node.destroy
        rclpy.shutdown()

if __name__ == '__main__':
    main()