#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2 

class PointCloudFilterNode(Node):
    def __init__(self):
        super().__init__('pointcloud_filter_node')

        # Subscribe to the heavy raw data
        self.sub = self.create_subscription(
            PointCloud2, '/camera/rgbd/points', self.pc_callback, 1)

        # Publish the lightweight filtered data
        self.pub = self.create_publisher(
            PointCloud2, '/camera/rgbd/points_filtered', 1)

        self.get_logger().info("Python PointCloud Filter Started.")
    
    def pc_callback(self, msg):
        # 1. Read the raw points into a list
        points = list(pc2.read_points(msg, skip_nans=True))

        # 2. DECIMATION: Take only 1 out of every 10 points (slice the list)
        filtered_points = points[::10]

        # 3. Package it back up into a PointCloud2 message
        filtered_msg = pc2.create_cloud(msg.header, msg.fields, filtered_points)

        # 4. Publish and log
        self.pub.publish(filtered_msg)
        self.get_logger().info(f"Filtered cloud from {len(points)} to {len(filtered_points)} points")

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudFilterNode()

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        node.get_logger().info('Spin finished. Cleaning up...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()