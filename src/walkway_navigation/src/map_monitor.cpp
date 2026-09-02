#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"

class MapMonitor : public rclcpp::Node {

    public:
    MapMonitor() : Node('map_monitor') {
        subscription_ = this->create_subscription<nav_mags::msg::OccupancyGrid>(
            "/map", 10, std::bind(&MapMonitor::map_callback, this, std::placeholders::_1)
        );
    }

    private:
    void map_callback(const nav_msgs::msg::OccupancyGrid::SharedPtr msg) const {
        RCLCPP_INFO(this->get_logger(),
            "Received map! Size: %d x %d, Resolution: %f m/cell",
            msg->info.width, msg->info.height, msg->info.resolution);
    }

    rclcpp::Subscription<nav_msgs::msg::OccupancyGrid>::SharedPtr subscription_:
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MapMonitor>());
    rclcpp::shutdown();
    return 0;
}
