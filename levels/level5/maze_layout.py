level_map = [
    "#############",
    "#    S#  E  #",
    "### ### #####",
    "#     #     #",
    "# ### # ### #",
    "# #   #   # #",
    "# ### ### # #",
    "#           #",
    "#############",
]

# Define portals (removed)
portals = {}

moving_walls = [
    {"position": [5, 3], "direction": [-1, 0], "slowness": 5, "counter": 0},  # Moves horizontally
    {"position": [7, 5], "direction": [0, 1], "slowness": 10, "counter": 0},  # Moves vertically
]

def get_level_map():
    return level_map

def get_portals():
    return portals

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

def get_moving_walls():
    return moving_walls
