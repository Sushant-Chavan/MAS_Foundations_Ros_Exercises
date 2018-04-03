#!/usr/bin/env python

PACKAGE = "turtle_controller"
NODE = "velocity_client"

import rospy
from geometry_msgs.msg import Twist

class velocity_client:
    def __init__(self):
        # initialize the node
        rospy.init_node(NODE)

        # create a publisher
        self.target_velocity_publisher = rospy.Publisher("turtle_controller/cmd_vel", Twist, queue_size=10)

        #create a targetVelocityMessage
        self.target_vel = Twist()

    def readInput(self):
        try:
            self.target_vel.linear.x = float(raw_input("Enter velocity x : "))
        except ValueError:
            self.target_vel.linear.x = 0.0

        try:
            self.target_vel.angular.z = float(raw_input("Enter angular vel z : "))
        except ValueError:
            self.target_vel.angular.z = 0.0

if __name__ == "__main__":
    n = velocity_client()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        n.readInput()
        n.target_velocity_publisher.publish(n.target_vel)
        rate.sleep()