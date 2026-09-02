#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"

using NavigateAction = nav2_msgs::action::NavigateToPose;

class NavToPoseClient : public rclcpp::Node {
    public:
    NavToPoseClient() : Node("nav_client_cpp") {
        // 1. Create the Action Client
        client_ptr_ = rclcpp_action::create_client<NavigateAction>(this,"navigate_to_pose");
    }

    void send_goal(double x, double y) {
        if (!client_ptr_->wait_for_action_server(std::chrono::seconds(5))) {
            RCLCPP_ERROR(this->get_logger(), "Action server not available");
            return;
        }

        // 2. Define the Goal Message
        auto goal_msg = NavigateAction::Goal();
        goal_msg.pose.header.frame_id = "map";
        goal_msg.pose.pose.position.x = x;
        goal_msg.pose.pose.position.y = y;
        goal_msg.pose.pose.orientation.w = 1.0;

        // 3. Setup Goal Options and Feedback Callback
        auto send_goal_options = rclcpp_action::Client<NavigateAction>::SendGoalOptions();
        send_goal_options.feedback_callback = 
            std::bind(&NavToPoseClient::feedback_callback, this, std::placeholders::_1, std::placeholders::_2);

        RCLCPP_INFO(this->get_logger(), "Sending Goal: X=%f, Y=%f", x, y);
        client_ptr_->async_send_goal(goal_msg, send_goal_options);
    }

    private:
    void feedback_callback(
        rclcpp_action::ClientGoalHandle<NavigateAction>::SharedPtr,
        const std::shared_ptr<const NavigateAction::Feedback> feedback) {

        // 4. Read the feedback
        RCLCPP_INFO(this->get_logger(), "Distance remaining: %.2f meters", feedback->distance_remaining);
    }

    rclcpp_action::Client<NavigateAction>::SharedPtr client_ptr_;
};

int main(int argc, char ** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NavToPoseClient>();
    node->send_goal(2.0, 2.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}