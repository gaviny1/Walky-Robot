#include <algorithm>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "std_msgs/msg/bool.hpp"
#include "rclcpp/qos.hpp"

class ObstacleDetector : public rclcpp::Node {
    public:
    ObstacleDetector() : Node("obstacle_detector"), danger_threshold_(1.5) {
        subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", rclcpp::SensorDataQoS(), std::bind(&ObstacleDetector::scan_callback, this, std::placeholders::_1)
        );

        publisher_ = this->create_publisher<std_msgs::msg::Bool>("/obstacle_alert", 10);
    }

    private:
    void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) const {
        
        auto start_it = msg->ranges.begin() + 150;
        auto end_it = msg->ranges.begin() + 210;

        auto min_it = std::min_element(start_it, end_it);
        float closest_distance = *min_it;

        auto alert_msg = std_msgs::msg::Bool(); // Create the message object

        if (closest_distance < danger_threshold_) {
            alert_msg.data = true;
            RCLCPP_WARN(this->get_logger(), "OBSTACLE AHEAD! Distance: %.2fm", closest_distance);
        } else {
            alert_msg.data = false;
            RCLCPP_INFO(this->get_logger(), "Path clear.");
        }

        publisher_->publish(alert_msg);
    }

    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
    rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr publisher_;
    float danger_threshold_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ObstacleDetector>());
    rclcpp::shutdown();
    return 0;
}