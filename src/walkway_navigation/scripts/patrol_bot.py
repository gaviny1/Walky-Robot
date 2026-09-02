#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

class PatrolBot(Node):
    def __init__(self):
        super().__init__('patrol_bot')
        # 1. Create an Action Client targeting the Nav2 Server
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y, theta_w):
        # 2. Construct the Goal Message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y 
        goal_msg.pose.pose.orientation.w = theta_w

        # 3. Wait for Nav2 to be ready, then send asynchronously
        self.get_logger().info('Waiting for Nav2 server...')
        self.action_client.wait_for_server()
        self.get_logger().info('Sending goal!')
        self.action_client.send_goal_async(goal_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PatrolBot()
    # Command the robot to drive to coordinate (2.0, 2.0)
    node.send_goal(2.0, 2.0, 1.0)
    rclpy.spin(node)
    rclpy.shutdown()
