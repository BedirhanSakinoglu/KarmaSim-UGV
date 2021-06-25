#!/usr/bin/env python

import rospy
import time
import threading
from karmasim_ros_wrapper.msg import UxvStates
from karmasim_ros_wrapper.msg import PointsOfInterest
from karmasim_ros_wrapper.msg import CarControls
from karmasim_ros_wrapper.srv import VehicleStart, VehicleStop, VehicleUnload, VehicleLoad

poi_counter = 0
is_first_move = True
uxv_name = 'ugv_1'
uxv = None

def turn_left():
    global is_first_move
    print("this is turn left")
    print("Ori: " , uxv.pose.orientation.w )
    if uxv.pose.orientation.w > 0.135:
        car_cmd.handbrake = False
        car_cmd.gear_immediate = False
        car_cmd.brake = 0
        car_cmd.manual = False
        car_cmd.throttle = 0.4
        car_cmd.steering = -3.0
        if car_cmd.manual_gear != 1:
            car_cmd.manual_gear = 1

    else:
        print("turning complete")
        car_cmd.steering = 0
        is_first_move = False
    #rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.position.x, uxv.pose.position.y, uxv.pose.position.z)
    #rospy.loginfo("This is the orientation of %s  : W: %f , X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.orientation.w, uxv.pose.orientation.x, uxv.pose.orientation.y, uxv.pose.orientation.z)
    pub.publish(car_cmd)


def looper():
    global is_first_move

    if is_first_move:
        start_move()
    
    counter = 0
    for x in turns:
        if abs(x[0] - uxv.pose.position.x) < 5:
            if abs(x[1] - uxv.pose.position.y) < 5:
                rospy.loginfo("TURN")
                # rospy.Subscriber("/karmasim_node/points_of_interest", PointsOfInterest, callback2)

#rospy.Timer(rospy.Duration(1), looper)
#print("timer is here")


def start_move():
    print("vehicle name: %s", uxv_name)

    if uxv.pose.position.y > -22:
        car_cmd.handbrake = False
        car_cmd.gear_immediate = False
        car_cmd.brake = 0
        car_cmd.manual = False
        car_cmd.throttle = 0.4
        if car_cmd.manual_gear != 1:
            car_cmd.manual_gear = 1

        #rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.position.x, uxv.pose.position.y, uxv.pose.position.z)

        #rospy.loginfo("This is the orientation of %s  : W: %f , X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.orientation.w, uxv.pose.orientation.x, uxv.pose.orientation.y, uxv.pose.orientation.z)
        pub.publish(car_cmd)

    else:
        turn_left()
        
    #print("DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE")

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
    global uxv
    for x in data.uxvs:
        if (x.name == uxv_name):
            uxv = x
            #print("burdayim)
    looper()

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
    
    try:
        uxv_name = rospy.get_param('~uxv_name', 'ugv_1')
        pub = rospy.Publisher('/karmasim_node/ugv_1/ugv_cmd', CarControls, queue_size=10)
        car_cmd = CarControls()
        rospy.Subscriber("/karmasim_node/uxv_states", UxvStates, callback)
        rospy.wait_for_service('/karmasim_node/vehicle_start')
        request = rospy.ServiceProxy('/karmasim_node/vehicle_start', VehicleStart)
        result = request(uxv_name)
        #self.timer = rospy.Timer(rospy.Duration(1), looper)
        rospy.spin()
    except:
        pass
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
