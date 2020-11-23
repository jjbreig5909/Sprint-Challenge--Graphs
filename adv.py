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

# paths = Stack()
# visited = set()
room_map = {}
last_room = []


# While loop until all rooms are visited:
def find_all_rooms(traversal_path, visited, paths):
    while len(visited) < len(world.rooms):

        exits = player.current_room.get_exits() #Returning all potential exits from room
        path = []

        for exit in exits:
            if player.current_room.name not in room_map: #Adding room to room map if it doesn't exist
                room_map[player.current_room.name] = {'n': '?', 's': '?', 'e': '?', 'w' : '?'}
                for direction in room_map[player.current_room.name]:
                    if player.current_room.get_room_in_direction(direction) != None:
                        room_map[player.current_room.name][direction] = player.current_room.get_room_in_direction(direction).id #Adds neighboring room to room map. Still need to delete "None" at end...

            if exit is not None and player.current_room.get_room_in_direction(exit) not in visited: 
                path.append(exit) #Adding all unexplored exits to path (up to 4: n,s,e,w)

        visited.add(player.current_room)

        if len(path) > 0:
            move = random.choice(path) #Picking random move index
            player.travel(move)
            paths.add(move)
            traversal_path.append(move)

        else:
            end = paths.remove()
            player.travel(escape_route(end))
            if len(visited) < len(world.rooms): #Putting this in an 'if' keeps from appending unnecessary move at end. 
                traversal_path.append(escape_route(end))
    return traversal_path

#Estab;ish variables to keep searching
keep_searching = True
final_path = []
lowest_moves = 1000

while keep_searching:
    temp_traversal_path = []
    visited = set()
    paths = Stack()
    player = Player(world.starting_room)
    temp_traversal_path = find_all_rooms(temp_traversal_path, visited, paths)
    if len(temp_traversal_path) < lowest_moves:
        lowest_moves = len(temp_traversal_path)
        print("New lowest moves found: ", lowest_moves)
        user_choice = input("Continue? ")
        if user_choice == "n" or user_choice == "q":
            keep_searching = False
            final_path = temp_traversal_path
    if lowest_moves < 960:
        final_path = temp_traversal_path
        keep_searching = False

traversal_path = final_path


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

