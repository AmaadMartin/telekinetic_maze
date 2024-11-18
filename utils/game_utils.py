# utils/game_utils.py

import pygame
import numpy as np

# Tile size in pixels
TILE_SIZE = 40

# Colors
COLOR_WALL = (0, 0, 0)        # Black
COLOR_PATH = (255, 255, 255)  # White
COLOR_PLAYER = (0, 0, 255)    # Blue
COLOR_EXIT = (0, 255, 0)      # Green
COLOR_START = (255, 255, 0)   # Yellow
COLOR_GATE = (255, 0, 0)      # Red
COLOR_PORTAL = (255, 0, 255)  # Magenta
COLOR_STAIR_UP = (128, 128, 128)  # Gray
COLOR_STAIR_DOWN = (64, 64, 64)   # Dark Gray
COLOR_BOMB = (255, 128, 0)    # Orange
COLOR_BALL = (0, 255, 255)    # Cyan
# Add more colors for different objects as needed

def load_maze(level_map):
    """
    Converts the level map into a 2D list representing the maze.
    """
    maze = []
    for row in level_map:
        maze.append(list(row))
    return maze

def draw_maze(screen, maze, player_pos):
    """
    Draws the maze, objects, and the player on the screen.
    """
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == '#':
                pygame.draw.rect(screen, COLOR_WALL, rect)
            elif tile == ' ':
                pygame.draw.rect(screen, COLOR_PATH, rect)
            elif tile == 'S':
                pygame.draw.rect(screen, COLOR_START, rect)
            elif tile == 'E':
                pygame.draw.rect(screen, COLOR_EXIT, rect)
            elif tile == 'G':
                pygame.draw.rect(screen, COLOR_GATE, rect)
            elif tile == 'P':
                pygame.draw.rect(screen, COLOR_PORTAL, rect)
            elif tile == '^':
                pygame.draw.rect(screen, COLOR_STAIR_UP, rect)
            elif tile == 'v':
                pygame.draw.rect(screen, COLOR_STAIR_DOWN, rect)
            elif tile == 'B':
                pygame.draw.rect(screen, COLOR_BOMB, rect)
            elif tile == 'O':
                pygame.draw.rect(screen, COLOR_BALL, rect)
            # Add more object types as needed
            else:
                pygame.draw.rect(screen, COLOR_PATH, rect)
    # Draw the player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLOR_PLAYER, player_rect)

def get_start_position(maze):
    """
    Finds the starting position (marked with 'S') in the maze.
    """
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 'S':
                return (x, y)
    return (0, 0)  # Default start position if 'S' not found

def is_move_valid(maze, pos):
    """
    Checks if the player's move is valid (not a wall and within maze bounds).
    """
    x, y = pos
    if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
        return maze[y][x] != '#'
    return False

def is_exit(maze, pos):
    """
    Checks if the player has reached the exit tile ('E').
    """
    x, y = pos
    return maze[y][x] == 'E'

def is_portal(maze, pos, portals):
    """
    Checks if the current position is a portal.
    """
    x, y = pos
    return (y, x) in portals

def get_portal_destination(portals, pos):
    """
    Returns the destination position of a portal.
    """
    x, y = pos
    current = (y, x)
    destination = portals[current]
    return [destination[1], destination[0]]  # Return as [x, y]

def is_gate(maze, pos, gates):
    """
    Checks if the current position is a gate that requires solving a puzzle.
    """
    x, y = pos
    return (y, x) in gates

def solve_puzzle(gate_id):
    """
    Simulates solving a puzzle associated with a gate.
    """
    print(f"Attempting to solve puzzle: {gate_id}")
    # For simplicity, we'll assume the puzzle is always solved successfully.
    # You can implement actual puzzle logic here.
    return True

def update_visibility(maze, player_pos, visibility_radius):
    """
    Updates the list of visible tiles based on the player's position and visibility radius.
    """
    visible_tiles = []
    x0, y0 = player_pos
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            distance = abs(x - x0) + abs(y - y0)
            if distance <= visibility_radius:
                visible_tiles.append((x, y))
    return visible_tiles

def draw_maze_with_visibility(screen, maze, player_pos, visibility_radius):
    """
    Draws the maze with limited visibility around the player.
    """
    visible_tiles = update_visibility(maze, player_pos, visibility_radius)
    visible_set = set(visible_tiles)
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if (x, y) in visible_set:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == '#':
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                elif tile == ' ':
                    pygame.draw.rect(screen, COLOR_PATH, rect)
                elif tile == 'S':
                    pygame.draw.rect(screen, COLOR_START, rect)
                elif tile == 'E':
                    pygame.draw.rect(screen, COLOR_EXIT, rect)
                elif tile == 'G':
                    pygame.draw.rect(screen, COLOR_GATE, rect)
                elif tile == 'P':
                    pygame.draw.rect(screen, COLOR_PORTAL, rect)
                elif tile == '^':
                    pygame.draw.rect(screen, COLOR_STAIR_UP, rect)
                elif tile == 'v':
                    pygame.draw.rect(screen, COLOR_STAIR_DOWN, rect)
                elif tile == 'B':
                    pygame.draw.rect(screen, COLOR_BOMB, rect)
                elif tile == 'O':
                    pygame.draw.rect(screen, COLOR_BALL, rect)
                # Add more object types as needed
                else:
                    pygame.draw.rect(screen, COLOR_PATH, rect)
    # Draw the player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLOR_PLAYER, player_rect)

def update_moving_walls(maze, moving_walls, time_elapsed):
    """
    Updates the state of moving walls based on the elapsed time.
    """
    for wall in moving_walls:
        interval = wall['interval']
        position = wall['position']  # (row, column)
        x, y = position[1], position[0]
        # Calculate if wall should be open or closed based on time_elapsed
        phase = int((time_elapsed % (2 * interval)) / interval)
        if phase == 0:
            maze[y][x] = '#'  # Wall is closed
        else:
            maze[y][x] = ' '  # Wall is open

def is_moving_wall(maze, pos):
    """
    Checks if the tile at the position is a moving wall.
    """
    x, y = pos
    return maze[y][x] == 'M'

def get_stairs_destination(maze, pos, current_floor, floors):
    """
    Determines the destination floor and position when using stairs.
    """
    x, y = pos
    tile = maze[y][x]
    if tile == '^':
        # Stairs up
        next_floor = current_floor + 1
    elif tile == 'v':
        # Stairs down
        next_floor = current_floor - 1
    else:
        return None, None, current_floor  # Not on stairs
    if next_floor in floors:
        new_maze = load_maze(floors[next_floor])
        new_pos = get_start_position(new_maze)
        return new_maze, new_pos, next_floor
    else:
        return None, None, current_floor  # No such floor

def get_object_at_position(maze, pos):
    """
    Returns the object at the given position, if any.
    """
    x, y = pos
    tile = maze[y][x]
    if tile == 'B':
        return {'type': 'Bomb', 'position': (x, y)}
    elif tile == 'O':
        return {'type': 'Ball', 'position': (x, y)}
    # Add more object types as needed
    return None

def interact_with_object(obj, maze, player_pos):
    """
    Interacts with the given object.
    """
    if obj['type'] == 'Bomb':
        # Remove the bomb and open a path
        x, y = obj['position']
        maze[y][x] = ' '  # Remove the bomb
        print("Bomb removed, path opened!")
    elif obj['type'] == 'Ball':
        # Implement logic to move the ball
        # For simplicity, we'll move the ball in the same direction as the player's last movement
        direction = (obj['position'][0] - player_pos[0], obj['position'][1] - player_pos[1])
        new_x = obj['position'][0] + direction[0]
        new_y = obj['position'][1] + direction[1]
        if is_move_valid(maze, (new_x, new_y)):
            move_object(obj, (new_x, new_y), maze)
            print("Ball moved!")
    # Handle other object types

def move_object(obj, new_pos, maze):
    """
    Moves an object to a new position.
    """
    old_x, old_y = obj['position']
    new_x, new_y = new_pos
    # Check if the new position is valid
    if maze[new_y][new_x] == ' ':
        # Move the object
        maze[old_y][old_x] = ' '
        obj['position'] = (new_x, new_y)
        # Update the maze
        if obj['type'] == 'Bomb':
            maze[new_y][new_x] = 'B'
        elif obj['type'] == 'Ball':
            maze[new_y][new_x] = 'O'
        # Add more object types as needed

def is_enemy(maze, pos):
    """
    Checks if there is an enemy at the given position.
    """
    x, y = pos
    tile = maze[y][x]
    return tile == 'X'  # Assuming 'X' represents an enemy

def attack_enemy(maze, pos):
    """
    Handles attacking an enemy at the given position.
    """
    x, y = pos
    # Remove the enemy from the maze
    maze[y][x] = ' '
    print("Enemy defeated!")

def apply_gravity(maze, player_pos):
    """
    Applies gravity to the player if there's no solid ground beneath.
    """
    x, y = player_pos
    while is_move_valid(maze, (x, y + 1)):
        y += 1
    return (x, y)
