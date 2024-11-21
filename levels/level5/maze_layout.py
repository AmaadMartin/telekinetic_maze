level_map = [
    "###############",
    "#S   #   #   E#",
    "### ### ### ###",
    "#     #     # #",
    "### ### ### # #",
    "#   ##  #   # #",
    "### # ### ### #",
    "#     #     # #",
    "### ### ### ###",
    "#     P       #",
    "###############",
]

# Define portal
portals = {
    (9,6): (1,6),  # From position (row 9, column 6) to (row 1, column 6)
}

def get_level_map():
    return level_map

def get_portals():
    return portals
