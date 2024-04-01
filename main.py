import pygame
import game
from game import Game
from ai import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Files/music.mp3')
pygame.mixer.music.play(-1)
pygame.display.set_caption('Jogo Cogito')


# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load('Files/background.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

if __name__ == "__main__":
    # game.Game(font=pygame.font.Font(None, 50)).play()

    game = Game(font=pygame.font.Font(None, 50), level=2)
    

    node = greedy_search(game, h1)
    node.print_solution()
