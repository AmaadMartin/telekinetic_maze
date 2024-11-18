# levels/level7.py
level_map = [
    "##########",
    "#S  P#   #",
    "# ## # # #",
    "#    # # #",
    "#### # # #",
    "#      # #",
    "# #P#### #",
    "#        #",
    "########E#",
    "##########",
]

portals = {
    (1, 4): (6, 2),
    (6, 2): (1, 4),
}

def load_level():
    return level_map, portals
