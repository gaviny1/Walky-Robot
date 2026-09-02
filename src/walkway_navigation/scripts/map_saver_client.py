#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.srv import GetMap

class MapSaverClient(Node):
    def __init__(self):
        super().__init__('map_saver_client')

        # 1. Create the Service Client
        self.client = self.create_client(GetMap, '/map_saver/map')

        # 2. Wait for the service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for GetMap service to become available...')

        # 3. Create an empty request object defined by the GetMap service
        self.request = GetMap.Request()

    def send_request(self):
        # 4. Send the request asynchronously so we don't freeze the node 
        self.future = self.client.call_async(self.request)

        # Spin the node until the server responds
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client_node = MapSaverClient()

    response = client_node.send_request()

    if response is not None:
        client_node.get_logger().info(
            f'Success! Received map snapshot. Resolution: {response.map.info.resolution} m/cell'
        )
    else:
        client_node.get_logger.error(
            'Failed to get map from service.'
        )

    client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    