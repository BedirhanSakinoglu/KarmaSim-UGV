import globals
import math

class GoToTarget:

    def looper(self):
        min_distance = 100000
        for a in globals.turns:
            distance = math.sqrt(math.pow(globals.uxv.pose.position.x - a[0], 2) + math.pow(globals.uxv.pose.position.y - a[1], 2))
            if distance < min_distance:
                min_distance = distance
                index_of_closest_turn = globals.turns.index(a)

        for b in globals.turns[index_of_closest_turn][3]:
            if globals.directions[globals.direction_index] == 'N' or globals.directions[globals.direction_index] == 'S':
                if ((globals.uxv.pose.position.x <= globals.turns[index_of_closest_turn][0]) and (globals.uxv.pose.position.x) >= globals.turns[b][0]) or ((globals.uxv.pose.position.x >= globals.turns[index_of_closest_turn][0]) and (globals.uxv.pose.position.x <= globals.turns[b][0])):
                    print('Car is between turns ', globals.turns[index_of_closest_turn][4], ' and ', globals.turns[b][4])
            if globals.directions[globals.direction_index] == 'W' or globals.directions[globals.direction_index] == 'E':
                if ((globals.uxv.pose.position.y <= globals.turns[index_of_closest_turn][1]) and (globals.uxv.pose.position.y >= globals.turns[b][1])) or ((globals.uxv.pose.position.y >= globals.turns[index_of_closest_turn][1]) and (globals.uxv.pose.position.y <= globals.turns[b][1])):
                    print('Car is between turns ', globals.turns[index_of_closest_turn][4], ' and ', globals.turns[b][4])

        agent = globals.uxv
        poi = globals.poi
        vertices = [agent, poi, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        edges = []
        graph = [vertices, edges]
