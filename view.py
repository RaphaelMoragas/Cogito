import pygame

CELL_SIZE = 60


class View:
    def __init__(self, font, screen, background=pygame.transform.scale(pygame.image.load('Files/background.jpg'),
                                                                       (1280, 720))):
        self.font = font
        self.screen = screen
        self.background = background
        self.EDGE_SIZE = CELL_SIZE // 3
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = 0

        # Imagens
        self.ORB = pygame.image.load('Files/orb.jpeg')
        self.GAME_ORB = pygame.transform.scale(self.ORB, (CELL_SIZE, CELL_SIZE))
        self.GOAL_ORB = pygame.transform.scale(self.ORB, (CELL_SIZE // 3, CELL_SIZE // 3))
        self.RED_ORB = pygame.image.load('Files/redOrb.jpeg')
        self.GAME_RED_ORB = pygame.transform.scale(self.RED_ORB, (CELL_SIZE, CELL_SIZE))
        self.GOAL_RED_ORB = pygame.transform.scale(self.RED_ORB, (CELL_SIZE // 3, CELL_SIZE // 3))
