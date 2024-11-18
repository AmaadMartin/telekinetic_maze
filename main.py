# main.py

import pygame
import sys
import time
import importlib
from utils.HandInput import HandInput
from utils.game_utils import (
    load_maze, draw_maze, get_start_position, is_move_valid,
    is_exit, is_portal, get_portal_destination,
    is_gate, solve_puzzle, update_visibility,
    draw_maze_with_visibility, update_moving_walls,
    is_moving_wall, get_stairs_destination,
    get_object_at_position, move_object, interact_with_object,
    apply_gravity, attack_enemy, is_enemy,
)
# Add any other necessary imports

# Constants
TILE_SIZE = 40

# Colors (defined in game_utils.py)

# List of levels
levels = [
    'level1',
    'level2',
    'level3',
    'level4',
    'level5',
    'level6',
    'level7',
    'level8',
    'level9',
    'level10',
]

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Initialize HandInput
hand_input = HandInput()

def main():
    current_level_index = 0

    while current_level_index < len(levels):
        level_name = levels[current_level_index]
        level_module = importlib.import_module(f'levels.{level_name}')
        level_data = level_module.load_level()

        # Initialize variables for special mechanics
        timer_seconds = None
        portals = {}
        moving_walls = []
        visibility_radius = None
        gates = {}
        floors = {}
        current_floor = 1

        # Handle level data
        if isinstance(level_data, dict):
            # Multi-floor level (Level 3)
            floors = level_data
            maze = load_maze(floors[current_floor])
        elif isinstance(level_data, tuple):
            # Level data with special mechanics
            level_map = level_data[0]
            maze = load_maze(level_map)
            for item in level_data[1:]:
                if isinstance(item, int):
                    timer_seconds = item
                elif isinstance(item, dict):
                    if hasattr(level_module, 'portals'):
                        portals = level_module.portals
                    elif hasattr(level_module, 'moving_walls'):
                        moving_walls = level_module.moving_walls
                    elif hasattr(level_module, 'gates'):
                        gates = level_module.gates
        else:
            # Standard level data
            level_map = level_data
            maze = load_maze(level_map)

        # Additional level-specific mechanics
        if hasattr(level_module, 'timer_seconds'):
            timer_seconds = level_module.timer_seconds
        if hasattr(level_module, 'portals'):
            portals = level_module.portals
        if hasattr(level_module, 'moving_walls'):
            moving_walls = level_module.moving_walls
        if hasattr(level_module, 'visibility_radius'):
            visibility_radius = level_module.visibility_radius
        if hasattr(level_module, 'gates'):
            gates = level_module.gates

        # Get player start position
        player_pos = list(get_start_position(maze))
        level_complete = False

        # Calculate screen size based on maze size
        maze_height = len(maze)
        maze_width = len(maze[0])
        screen_size = (maze_width * TILE_SIZE, maze_height * TILE_SIZE)
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(f"Maze Game - Level {current_level_index + 1}")

        # Initialize timer
        if timer_seconds:
            start_time = time.time()

        # For moving walls, initialize time
        if moving_walls:
            moving_walls_start_time = time.time()

        # Variables for movement direction
        movement_direction = None

        # Game loop for the level
        while not level_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    hand_input.release()
                    pygame.quit()
                    sys.exit()

            # Get actions from hand input
            actions = hand_input.get_actions()
            right_actions = actions.get('Right', {})
            left_actions = actions.get('Left', {})
            # print(actions)
            # print(hand_input.prev_positions)

            # Handle right hand actions
            if right_actions:
                # Movement
                if 'Index' in right_actions:
                    # Determine movement direction based on hand movement
                    movement_direction = hand_input.get_movement_direction('Right')
                    if movement_direction:
                        dx, dy = movement_direction
                        new_pos = (player_pos[0] + dx, player_pos[1] + dy)
                        if is_move_valid(maze, new_pos):
                            player_pos = list(new_pos)
                            # Apply gravity if needed
                            # player_pos = apply_gravity(maze, player_pos)
                # Jumping
                elif 'Middle' in right_actions:
                    # Jump over one tile in the movement direction
                    if movement_direction:
                        dx, dy = movement_direction
                        new_pos = (player_pos[0] + 2 * dx, player_pos[1] + 2 * dy)
                        if is_move_valid(maze, new_pos):
                            player_pos = list(new_pos)
                            print("Jumped!")
                            # Apply gravity if needed
                            # player_pos = apply_gravity(maze, player_pos)
                # Shooting
                elif 'Ring' in right_actions:
                    # Implement shooting logic
                    if movement_direction:
                        dx, dy = movement_direction
                        projectile_pos = [player_pos[0] + dx, player_pos[1] + dy]
                        while is_move_valid(maze, projectile_pos):
                            if is_enemy(maze, projectile_pos):
                                attack_enemy(maze, projectile_pos)
                                break
                            projectile_pos[0] += dx
                            projectile_pos[1] += dy
                        print("Shot fired!")
                # Dashing
                elif 'Pinky' in right_actions:
                    # Dash three tiles in the movement direction
                    if movement_direction:
                        dx, dy = movement_direction
                        for step in range(1, 4):
                            new_pos = (player_pos[0] + dx * step, player_pos[1] + dy * step)
                            if is_move_valid(maze, new_pos):
                                player_pos = list(new_pos)
                            else:
                                break
                        print("Dashed!")
            # Handle left hand actions
            elif left_actions:
                if 'Index' in left_actions:
                    # Grabbing or interacting with objects
                    obj = get_object_at_position(maze, player_pos)
                    if obj:
                        interact_with_object(obj, maze, player_pos)
                        print(f"Interacted with {obj['type']}")
            else:
                hand_input.prev_positions['Right'] = None
                hand_input.prev_positions['Left'] = None

            # Check for exit
            if is_exit(maze, player_pos):
                level_complete = True
                print(f"Level {current_level_index + 1} Complete!")
                break

            # Update moving walls
            if moving_walls:
                time_elapsed = time.time() - moving_walls_start_time
                update_moving_walls(maze, moving_walls, time_elapsed)

            # Update timer
            if timer_seconds:
                elapsed_time = time.time() - start_time
                remaining_time = timer_seconds - elapsed_time
                if remaining_time <= 0:
                    print("Time's up! Game Over.")
                    hand_input.release()
                    pygame.quit()
                    sys.exit()

            # Clear screen
            screen.fill((0, 0, 0))

            # Draw maze and player
            if visibility_radius is not None:
                draw_maze_with_visibility(screen, maze, player_pos, visibility_radius)
            else:
                draw_maze(screen, maze, player_pos)

            # Display remaining time
            if timer_seconds:
                font = pygame.font.Font(None, 36)
                timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (255, 0, 0))
                screen.blit(timer_text, (10, 10))

            # Update display
            pygame.display.flip()
            clock.tick(30)  # Limit to 30 FPS

        # Level complete, move to next level
        current_level_index += 1

    print("Congratulations! You have completed all levels.")
    hand_input.release()
    pygame.quit()

if __name__ == '__main__':
    main()
