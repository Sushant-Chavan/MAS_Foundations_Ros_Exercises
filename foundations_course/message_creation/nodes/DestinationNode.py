#!/usr/bin/env python

PACKAGE = "message_creation"
NODE = "destination_node"

import rospy
from geometry_msgs.msg import Twist
from message_creation.msg import CustomMessage

class DestinationNode:
    def __init__(self):
        # initialize the node
        rospy.init_node(NODE)

        # create subscribers
        self.relayImageSubscriber = rospy.Subscriber("relay/custom_topic", CustomMessage, self.msgCallback)

    def msgCallback(self, msg):
        rospy.loginfo("Received Data")
        pass

if __name__ == "__main__":
    n = DestinationNode()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        rate.sleep()