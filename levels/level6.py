# levels/level6.py
level_map = [
    "##########",
    "#S   #   #",
    "# ## M # #",
    "#    # # #",
    "#### # # #",
    "#   M  # #",
    "# ###### #",
    "#   M    #",
    "########E#",
    "##########",
]

moving_walls = [
    {'position': (2, 6), 'interval': 5},  # Moves every 5 seconds
    {'position': (5, 5), 'interval': 3},
    {'position': (7, 5), 'interval': 4},
]

def load_level():
    return level_map, moving_walls
