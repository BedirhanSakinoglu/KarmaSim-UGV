#!/usr/bin/env python
from target_layer import GoToTarget
import rospy
import time
import threading
import math
from karmasim_ros_wrapper.msg import UxvStates
from karmasim_ros_wrapper.msg import PointsOfInterest
from karmasim_ros_wrapper.msg import CarControls
from ros_controller import RosController
from coordinate_layer import GoToCoordinate
from turn_layer import GoToTurn
import globals
from vehicle_commands import VehicleCommands
from target_layer import GoToTarget

def callback(data):
    for x in data.uxvs:
        #print("This is callback: ", uxv_name)
        if (x.name == globals.uxv_name):
            globals.uxv = x

def callback2(data):
    globals.poi = data.pois
    #rospy.loginfo("POI X: %f , Y: %f", data.pois[poi_counter].pose.position.x, data.pois[poi_counter].pose.position.y)
    # poi_counter += 1

if __name__ == "__main__":
    rospy.init_node('contester_node')
    print('Hello World')
    contest_parameters = rospy.get_param('/scenario')
    world_boundaries = contest_parameters["world_boundaries"]
    print('World Boundaries')
    print(world_boundaries)
    globals.turns = [
        (85, -142.6, -0.5, [1,3], 0),
        (85, -92.6, -0.5, [0,2,4], 1),
        (85, 77.2, -0.5, [1,7], 2),

        (30.1, -142.8, -0.5, [0,4,12], 3),
        (30.1, -92.6, -0.5, [1,3,5], 4),
        (30.1, -27.7, -0.5, [4,6,8], 5),
        (30.1, 27.5, -0.5, [5,7,9], 6),
        (29.9, 77.2, -0.5, [2,6,11], 7),

        (-25, -27.6, -0.5, [5,9,10], 8),
        (-25, 27.5, -0.5, [6,8], 9),
        
        (-75, -27.6, -0.5, [8,11,13], 10),
        (-75, 77.2, -0.5, [7,10,14], 11),

        (-129.9, -142.8, -0.5, [3,13], 12),
        (-129.9, -27.8, -0.5, [10,12,14], 13),
        (-129.9, 77.2, -0.5, [11,13], 14),
        
        #(0, -27.7, -0.5, []),
        # (0, -27.7, -0.5, [16,17,18]),
        # (6.4, -12.2, -0.5),
        # (0, -12.2, -0.5),
        # (-6.4, -12.2, -0.5)
    ]

    globals.rsc = RosController()
    globals.gtc = GoToCoordinate()
    globals.gtt = GoToTurn()
    globals.gttarget = GoToTarget()
    globals.vcoms = VehicleCommands()
    
    try:
        timer = rospy.Timer(rospy.Duration(0.01), globals.vcoms.looper)
        rospy.Subscriber("/karmasim_node/uxv_states", UxvStates, callback)
        rospy.Subscriber("/karmasim_node/points_of_interest", PointsOfInterest, callback2)
        #rospy.Subscriber("/karmasim_node/ugv_1/odom_local_ned", callback3)
        rospy.wait_for_service('/karmasim_node/vehicle_start')
        rospy.spin()
    except:
        pass
    finally:
        globals.rsc.finish()
