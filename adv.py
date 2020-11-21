from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# My code: 
# Creating stack class
class Stack:
    def __init__(self):
        self.storage = []
    def add(self, value):
        self.storage.append(value)
    def remove(self):
        if len(self.storage) > 0:
            return self.storage.pop()
        else:
            return None
    def size(self):
        return len(self.storage)

# Starting traversal:
def escape_route(direction):
    # save our route back to unvisited exits
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

paths = Stack()
visited = set()
room_map = {}
last_room = []
use_temp_path = False #I need this to know if I should be randomly picking a direction or not. Default is not!

# While loop until all rooms are visited:
while len(visited) < len(world.rooms):
    exits = player.current_room.get_exits() #Returning all potential exits from room
    
    path = []
    temp_path = []

    for exit in exits:
        if player.current_room.name not in room_map: #Adding room to room map if it doesn't exist
            room_map[player.current_room.name] = {'n': '?', 's': '?', 'e': '?', 'w' : '?'}
            for direction in room_map[player.current_room.name]:
                if player.current_room.get_room_in_direction(direction) != None:
                    room_map[player.current_room.name][direction] = player.current_room.get_room_in_direction(direction).id #Adds neighboring room to room map. Still need to delete "None" at end...

        if exit is not None:
            potential_room = player.current_room.get_room_in_direction(exit)
            if potential_room in visited:
                if potential_room is not last_room:
                    explored_room = potential_room
                    for new_exit in explored_room.get_exits():
                        if new_exit is not None and explored_room.get_room_in_direction(new_exit) not in visited: #Basically, "if the already explored room has rooms that are unexplored":
                            temp_path.append(exit) 
                            temp_path.append(new_exit)
                            use_temp_path = True
                            # print("Current Room ", player.current_room.id)
                            # print("moves so far:", traversal_path)
                            # print("moves added: ", temp_path)
                            break #I don't want to add more than one new path to travel down and I only want to surpass loop point
                            
            if potential_room not in visited: 
                path.append(exit) #Adding all unexplored exits to path (up to 4: n,s,e,w)
            

    visited.add(player.current_room)

    if len(path) > 0 and use_temp_path == False:
        move = random.randint(0, len(path) - 1) #Picking random move index
        paths.add(path[move])
        last_room = player.current_room
        player.travel(path[move])
        traversal_path.append(path[move])

    elif use_temp_path == True:
        # print("Moves so far: ", traversal_path)
        # print("using temp path", temp_path)
        for move in temp_path: 
           
            last_room = player.current_room
            player.travel(move)
            print("Moved: ", move)
            print(len(visited))
            traversal_path.append(move)
        use_temp_path = False
        print(paths.storage)
        paths.storage=[temp_path[1]]
        print(paths.storage)


    else:
        print("backtracking!")
        print(paths.storage)
        end = paths.remove()
        print("This is end: ", end)
        if end is None:
            print("Moves so far: ", traversal_path) 
            break
        player.travel(escape_route(end))
        if len(visited) < len(world.rooms): #Putting this in an 'if' keeps from appending unnecessary move at end. 
            traversal_path.append(escape_route(end))
            # print("Moves so far: ", traversal_path)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    print(traversal_path)
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")



######## IF SOMETHING GOES HORRIBLY WRONG REPLACE EVERYTHING WITH THIS: #########
# while len(visited) < len(world.rooms):
#     exits = player.current_room.get_exits() #Returning all potential exits from room
    
#     path = []
#     for exit in exits:
#         if player.current_room.name not in room_map: #Adding room to room map if it doesn't exist
#             room_map[player.current_room.name] = {'n': '?', 's': '?', 'e': '?', 'w' : '?'}
#             for direction in room_map[player.current_room.name]:
#                 if player.current_room.get_room_in_direction(direction) != None:
#                     room_map[player.current_room.name][direction] = player.current_room.get_room_in_direction(direction).id #Adds neighboring room to room map. Still need to delete "None" at end...

#         if exit is not None and player.current_room.get_room_in_direction(exit) not in visited: 
#             print("Room in direction", player.current_room.get_room_in_direction(exit))
#             path.append(exit) #Adding all unexplored exits to path (up to 4: n,s,e,w)

#     visited.add(player.current_room)

#     if len(path) > 0:
#         move = random.randint(0, len(path) - 1) #Picking random move index
#         paths.add(path[move])
#         player.travel(path[move])
#         traversal_path.append(path[move])

#     else:
#         end = paths.remove()
#         player.travel(escape_route(end))
#         if len(visited) < len(world.rooms): #Putting this in an 'if' keeps from appending unnecessary move at end. 
#             traversal_path.append(escape_route(end))

# print(room_map)