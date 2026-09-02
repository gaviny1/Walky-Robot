#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.parameter import Parameter
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from nav_msgs.msg import Odometry

class WaypointPatrol(Node):
    def __init__(self):
        super().__init__('waypoint_patrol_py', allow_undeclared_parameters=True)

        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.speed_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.latest_speed = None

        self.report_rate = 1.0

        self.timer = self.create_timer(self.report_rate, self.timer_callback)
        
        # 1. Define Patrol Route (List of X, Y tuples)
        self.waypoints = [(26.0, -4.0)]
        self.current_waypoint_index = 0

    def send_next_goal(self):
        if self.current_waypoint_index >= len(self.waypoints):
            self.get_logger().info('Patrol Complete! Shutting down...')
            raise SystemExit

        target_x, target_y = self.waypoints[self.current_waypoint_index]
        self.get_logger().info(f'Heading to waypoint {self.current_waypoint_index}: X={target_x}, Y={target_y}')

        self.action_client.wait_for_server()
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = target_x
        goal_msg.pose.pose.position.y = target_y
        goal_msg.pose.pose.orientation.w = 1.0

        # 2. Send the goal and attach a callback from when it finishes
        send_goal_future = self.action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected by Nav2 server.')
            return

        # Wait for the actual result of the driving
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        # 3. When finished, increment index and loop, otherwise, return error
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Waypoint reached successfully!')
            self.current_waypoint_index += 1
            self.send_next_goal()
        else:
            self.get_logger().error(f'Goal failed with status code: {status}')
            return

    def odom_callback(self, msg):
        # Extract the forward (x) velocity
        self.latest_speed = msg.twist.twist.linear.x
    
    def timer_callback(self):
        if self.latest_speed is not None:
            self.get_logger().info(f'Current speed: {self.latest_speed:.2f} m/s')

def main(args=None):
    rclpy.init(args=args)
    node = WaypointPatrol()

    try:
        node.send_next_goal()
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        node.get_logger().info('Spin broken. Cleaning up...')
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()