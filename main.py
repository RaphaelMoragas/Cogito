import pygame
from enums import *
from ai import *

#pygame.init()
#pygame.mixer.init()
#pygame.mixer.music.load('Files/music.mp3')
#pygame.mixer.music.play(-1)
#pygame.display.set_caption('Jogo Cogito')

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#BACKGROUND_IMG = pygame.transform.scale(pygame.image.load('Files/background.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

if __name__ == "__main__":
    # font = pygame.font.Font(None, 50)
    # MainMenu(font=font).menu_loop()

    # cogitogame.CogitoGame(pygame.font.Font(None,50), player=enums.Player.AI).play()

    initial_state = State(2, False, Difficulty.EASY)
    final_node = greedy_search(initial_state, h1, True)
    move_list = []
    while final_node.parent is not None:
        move_list.append(final_node.move)
        final_node = final_node.parent
    move_list.append(final_node.move)
    move_list.reverse()
    for move in move_list:
        print(move)
