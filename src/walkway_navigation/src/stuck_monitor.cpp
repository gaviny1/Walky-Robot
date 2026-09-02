#include "rclcpp/rclcpp.hpp"
#include "action_msgs/msg/goal_status_array.hpp"
#include "nav2_msgs/srv/clear_entire_costmap.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;

class StuckMonitor : public rclcpp::Node {
    public:
    StuckMonitor() : Node("stuck_monitor"), is_clearing_active_(false) {
        status_sub_ = this->create_subscription<action_msgs::msg::GoalStatusArray>(
            "/navigate_to_pose/_action/status", 
            10,
            std::bind(&StuckMonitor::status_callback, this, _1)
        );

        clear_client_ = this->create_client<nav2_msgs::srv::ClearEntireCostmap>(
            "/local_costmap/clear_entirely_local_costmap"
        );
    }

    private:
    void status_callback(const action_msgs::msg::GoalStatusArray::SharedPtr msg) {
        if (msg->status_list.empty()) return;

        if (msg->status_list.back().status == action_msgs::msg::GoalStatus::STATUS_ABORTED) {
            if (!is_clearing_active_) {
                RCLCPP_WARN(this->get_logger(), "Robot stuck! Triggering clear...");
                trigger_clear();
            }
        }
    }

    void trigger_clear() {
        if (clear_client_->service_is_ready()) {
            is_clearing_active_ = true;

            auto request = std::make_shared<nav2_msgs::srv::ClearEntireCostmap::Request>();

            clear_client_->async_send_request(
                request,
                std::bind(&StuckMonitor::clear_finished_callback, this, std::placeholders::_1)
            );
        }
    }

    void clear_finished_callback(rclcpp::Client<nav2_msgs::srv::ClearEntireCostmap>::SharedFuture future) {
        RCLCPP_INFO(this->get_logger(), "Costmap successfully cleared.");
        is_clearing_active_ = false;
    }

    rclcpp::Subscription<action_msgs::msg::GoalStatusArray>::SharedPtr status_sub_;
    rclcpp::Client<nav2_msgs::srv::ClearEntireCostmap>::SharedPtr clear_client_;
    bool is_clearing_active_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<StuckMonitor>());
    rclcpp::shutdown();
    return 0;
}