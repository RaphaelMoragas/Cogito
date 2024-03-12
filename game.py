# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random
import csv

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
N_CELLS = 9
CELL_SIZE = 60
EDGE_SIZE = CELL_SIZE // 3
BOARD_SIZE = CELL_SIZE * N_CELLS

# Cores
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)

# PyGame Init
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Files/music.mp3')
pygame.mixer.music.play(-1)
pygame.display.set_caption('Jogo Cogito')

# Imagem de fundo
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load('Files/background.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Imagens
ORB = pygame.image.load('Files/orb.jpeg')
GAME_ORB = pygame.transform.scale(ORB, (CELL_SIZE, CELL_SIZE))
GOAL_ORB = pygame.transform.scale(ORB, (CELL_SIZE // 3, CELL_SIZE // 3))
RED_ORB = pygame.image.load('Files/redOrb.jpeg')
GAME_RED_ORB = pygame.transform.scale(RED_ORB, (CELL_SIZE, CELL_SIZE))
GOAL_RED_ORB = pygame.transform.scale(RED_ORB, (CELL_SIZE // 3, CELL_SIZE // 3))


def load_board(file_name):
    board = []
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            int_row = [int(char) for char in row]
            board.append(int_row)
    return board


class Game:
    def __init__(self, level=0, difficulty=1, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.screen_width = width
        self.screen_height = height
        self.difficulty = difficulty
        self.level = level
        self.font = pygame.font.Font(None, 50)
        self.screen = pygame.display.set_mode((width, height))
        self.board = load_board(f"levels/level{level}/start.csv")
        self.goal_board = load_board(f"levels/level{level}/goal.csv")

    def play(self):
        running = True
        pontos = 0  # Pontuação inicial
        while running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    process_click(x, y, self.board, self.difficulty)
                    pontos = evaluate_board(self.board, self.goal_board)  # Atualiza a pontuação após cada clique

            draw(self.board, self.goal_board, pontos)

            if pontos == N_CELLS:  # Condição de vitória
                print("You won!")
                running = False

            pygame.display.flip()


# ##################################### MODEL #########################################

def random_board():
    tab = [[0 for i in range(N_CELLS)] for j in range(N_CELLS)]
    for i in range(N_CELLS):
        while True:
            x, y = random.randint(0, N_CELLS - 1), random.randint(0, N_CELLS - 1)
            if tab[x][y] == 0:
                tab[x][y] = 1
                break
    return tab


def ciclo_lista(lista):
    return lista[-1:] + lista[:-1]


def move_column(index, direction, board):
    if direction == 'esq':
        board[index] = ciclo_lista(board[index])
    elif direction == 'dir':
        board[index] = list(reversed(ciclo_lista(list(reversed(board[index])))))
    return board


def move_line(index, direction, board):
    column = [board[i][index] for i in range(N_CELLS)]
    if direction == 'cim':
        column = ciclo_lista(column)
    elif direction == 'bai':
        column = list(reversed(ciclo_lista(list(reversed(column)))))
    for i in range(N_CELLS):
        board[i][index] = column[i]
    return board


def evaluate_board(board, goal_board):
    pontos = 0
    for x in range(N_CELLS):
        for y in range(N_CELLS):
            if goal_board[x][y] == 1 and board[x][y] == 1:
                pontos += 1
    return pontos


# ##################################### VIEW #########################################
def draw_goal(goal_board):
    margin = 50
    xi = SCREEN_WIDTH - N_CELLS * (CELL_SIZE // 3) - margin
    yi = SCREEN_HEIGHT - N_CELLS * (CELL_SIZE // 3) - margin
    for x in range(N_CELLS):
        for y in range(N_CELLS):
            rect_x = xi + x * (CELL_SIZE // 3)
            rect_y = yi + y * (CELL_SIZE // 3)
            pygame.draw.rect(screen, WHITE, (rect_x, rect_y, CELL_SIZE // 3, CELL_SIZE // 3), 1)
            if goal_board[x][y] == 1:
                screen.blit(GOAL_ORB, (xi + x * (CELL_SIZE // 3), yi + y * (CELL_SIZE // 3)))


def draw_buttons():
    for i in range(N_CELLS):
        pygame.draw.rect(screen, CYAN, (i * CELL_SIZE + 2 * EDGE_SIZE, EDGE_SIZE, CELL_SIZE, EDGE_SIZE))
        pygame.draw.rect(screen, CYAN,
                         (i * CELL_SIZE + 2 * EDGE_SIZE, BOARD_SIZE + 2 * EDGE_SIZE, CELL_SIZE, EDGE_SIZE))
        pygame.draw.rect(screen, CYAN, (EDGE_SIZE, i * CELL_SIZE + 2 * EDGE_SIZE, 2 * EDGE_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, CYAN,
                         (BOARD_SIZE + 2 * EDGE_SIZE, i * CELL_SIZE + 2 * EDGE_SIZE, EDGE_SIZE, CELL_SIZE))


def draw_board(board):
    for x in range(N_CELLS):
        for y in range(N_CELLS):
            rect = pygame.Rect(x * CELL_SIZE + 2 * EDGE_SIZE, y * CELL_SIZE + 2 * EDGE_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if board[x][y] == 1:
                screen.blit(GAME_ORB, (x * CELL_SIZE + 2 * EDGE_SIZE, y * CELL_SIZE + 2 * EDGE_SIZE))
            elif board[x][y] == 0:
                screen.blit(RED_ORB, (x * CELL_SIZE + 2 * EDGE_SIZE, y * CELL_SIZE + 2 * EDGE_SIZE))


def draw_game_board(board):
    screen.blit(BACKGROUND_IMG, (0, 0))
    draw_buttons()
    draw_board(board)


def draw_points(pontos):
    # Configurações da barra de pontuação
    margem = 60
    largura_total = 200
    altura = 20
    barra_x = SCREEN_WIDTH - N_CELLS * (CELL_SIZE // 3) - margem  # Posição x onde a barra começa
    barra_y = 680  # Posição y onde a barra começa

    # Incrementos de % do total de pontos
    largura_preenchida = (largura_total / N_CELLS) * pontos

    # Contorno
    pygame.draw.rect(screen, WHITE, (barra_x, barra_y, largura_total, altura), 2)
    # Barra preenchida
    pygame.draw.rect(screen, GREEN, (barra_x, barra_y, largura_preenchida, altura))


def draw(board, goal_board, points):
    draw_game_board(board)
    draw_goal(goal_board)
    draw_points(points)


# ##################################### CONTROLLER #########################################
def get_index(c):
    return (c - (2 * EDGE_SIZE)) // CELL_SIZE


def cond1(c):  # TODO LOOK FOR A BETTER NAME
    return 2 * EDGE_SIZE < c < BOARD_SIZE + 2 * EDGE_SIZE


def cond2(c):
    return EDGE_SIZE < c < 2 * EDGE_SIZE


def cond3(c):
    return BOARD_SIZE + (2 * EDGE_SIZE) < c < BOARD_SIZE + (3 * EDGE_SIZE)


def process_click(x, y, board, difficulty):
    if cond1(y):  # Linhas
        index = get_index(y)
        if cond2(x):  # Botão esquerdo
            move_line(index, 'cim', board)
            if difficulty == 3:
                move_column(index, 'dir', board)
        elif cond3(x):  # Botão direito
            move_line(index, 'bai', board)
            if difficulty == 3:
                move_column(index, 'esq', board)
    elif cond1(x):  # Colunas
        index = get_index(x)
        if cond2(y):  # Botão superior
            move_column(index, 'esq', board)
            if difficulty == 3:
                move_line(index, 'bai', board)
        elif cond3(y):  # Botão inferior
            move_column(index, 'dir', board)
            if difficulty == 3:
                move_line(index, 'cim', board)
    pygame.mixer.Sound('Files/click_music.wav').play()


if __name__ == "__main__":
    Game(level=1).play()
