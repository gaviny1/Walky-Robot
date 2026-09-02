#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav2_msgs.srv import ClearEntireCostmap

class ClearCostmapClient(Node):
    def __init__(self):
        super().__init__('clear_costmap_client')
        # Initialize client without blocking the constructor
        self.local_client = self.create_client(
            ClearEntireCostmap, 
            '/local_costmap/clear_entirely_local_costmap'
        )

        self.global_client = self.create_client(
            ClearEntireCostmap,
            '/global_costmap/clear_entirely_global_costmap'
        )

    def send_clear_request(self):
        # Implement a safe timeout so the node doesn't hang indefinitely
        if not self.local_client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('Costmap service not available after 3 seconds.')
            return False

        request = ClearEntireCostmap.Request()
        self.get_logger().info('Sending request to clear costmaps...')
        
        # Store the future as an instance attribute so we can spin on it in main
        self.local_future = self.local_client.call_async(request)
        self.global_future = self.global_client.call_async(request)
        return True

def main(args=None):
    rclpy.init(args=args)
    node = ClearCostmapClient()

    try:
        if node.send_clear_request():
            # Spin the executor safely until the future is resolved
            rclpy.spin_until_future_complete(node, node.local_future)
            
            if node.local_future.result() is not None:
                node.get_logger().info('Local costmap cleared successfully!')
            if node.global_future.result() is not None:
                node.get_logger().info('Global costmap cleared successfully!')
            else:
                node.get_logger().error('Service call completed, but returned an empty/failed response.')
    
    except KeyboardInterrupt:
        node.get_logger().info('Manual interruption detected. Shutting down.')
    except Exception as e:
        node.get_logger().error(f'An unexpected error occurred: {e}')
        
    finally:
        # Guarantee clean teardown of the ROS 2 context
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()