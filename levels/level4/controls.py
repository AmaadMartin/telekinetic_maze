# levels/level4/controls.py

from utils.HandInput import HandInput

def get_actions(hand_input):
    actions = hand_input.get_actions()
    right_actions = actions.get('Right', {})
    movement_direction = None

    if right_actions:
        if 'Index' in right_actions:
            # Move player based on hand movement
            movement_direction = hand_input.get_movement_direction('Right')
        # Add more control logic as needed

    return {'movement_direction': movement_direction}

def index_pinched(hand_input):
    actions = hand_input.get_actions()
    right_actions = actions.get('Right', {})
    return right_actions.get('Index', False)
