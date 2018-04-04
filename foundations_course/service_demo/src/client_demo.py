#!/usr/bin/env python

from service_demo.srv import two_ints
import rospy

class client:
    def __init__(self):
        #Initialize the client node
        rospy.init_node("client_demo")

        #Show in the console the message
        rospy.loginfo("Client initiated")

        #Pause the node untill the service specified(service_label) is active
        rospy.wait_for_service("ProcessNums")

        self.num_client = rospy.ServiceProxy("ProcessNums", two_ints)


if __name__=='__main__':
    n = client()

    while not rospy.is_shutdown():
        try:
            num1 = int(raw_input("Enter Num1 : "))
        except ValueError:
            num1 = 0

        try:
            num2 = int(raw_input("Enter Num2 : "))
        except ValueError:
            num2 = 0.0

        result = n.num_client(num1, num2)

        print "\nClient Received\n", result

        rospy.spin()
