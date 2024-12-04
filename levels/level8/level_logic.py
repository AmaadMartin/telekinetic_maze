# levels/level_with_blurred_vision/level_logic.py

import pygame
import os
import sys
import math
from utils.game_utils import *
from .maze_layout import get_level_map, get_moving_walls, update_moving_walls
from .controls import get_actions, index_pinched
from utils.HandInput import HandInput

TILE_SIZE = 40  # Ensure this matches the TILE_SIZE in utils.game_utils
VISION_RADIUS = 2  # Define the vision radius in tiles

def run_level(music_start_time = 0):
    # Initialize Pygame and other resources
    pygame.init()
    clock = pygame.time.Clock()

    # Load background music
    music_path = os.path.join("levels/level8/music.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, music_start_time)

    # Load maze layout
    level_map = get_level_map()
    maze = load_maze(level_map)

    # Initialize screen
    maze_height = len(maze)
    maze_width = len(maze[0])
    screen_size = (maze_width * TILE_SIZE, maze_height * TILE_SIZE)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Maze Game - Blurred Vision Level")

    # Load images
    images = load_images()

    # Load player images
    graphics_path = os.path.join(os.path.dirname(__file__), 'graphics')

    # Load player standing image
    player_image_path = os.path.join(graphics_path, 'player.png')
    if os.path.exists(player_image_path):
        player_image_standing = pygame.image.load(player_image_path).convert_alpha()
        player_image_standing = pygame.transform.scale(player_image_standing, (TILE_SIZE, TILE_SIZE))
    else:
        print("Error: Player image not found.")
        pygame.quit()
        sys.exit()

    # Load player moving image
    player_moving_image_path = os.path.join(graphics_path, 'player_moving.png')
    if os.path.exists(player_moving_image_path):
        player_image_moving = pygame.image.load(player_moving_image_path).convert_alpha()
        player_image_moving = pygame.transform.scale(player_image_moving, (TILE_SIZE, TILE_SIZE))
    else:
        print("Error: Player moving image not found.")
        pygame.quit()
        sys.exit()

    # Set initial player image to standing
    player_image = player_image_standing

    # Get player start position
    player_pos = list(get_start_position(maze))

    # Initialize HandInput
    hand_input = HandInput()

    level_complete = False
    while not level_complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hand_input.release()
                pygame.quit()
                sys.exit()

        # Move the walls
        update_moving_walls(maze)
        # Check if player collides with any moving wall
        for wall in get_moving_walls():
            if wall["position"] == player_pos:
                player_pos = list(get_start_position(maze))

        # Update player image based on whether the index finger is pinched
        if index_pinched(hand_input):
            player_image = player_image_moving
        else:
            player_image = player_image_standing
            hand_input.prev_positions['Right'] = None

        # Get actions from controls
        actions = get_actions(hand_input)
        # Process actions and update game state
        movement_direction = actions.get('movement_direction')
        if movement_direction:
            dx, dy = movement_direction
            new_pos = (player_pos[0] + dx, player_pos[1] + dy)
            if is_move_valid(maze, new_pos):
                player_pos = list(new_pos)

        # Check for exit
        if is_exit(maze, player_pos):
            level_complete = True
            print("Level Complete!")
            break

        # Draw maze and player with vision mechanic
        screen.fill((0, 0, 0))
        draw_maze_with_blurred_vision(screen, maze, player_pos, images, player_image, VISION_RADIUS)
        pygame.display.flip()
        clock.tick(30)  # Limit to 30 FPS

    hand_input.release()
    music_end_time = pygame.mixer.music.get_pos() / 1000
    pygame.quit()
    return True, music_end_time

def load_images():
    images = {}
    graphics_path = os.path.join(os.path.dirname(__file__), 'graphics')

    # Tile symbols and corresponding image filenames
    tile_images = {
        '#': 'wall.png',
        ' ': 'path.png',
        'S': 'start.png',
        'E': 'exit.png',
        '*': 'spike.png',
        # Add more tile-image mappings as needed
    }

    for tile_symbol, filename in tile_images.items():
        image_path = os.path.join(graphics_path, filename)
        if os.path.exists(image_path):
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            images[tile_symbol] = image
        else:
            print(f"Warning: Image file {filename} not found for tile '{tile_symbol}'")

    # Load vision mask image
    vision_mask_path = os.path.join(graphics_path, 'vision_mask.png')
    if os.path.exists(vision_mask_path):
        vision_mask = pygame.image.load(vision_mask_path).convert_alpha()
        vision_mask = pygame.transform.scale(vision_mask, (VISION_RADIUS * 2 * TILE_SIZE, VISION_RADIUS * 2 * TILE_SIZE))
        images['vision_mask'] = vision_mask
    else:
        print("Warning: Image file 'vision_mask.png' not found for vision mask.")

    return images

def draw_maze_with_blurred_vision(screen, maze, player_pos, images, player_image, vision_radius):
    # Draw the visible tiles
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            dx = x - player_pos[0]
            dy = y - player_pos[1]
            distance = math.hypot(dx, dy)
            if distance <= vision_radius + 1:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile in images:
                    screen.blit(images[tile], rect)
                else:
                    # Default to path if image not found for the tile
                    screen.blit(images[' '], rect)

    # Draw moving walls
    for wall in get_moving_walls():
        wall_x, wall_y = wall["position"]
        wall_rect = pygame.Rect(wall_x * TILE_SIZE, wall_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(images['*'], wall_rect)

    # Draw the player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_image, player_rect)

    # Apply the vision mask
    if 'vision_mask' in images:
        mask_rect = images['vision_mask'].get_rect()
        mask_rect.center = (player_pos[0] * TILE_SIZE + TILE_SIZE // 2, player_pos[1] * TILE_SIZE + TILE_SIZE // 2)
        screen.blit(images['vision_mask'], mask_rect, special_flags=pygame.BLEND_RGBA_MULT)
    else:
        # If no vision mask image is available, draw a simple black overlay with a circular cutout
        overlay = pygame.Surface(screen.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 255))  # Semi-transparent black

        # Create a circular cutout
        pygame.draw.circle(overlay, (0, 0, 0, 0), (player_pos[0] * TILE_SIZE + TILE_SIZE // 2, player_pos[1] * TILE_SIZE + TILE_SIZE // 2), vision_radius * TILE_SIZE)
        screen.blit(overlay, (0, 0))