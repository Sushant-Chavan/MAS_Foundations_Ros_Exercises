#!/usr/bin/env python

PACKAGE = "turtle_controller"
NODE = "velocity_controller"

import rospy
from geometry_msgs.msg import Twist

class velocity_controller:
    def __init__(self):
        # initialize the node
        rospy.init_node(NODE)

        # create a publisher
        self.target_velocity_publisher = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=10)

        #create a targetVelocityMessage
        self.target_vel = Twist()

        #create a subscriber 
        self.vel_sub = rospy.Subscriber("turtle_controller/cmd_vel", Twist, self.velocity_callback)

    def velocity_callback(self, msg):
        self.target_vel = msg



if __name__ == "__main__":
    n = velocity_controller()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        n.target_velocity_publisher.publish(n.target_vel)
        rate.sleep()