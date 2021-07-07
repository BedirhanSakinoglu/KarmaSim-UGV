#!/usr/bin/env python

import rospy
import time
import threading
import math
from karmasim_ros_wrapper.msg import UxvStates
from karmasim_ros_wrapper.msg import PointsOfInterest
from karmasim_ros_wrapper.msg import CarControls
from karmasim_ros_wrapper.srv import VehicleStart, VehicleStop, VehicleUnload, VehicleLoad

poi_counter = 0
is_first_move = True
uxv_name = 'ugv_1'
uxv = None
uxv_speed = 0
directions = ['W','N','E','S']
direction_index = 0
recent_turn = None
recent_index = 0
turning_flag = False
poi = None
timer = None
car_cmd = None
rsc = None
gtc = None
target_index = 0
vehicle_state = None

class GoToTarget:
    pass

class GoToTurn:
    turn_index = None
    target_direction = None
    flag = False
    #target_corner = None

    def set_target_corner(self, turn_index, target_direction):
        self.turn_index = turn_index
        self.target_direction = target_direction
        gtc.set_location(turns[self.turn_index][0], turns[self.turn_index][1])

    def looper(self):
        if self.turn_index == None:
            return            
        if vehicle_state == 'TURN':
            if self.target_direction == 'RIGHT':
                print("heeyo")
                turn_right()
                self.flag = True
            elif self.target_direction == 'LEFT':
                print("aaaayo")
                turn_left()
                self.flag = True
        elif self.flag:
            self.target_direction = None
            self.turn_index = None
            self.flag = False
            gtc.mission_completed()
            print("Mission failed succesfully")

class GoToCoordinate:
    target = None

    def set_location(self, x, y):
        self.target = (x,y)

    def mission_completed(self):
        self.target = None
    
    def looper(self):
        if vehicle_state == 'TURN':
            return

        if self.target == None:
            return
        
        #print("Speed: ", uxv.state)
        if directions[direction_index] == 'W':
            #print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
            if (uxv.pose.position.y > (self.target[1] - 5)) and (uxv.pose.position.y < (self.target[1] + 5)) and rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif uxv.pose.position.y > self.target[1] and rsc.current_speed == 0 :
                rsc.forward_gear()
                rsc.brake(False)
                rsc.throttle(0.4)
                print("VIN VIN")
            elif (uxv.pose.position.y > self.target[1] - 2.5) and rsc.gear == -1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")
            elif uxv.pose.position.y > self.target[1] + 5:
                rsc.forward_gear()
                rsc.throttle(0.4)
                rsc.brake(False)
                print("go go go")
            elif uxv.pose.position.y < self.target[1] and rsc.current_speed == 0 :
                rsc.reverse_gear()
                rsc.brake(False)
                rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif uxv.pose.position.y < self.target[1] - 2.5 and rsc.gear == -1 :
                rsc.brake(False)
                #rsc.reverse_gear()
                rsc.throttle(-0.4)
                print("gear : " , rsc.gear)
                print("GO BACK")
            elif uxv.pose.position.y < self.target[1] + 5 and rsc.gear == 1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")
            
        elif directions[direction_index] == 'N':
            if (uxv.pose.position.x < self.target[0] + 5) and (uxv.pose.position.x > self.target[0] - 5) and rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif uxv.pose.position.x < self.target[0] and rsc.current_speed == 0 :
                rsc.forward_gear()
                rsc.brake(False)
                rsc.throttle(0.4)
                print("VIN VIN")
            elif (uxv.pose.position.x < self.target[0] + 2.5) and rsc.gear == -1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")
            elif uxv.pose.position.x < self.target[0] - 5:
                rsc.forward_gear()
                rsc.throttle(0.4)
                rsc.brake(False)
                print("go go go")
            elif uxv.pose.position.x > self.target[0] and rsc.current_speed == 0 :
                rsc.reverse_gear()
                rsc.brake(False)
                rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif uxv.pose.position.x > self.target[0] + 2.5 and rsc.gear == -1 :
                rsc.brake(False)
                #rsc.reverse_gear()
                rsc.throttle(-0.4)
                print("gear : " , rsc.gear)
                print("GO BACK")
            elif uxv.pose.position.x > self.target[0] - 5 and rsc.gear == 1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")
            
        elif directions[direction_index] == 'E':
            if (uxv.pose.position.y < (self.target[1] + 5)) and (uxv.pose.position.y > (self.target[1] - 5)) and rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif uxv.pose.position.y < self.target[1] and rsc.current_speed == 0 :
                rsc.forward_gear()
                rsc.brake(False)
                rsc.throttle(0.4)
                print("VIN VIN")
            elif (uxv.pose.position.y < self.target[1] + 2.5) and rsc.gear == -1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")
            elif uxv.pose.position.y < self.target[1] - 5:
                rsc.forward_gear()
                rsc.throttle(0.4)
                rsc.brake(False)
                print("go go go")
            elif uxv.pose.position.y > self.target[1] and rsc.current_speed == 0 :
                rsc.reverse_gear()
                rsc.brake(False)
                rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif uxv.pose.position.y > self.target[1] + 2.5 and rsc.gear == -1 :
                rsc.brake(False)
                #rsc.reverse_gear()
                rsc.throttle(-0.4)
                print("gear : " , rsc.gear)
                print("GO BACK")
            elif uxv.pose.position.y > self.target[1] - 5 and rsc.gear == 1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")

        elif directions[direction_index] == 'S':
            if (uxv.pose.position.x > self.target[0] - 5 ) and (uxv.pose.position.x < self.target[0] + 5) and rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif uxv.pose.position.x > self.target[0] and rsc.current_speed == 0 :
                rsc.forward_gear()
                rsc.brake(False)
                rsc.throttle(0.4)
                print("VIN VIN")
            elif (uxv.pose.position.x > self.target[0] - 2.5) and rsc.gear == -1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")
            elif uxv.pose.position.x > self.target[0] + 5:
                rsc.forward_gear()
                rsc.throttle(0.4)
                rsc.brake(False)
                print("go go go")
            elif uxv.pose.position.x < self.target[0] and rsc.current_speed == 0 :
                rsc.reverse_gear()
                rsc.brake(False)
                rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif uxv.pose.position.x < self.target[0] - 2.5 and rsc.gear == -1 :
                rsc.brake(False)
                #rsc.reverse_gear()
                rsc.throttle(-0.4)
                print("gear : " , rsc.gear)
                print("GO BACK")
            elif uxv.pose.position.x < self.target[0] + 5 and rsc.gear == 1 :
                rsc.throttle(0)
                rsc.brake(True)
                print("STOP")

class RosController:
    uxv_name = rospy.get_param('~uxv_name', 'ugv_1')
    request = rospy.ServiceProxy('/karmasim_node/vehicle_start', VehicleStart)
    result = request(uxv_name)
    pub = rospy.Publisher('/karmasim_node/ugv_1/ugv_cmd', CarControls, queue_size=10)
    car_cmd = CarControls()
    last_position = (0,0)
    last_time = 0
    current_speed = 0.0
    gear = 0
    
    def set_last_position(self):
        self.last_position = (uxv.pose.position.x, uxv.pose.position.y)
        
    def set_last_time(self):
        self.last_time = rospy.get_time()

    def calculate_speed(self):
        distance = math.sqrt(math.pow(uxv.pose.position.x - self.last_position[0], 2) + math.pow(uxv.pose.position.y - self.last_position[1], 2))
        time = rospy.get_time() - self.last_time
        print("distance: ", distance)
        print("time: ", time)
        self.current_speed = distance/time

    def set_for_start(self):
        self.car_cmd.handbrake = False
        self.car_cmd.gear_immediate = True
        self.car_cmd.brake = 0
        self.car_cmd.manual = False
        self.car_cmd.throttle = 0.4
        self.gear = 1
        if self.car_cmd.manual_gear != 1:
            self.car_cmd.manual_gear = 1
        self.pub.publish(self.car_cmd)

    def steer(self, steering_value):
        #print("uxv name is : ", uxv_name)
        #print("steering value = ", steering_value)
        self.car_cmd.throttle = 0.4
        self.car_cmd.brake = False  #TODO
        self.car_cmd.steering = steering_value
        self.pub.publish(self.car_cmd)

    def throttle(self, throttle_value):
        self.car_cmd.throttle = throttle_value
        self.car_cmd.manual_gear = self.gear
        self.pub.publish(self.car_cmd)

    def brake(self, is_brake):
        self.car_cmd.brake = is_brake
        self.pub.publish(self.car_cmd)

    def reverse_gear(self):
        self.car_cmd.manual = True
        self.gear = -1
        self.car_cmd.manual_gear = -1
        self.car_cmd.gear_immediate = True
        self.pub.publish
        #self.car_cmd.manual = False

    def forward_gear(self):
        self.gear = 1
        self.car_cmd.manual = False
        self.car_cmd.manual_gear = 1
        self.pub.publish
        #self.car_cmd.manual = False

    def finish(self):
        car_cmd = CarControls()
        car_cmd.handbrake = False
        car_cmd.manual = False
        car_cmd.gear_immediate = True
        car_cmd.throttle = 0
        car_cmd.steering = 0
        car_cmd.brake = 0
        self.pub.publish(car_cmd)
        request = rospy.ServiceProxy('/karmasim_node/vehicle_stop', VehicleStop)
        self.result = request(uxv_name)

    def looper(self):
        if (rospy.get_time() - self.last_time) > 1:
            #time.sleep(0.4)
            self.calculate_speed()
            self.set_last_position()
            self.set_last_time()
            print("SPEED: ", self.current_speed)

def adjuster():
    #print("W: ", uxv.pose.orientation.w)
    if directions[direction_index] == 'W':
        if uxv.pose.orientation.w < 0.7:
            turn_value = (0.7 - uxv.pose.orientation.w)*4 + 0.05
            rsc.steer(rsc.gear * turn_value) 
        elif uxv.pose.orientation.w > 0.7:
            turn_value = (0.7 - uxv.pose.orientation.w)*8 - 0.05
            rsc.steer(rsc.gear * turn_value)
    elif directions[direction_index] == 'N':
        if uxv.pose.orientation.z < 0:
            #print("right right right")
            turn_value = (1 - uxv.pose.orientation.w)*8 + 0.05
            rsc.steer(rsc.gear * turn_value)
        elif uxv.pose.orientation.z > 0:
            #print("left left left")
            turn_value = (1 - uxv.pose.orientation.w)*8 + 0.05
            rsc.steer(rsc.gear * -turn_value)
    elif directions[direction_index] == 'E':
        if uxv.pose.orientation.w < 0.7:
            turn_value = (0.7 - uxv.pose.orientation.w)*4 + 0.05
            rsc.steer(rsc.gear * -turn_value)
        elif uxv.pose.orientation.w > 0.7:
            turn_value = (0.7 - uxv.pose.orientation.w)*8 - 0.05
            rsc.steer(rsc.gear * -turn_value)
    elif directions[direction_index] == 'S':
        if uxv.pose.orientation.z < 0:
            turn_value = (0 - uxv.pose.orientation.w)*4 - 0.05
            rsc.steer(rsc.gear * turn_value)
        elif uxv.pose.orientation.z > 0:
            turn_value = (0 - uxv.pose.orientation.w)*4 - 0.05
            rsc.steer(rsc.gear * -turn_value)
    
    #rsc.throttle(0.35)

def turn_right():
    global is_first_move
    global direction_index
    global turning_flag

    if directions[direction_index] == 'W':
        #print("heading West, turn right")
        if uxv.pose.orientation.w < 0.98:
            rsc.steer(3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index += 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'N':
        #print("heading North, turn right")
        if uxv.pose.orientation.w > 0.80:
            rsc.steer(3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index += 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'E':
        #print("heading East, turn right")
        if uxv.pose.orientation.w > 0.05:
            rsc.steer(3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index += 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'S':
        #print("heading South, turn right")
        if uxv.pose.orientation.w < 0.68:
            rsc.steer(3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index += 1
            is_first_move = False
            turning_flag = False

    direction_index= direction_index % 4

def turn_left():
    global is_first_move
    global direction_index
    global turning_flag
    
    if directions[direction_index] == 'W':
        #print("heading West, turn left")
        if uxv.pose.orientation.w > 0.05:
            rsc.steer(-3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'N':
        #print("heading North, turn left")
        if uxv.pose.orientation.w > 0.80:
            rsc.steer(-3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'E':
        #print("heading East, turn left")
        if uxv.pose.orientation.w < 0.98:
            rsc.steer(-3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    elif directions[direction_index] == 'S':
        #print("heading South, turn left")
        if uxv.pose.orientation.w < 0.7:
            rsc.steer(-3.0)
        else:
            #print("turning complete")
            rsc.steer(0)
            direction_index -= 1
            is_first_move = False
            turning_flag = False

    #-------------------------------------------------
    #print("this is turn left")
    #print("Ori: " , uxv.pose.orientation.w )
    
    #rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.position.x, uxv.pose.position.y, uxv.pose.position.z)
    #rospy.loginfo("This is the orientation of %s  : W: %f , X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.orientation.w, uxv.pose.orientation.x, uxv.pose.orientation.y, uxv.pose.orientation.z)
    direction_index= direction_index % 4

def start_move():
    #print("vehicle name: %s", uxv_name)

    if uxv.pose.position.y > -22:
        rsc.set_for_start()

    else:
        turn_right()

    #print("DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE")

def looper(timer):
    if uxv == None:
        return

    rsc.looper()
    #if directions[direction_index] == 'S':
        #gtc.set_location(0,26)
    

    #return

    global is_first_move
    global recent_turn
    global recent_index
    global turning_flag
    global direction_index 

    if is_first_move:
        start_move()
    else:
        gtc.looper()
        gtt.looper()
        global vehicle_state
        #if directions[direction_index] == 'S':
            #gtc.set_location(-5,26)
        counter = 0
        #print("X : ", uxv.pose.position.x, ", Y : ", uxv.pose.position.y)
        #print(uxv.pose.position.y)
        vehicle_state = None
        for x in turns:
            if abs(x[0]-uxv.pose.position.x) < 5 or turning_flag:
                if abs(x[1]-uxv.pose.position.y) < 5 or turning_flag:
                    #print("Direction index: ", direction_index , ", Recent index: ", recent_index)
                    if direction_index != recent_index and x == recent_turn:
                        pass
                        #print("hadi")
                    else:
                        global vehicle_state
                        turning_flag = True
                        recent_index = direction_index
                        if abs(x[0]-uxv.pose.position.x) < 5 and abs(x[1]-uxv.pose.position.y) < 5:
                            recent_turn = x
                            #print("INDEX: ", turns.index(x))
                        #turn_right()
                        vehicle_state = 'TURN'

                else:
                    #print("ADJUST")
                    adjuster()
            else:
                #print("ADJUST")
                adjuster()
        
        #poi --------------
        #print (vehicle_state)
        #for a in turns:
        #    for b in a[3]:
        #        if (poi[target_index].pose.position.x <= a[0] and poi[target_index].pose.position.x >= turns[b][0]) or (poi[target_index].pose.position.x >= a[0] and poi[target_index].pose.position.x <= turns[b][0]):
        #            rospy.loginfo("heyo")
        #            if (poi[target_index].pose.position.y <= a[1] and poi[target_index].pose.position.y >= turns[b][1]) or (poi[target_index].pose.position.y >= a[1] and poi[target_index].pose.position.y <=turns[b][1]):
        #                print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        #                print("this poi is between turns ", turns.index(a), " and ", turns.index(b))

#rospy.Timer(rospy.Duration(1), looper)
#print("timer is here")

def callback2(data):
    global poi
    poi = data.pois
    #rospy.loginfo("POI X: %f , Y: %f", data.pois[poi_counter].pose.position.x, data.pois[poi_counter].pose.position.y)
    # poi_counter += 1

def callback(data):
    global uxv
    for x in data.uxvs:
        #print("This is callback: ", uxv_name)
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

    rsc = RosController()
    gtc = GoToCoordinate()
    gtt = GoToTurn()

    gtt.set_target_corner(10, 'RIGHT')
    
    try:
        timer = rospy.Timer(rospy.Duration(0.01), looper)
        rospy.Subscriber("/karmasim_node/uxv_states", UxvStates, callback)
        rospy.Subscriber("/karmasim_node/points_of_interest", PointsOfInterest, callback2)
        #rospy.Subscriber("/karmasim_node/ugv_1/odom_local_ned", callback3)
        rospy.wait_for_service('/karmasim_node/vehicle_start')
        rospy.spin()
    except:
        pass
    finally:
        rsc.finish()
