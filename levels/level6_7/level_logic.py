import pygame
import sys

def run_level(music_start_time = 0):
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("The Shadows Deepen")

    # Colors
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    # Font and text
    font = pygame.font.Font(None, 36)  # Regular text font
    title_font = pygame.font.Font(None, 48)  # Title font
    title_text = "The Shadows Deepen"
    text_lines = [
        "Emerging from the maze's perilous traps,",
        "you sense a change in the air.",
        "",
        "A dense fog begins to envelop the corridors,",
        "and the light of the golden star dims ever so slightly.",
        "",
        "The shadows grow bolder,",
        "cloaking your path in an unsettling darkness.",
        "",
        "Your vision narrows,",
        "and only the immediate surroundings remain visible.",
        "",
        "Trust in your instincts and memory,",
        "for the maze now hides its secrets more closely.",
        "",
        "Navigate carefully through the obscured passages.",
        "",
        "The darkness tests your resolve,",
        "but the flicker of hope remains.",
        "",
        "Press on, for the fate of your world depends on you.",
        "",
        "The journey continues..."
    ]

    # Scroll speed and initial position
    scroll_speed = 1
    title_y = screen_height  # Start the title off-screen at the bottom
    text_y = screen_height + 100  # Start the text below the title

    # Load and play music (optional)
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("levels/level6_7/transition_music.mp3")  # Replace with your music file
        pygame.mixer.music.play(-1)  # Loop the music indefinitely
    except pygame.error as e:
        print(f"Unable to load music: {e}")

    # Clock for frame rate control
    clock = pygame.time.Clock()

    # Function to draw scrolling text
    def draw_text(screen, lines, y_pos, font, color):
        for line in lines:
            if line == "":
                y_pos += 30  # Add extra space for blank lines
            else:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y_pos))
                y_pos += 50  # Space between lines
        return y_pos

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the title and text scrolling upward
        draw_text(screen, [title_text], title_y, title_font, YELLOW)
        draw_text(screen, text_lines, text_y, font, YELLOW)

        # Update positions for scrolling
        title_y -= scroll_speed
        text_y -= scroll_speed

        # Stop scrolling when all text has fully scrolled out of view
        if text_y < -len(text_lines) * 50:
            running = False

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    # Stop music and cleanup
    music_end_time = pygame.mixer.music.get_pos() / 1000
    pygame.mixer.music.stop()
    pygame.quit()
    return True, music_end_time
