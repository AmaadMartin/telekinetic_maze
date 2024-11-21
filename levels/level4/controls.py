# levels/level1/controls.py

from utils.HandInput import HandInput

def get_actions(hand_input):
    movement_direction = hand_input.get_finger_direction('Right', 'Thumb')

    return {'movement_direction': movement_direction}

def index_pinched(hand_input):
    actions = hand_input.get_actions()
    right_actions = actions.get('Right', {})
    return right_actions.get('Index', False)
