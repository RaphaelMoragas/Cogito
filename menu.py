import pygame
import sys

import enums

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Menu Example")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define fonts
font = pygame.font.Font(None, 50)


class Menu:
    def __init__(self,
                 font,
                 width=1280,
                 height=720,
                 screen=pygame.display.set_mode((1280, 720)),
                 background=pygame.transform.scale(pygame.image.load('Files/background.jpg'), (1280, 720)),
                 random_start=False,
                 level=1,
                 difficulty=enums.Difficulty.EASY
                 ):
        self.font = font
        self.width = width
        self.height = height
        self.screen = screen
        self.background = background

# Define menu options
menu_options = ["Play", "Options", "Quit"]
selected_option = 0


# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    print("Start game!")
                    # Add your game code here
                elif selected_option == 1:
                    print("Options selected!")
                    # Add your options code here
                elif selected_option == 2:
                    print("Quit selected!")
                    running = False
                    pygame.quit()
                    sys.exit()

    # Draw menu options
    for i, option in enumerate(menu_options):
        if i == selected_option:
            draw_text(option, font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
        else:
            draw_text(option, font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
