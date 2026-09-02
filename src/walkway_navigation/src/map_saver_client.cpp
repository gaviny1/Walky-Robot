#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/srv/get_map.hpp"
#include <chrono>
#include <memory>

using namespace std::chrono_literals;

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);

    // Create a shared pointer to node
    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("map_saver_client");

    // 1. Create the Service Client
    rclcpp::Client<nav_msgs::srv::GetMap>::SharedPtr client =
        node->create_client<nav_msgs::srv::GetMap>("/map_server/map");

    // 2. Wait for the service to be available
    while (!client->wait_for_service(1s)) {
        if (!rclcpp::ok()) {
            RCLCPP_ERROR(node->get_logger(), "Interrupted while waiting for the service. Exiting.");
            return 0;
        }
        RCLCPP_INFO(node->get_logger(), "GetMap service not available, waiting again...");
    }

    // 3. Create an empty request object
    auto request = std::make_shared<nav_msgs::srv::GetMap::Request>();

    // 4. Send the request asynchronously
    auto result = client->async_send_request(request);

    // Spin the node until the future (the response) is complete
    if (rclcpp::spin_until_future_complete(node, result) == rclcpp::FutureReturnCode::SUCCESS) {
        RCLCPP_INFO(node->get_logger(), "Success! Received map snapshot. Resolution: %f m/cell",
                    result.get()->map.info.resolution);
    } else {
        RCLCPP_ERROR(node->get_logger(), "Failed to call service GetMap");
    }

    rclcpp::shutdown();
    return 0;
}