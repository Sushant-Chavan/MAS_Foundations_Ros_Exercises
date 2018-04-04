#!/usr/bin/env python

PACKAGE = 'turtle_controller'
NODE = 'pose_controller'

import rospy
import std_msgs
import numpy as np

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from service_demo.srv import turtle_control

class PoseController:
	def __init__(self):
		self.eps_linear = 0.1
		self.eps_angular = 0.01
		# Initialize the node
		rospy.init_node(NODE)

		#Display in the console the message
		rospy.loginfo("Server initiated")

		# Create current and target pose
		self.current_pose = Pose()
		self.target_pose = Pose()

		# Create velocity
		self.target_vel = Twist()

		# Create subscriber for pose from turtle
		self.current_pose_sub = rospy.Subscriber("turtle1/pose", Pose, self.current_pose_callback)
		
		self.turtle_server = rospy.Service("positionTurtle", turtle_control, self.setPosition)

		# Create publisher for velocity
		self.target_vel_pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size = 10)

	def current_pose_callback(self, msg):
		self.current_pose = msg
		self.calculate_velocity()
		pass

	def setPosition(self, msg):
		print "Server SetPosition called with position: ", msg
		self.target_pose = Pose()
		self.target_pose.x = msg.x
		self.target_pose.y = msg.y
		self.calculate_velocity()
		return True

	def calculate_velocity(self):
		# Get dx, dy, dtheta
		dx = np.abs(self.current_pose.x - self.target_pose.x)
		dy = np.abs(self.current_pose.y - self.target_pose.y)
		dtheta = np.abs(self.target_pose.theta - self.current_pose.theta)
		# Check if (x,y) is okay
		if ((dx < self.eps_linear) and (dy < self.eps_linear)):
			self.target_vel.linear.x = 0.0
			# We reached the correct (x,y), rotate to theta
			if (dtheta > self.eps_angular):
				self.target_vel.angular.z = (self.target_pose.theta - self.current_pose.theta) / 3.0
			else:
				self.target_vel.angular.z = 0.0
		else:
			# Orient towards target pose
			#angle = np.arctan2(dx, dy) - self.current_pose.theta# + np.pi
			angle = np.arctan2(self.target_pose.y - self.current_pose.y, self.target_pose.x - self.current_pose.x);
			#print angle - self.current_pose.theta
			if (np.abs(angle - self.current_pose.theta) > self.eps_angular):
				self.target_vel.linear.x = 0.0
				self.target_vel.angular.z = angle - self.current_pose.theta
			else:
				self.target_vel.linear.x = 0.3
				self.target_vel.angular.z = 0.0

if __name__ == '__main__':
	n = PoseController()
	rate = rospy.Rate(1)
	# Read in input
	while not rospy.is_shutdown():
		# Publish message
		n.target_vel_pub.publish(n.target_vel)
		rate.sleep()
