import globals
from vehicle_commands import VehicleCommands

class GoToTurn:
    turn_index = None
    target_direction = None
    flag = False
    #target_corner = None

    def set_target_corner(self, turn_index, target_direction):
        self.turn_index = turn_index
        self.target_direction = target_direction
        globals.gtc.set_location(globals.turns[self.turn_index][0], globals.turns[self.turn_index][1])

    def looper(self):
        if self.turn_index == None:
            return            
        if globals.vehicle_state == 'TURN':
            if self.target_direction == 'RIGHT':
                print("heeyo")
                globals.vcoms.turn_right()
                self.flag = True
            elif self.target_direction == 'LEFT':
                print("aaaayo")
                globals.vcoms.turn_left()
                self.flag = True
        elif self.flag:
            self.target_direction = None
            self.turn_index = None
            self.flag = False
            globals.gtc.mission_completed()
            print("Mission failed succesfully")
