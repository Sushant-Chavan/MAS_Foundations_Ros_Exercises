#!/usr/bin/env python

PACKAGE = 'turtle_controller'
NODE = 'pose_controller'

import rospy
import math
import std_msgs
import numpy as np

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

DEGREES_TO_ROTATE = 10.0
LINEAR_VELOCITY = 0.5

EPSILON = 5.0

class PoseController:

	def __init__(self):
		# Initialize the node
		rospy.init_node(NODE)
		self.targetInitialized = False

		# Create publisher
		self.target_vel_pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size = 10)

		# Create current and target pose
		self.current_pose = Pose()
		self.target_pose = Pose()

		# Create velocity
		self.target_vel = Twist()

		# Create subscriber for pose from turtle
		self.vel_sub = rospy.Subscriber("turtle1/pose", Pose, self.current_pose_callback)

		# Create subscriber for pose from keyboard
		self.vel_sub = rospy.Subscriber("turtle_controller/pose", Pose, self.target_pose_callback)

		# Create publisher for velocity
		self.target_vel_pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size = 10)

	def current_pose_callback(self, msg):
		self.current_pose = msg
		if not self.targetInitialized:
			self.target_pose = msg
			self.targetInitialized = True
		pass

	def target_pose_callback(self, msg):
		self.target_pose = msg
		pass

	def adjustAngle(self):
		pass
	
	def adjustAngleToGoal(self):
		destAngle = math.atan2( (self.target_pose.y - self.current_pose.y) , (self.target_pose.x - self.current_pose.x) )
		rotationAngle = destAngle - self.current_pose.theta

		retVal = False
		if math.fabs(rotationAngle) > EPSILON:
			self.target_vel.angular.z = np.deg2rad(DEGREES_TO_ROTATE)
		else:
			retVal = True

		return retVal

	def moveForward(self):
		self.target_vel.linear.x = LINEAR_VELOCITY
		pass

	def calculate_velocity(self):
		# # Your code here
		# distanceToDestination = math.sqrt( (self.target_pose.x - self.current_pose.x)**2 + (self.target_pose.y - self.current_pose.y)**2 )
		# destAngle = 0.0
		# if (distanceToDestination > 0): 
		# 	 destAngle = math.acos((self.target_pose.x - self.current_pose.x)/distanceToDestination)

		# if(destAngle != self.current_pose.theta):
		# 	self.target_vel.angular.z = np.deg2rad(DEGREES_TO_ROTATE)
		# elif(distanceToDestination != 0):
		# 	self.target_vel.linear.x = LINEAR_VELOCITY
		# pass

		# distanceToDestination = math.sqrt( (self.target_pose.x - self.current_pose.x)**2 + (self.target_pose.y - self.current_pose.y)**2 )
		# destAngle = math.atan2( (self.target_pose.y - self.current_pose.y) , (self.target_pose.x - self.current_pose.x) )
		# rotationAngle = destAngle - self.current_pose.theta

		# if self.current_pose.theta < rotationAngle:
		# 	self.target_vel.angular.z = np.deg2rad(DEGREES_TO_ROTATE)
		# 	self.target_vel.linear.x = 0.0
		# elif math.fabs(distanceToDestination - 1) > 0.0:
		# 	self.target_vel.linear.x = LINEAR_VELOCITY
		# 	self.target_vel.angular.z = 0.0
		# 	pass

		dx = self.target_pose.x - self.current_pose.x
		dy = self.target_pose.y - self.current_pose.y
		self.target_vel.linear.x = 0.0
		self.target_vel.angular.z = 0.0

		if(math.fabs(dx) <= EPSILON and math.fabs(dy) <= EPSILON):
			self.adjustAngle()
		elif(math.fabs(dx) > EPSILON or math.fabs(dy) > EPSILON):
			if self.adjustAngleToGoal():
				self.moveForward()



if __name__ == '__main__':
	n = PoseController()
	rate = rospy.Rate(1)
	# Read in input
	while not rospy.is_shutdown():
		# Publish message
		n.calculate_velocity()
		n.target_vel_pub.publish(n.target_vel)
		rate.sleep()
