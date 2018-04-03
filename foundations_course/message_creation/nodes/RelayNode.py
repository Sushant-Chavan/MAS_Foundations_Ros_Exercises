#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
from message_creation.msg import CustomMessage

PACKAGE = "message_creation"
NODE = "relay_node"

class RelayNode:
    def __init__(self):
        # initialize the node
        rospy.init_node(NODE)

        # create a publisher
        self.relayPublisher = rospy.Publisher("relay/custom_topic", CustomMessage, queue_size=10)

        # create subscribers
        self.relayImageSubscriber = rospy.Subscriber("wide_stereo/left/image_rect_throttle", Image, self.imageCallBack)
        self.relayLaserSubscriber = rospy.Subscriber("base_scan", LaserScan, self.laserCallback)
        self.relayPoseSubscriber = rospy.Subscriber("robot_pose_ekf/odom_combined", PoseWithCovarianceStamped, self.poseCallback)

        # create members
        self.customMsg = CustomMessage()
        self.inputLaserData = LaserScan()
        self.inputPose = PoseWithCovarianceStamped()
        self.inputImageData = Image()

    def imageCallBack(self, msg):
        self.inputImageData = msg
        self.customMsg.imageData = msg
        self.customMsg.pose = self.inputPose
        self.customMsg.laserData = self.inputLaserData
        self.relayPublisher.publish(node.customMsg)

    
    def laserCallback(self, msg):
        self.inputLaserData = msg
        self.customMsg.imageData = self.inputImageData
        self.customMsg.pose = self.inputPose
        self.customMsg.laserData = msg
        self.relayPublisher.publish(node.customMsg)

    def poseCallback(self, msg):
        self.inputPose = msg
        self.customMsg.imageData = self.inputImageData
        self.customMsg.pose = msg
        self.customMsg.laserData = self.inputLaserData
        self.relayPublisher.publish(node.customMsg)


if __name__ == "__main__":
    node = RelayNode()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        rate.sleep()