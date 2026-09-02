#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

class NavToPoseClient(Node):
    def __init__(self):
        super().__init__('nav_client_py')
        # 1. Create the Action Client
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y):
        self.get_logger().info('Waiting for action server...')
        self.action_client.wait_for_server()

        # 2. Define the Goal Message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0 # Pointing straight ahead

        self.get_logger().info(f'Sending Goal: X={x}, Y={y}')

        # 3. Send the Goal and attach a callback for the feedback
        self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        # 4. Read the continuous feedback while the robot drives
        distance = feedback_msg.feedback.distance_remaining
        self.get_logger().info(f'Distance remaining: {distance:.2f} meters')

def main(args=None):
    rclpy.init(args=args)
    client = NavToPoseClient()
    client.send_goal(2.0, 2.0)
    rclpy.spin(client)

