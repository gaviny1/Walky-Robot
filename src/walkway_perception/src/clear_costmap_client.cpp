#include "rclcpp/rclcpp.hpp"
#include "nav2_msgs/srv/clear_entire_costmap.hpp"

#include <chrono>
#include <memory>

using namespace std::chrono_literals;

class ClearCostmapClient : public rclcpp::Node {
    public:
    ClearCostmapClient() : Node("clear_costmap_client") {
        client_ = this->create_client<nav2_msgs::srv::ClearEntireCostmap>(
            "/local_costmap/clear_entirely_local_costmap"
        );
    }

    // Returns a shared future so the main thread can spin on it
    std::shared_future<std::shared_ptr<nav2_msgs::srv::ClearEntireCostmap::Response>> send_request() 
    {
        if (!client_->wait_for_service(3s)) {
            RCLCPP_ERROR(this->get_logger(), "Costmap service not available.");
            // Return an invalid future to indicate failure
            return {};
        }

        auto request = std::make_shared<nav2_msgs::srv::ClearEntireCostmap::Request>();
        RCLCPP_INFO(this->get_logger(), "Sending request to clear the local costmap...");

        // Asynchronously send the request
        return client_->async_send_request(request).future.share();
    }

    private:
    rclcpp::Client<nav2_msgs::srv::ClearEntireCostmap>::SharedPtr client_;
};

int main(int argc, char **argv) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ClearCostmapClient>();

    auto future = node->send_request();

    // Check if the future is valid
    if (future.valid()) {
        // Spin the node until the future completes
        if (rclcpp::spin_until_future_complete(node, future) == rclcpp::FutureReturnCode::SUCCESS) {
            RCLCPP_INFO(node->get_logger(), "Costmap cleared successfully!");
        } else {
            RCLCPP_ERROR(node->get_logger(), "Failed to call clear costmap service.");
        }
    } else {
        RCLCPP_ERROR(node->get_logger(), "Service call was not initiated. Shutting down.");
    }

    rclcpp::shutdown();
    return 0;
}