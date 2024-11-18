# levels/level10.py
level_map = [
    "###########",
    "#S   #   G#",
    "# ### # ###",
    "#     #   #",
    "##### # # #",
    "#     #   #",
    "### ##### #",
    "#       E#",
    "###########",
]

gates = {
    (1, 8): 'puzzle1',  # Position and puzzle identifier
}

def load_level():
    return level_map, gates
