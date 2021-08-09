import globals
import math
import sys
import dijkstra

class GoToTarget:

    def looper(self):

        index_of_closest_turn = None
        min_distance = 100000
        distance = 100000
        for a in globals.turns:
            if globals.directions[globals.direction_index] == 'W' or globals.directions[globals.direction_index] == 'E':
                if abs(a[0] - globals.uxv.pose.position.x) < 5:
                    distance = abs(globals.uxv.pose.position.y - a[1])
            if globals.directions[globals.direction_index] == 'N' or globals.directions[globals.direction_index] == 'S':
                if abs(a[1] - globals.uxv.pose.position.y) < 5:
                    distance = abs(globals.uxv.pose.position.x - a[0])
            
            if distance < min_distance:
                min_distance = distance
                index_of_closest_turn = globals.turns.index(a)

        if index_of_closest_turn == None:
            return

        agent_flag = False
        if globals.vehicle_state != 'TURN':
            for b in globals.turns[index_of_closest_turn][3]:
                if globals.directions[globals.direction_index] == 'N' or globals.directions[globals.direction_index] == 'S':
                    if ((globals.uxv.pose.position.x <= globals.turns[index_of_closest_turn][0]) and (globals.uxv.pose.position.x) >= globals.turns[b][0]) or ((globals.uxv.pose.position.x >= globals.turns[index_of_closest_turn][0]) and (globals.uxv.pose.position.x <= globals.turns[b][0])):
                        #print('Car is between turns ', globals.turns[index_of_closest_turn][4], ' and ', globals.turns[b][4])
                        agent_turn1 = globals.turns[index_of_closest_turn]
                        agent_turn2 = globals.turns[b]
                        agent_flag = True
                if globals.directions[globals.direction_index] == 'W' or globals.directions[globals.direction_index] == 'E':
                    if ((globals.uxv.pose.position.y <= globals.turns[index_of_closest_turn][1]) and (globals.uxv.pose.position.y >= globals.turns[b][1])) or ((globals.uxv.pose.position.y >= globals.turns[index_of_closest_turn][1]) and (globals.uxv.pose.position.y <= globals.turns[b][1])):
                        #print('Car is between turns ', globals.turns[index_of_closest_turn][4], ' and ', globals.turns[b][4])
                        agent_turn1 = globals.turns[index_of_closest_turn]
                        agent_turn2 = globals.turns[b]
                        agent_flag = True

        globals.vertices = [15, 16, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        # H -> Horizontal
        # V -> Vertical
        globals.edges = [
            (0,1,50,'H'),
            (1,0,50,'H'),
            (0,3,60,'V'),
            (3,0,60,'V'),
            (1,4,60,'V'),
            (4,1,60,'V'),
            (3,4,50,'H'),
            (4,3,50,'H'),
            (1,2,170,'H'),
            (2,1,170,'H'),
            (2,7,60,'V'),
            (7,2,60,'V'),
            (4,5,70,'H'),
            (5,4,70,'H'),
            (5,6,50,'H'),
            (6,5,50,'H'),
            (6,7,50,'H'),
            (7,6,50,'H'),
            (3,12,155,'V'),
            (12,3,155,'V'),
            (5,8,50,'V'),
            (8,5,50,'V'),
            (6,9,50,'V'),
            (9,6,50,'V'),
            (8,9,50,'H'),
            (9,8,50,'H'),
            (7,11,100,'V'),
            (11,7,100,'V'),
            (8,10,50,'V'),
            (10,8,50,'V'),
            (10,11,100,'H'),
            (11,10,100,'H'),
            (10,13,50,'V'),
            (13,10,50,'V'),
            (11,14,50,'V'),
            (14,11,50,'V'),
            (13,14,100,'H'),
            (14,13,100,'H'),
            (12,13,120,'H'),
            (13,12,120,'H')
        ]

        #poi finder algorithm
        for edge in globals.edges:
            if edge[3] == 'H':
                if abs( globals.turns[edge[0]][0] - globals.poi[globals.target_index].pose.position.x ) < 5:
                    if( globals.turns[edge[0]][1] < globals.poi[globals.target_index].pose.position.y and globals.turns[edge[1]][1] > globals.poi[globals.target_index].pose.position.y ) or ( globals.turns[edge[0]][1] > globals.poi[globals.target_index].pose.position.y and globals.turns[edge[1]][1] < globals.poi[globals.target_index].pose.position.y):
                        #print("poi is between ", edge[0] , " - " , edge[1])
                        poi_distance1 = math.sqrt(math.pow(globals.poi[globals.target_index].pose.position.x - globals.turns[edge[0]][0], 2) + math.pow(globals.poi[globals.target_index].pose.position.y - globals.turns[edge[0]][1], 2))
                        poi_distance2 = math.sqrt(math.pow(globals.poi[globals.target_index].pose.position.x - globals.turns[edge[1]][0], 2) + math.pow(globals.poi[globals.target_index].pose.position.y - globals.turns[edge[1]][1], 2))

                        globals.edges.append( (16, edge[0], poi_distance1, '') )
                        globals.edges.append( (edge[0], 16, poi_distance1, '') )
                        globals.edges.append( (16, edge[1], poi_distance2, '') )
                        globals.edges.append( (edge[1], 16, poi_distance2, '') )

                        globals.edges.remove(edge)

            elif edge[3] == 'V':
                if abs( globals.turns[edge[0]][1] - globals.poi[globals.target_index].pose.position.y ) < 5:
                    if( globals.turns[edge[0]][0] < globals.poi[globals.target_index].pose.position.x and globals.turns[edge[1]][0] > globals.poi[globals.target_index].pose.position.x ) or ( globals.turns[edge[0]][0] > globals.poi[globals.target_index].pose.position.x and globals.turns[edge[1]][0] < globals.poi[globals.target_index].pose.position.x):
                        #print("poi is between ", edge[0] , " - " , edge[1])
                        poi_distance1 = math.sqrt(math.pow(globals.poi[globals.target_index].pose.position.x - globals.turns[edge[0]][0], 2) + math.pow(globals.poi[globals.target_index].pose.position.y - globals.turns[edge[0]][1], 2))
                        poi_distance2 = math.sqrt(math.pow(globals.poi[globals.target_index].pose.position.x - globals.turns[edge[1]][0], 2) + math.pow(globals.poi[globals.target_index].pose.position.y - globals.turns[edge[1]][1], 2))

                        globals.edges.append( (16, edge[0], poi_distance1, '') )
                        globals.edges.append( (edge[0], 16, poi_distance1, '') )
                        globals.edges.append( (16, edge[1], poi_distance2, '') )
                        globals.edges.append( (edge[1], 16, poi_distance2, '') )

                        globals.edges.remove(edge)
                        
        if agent_flag:
            for item in globals.edges:
                if (item[0] == agent_turn1[4] and item[1] == agent_turn2[4]) or (item[0] == agent_turn2[4] and item[1] == agent_turn1[4]):
                    globals.edges.remove(item)
            
            agent_distance1 = math.sqrt(math.pow(globals.uxv.pose.position.x - agent_turn1[0], 2) + math.pow(globals.uxv.pose.position.y - agent_turn1[1], 2))
            agent_distance2 = math.sqrt(math.pow(globals.uxv.pose.position.x - agent_turn2[0], 2) + math.pow(globals.uxv.pose.position.y - agent_turn2[1], 2))


            heading_vertice = -1

            if globals.directions[globals.direction_index] == "W":
                if agent_turn1[4] < agent_turn2[4]:
                    heading_vertice = 1
                elif agent_turn1[4] > agent_turn2[4]:
                    heading_vertice = 2
            elif globals.directions[globals.direction_index] == "N":
                if agent_turn1[4] < agent_turn2[4]:
                    heading_vertice = 1
                elif agent_turn1[4] > agent_turn2[4]:
                    heading_vertice = 2
            elif globals.directions[globals.direction_index] == "E":
                if agent_turn1[4] < agent_turn2[4]:
                    heading_vertice = 2
                elif agent_turn1[4] > agent_turn2[4]:
                    heading_vertice = 1
            elif globals.directions[globals.direction_index] == "S":
                if agent_turn1[4] < agent_turn2[4]:
                    heading_vertice = 2
                elif agent_turn1[4] > agent_turn2[4]:
                    heading_vertice = 1

            if heading_vertice == 1:
                curr = globals.vertices[agent_turn1[4]]
                globals.edges.append( (15, agent_turn1[4], agent_distance1, '') )
            elif heading_vertice == 2:
                curr = globals.vertices[agent_turn2[4]]
                globals.edges.append( (15, agent_turn2[4], agent_distance2, '') )
        
        #if poi_flag:
        #    for item in edges:
        #        if (item[0] == poi_turn1[4] and item[1] == poi_turn2[4]) or (item[0] == poi_turn2[4] and item[1] == poi_turn1[4]):
        #            edges.remove(item)
        #    
        #    poi_distance1 = math.sqrt(math.pow(globals.uxv.pose.position.x - poi_turn1[0], 2) + math.pow(globals.uxv.pose.position.y - poi_turn1[1], 2))
        #    poi_distance2 = math.sqrt(math.pow(globals.uxv.pose.position.x - poi_turn2[0], 2) + math.pow(globals.uxv.pose.position.y - poi_turn2[1], 2))
        #
        #    edges.append( (poi, poi_turn1, poi_distance1) )
        #    edges.append( (poi, poi_turn2, poi_distance2) )

        #print("hey")
        #print(globals.edges)
        #print(globals.edges)
        dsp = dijkstra.Graph(17)
        dsp.looper()
        
        #---------------------------------------------------------------------------------
        print('-----------------------------------------------')
        #print('is_turn: ', globals.is_turn)
        #print('vehicle_state: ', globals.vehicle_state)

        if globals.is_turn and globals.vehicle_state != 'TURN':

            route = globals.path

            print(route)
            print(globals.curr_turn)

            if len(route) == 1:
                return

            flag = False
            direction = None
            #yeniden shortest path bulmasin
            if len(route) > 2:

                if(route[2] == 16):
                    direction = globals.directions[globals.direction_index]
                    globals.is_turn = False
                    print('its also false ')
                    globals.gtc.set_location( globals.poi[globals.target_index].pose.position.x , globals.poi[globals.target_index].pose.position.y )
                    return

                else:
                    for road in dijkstra.roads:
                        flag = False
                        for spot in road:
                            if(spot == route[1]):
                                flag = True
                        for spot in road:
                            if(spot == route[2] and flag):
                                if(globals.directions[globals.direction_index] == 'N' or globals.directions[globals.direction_index] == 'S'):
                                    if(road[0] == 'V'):
                                        direction = globals.directions[globals.direction_index]
                                        globals.is_turn = False
                                        print('its false uf')
                                elif(globals.directions[globals.direction_index] == 'W' or globals.directions[globals.direction_index] == 'E'):
                                    if(road[0] == 'H'):
                                        direction = globals.directions[globals.direction_index]
                                        globals.is_turn = False
                                        print('its false b')

            if direction == None:
                print("here")
                if len(globals.path) > 1:
                    if globals.curr_turn != None:
                        if globals.path[1] != globals.curr_turn:
                            globals.is_turn = False
                            print("donme")
                            return 
                globals.is_turn = True
                if globals.directions[globals.direction_index] == 'W':
                    if route[1] < route[2]:
                        direction = 'LEFT'
                    elif route[1] > route[2]:
                        direction = 'RIGHT'
                if globals.directions[globals.direction_index] == 'N':
                    if route[1] < route[2]:
                        direction = 'RIGHT'
                    elif route[1] > route[2]:
                        direction = 'LEFT'
                if globals.directions[globals.direction_index] == 'E':
                    if route[1] < route[2]:
                        direction = 'RIGHT'
                    elif route[1] > route[2]:
                        direction = 'LEFT'
                if globals.directions[globals.direction_index] == 'S':
                    if route[1] < route[2]:
                        direction = 'LEFT'
                    elif route[1] > route[2]:
                        direction = 'RIGHT'

            if(len(route) > 2):
                globals.gtt.set_target_corner( route[1] , direction )
                #print("****")
                #print(globals.directions[globals.direction_index])
                #print(direction)
            if(len(route) == 2):
                globals.gtc.set_location( globals.poi[globals.target_index].pose.position.x , globals.poi[globals.target_index].pose.position.y )

        #---------------------------------------------------------------------------------


        #print(edges)
        #print(graph)