#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include <cmath>

class EKFMonitor : public rclcpp::Node {
    public:
    EKFMonitor() : Node("ekf_monitor"), raw_x_(0.0), raw_y_(0.0) {
        raw_sub_ = this->create_subscription<nav_msgs::msg::Odometry>(
            "/odom", 10, std::bind(&EKFMonitor::raw_odom_callback, this, std::placeholders::_1)
        );

        ekf_sub_ = this->create_subscription<nav_msgs::msg::Odometry>(
            "/odometry/filtered", 10, std::bind(&EKFMonitor::ekf_callback, this, std::placeholders::_1)
        );
    }

    private:
    void raw_odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg) {
        raw_x_ = msg->pose.pose.position.x;
        raw_y_ = msg->pose.pose.position.y;
    }

    void ekf_callback(const nav_msgs::msg::Odometry::SharedPtr msg) const {
        double ekf_x = msg->pose.pose.position.x;
        double ekf_y = msg->pose.pose.position.y;
        double drift_x = std::abs(ekf_x - raw_x_);
        double drift_y = std::abs(ekf_y - raw_y_);
        RCLCPP_INFO(this->get_logger(), "Current X Drift between wheels and EKF: %.4f meters", drift_x);
        RCLCPP_INFO(this->get_logger(), "Current Y Drift between wheels and EKF: %.4f meters", drift_y);
    }

    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr raw_sub_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr ekf_sub_;
    double raw_x_, raw_y_;
};

int main(int argc, char ** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<EKFMonitor>();

    try {
        rclcpp::spin(node);
    }
    catch (const std::exception & e) {
        RCLCPP_ERROR(node->get_logger(), "Exception caught: %s", e.what());
    }

    RCLCPP_INFO(node->get_logger(), "Shutting down cleanly...");
    rclcpp::shutdown();
    return 0;
}