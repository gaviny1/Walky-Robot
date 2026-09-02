#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals;

// Inherit from the standard rclcpp::Node
class SimpleDriverCpp : public rclcpp::Node {
    public:
    SimpleDriverCpp() : Node("simple_driver_cpp") {
        // 1. Create Publisher
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);

        // 2. Create Timer
        timer_ = this->create_wall_timer(
            500ms, std::bind(&SimpleDriverCpp::timer_callback, this)
        );
    }

    private:
    void timer_callback() {
        // 3. Create and fill the message
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 0.5;
        msg.angular.z = 0.0;

        // 4. Publish
        publisher_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "Publishing: Driving forward at 0.5 m/s");
    }

    // Declare member variables
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SimpleDriverCpp>());
    rclcpp::shutdown();
    return 0;
}