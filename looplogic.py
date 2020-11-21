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