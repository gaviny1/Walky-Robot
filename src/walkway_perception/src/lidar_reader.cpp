#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <algorithm> // Required for std::min_element

class LidarReader : public rclcpp::Node {
    public:
    LidarReader() : Node("lidar_reader") {
        // create_subscription<Message Type>(Topic, Queue Size, Callback FUnction)
        // std::bind is used to attach the callback function to this specific class instance
        subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10, std::bind(&LidarReader::listener_callback, this, std::placeholders::_1)
        );
    }

    private:
    void listener_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) const {
        int center_index = msg->ranges.size() / 2;
        float distance_ahead = msg->ranges[center_index];

        // std::min_element searches from the beginning to the end of the vector
        auto min_it = std::min_element(msg->ranges.begin(), msg->ranges.end());

        // The asterisk (*) dereferences the iterator to get the actual float value
        float closest_obs_distance = *min_it;
        int closest_obs_index = std::distance(msg->ranges.begin(), min_it);


        RCLCPP_INFO(this->get_logger(), "Distance straight ahead: %.2f meters", distance_ahead);
        RCLCPP_INFO(this->get_logger(), "Closest obstacle distance: %.2f meters, at %d", closest_obs_distance, closest_obs_index);
    }

    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<LidarReader>());
    rclcpp::shutdown();
    return 0;
}