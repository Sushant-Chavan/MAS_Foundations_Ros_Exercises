#!/usr/bin/env python

PACKAGE = "turtle_controller"
NODE = "pose_input"

import rospy
from turtlesim.msg import Pose

class PoseInput:
    def __init__(self):
        # initialize the node
        rospy.init_node(NODE)

        # create a publisher
        self.target_velocity_publisher = rospy.Publisher("turtle_controller/pose", Pose, queue_size=10)

        #create a targetVelocityMessage
        self.pose = Pose()

    def readInput(self):
        try:
            self.pose.x = float(raw_input("Enter destination x : "))
        except ValueError:
            self.pose.x = 0.0

        try:
            self.pose.x = float(raw_input("Enter destination y : "))
        except ValueError:
            self.pose.x = 0.0

if __name__ == "__main__":
    n = PoseInput()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        n.readInput()
        n.target_velocity_publisher.publish(n.pose)
        rate.sleep()