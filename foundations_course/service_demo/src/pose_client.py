#!/usr/bin/env python

PACKAGE = 'turtle_controller'
NODE = 'pose_client'

import rospy
import std_msgs

from turtlesim.msg import Pose
from service_demo.srv import turtle_control

class PoseClient:

    def __init__(self):
        # Initialize the node
        rospy.init_node(NODE)

        # Create target pose msgs
        self.requestPositions = self.getPositions()

        #Show in the console the message
        rospy.loginfo("Client initiated")
        
        #Pause the node untill the service specified(service_label) is active
        rospy.wait_for_service("positionTurtle")

        # Setup proxy for service
        self.turtle_client = rospy.ServiceProxy("positionTurtle", turtle_control)

    def getPositions(self):
        newPositions = []
        xvals = [2.0, 3.5, 7.0, 5.0, 1.0]
        yvals = [7.0, 3.5, 9.0, 2.0, 0.0]
        for i in range(0,5):
            newPos = Pose()
            newPos.x = xvals[i]
            newPos.y = yvals[i]
            newPositions.append(newPos)
        return newPositions

    def requestPositioning(self):
        for i in range(0,5): 
            position = self.requestPositions[i]
            print "\nClient Requesting position: ", position
            success = self.turtle_client(position.x, position.y)
            if success:
                print "Position set successfully"
            else:
                print "Setting Position failed"

if __name__ == '__main__':
    n = PoseClient()
    # Read in input
    while not rospy.is_shutdown():
        n.requestPositioning()
        rospy.spin()

