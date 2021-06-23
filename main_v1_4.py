#!/usr/bin/env python

import rospy
import time
from karmasim_ros_wrapper.msg import UxvStates
from karmasim_ros_wrapper.msg import PointsOfInterest
from karmasim_ros_wrapper.msg import CarControls
from karmasim_ros_wrapper.srv import VehicleStart, VehicleStop, VehicleUnload, VehicleLoad

poi_counter = 0
uxv_name = 'ugv_1'
is_first_move = True

def turn_left():
    print("TURN LEFT")

def start_move(uxvs, index):
	print("sadasdasd\n\n\n")
	print("vehicle name: %s", uxv_name)
	car_cmd.handbrake = False
	car_cmd.gear_immediate = False
	car_cmd.brake = 0
	car_cmd.manual = False
	car_cmd.throttle = 1.0
	if car_cmd.manual_gear != 1:
	    car_cmd.manual_gear = 1
	while (uxvs[index].pose.position.y > -22):
	    pub.publish(car_cmd)
	    print("hey: ", uxvs[index].pose.position.y)
	turn_left()
	print("DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE")

def callback2(data):
    global poi_counter
    rospy.loginfo("POI X: %f , Y: %f", data.pois[poi_counter].pose.position.x, data.pois[poi_counter].pose.position.y)
    for a in turns:
        for b in a[3]:
            if (data.pois[poi_counter].pose.position.x <= a[0] and data.pois[poi_counter].pose.position.x >= turns[b][
                0]) or (data.pois[poi_counter].pose.position.x <= a[0] and data.pois[poi_counter].pose.position.x >=
                        turns[b][0]):
                rospy.loginfo("")
                if (data.pois[poi_counter].pose.position.y <= a[1] and data.pois[poi_counter].pose.position.y >=
                    turns[b][1]) or (
                        data.pois[poi_counter].pose.position.y <= a[1] and data.pois[poi_counter].pose.position.y >=
                        turns[b][1]):
                    rospy.loginfo("")
    # poi_counter += 1


def callback(data):
    global uxv_name
    global is_first_move
    uxv_name = rospy.get_param('~uxv_name', 'ugv_1')
    index = 0
    for x in data.uxvs:
        if (x.name == uxv_name):
            index = data.uxvs.index(x)
    rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", data.uxvs[index].name,
                  data.uxvs[index].pose.position.x, data.uxvs[index].pose.position.y, data.uxvs[index].pose.position.z)
    counter = 0
    if (is_first_move):
        rospy.wait_for_service('/karmasim_node/vehicle_start')
        request = rospy.ServiceProxy('/karmasim_node/vehicle_start', VehicleStart)
        result = request(uxv_name)
        start_move(data.uxvs, index)
        is_first_move = False
    for x in turns:
        if abs(x[0] - data.uxvs[index].pose.position.x) < 5:
            if abs(x[1] - data.uxvs[index].pose.position.y) < 5:
                # rospy.loginfo("TURN")
                print(counter + 1)
                # rospy.Subscriber("/karmasim_node/points_of_interest", PointsOfInterest, callback2)
        counter += 1


def my_func():
    global is_first_move
    is_first_move = True
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
        (85, -142.6, -0.5, [1, 8, 11]),
        (85, -92.6, -0.5, [2, 9]),
        (85, -77.2, -0.5, [3]),
        (29.9, -77.2, -0.5, [4, 11]),
        (-75, -77.2, -0.5, [5, 14]),
        (-129.9, -77.2, -0.5, [6]),
        (-129.9, -27.8, -0.5, [7, 14]),
        (-129.9, -142.8, -0.5, [8]),
        (30.1, -142.8, -0.5, [9]),
        (30.1, -92.6, -0.5, [10]),
        (30.1, -27.7, -0.5, [11, 15]),
        (30.1, 27.5, -0.5, [12]),
        (-25, 27.5, -0.5, [13]),
        (-25, -27.6, -0.5, [14, 15]),
        (-75, -27.6, -0.5, []),
        (0, -27.7, -0.5, []),
        # (0, -27.7, -0.5, [16,17,18]),
        # (6.4, -12.2, -0.5),
        # (0, -12.2, -0.5),
        # (-6.4, -12.2, -0.5)
    ]
    uxv_name = rospy.get_param('~uxv_name', 'ugv_1')
    pub = rospy.Publisher('/karmasim_node/ugv_1/ugv_cmd', CarControls, queue_size=10)
    car_cmd = CarControls()
    try:
        # start_move()
        my_func()
    except:
        print()
    finally:
        car_cmd = CarControls()
        car_cmd.handbrake = False
        car_cmd.manual = False
        car_cmd.gear_immediate = True
        car_cmd.throttle = 0
        car_cmd.steering = 0
        car_cmd.brake = 0
        pub.publish(car_cmd)
        request = rospy.ServiceProxy('/karmasim_node/vehicle_stop', VehicleStop)
        result = request(uxv_name)



