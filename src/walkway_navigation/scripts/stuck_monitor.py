#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from action_msgs.msg import GoalStatusArray, GoalStatus
from nav2_msgs.srv import ClearEntireCostmap
import time

class StuckMonitor(Node):
    def __init__(self):
        super().__init__('stuck_monitor')

        # 1. Subscribe to the Action Status Topic
        self.status_sub = self.create_subscription(
            GoalStatusArray,
            '/navigate_to_pose/_action/status',
            self.status_callback,
            10
        )

        # 2. Setup the Service Client
        self.local_client = self.create_client(
            ClearEntireCostmap,
            '/local_costmap/clear_entirely_local_costmap'
        )

        self.global_client = self.create_client(
            ClearEntireCostmap,
            '/global_costmap/clear_entirely_global_costmap'
        )

        self.last_clear_time = 0.0
        self.cooldown_duration = 5.0

        #self.is_clearing_active = False

    def status_callback(self, msg):
        if not msg.status_list:
            return
        
        # Get the status of the most recent goal
        if msg.status_list[-1].status == GoalStatus.STATUS_ABORTED:
            current_time = time.time()

            # Check if the cooldown has passed
            if (current_time - self.last_clear_time) > self.cooldown_duration:
                self.get_logger().warn('Robot stuck! Triggering dual costmap clear...')
                self.trigger_clear_costmaps()
                self.last_clear_time = current_time
            else:
                self.get_logger().debug('Aborted status received, but clear is on cooldown.')

    def trigger_clear_costmaps(self):
        req = ClearEntireCostmap.Request()
        if self.local_client.service_is_ready():
            local_future = self.local_client.call_async(req)
        if self.global_client.service_is_ready():
            global_future = self.global_client.call_async(req)

        local_future.add_done_callback(self.clear_finished_callback)

    def clear_finished_callback(self, local_future):
        self.get_logger().info('Costmaps successfully cleared.')

def main(args=None):
    rclpy.init(args=args)
    node = StuckMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()