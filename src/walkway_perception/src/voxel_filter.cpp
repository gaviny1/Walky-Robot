#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>

class VoxelFilterNode : public rclcpp::Node {
    public:
    VoxelFilterNode() : Node("voxel_filter_node") {
        // Publish the lightweight filtered data
        pub_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("/camera/rgbd/points_filtered", 1);

        // Subscribe to the heavy raw data
        sub_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
            "/camera/rgbd/points", 1,
            std::bind(&VoxelFilterNode::cloud_callback, this, std::placeholders::_1)
        );

        RCLCPP_INFO(this->get_logger(), "C++ Voxel Grid Filter Started.");
    }

    private:
    void cloud_callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg) {
        // 1. Convert the ROS 2 message into a PCL data type
        pcl::PCLPointCloud2::Ptr pcl_cloud(new pcl::PCLPointCloud2());
        pcl_conversions::toPCL(*msg, *pcl_cloud);

        // 2. Setup the Voxel Grid Filter
        pcl::PCLPointCloud2::Ptr cloud_filtered(new pcl::PCLPointCloud2());
        pcl::VoxelGrid<pcl::PCLPointCloud2> sor;
        sor.setInputCloud(pcl_cloud);

        // Create 10cm x 10cm x 10cm Minecraft blocks
        sor.setLeafSize(0.1f, 0.1f, 0.1f);
        sor.filter(*cloud_filtered);

        // 3. Convert back to a ROS 2 message and publish
        sensor_msgs::msg::PointCloud2 output;
        pcl_conversions::fromPCL(*cloud_filtered, output);
        output.header = msg->header; // Keep the original timestamp and camera frame
        pub_->publish(output);
    }

    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pub_;
    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<VoxelFilterNode>());
    rclcpp::shutdown();
    return 0;
}