#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"

class PatrolBot : public rclcpp::Node {
    public:
    using NavigateToPose = nav2_msgs::action::NavigateToPose;

    PatrolBot() : Node("patrol_bot") {
        // 1. Create the Action Client
        client_ptr_ = rclcpp_action::create_client<NavigateToPose>(this, "navigate_to_pose");
    }

    void send_goal(double x, double y, double theta_w) {
        // 2. Wait for Nav2 to be ready
        if (!client_ptr_->wait_for_action_server(std::chrono::seconds(10))) {
            RCLCPP_ERROR(this->get_logger(), "Nav2 Action server not available!");
            return;
        }

        // 3. Construct the Goal Message
        auto goal_msg = NavigateToPose::Goal();
        goal_msg.pose.header.frame_id = "map";
        goal_msg.pose.pose.position.x = x;
        goal_msg.pose.pose.position.y = y;
        goal_msg.pose.pose.orientation.w = theta_w;

        // 4. Send asynchronously
        RCLCPP_INFO(this->get_logger(), "Sending goal!");
        client_ptr_->async_send_goal(goal_msg);
    }

    private:
    rclcpp_action::Client<NavigateToPose>::SharedPtr client_ptr_;
};

int main(int argc, char ** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PatrolBot>();
    node->send_goal(2.0, 2.0, 1.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}