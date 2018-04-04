#!/usr/bin/env python

PACKAGE = 'turtle_controller'
NODE = 'pose_client'

import rospy
import std_msgs

from turtlesim.msg import Pose

class PoseClient:

	def __init__(self):
		# Initialize the node
		rospy.init_node(NODE)

		# Create publisher
		self.target_vel_pub = rospy.Publisher("turtle_controller/pose", Pose, queue_size = 10)

		# Create target pose msg
		self.target_pose = Pose()


	def read_input(self):
		try:
			self.target_pose.x = float(raw_input("Enter pose x: "))
		except ValueError:
			self.target_pose.x = 0.0
		try:
			self.target_pose.y = float(raw_input("Enter pose y: "))
		except ValueError:
			self.target_pose.y = 0.0
		try:
			self.target_pose.theta = float(raw_input("Enter pose theta: "))
		except ValueError:
			self.target_pose.theta = 0.0


if __name__ == '__main__':
	n = PoseClient()
	rate = rospy.Rate(1)
	# Read in input
	while not rospy.is_shutdown():
		n.read_input()
		# Publish message
		n.target_vel_pub.publish(n.target_pose)
		rate.sleep()

