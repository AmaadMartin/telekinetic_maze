# levels/level8.py
level_map = [
    "##########",
    "#S       #",
    "## #######",
    "#        #",
    "####### ##",
    "#        #",
    "####### ##",
    "#        #",
    "########E#",
    "##########",
]

visibility_radius = 2  # Tiles

def load_level():
    return level_map, visibility_radius
