# levels/level1/maze_layout.py

level_map = [
    "##########",
    "#S   #   P",
    "# #### # #",
    "#      # #",
    "###### # #",
    "#      # #",
    "# ###### #",
    "#   #    #",
    "### # ##E#",
    "##########",
]

def get_level_map():
    return level_map

portals = {
    (1,9): (8,3),
}

def get_portals():
    return portals