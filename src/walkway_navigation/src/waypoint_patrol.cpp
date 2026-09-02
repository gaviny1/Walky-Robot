#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"

using NavigateAction = nav2_msgs::action::NavigateToPose;
using GoalHandleNav = rclcpp_action::ClientGoalHandle<NavigateAction>;

class WaypointPatrol : public rclcpp::Node {
    public:
    WaypointPatrol() : Node("waypoint_patrol_cpp"), current_waypoint_index_(0) {
        this->declare_parameter("use_sim_time", true);
        client_ptr_ = rclcpp_action::create_client<NavigateAction>(this, "navigate_to_pose");
        // 1. Define the route
        waypoints_ = {{2.0, 2.0}, {2.0, -2.0}, {0.0, 0.0}};
    }

    void send_next_goal() {
        if (current_waypoint_index_ >= waypoints_.size()) {
            RCLCPP_INFO(this->get_logger(), "Patrol Complete!");
            return;
        }

        auto target = waypoints_[current_waypoint_index_];
        auto goal_msg = NavigateAction::Goal();
        goal_msg.pose.header.frame_id = "map";
        goal_msg.pose.pose.position.x = target.first;
        goal_msg.pose.pose.position.y = target.second;
        goal_msg.pose.pose.orientation.w = 1.0;

        auto send_goal_options = rclcpp_action::Client<NavigateAction>::SendGoalOptions();

        // 2. Attach the callback for when the robot finishes driving
        send_goal_options.result_callback = std::bind(&WaypointPatrol::result_callback, this, std::placeholders::_1);
        RCLCPP_INFO(this->get_logger(), "Heading to waypoint %zu", current_waypoint_index_);
        client_ptr_->async_send_goal(goal_msg, send_goal_options);
    }

    private:
    void result_callback(const GoalHandleNav::WrappedResult & result) {
        if (result.code == rclcpp_action::ResultCode::SUCCEEDED) {
            RCLCPP_INFO(this->get_logger(), "Waypoint reached!");
            // 3. Increment and loop
            current_waypoint_index_++;
            send_next_goal();
        }
    }

    rclcpp_action::Client<NavigateAction>::SharedPtr client_ptr_;
    std::vector<std::pair<double, double>> waypoints_;
    size_t current_waypoint_index_;
};

int main(int argc, char ** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<WaypointPatrol>();
    node->send_next_goal();
    rclcpp::spin(node);
    RCLCPP_INFO(node->get_logger(), "Shutting down cleanly...");
    rclcpp::shutdown();
    return 0;
}