#!/usr/bin/env python

from service_demo.srv import two_ints
import rospy

class server:
    def __init__(self):
        #initialize the server node
        rospy.init_node("server_demo")

        #Display in the console the message
        rospy.loginfo("Server initiated")

        self.int_server = rospy.Service("ProcessNums", two_ints, self.processNumbers)

    def processNumbers(self, req):
        response = two_ints()
        response.sum = req.num1 + req.num2
        response.sub = req.num1 - req.num2
        response.mul = req.num1 * req.num2
        response.div = float(req.num1) / req.num2
        print(response.sum, response.sub, response.mul, response.div)
        return response.sum, response.sub, response.mul, response.div

if __name__ == '__main__':
    n = server()

    rospy.spin()
