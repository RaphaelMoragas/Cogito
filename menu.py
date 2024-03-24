import pygame
import enums
from cogitogame import CogitoGame

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pygame.display.set_caption("Pygame Menu Example")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class MainMenu:

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
        self.random_start = random_start
        self.level = level
        self.difficulty = difficulty
        self.menu_options = ["Play", "Difficulty", "Quit"]
        self.difficulty_options = [difficulty.name.capitalize() for difficulty in enums.Difficulty]
        self.selected_option = 0
        self.selected_difficulty = 0
        self.in_difficulty_menu = False

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_difficulty_menu(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.difficulty_options):
            if i == self.selected_difficulty:
                self.draw_text(option, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
            else:
                self.draw_text(option, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
    def process_difficulty_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulty_options)
            elif event.key == pygame.K_DOWN:
                self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulty_options)
            elif event.key == pygame.K_RETURN:
                self.difficulty = list(enums.Difficulty)[self.selected_difficulty]
                self.in_difficulty_menu = False

    def menu_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                running = self.process_event(event)
            if self.in_difficulty_menu:
                self.draw_difficulty_menu()
            else:
                self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                self.draw_text(option, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
            else:
                self.draw_text(option, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

    def process_event(self, event):
        running = True
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if self.in_difficulty_menu:
                # Processa a seleção de dificuldade
                self.process_difficulty_selection(event)
            else:
                # Processa a navegação do menu principal
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        print("Start game!")
                        game = CogitoGame(font=self.font, difficulty=self.difficulty)
                        game.play()
                    elif self.selected_option == 1:
                        self.in_difficulty_menu = True
                    elif self.selected_option == 2:
                        print("Quit selected!")
                        running = False
        return running



if __name__ == "__main__":
    MainMenu(font=pygame.font.Font(None, 50)).menu_loop()
