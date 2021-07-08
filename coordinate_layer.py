import globals

class GoToCoordinate:
    target = None

    def set_location(self, x, y):
        self.target = (x,y)

    def mission_completed(self):
        self.target = None
    
    def looper(self):
        if globals.vehicle_state == 'TURN':
            return

        if self.target == None:
            return
        
        #print("Speed: ", uxv.state)
        if globals.directions[globals.direction_index] == 'W':
            #print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
            if (globals.uxv.pose.position.y > (self.target[1] - 5)) and (globals.uxv.pose.position.y < (self.target[1] + 5)) and globals.rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif globals.uxv.pose.position.y > self.target[1] and globals.rsc.current_speed == 0 :
                globals.rsc.forward_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(0.4)
                print("VIN VIN")
            elif (globals.uxv.pose.position.y > self.target[1] - 2.5) and globals.rsc.gear == -1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")
            elif globals.uxv.pose.position.y > self.target[1] + 5:
                globals.rsc.forward_gear()
                globals.rsc.throttle(0.4)
                globals.rsc.brake(False)
                #print("go go go")
            elif globals.uxv.pose.position.y < self.target[1] and globals.rsc.current_speed == 0 :
                globals.rsc.reverse_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif globals.uxv.pose.position.y < self.target[1] - 2.5 and globals.rsc.gear == -1 :
                globals.rsc.brake(False)
                #rsc.reverse_gear()
                globals.rsc.throttle(-0.4)
                print("gear : " , globals.rsc.gear)
                print("GO BACK")
            elif globals.uxv.pose.position.y < self.target[1] + 5 and globals.rsc.gear == 1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")
            
        elif globals.directions[globals.direction_index] == 'N':
            if (globals.uxv.pose.position.x < self.target[0] + 5) and (globals.uxv.pose.position.x > self.target[0] - 5) and globals.rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif globals.uxv.pose.position.x < self.target[0] and globals.rsc.current_speed == 0 :
                globals.rsc.forward_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(0.4)
                print("VIN VIN")
            elif (globals.uxv.pose.position.x < self.target[0] + 2.5) and globals.rsc.gear == -1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")
            elif globals.uxv.pose.position.x < self.target[0] - 5:
                globals.rsc.forward_gear()
                globals.rsc.throttle(0.4)
                globals.rsc.brake(False)
                #print("go go go")
            elif globals.uxv.pose.position.x > self.target[0] and globals.rsc.current_speed == 0 :
                globals.rsc.reverse_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif globals.uxv.pose.position.x > self.target[0] + 2.5 and globals.rsc.gear == -1 :
                globals.rsc.brake(False)
                #rsc.reverse_gear()
                globals.rsc.throttle(-0.4)
                print("gear : " , globals.rsc.gear)
                print("GO BACK")
            elif globals.uxv.pose.position.x > self.target[0] - 5 and globals.rsc.gear == 1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")
            
        elif globals.directions[globals.direction_index] == 'E':
            if (globals.uxv.pose.position.y < (self.target[1] + 5)) and (globals.uxv.pose.position.y > (self.target[1] - 5)) and globals.rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif globals.uxv.pose.position.y < self.target[1] and globals.rsc.current_speed == 0 :
                globals.rsc.forward_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(0.4)
                print("VIN VIN")
            elif (globals.uxv.pose.position.y < self.target[1] + 2.5) and globals.rsc.gear == -1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")
            elif globals.uxv.pose.position.y < self.target[1] - 5:
                globals.rsc.forward_gear()
                globals.rsc.throttle(0.4)
                globals.rsc.brake(False)
                #print("go go go")
            elif globals.uxv.pose.position.y > self.target[1] and globals.rsc.current_speed == 0 :
                globals.rsc.reverse_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif globals.uxv.pose.position.y > self.target[1] + 2.5 and globals.rsc.gear == -1 :
                globals.rsc.brake(False)
                #rsc.reverse_gear()
                globals.rsc.throttle(-0.4)
                print("gear : " , globals.rsc.gear)
                print("GO BACK")
            elif globals.uxv.pose.position.y > self.target[1] - 5 and globals.rsc.gear == 1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")

        elif globals.directions[globals.direction_index] == 'S':
            if (globals.uxv.pose.position.x > self.target[0] - 5 ) and (globals.uxv.pose.position.x < self.target[0] + 5) and globals.rsc.current_speed == 0:
                print("OK")
                self.mission_completed()
                #action
            elif globals.uxv.pose.position.x > self.target[0] and globals.rsc.current_speed == 0 :
                globals.rsc.forward_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(0.4)
                print("VIN VIN")
            elif (globals.uxv.pose.position.x > self.target[0] - 2.5) and globals.gear == -1 :
                globals.throttle(0)
                globals.brake(True)
                print("STOP")
            elif globals.uxv.pose.position.x > self.target[0] + 5:
                globals.rsc.forward_gear()
                globals.rsc.throttle(0.4)
                globals.rsc.brake(False)
                #print("go go go")
            elif globals.uxv.pose.position.x < self.target[0] and globals.rsc.current_speed == 0 :
                globals.rsc.reverse_gear()
                globals.rsc.brake(False)
                globals.rsc.throttle(-1)
                print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
            elif globals.uxv.pose.position.x < self.target[0] - 2.5 and globals.rsc.gear == -1 :
                globals.rsc.brake(False)
                #rsc.reverse_gear()
                globals.rsc.throttle(-0.4)
                print("gear : " , globals.rsc.gear)
                print("GO BACK")
            elif globals.uxv.pose.position.x < self.target[0] + 5 and globals.rsc.gear == 1 :
                globals.rsc.throttle(0)
                globals.rsc.brake(True)
                print("STOP")