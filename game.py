import enums

import pygame
import random
import csv


def load_board(file_name):
    board = []
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            int_row = [int(char) for char in row]
            board.append(int_row)
    return board


def random_board(n):
    tab = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        while True:
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
            if tab[x][y] == 0:
                tab[x][y] = 1
                break
    return tab


def ciclo_lista(lista):
    return lista[-1:] + lista[:-1]




class Game:
    level_size = {1: 9}  # Adicionar aqui sempre que criar um level o tamanho dele

    CELL_SIZE = 60

    # Cores
    WHITE = (255, 255, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)

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
        self.screen_width = width
        self.screen_height = height
        self.background = background
        self.difficulty = difficulty
        self.font = font
        self.screen = screen
        self.level = level
        self.N_CELLS = self.level_size[self.level]
        self.EDGE_SIZE = self.CELL_SIZE // 3
        self.BOARD_SIZE = self.CELL_SIZE * self.N_CELLS
        if random_start:
            self.board = random_board(self.N_CELLS)
        else:
            self.board = load_board(f"levels/level{level}/start.csv")
        self.goal_board = load_board(f"levels/level{level}/goal.csv")
        self.points = self.evaluate_board()

        # Imagens
        self.ORB = pygame.image.load('Files/orb.jpeg')
        self.GAME_ORB = pygame.transform.scale(self.ORB, (self.CELL_SIZE, self.CELL_SIZE))
        self.GOAL_ORB = pygame.transform.scale(self.ORB, (self.CELL_SIZE // 3, self.CELL_SIZE // 3))
        self.RED_ORB = pygame.image.load('Files/redOrb.jpeg')
        self.GAME_RED_ORB = pygame.transform.scale(self.RED_ORB, (self.CELL_SIZE, self.CELL_SIZE))
        self.GOAL_RED_ORB = pygame.transform.scale(self.RED_ORB, (self.CELL_SIZE // 3, self.CELL_SIZE // 3))

    def play(self):  # Gameplay loop
        running = True
        while running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    self.process_click(x, y)
                    pontos = self.evaluate_board()  # Atualiza a pontuação após cada clique

            self.draw()

            if self.points == self.N_CELLS:  # Condição de vitória
                print("You won!")
                running = False

            pygame.display.flip()

    # ################################### MODEL ####################################
    def move_column(self, index, direction):
        if direction == enums.Direction.DOWN:
            self.board[index] = ciclo_lista(self.board[index])
        elif direction == enums.Direction.UP:
            self.board[index] = list(reversed(ciclo_lista(list(reversed(self.board[index])))))
        return self.board

    def move_line(self, index, direction):
        column = [self.board[i][index] for i in range(self.N_CELLS)]
        if direction == enums.Direction.RIGHT:
            column = ciclo_lista(column)
        elif direction == enums.Direction.LEFT:
            column = list(reversed(ciclo_lista(list(reversed(column)))))
        for i in range(self.N_CELLS):
            self.board[i][index] = column[i]
        return self.board

    def evaluate_board(self):
        pontos = 0
        for x in range(self.N_CELLS):
            for y in range(self.N_CELLS):
                if self.goal_board[x][y] == 1 and self.board[x][y] == 1:
                    pontos += 1
        return pontos

    # ##################################### VIEW #########################################
    def draw_goal(self):
        margin = 50
        xi = self.screen_width - self.N_CELLS * (self.CELL_SIZE // 3) - margin
        yi = self.screen_height - self.N_CELLS * (self.CELL_SIZE // 3) - margin
        for x in range(self.N_CELLS):
            for y in range(self.N_CELLS):
                rect_x = xi + x * (self.CELL_SIZE // 3)
                rect_y = yi + y * (self.CELL_SIZE // 3)
                pygame.draw.rect(self.screen, self.WHITE, (rect_x, rect_y, self.CELL_SIZE // 3, self.CELL_SIZE // 3), 1)
                if self.goal_board[x][y] == 1:
                    self.screen.blit(self.GOAL_ORB, (xi + x * (self.CELL_SIZE // 3), yi + y * (self.CELL_SIZE // 3)))

    def draw_buttons(self):
        for i in range(self.N_CELLS):
            pygame.draw.rect(self.screen, self.CYAN,
                             (i * self.CELL_SIZE + 2 * self.EDGE_SIZE, self.EDGE_SIZE, self.CELL_SIZE, self.EDGE_SIZE))
            pygame.draw.rect(self.screen, self.CYAN,
                             (i * self.CELL_SIZE + 2 * self.EDGE_SIZE, self.BOARD_SIZE + 2 * self.EDGE_SIZE,
                              self.CELL_SIZE, self.EDGE_SIZE))
            pygame.draw.rect(self.screen, self.CYAN, (
                self.EDGE_SIZE, i * self.CELL_SIZE + 2 * self.EDGE_SIZE, 2 * self.EDGE_SIZE, self.CELL_SIZE))
            pygame.draw.rect(self.screen, self.CYAN,
                             (self.BOARD_SIZE + 2 * self.EDGE_SIZE, i * self.CELL_SIZE + 2 * self.EDGE_SIZE,
                              self.EDGE_SIZE, self.CELL_SIZE))

    def draw_board(self):
        for x in range(self.N_CELLS):
            for y in range(self.N_CELLS):
                rect = pygame.Rect(x * self.CELL_SIZE + 2 * self.EDGE_SIZE, y * self.CELL_SIZE + 2 * self.EDGE_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)
                if self.board[x][y] == 1:
                    self.screen.blit(self.GAME_ORB,
                                     (x * self.CELL_SIZE + 2 * self.EDGE_SIZE, y * self.CELL_SIZE + 2 * self.EDGE_SIZE))
                elif self.board[x][y] == 0:
                    self.screen.blit(self.GAME_RED_ORB,
                                     (x * self.CELL_SIZE + 2 * self.EDGE_SIZE, y * self.CELL_SIZE + 2 * self.EDGE_SIZE))

    def draw_game_board(self):
        self.draw_buttons()
        self.draw_board()

    def draw_points(self):  # TODO reduce function size (make it more intuitive)
        # Configurações da barra de pontuação
        margem = 60
        largura_total = 200
        altura = 20
        barra_x = self.screen_width - self.N_CELLS * (self.CELL_SIZE // 3) - margem  # Posição x onde a barra começa
        barra_y = 680  # Posição y onde a barra começa

        # Incrementos de % do total de pontos
        largura_preenchida = (largura_total / self.N_CELLS) * self.points

        # Contorno
        pygame.draw.rect(self.screen, self.WHITE, (barra_x, barra_y, largura_total, altura), 2)
        # Barra preenchida
        pygame.draw.rect(self.screen, self.GREEN, (barra_x, barra_y, largura_preenchida, altura))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_game_board()
        self.draw_goal()
        self.draw_points()

    # ##################################### CONTROLLER #########################################
    def line_click(self, index, dir1, dir2):
        if self.difficulty == enums.Difficulty.EASY:
            self.move_line(index, dir1)
        elif self.difficulty == enums.Difficulty.MEDIUM:
            self.move_column(index, dir2)
        elif self.difficulty == enums.Difficulty.HARD:
            self.move_line(index, dir1)
            self.move_column(index, dir2)

    def column_click(self, index, dir1, dir2):
        if self.difficulty == enums.Difficulty.EASY:
            self.move_column(index, dir1)
        elif self.difficulty == enums.Difficulty.MEDIUM:
            self.move_line(index, dir2)
        elif self.difficulty == enums.Difficulty.HARD:
            self.move_column(index, dir1)
            self.move_line(index, dir2)

    def process_click(self, x, y):
        if self.cond1(y):  # Linhas
            index = self.get_index(y)
            if self.cond2(x):  # Botão esquerdo
                self.line_click(index, enums.Direction.RIGHT, enums.Direction.UP)
            elif self.cond3(x):  # Botão direito
                self.line_click(index, enums.Direction.LEFT, enums.Direction.DOWN)
        elif self.cond1(x):  # Colunas
            index = self.get_index(x)
            if self.cond2(y):  # Botão superior
                self.column_click(index, enums.Direction.DOWN, enums.Direction.LEFT)
            elif self.cond3(y):  # Botão inferior
                self.column_click(index, enums.Direction.UP, enums.Direction.RIGHT)
        pygame.mixer.Sound('Files/click_music.wav').play()

    def get_index(self, c):
        return (c - (2 * self.EDGE_SIZE)) // Game.CELL_SIZE

    def cond1(self, c):  # TODO LOOK FOR A BETTER NAME
        return 2 * self.EDGE_SIZE < c < self.BOARD_SIZE + 2 * self.EDGE_SIZE

    def cond2(self, c):
        return self.EDGE_SIZE < c < 2 * self.EDGE_SIZE

    def cond3(self, c):
        return self.BOARD_SIZE + (2 * self.EDGE_SIZE) < c < self.BOARD_SIZE + (3 * self.EDGE_SIZE)
