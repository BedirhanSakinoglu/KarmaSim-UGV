import globals

class VehicleCommands:

    def adjuster(self):
        #print("W: ", uxv.pose.orientation.w)
        if globals.directions[globals.direction_index] == 'W':
            if globals.uxv.pose.orientation.w < 0.7:
                turn_value = (0.7 - globals.uxv.pose.orientation.w)*4 + 0.05
                globals.rsc.steer(globals.rsc.gear * turn_value) 
            elif globals.uxv.pose.orientation.w > 0.7:
                turn_value = (0.7 - globals.uxv.pose.orientation.w)*8 - 0.05
                globals.rsc.steer(globals.rsc.gear * turn_value)
        elif globals.directions[globals.direction_index] == 'N':
            if globals.uxv.pose.orientation.z < 0:
                #print("right right right")
                turn_value = (1 - globals.uxv.pose.orientation.w)*8 + 0.05
                globals.rsc.steer(globals.rsc.gear * turn_value)
            elif globals.uxv.pose.orientation.z > 0:
                #print("left left left")
                turn_value = (1 - globals.uxv.pose.orientation.w)*8 + 0.05
                globals.rsc.steer(globals.rsc.gear * -turn_value)
        elif globals.directions[globals.direction_index] == 'E':
            if globals.uxv.pose.orientation.w < 0.7:
                turn_value = (0.7 - globals.uxv.pose.orientation.w)*4 + 0.05
                globals.rsc.steer(globals.rsc.gear * -turn_value)
            elif globals.uxv.pose.orientation.w > 0.7:
                turn_value = (0.7 - globals.uxv.pose.orientation.w)*8 - 0.05
                globals.rsc.steer(globals.rsc.gear * -turn_value)
        elif globals.directions[globals.direction_index] == 'S':
            if globals.uxv.pose.orientation.z < 0:
                turn_value = (0 - globals.uxv.pose.orientation.w)*4 - 0.05
                globals.rsc.steer(globals.rsc.gear * turn_value)
            elif globals.uxv.pose.orientation.z > 0:
                turn_value = (0 - globals.uxv.pose.orientation.w)*4 - 0.05
                globals.rsc.steer(globals.rsc.gear * -turn_value)
        
        #rsc.throttle(0.35)

    def turn_right(self):
        if globals.directions[globals.direction_index] == 'W':
            #print("heading West, turn right")
            if globals.uxv.pose.orientation.w < 0.98:
                globals.rsc.steer(3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index += 1
                globals.is_first_move = False
                globals.turning_flag = False

        elif globals.directions[globals.direction_index] == 'N':
            #print("heading North, turn right")
            if globals.uxv.pose.orientation.w > 0.80:
                globals.rsc.steer(3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index += 1
                globals.is_first_move = False
                globals.turning_flag = False

        elif globals.directions[globals.direction_index] == 'E':
            #print("heading East, turn right")
            if globals.uxv.pose.orientation.w > 0.05:
                globals.rsc.steer(3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index += 1
                globals.is_first_move = False
                globals.turning_flag = False

        elif globals.directions[globals.direction_index] == 'S':
            #print("heading South, turn right")
            if globals.uxv.pose.orientation.w < 0.68:
                globals.rsc.steer(3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index += 1
                globals.is_first_move = False
                globals.turning_flag = False

        direction_index= globals.direction_index % 4

    def turn_left(self):
        if globals.directions[globals.direction_index] == 'W':
            #print("heading West, turn left")
            if globals.uxv.pose.orientation.w > 0.05:
                globals.rsc.steer(-3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index -= 1
                globals.is_first_move = False
                globals.turning_flag = False

        elif globals.directions[globals.direction_index] == 'N':
            #print("heading North, turn left")
            if globals.uxv.pose.orientation.w > 0.80:
                globals.rsc.steer(-3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index -= 1
                globals.is_first_move = False
                globals.turning_flag = False

        elif globals.directions[globals.direction_index] == 'E':
            #print("heading East, turn left")
            if globals.uxv.pose.orientation.w < 0.98:
                globals.rsc.steer(-3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index -= 1
                globals.is_first_move = False
                globals.turning_flag = False

        elif globals.directions[globals.direction_index] == 'S':
            #print("heading South, turn left")
            if globals.uxv.pose.orientation.w < 0.7:
                globals.rsc.steer(-3.0)
            else:
                #print("turning complete")
                globals.rsc.steer(0)
                globals.direction_index -= 1
                globals.is_first_move = False
                globals.turning_flag = False

        #-------------------------------------------------
        #print("this is turn left")
        #print("Ori: " , uxv.pose.orientation.w )
        
        #rospy.loginfo("This is the loc of %s  : X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.position.x, uxv.pose.position.y, uxv.pose.position.z)
        #rospy.loginfo("This is the orientation of %s  : W: %f , X : %f , Y : %f , Z : %f", uxv.name, uxv.pose.orientation.w, uxv.pose.orientation.x, uxv.pose.orientation.y, uxv.pose.orientation.z)
        direction_index= globals.direction_index % 4

    def start_move(self):
        #print("vehicle name: %s", uxv_name)

        if globals.uxv.pose.position.y > -22:
            globals.rsc.set_for_start()

        else:
            self.turn_right()

        #print("DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE-DONE")

    def looper(self, timer):
        if globals.uxv == None:
            return

        globals.rsc.looper()
        #if directions[direction_index] == 'S':
            #gtc.set_location(0,26)
        #return

        if globals.is_first_move:
            self.start_move()
        else:
            #print("----")
            globals.gtc.looper()
            globals.gtt.looper()
            globals.gttarget.looper()
            
            #if directions[direction_index] == 'S':
                #gtc.set_location(-5,26)
            #counter = 0
            #print("X : ", uxv.pose.position.x, ", Y : ", uxv.pose.position.y)
            #print(uxv.pose.position.y)
            globals.vehicle_state = None
            for x in globals.turns:
                if abs(x[0]-globals.uxv.pose.position.x) < 5 or globals.turning_flag:
                    if abs(x[1]-globals.uxv.pose.position.y) < 5 or globals.turning_flag:
                        #print("Direction index: ", direction_index , ", Recent index: ", recent_index)
                        if globals.direction_index != globals.recent_index and x == globals.recent_turn:
                            pass
                            #print("hadi")
                        else:
                            globals.vehicle_state
                            globals.turning_flag = True
                            globals.recent_index = globals.direction_index
                            if abs(x[0]-globals.uxv.pose.position.x) < 5 and abs(x[1]-globals.uxv.pose.position.y) < 5:
                                globals.recent_turn = x
                                #print("INDEX: ", turns.index(x))
                            #turn_right()
                            globals.vehicle_state = 'TURN'

                    else:
                        #print("ADJUST")
                        self.adjuster()
                else:
                    #print("ADJUST")
                    self.adjuster()
            
            #print("POI LOCATION : ", globals.poi[globals.target_index].pose.position.x , " ", globals.poi[globals.target_index].pose.position.y)
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