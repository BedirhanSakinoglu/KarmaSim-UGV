import rospy
import globals
import math
from karmasim_ros_wrapper.srv import VehicleStart, VehicleStop, VehicleUnload, VehicleLoad
from karmasim_ros_wrapper.msg import CarControls

class RosController:
    uxv_name = rospy.get_param('~uxv_name', 'ugv_1')
    request = rospy.ServiceProxy('/karmasim_node/vehicle_start', VehicleStart)
    result = request(uxv_name)
    pub = rospy.Publisher('/karmasim_node/ugv_1/ugv_cmd', CarControls, queue_size=10)
    car_cmd = CarControls()
    last_position = (0,0)
    last_time = 0
    current_speed = 0
    gear = 0
    
    def __init__(self):
        self.gear = 0

    def set_last_position(self):
        self.last_position = (globals.uxv.pose.position.x, globals.uxv.pose.position.y)
        
    def set_last_time(self):
        self.last_time = rospy.get_time()

    def calculate_speed(self):
        distance = math.sqrt(math.pow(globals.uxv.pose.position.x - self.last_position[0], 2) + math.pow(globals.uxv.pose.position.y - self.last_position[1], 2))
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
        self.result = request(globals.uxv_name)

    def looper(self):
        if (rospy.get_time() - self.last_time) > 1:
            #time.sleep(0.4)
            self.calculate_speed()
            self.set_last_position()
            self.set_last_time()
            #print("SPEED: ", self.current_speed)
