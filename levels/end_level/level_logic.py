import pygame
import sys
import math

def run_level(music_start_time = 0):
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Star Maze: Victory")

    # Colors
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (135, 206, 235)

    # Load the star texture
    try:
        star_texture = pygame.image.load("levels/end_level/star.png")  # Replace with your star texture path
        star_texture = pygame.transform.scale(star_texture, (40, 40))  # Initial size of the star
    except pygame.error as e:
        print(f"Unable to load star texture: {e}")
        sys.exit()

    # Variables for dynamic scaling
    star_scale_factor = 1.0
    scale_increment = 0.005  # How much the scale increases per frame

    # Star properties
    star_x = screen_width // 2
    star_y = screen_height
    ascent_speed = 2

    # Sky gradient
    gradient_speed = 1
    current_sky_color = BLACK

    # Rays of light
    light_rays = []
    for i in range(12):  # 12 rays of light
        angle = i * (360 // 12)
        light_rays.append({"angle": angle, "length": 50})

    # Font for "Victory" text
    font = pygame.font.Font(None, 72)
    victory_text = font.render("The Light Returns!", True, (255, 255, 0))  # Yellow text
    victory_text_x = screen_width // 2 - victory_text.get_width() // 2
    victory_text_y = screen_height // 2 - 100

    # Load and play triumphant music
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("levels/end_level/victory_theme.mp3")  # Replace with your music file
        pygame.mixer.music.play(-1)  # Loop the music indefinitely
    except pygame.error as e:
        print(f"Unable to load music: {e}")

    # Clock for frame rate control
    clock = pygame.time.Clock()

    # Ascend animation properties
    ascending = True
    glow_increase = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen with the current sky color
        screen.fill(current_sky_color)

        # Draw light rays
        for ray in light_rays:
            angle_rad = math.radians(ray["angle"])
            end_x = star_x + int(ray["length"] * math.cos(angle_rad))
            end_y = star_y - int(ray["length"] * math.sin(angle_rad))
            pygame.draw.line(screen, LIGHT_BLUE, (star_x, star_y), (end_x, end_y), 2)

            # Extend the ray length gradually
            ray["length"] += glow_increase

        # Dynamically scale the star texture
        star_scale_factor += scale_increment
        scaled_star = pygame.transform.scale(
            star_texture,
            (int(40 * star_scale_factor), int(40 * star_scale_factor))  # Scale width and height dynamically
        )
        # Draw the scaled star texture
        star_rect = scaled_star.get_rect(center=(star_x, star_y))
        screen.blit(scaled_star, star_rect)

        # Animate the star ascending
        if ascending:
            star_y -= ascent_speed
            if star_y <= screen_height // 4:  # Stop at top quarter of the screen
                ascending = False

        # Gradually change the sky color to blue
        if current_sky_color[0] < LIGHT_BLUE[0]:
            current_sky_color = (
                min(current_sky_color[0] + gradient_speed, LIGHT_BLUE[0]),
                min(current_sky_color[1] + gradient_speed, LIGHT_BLUE[1]),
                min(current_sky_color[2] + gradient_speed, LIGHT_BLUE[2]),
            )

        # Display the victory message once the star reaches its destination
        if not ascending:
            screen.blit(victory_text, (victory_text_x, victory_text_y))

        # Update display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    # Stop music and cleanup
    pygame.mixer.music.stop()
    pygame.quit()
    return True, 0