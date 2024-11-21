# levels/level4/maze_layout.py

level_map = [
    "###############",
    "#S     #     P#",
    "## ### # ### ##",
    "#    #   #   ##",
    "### # ### ### #",
    "#   #     #   #",
    "# ### ## #### #",
    "#     # #    ##",
    "#######   ##  #",
    "#       ##  E##",
    "###############",
]

# Define portals
portals = {
    (1, 13): (9, 1),  # From position (row 1, column 13) to (row 9, column 1)
}

def get_level_map():
    return level_map

def get_portals():
    return portals
