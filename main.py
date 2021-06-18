#!/usr/bin/env python

import rospy
from karmasim_ros_wrapper.msg import UxvStates

def callback(data):
    rospy.loginfo("hi")
    rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", data.uxvs[0].name, data.uxvs[0].pose.position.x, data.uxvs[0].pose.position.y, data.uxvs[0].pose.position.z)
    counter = 0
    for x in turns:
        if abs( x[0] - data.uxvs[0].pose.position.x ) < 5:
            if abs( x[1] - data.uxvs[0].pose.position.y ) < 5:
                rospy.loginfo("TURN")
                print(counter+1)
        counter += 1
                

def my_func():
    rospy.loginfo("Hey there")
    rospy.Subscriber("/karmasim_node/uxv_states", UxvStates, callback)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node('contester_node')
    print('Hello World')
    contest_parameters = rospy.get_param('/scenario')
    world_boundaries = contest_parameters["world_boundaries"]
    print('World Boundaries')
    print(world_boundaries)
    turns = [
        (85, -142.6, -0.5, [1,8,11]),
        (85, -92.6, -0.5, [2,9]),
        (85, -77.2, -0.5, [3]),
        (29.9, -77.2, -0.5, [4,11]),
        (-75, -77.2, -0.5, [5,14]),
        (-129.9, -77.2, -0.5, [6]),
        (-129.9, -27.8, -0.5, [7,14]),
        (-129.9, -142.8, -0.5, [8]),
        (30.1, -142.8, -0.5, [9]),
        (30.1, -92.6, -0.5, [10]),
        (30.1, -27.7, -0.5, [11,15]),
        (30.1, 27.5, -0.5, [12]),
        (-25, 27.5, -0.5, [13]),
        (-25, -27.6, -0.5, [14,15]),
        (-75, -27.6, -0.5, [16,17,18]),
        (0, -27.7, -0.5),
        (6.4, -12.2, -0.5),
        (0, -12.2, -0.5),
        (-6.4, -12.2, -0.5)
    ]
    try:
        my_func()
    except rospy.ROSInterruptException:
        pass
