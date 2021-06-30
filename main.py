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
directions = ['W','N','E','S']
direction_index = 0
recent_turn = None
recent_index = 0
turning_flag = False

def adjuster():
    #print("adjust direction...")
    if directions[direction_index] == 'W':
        if uxv.pose.orientation.w < 0.7:
            car_cmd.steering = 0.10
        elif uxv.pose.orientation.w > 0.7:
            car_cmd.steering = -0.10
    elif directions[direction_index] == 'N':
        if uxv.pose.orientation.z < 0:
            car_cmd.steering = 0.10
        elif uxv.pose.orientation.w > 0:
            car_cmd.steering = -0.10
    elif directions[direction_index] == 'E':
        if uxv.pose.orientation.w < 0.7:
            car_cmd.steering = -0.10
        elif uxv.pose.orientation.w > 0.7:
            car_cmd.steering = 0.10
    elif directions[direction_index] == 'S':
        if uxv.pose.orientation.z < 0:
            car_cmd.steering = -0.10
        elif uxv.pose.orientation.w > 0:
            car_cmd.steering = 0.10

    #pub.publish(car_cmd)
    #print("adjust speed...")
    
    car_cmd.throttle = 0.35
    pub.publish(car_cmd)

def turn_right():
    global is_first_move
    global direction_index
    global turning_flag

    
    if directions[direction_index] == 'W':
        print("heading West, turn right")
        if uxv.pose.orientation.w < 0.98:
            car_cmd.steering = 3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index += 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'N':
        print("heading North, turn right")
        if uxv.pose.orientation.w > 0.65:
            car_cmd.steering = 3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index += 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'E':
        print("heading East, turn right")
        if uxv.pose.orientation.w > 0.05:
            car_cmd.steering = 3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index += 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'S':
        print("heading South, turn right")
        if uxv.pose.orientation.w < 0.68:
            car_cmd.steering = 3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index += 1
            is_first_move = False
            turning_flag = False

    direction_index= direction_index % 4
    pub.publish(car_cmd)

def turn_left():
    global is_first_move
    global direction_index
    global turning_flag
    
    if directions[direction_index] == 'W':
        print("heading West, turn left")
        if uxv.pose.orientation.w > 0.05:
            car_cmd.steering = -3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'N':
        print("heading North, turn left")
        if uxv.pose.orientation.w > 0.80:
            car_cmd.steering = -3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'E':
        print("heading East, turn left")
        if uxv.pose.orientation.w < 0.98:
            car_cmd.steering = -3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'S':
        print("heading South, turn left")
        if uxv.pose.orientation.w < 0.7:
            car_cmd.steering = -3.0
        else:
            print("turning complete")
            car_cmd.steering = 0
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    #-------------------------------------------------
    #print("this is turn left")
    #print("Ori: " , uxv.pose.orientation.w )
    
    #rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.position.x, uxv.pose.position.y, uxv.pose.position.z)
    #rospy.loginfo("This is the orientation of %s  : W: %f , X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.orientation.w, uxv.pose.orientation.x, uxv.pose.orientation.y, uxv.pose.orientation.z)
    direction_index= direction_index % 4
    pub.publish(car_cmd)

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
        turn_right()
        
    #print("DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE")

def looper(timer):
    if uxv == None:
        return

    global is_first_move
    global recent_turn
    global recent_index
    global turning_flag
    global direction_index 

    if is_first_move:
        start_move()
    else:
        counter = 0
        #print("X : ", uxv.pose.position.x, ", Y : ", uxv.pose.position.y)
        #print(uxv.pose.position.y)
        for x in turns:
            if abs(x[0]-uxv.pose.position.x) < 5 or turning_flag:
                if abs(x[1]-uxv.pose.position.y) < 5 or turning_flag:
                    print("Direction index: ", direction_index , ", Recent index: ", recent_index)
                    if direction_index != recent_index and x == recent_turn:
                        print("hadi")
                    else:
                        turning_flag = True
                        recent_index = direction_index
                        if abs(x[0]-uxv.pose.position.x) < 5 and abs(x[1]-uxv.pose.position.y) < 5:
                            recent_turn = x
                            print("INDEX: ", turns.index(x))
                        turn_right()

                else:
                    adjuster()
            else:
                adjuster()

        rospy.Subscriber("/karmasim_node/points_of_interest", PointsOfInterest, callback2)

#rospy.Timer(rospy.Duration(1), looper)
#print("timer is here")

def callback2(data):
    global poi_counter
    rospy.loginfo("POI X: %f , Y: %f", data.pois[poi_counter].pose.position.x, data.pois[poi_counter].pose.position.y)
    for a in turns:
        for b in a[3]:
            if (data.pois[poi_counter].pose.position.x <= a[0] and data.pois[poi_counter].pose.position.x >= turns[b][
                0]) or (data.pois[poi_counter].pose.position.x >= a[0] and data.pois[poi_counter].pose.position.x <=
                        turns[b][0]):
                rospy.loginfo("heyo")
                if (data.pois[poi_counter].pose.position.y <= a[1] and data.pois[poi_counter].pose.position.y >= turns[b][1]) or (data.pois[poi_counter].pose.position.y >= a[1] and data.pois[poi_counter].pose.position.y <=turns[b][1]):
                    print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
                    print("this poi is between turns ", turns.index(a), " and ", turns.index(b))
    # poi_counter += 1

def callback(data):
    global uxv
    for x in data.uxvs:
        if (x.name == uxv_name):
            uxv = x

if __name__ == "__main__":
    rospy.init_node('contester_node')
    print('Hello World')
    contest_parameters = rospy.get_param('/scenario')
    world_boundaries = contest_parameters["world_boundaries"]
    print('World Boundaries')
    print(world_boundaries)
    turns = [
        (85, -142.6, -0.5, [1, 8]),
        (85, -92.6, -0.5, [0, 2, 9]),
        (85, 77.2, -0.5, [1,3]),
        (29.9, 77.2, -0.5, [2, 4, 11]),
        (-75, 77.2, -0.5, [3, 5, 14]),
        (-129.9, 77.2, -0.5, [4, 6]),
        (-129.9, -27.8, -0.5, [5, 7, 14]),
        (-129.9, -142.8, -0.5, [6, 8]),
        (30.1, -142.8, -0.5, [0, 7, 9]),
        (30.1, -92.6, -0.5, [1, 8, 10]),
        (30.1, -27.7, -0.5, [9, 11]),
        (30.1, 27.5, -0.5, [3, 10, 12]),
        (-25, 27.5, -0.5, [11, 13]),
        (-25, -27.6, -0.5, [12, 14]),
        (-75, -27.6, -0.5, [4, 6, 13]),
        #(0, -27.7, -0.5, []),
        # (0, -27.7, -0.5, [16,17,18]),
        # (6.4, -12.2, -0.5),
        # (0, -12.2, -0.5),
        # (-6.4, -12.2, -0.5)
    ]
    
    try:
        uxv_name = rospy.get_param('~uxv_name', 'ugv_1')
        request = rospy.ServiceProxy('/karmasim_node/vehicle_start', VehicleStart)
        result = request(uxv_name)
        pub = rospy.Publisher('/karmasim_node/ugv_1/ugv_cmd', CarControls, queue_size=10)
        car_cmd = CarControls()
        timer = rospy.Timer(rospy.Duration(0.01), looper)
        rospy.Subscriber("/karmasim_node/uxv_states", UxvStates, callback)
        rospy.wait_for_service('/karmasim_node/vehicle_start')
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
