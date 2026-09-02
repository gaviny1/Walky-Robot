#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"

class PoseTracker : public rclcpp::Node {
    public:
    PoseTracker() : Node("pose_tracker") {
        subscription_ = this->create_subscription<geometry_msgs::msg::PoseWithCovarianceStamped>(
            "/amcl_pose", 10, std::bind(&PoseTracker::pose_callback, this, std::placeholders::_1)
        );
    }

    private:
    void pose_callback(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg) const {
        double x = msg->pose.pose.position.x;
        double y = msg->pose.pose.position.y;

        RCLCPP_INFO(this->get_logger(), "Walkway Humanoid is currently at: X: %.2f, Y: %.2f", x, y);
    }

    rclcpp::Subscription<geometry_msgs::msg::PoseWithCovarianceStamped>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PoseTracker>());
    rclcpp::shutdown();
    return 0;
}