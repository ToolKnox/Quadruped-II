#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math

def lidar_publisher():
    rospy.init_node('lidar_simulator', anonymous=True)
    lidar_pub = rospy.Publisher('/lidar_scan', LaserScan, queue_size=10)
    rate = rospy.Rate(10)  # Publish data at 10 Hz

    while not rospy.is_shutdown():
        lidar_data = LaserScan()
        lidar_data.header.stamp = rospy.Time.now()
        lidar_data.header.frame_id = 'base_link'  # Update frame_id if needed
        lidar_data.angle_min = -math.pi / 2  # Start angle in radians
        lidar_data.angle_max = math.pi / 2  # End angle in radians
        lidar_data.angle_increment = math.pi / 180  # Angular resolution in radians
        lidar_data.range_min = 0.1  # Minimum range value
        lidar_data.range_max = 10.0  # Maximum range value
        lidar_data.ranges = [1.0] * 180  # Dummy range values for demonstration

        lidar_pub.publish(lidar_data)
        rate.sleep()

if __name__ == '__main__':
    try:
        lidar_publisher()
    except rospy.ROSInterruptException:
        pass
