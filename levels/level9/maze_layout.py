# levels/level7/maze_layout.py

level_map = [
    "#############################",  # Row 0
    "#     P#S   #     #     #   #",  # Row 1
    "### ####### ### ### ### ### #",  # Row 2
    "#   #     #     #     #     #",  # Row 3
    "# ### ### ##### ### ### ### #",  # Row 4
    "#     #     #     #     #  P#",  # Row 5
    "##### ### ### ### ### ##### #",  # Row 6
    "#     #     # #   #     #   #",  # Row 7
    "### ### ### ### ### ### ### #",  # Row 8
    "#   #     #     #     #     #",  # Row 9
    "### ### ### ###P### ### #####",  # Row10
    "#     #     #     #     #  E#",  # Row11
    "### ### ### ### ### ### #####",  # Row12
    "#   #     #     #     #     #",  # Row13
    "### ### ### ### ### ### ### #",  # Row14
    "# P   #     #     #     #   #",  # Row15
    "### # ### ### ### ### ### ###",  # Row16
    "#  #  #     #     #     #   #",  # Row17
    "###  ## ### ### ### ### ### #",  # Row18
    "#   #    #      #     #     #",  # Row19
    "### ### #  #### ### ### ### #",  # Row20
    "#     #     #     #     #P  #",  # Row21
    "#############################",  # Row22
]

def get_level_map():
    return level_map

# Define portals
portals = {
    (1, 6): (19, 21),    
    (5, 27): (1, 27),     
    (10,15): (11, 23),    
    (15,2): (21, 1),    
    (21,25): (11, 25),     
}

def get_portals():
    return portals

# Define moving walls
moving_walls = [
    {"position": [5, 5], "direction": [0, 1], "slowness": 5, "counter": 0},
    {"position": [25, 19], "direction": [1, 0], "slowness": 7, "counter": 0},
    {"position": [23, 11], "direction": [0, 1], "slowness": 6, "counter": 0},
    {"position": [9, 11], "direction": [1, 0], "slowness": 4, "counter": 0},
]

def get_moving_walls():
    return moving_walls

def update_moving_walls(maze):
    for wall in moving_walls:
        # Increment the wall's counter
        wall["counter"] += 1

        # Check if it's time to move the wall
        if wall["counter"] >= wall["slowness"]:
            wall["counter"] = 0  # Reset the counter

            # Calculate new position
            x, y = wall["position"]
            dx, dy = wall["direction"]
            new_x, new_y = x + dx, y + dy

            # Check boundaries and reverse direction if needed
            if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] == " ":
                wall["position"] = [new_x, new_y]
            else:
                # Reverse direction
                wall["direction"] = [-dx, -dy]
