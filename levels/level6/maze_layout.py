level_map = [
    "###############",
    "#S    #    # E#",
    "### ### #######",
    "#   #P  #     #",
    "### ### # ### #",
    "#     # #   # #",
    "### ### ### ###",
    "#   #     #   #",
    "# ### ### ### #",
    "#P    #       #",
    "###############",
]

# Define portals
portals = {
    (9,1): (3,13),  
    (3,5): (1,12),  
}

def get_level_map():
    return level_map

def get_portals():
    return portals
