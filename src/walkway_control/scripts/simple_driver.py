#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimpleDriverPy(Node):
    def __init__(self):
        # 1. Name the node
        super().__init__('simple_driver_py')

        # 2. Create the Publisher (Message Type, Topic Name, Queue Size)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # 3. Create a timer to execute a callback every 0.5 seconds (2 Hz)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        # 4. Create an empty Twist message
        msg = Twist()

        # 5. Fill in the data: Drive forward at 0.5 meters per second
        msg.linear.x = 0.5
        msg.angular.z = 0.0

        # 6. Publish the message to the topic
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Driving forward at 0.5 m/s')

def main(args=None):
    rclpy.init(args=args)       # Initialize ROS 2 communications
    node = SimpleDriverPy()     # Instantiate our node
    rclpy.spin(node)            # Keep the node alive and looping
    node.destroy_node()         # Clean up
    rclpy.shutdown()            # Shut down ROS 2

if __name__ == '__main__':
    main()