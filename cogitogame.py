import enums
import pygame
from state import State
import ai
import time

class CogitoGame:
    CELL_SIZE = 60

    # Cores
    WHITE = (255, 255, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)

    def __init__(self,
                 font,
                 screen=pygame.display.set_mode((1280, 720)),
                 background=pygame.transform.scale(pygame.image.load('Files/background.jpg'), (1280, 720)),
                 random_start=False,
                 level=1,
                 difficulty=enums.Difficulty.EASY,
                 player=enums.Player.PERSON,
                 heuristic=enums.Heuristic.MISMATCHED_PIECES,
                 algorithm=enums.Algorithm.A_STAR
                 ):
        self.background = background
        self.game_state = State(level, random_start, difficulty)
        self.player = player
        self.heuristic = heuristic
        self.algorithm = algorithm
        self.font = font
        self.screen = screen
        self.EDGE_SIZE = self.CELL_SIZE // 3
        self.BOARD_SIZE = self.CELL_SIZE * self.game_state.N_CELLS
    
        # Imagens
        self.ORB = pygame.image.load('Files/orb.jpeg')
        self.GAME_ORB = pygame.transform.scale(self.ORB, (self.CELL_SIZE, self.CELL_SIZE))
        self.GOAL_ORB = pygame.transform.scale(self.ORB, (self.CELL_SIZE // 3, self.CELL_SIZE // 3))
        self.RED_ORB = pygame.image.load('Files/redOrb.jpeg')
        self.GAME_RED_ORB = pygame.transform.scale(self.RED_ORB, (self.CELL_SIZE, self.CELL_SIZE))
        self.GOAL_RED_ORB = pygame.transform.scale(self.RED_ORB, (self.CELL_SIZE // 3, self.CELL_SIZE // 3))

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Lida com a entrada do jogador humano
                if self.player == enums.Player.PERSON:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        self.process_click(x, y)  # Processa o clique
                        self.game_state.points = self.game_state.evaluate_board()  # Atualiza a pontuação

                    self.draw()
                    pygame.display.flip()

            # Lida com a entrada da IA
            if self.player == enums.Player.AI:
                action = ai.next_move(self.game_state, ai.greedy_search)  # Decide o próximo movimento com a IA
                self.game_state = self.game_state.move(action[1], action[0])  # Aplica o movimento
                self.draw()
                pygame.display.flip()
                time.sleep(2) # Vizualizar o movimento

            # Verifica condição de vitória
            if self.game_state.check_win():
                print("You won!")
                running = False

    # ##################################### VIEW #########################################
    def draw_goal(self, goal_board, size):
        margin = 50
        xi = self.screen.get_width() - size * (self.CELL_SIZE // 3) - margin
        yi = self.screen.get_height() - size * (self.CELL_SIZE // 3) - margin
        for x in range(size):
            for y in range(size):
                rect_x = xi + x * (self.CELL_SIZE // 3)
                rect_y = yi + y * (self.CELL_SIZE // 3)
                pygame.draw.rect(self.screen, self.WHITE, (rect_x, rect_y, self.CELL_SIZE // 3, self.CELL_SIZE // 3), 1)
                if goal_board[x][y] == 1:
                    self.screen.blit(self.GOAL_ORB, (xi + x * (self.CELL_SIZE // 3), yi + y * (self.CELL_SIZE // 3)))

    def draw_buttons(self, size):
        for i in range(size):
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

    def draw_board(self, board, size):
        for x in range(size):
            for y in range(size):
                rect = pygame.Rect(x * self.CELL_SIZE + 2 * self.EDGE_SIZE, y * self.CELL_SIZE + 2 * self.EDGE_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)
                if board[y][x] == 1:
                    self.screen.blit(self.GAME_ORB,
                                     (x * self.CELL_SIZE + 2 * self.EDGE_SIZE, y * self.CELL_SIZE + 2 * self.EDGE_SIZE))
                elif board[y][x] == 0:
                    self.screen.blit(self.GAME_RED_ORB,
                                     (x * self.CELL_SIZE + 2 * self.EDGE_SIZE, y * self.CELL_SIZE + 2 * self.EDGE_SIZE))

    def draw_game_board(self):
        self.draw_buttons(self.game_state.N_CELLS)
        self.draw_board(self.game_state.board, self.game_state.N_CELLS)

    def draw_points(self, max_points, points):  # TODO reduce function size (make it more intuitive)
        # Configurações da barra de pontuação
        margem = 60
        largura_total = 200
        altura = 20
        barra_x = self.screen.get_width() - max_points * (self.CELL_SIZE // 3) - margem  # Posição x onde a barra começa
        barra_y = 680  # Posição y onde a barra começa

        # Incrementos de % do total de pontos
        largura_preenchida = (largura_total / max_points) * points

        # Contorno
        pygame.draw.rect(self.screen, self.WHITE, (barra_x, barra_y, largura_total, altura), 2)
        # Barra preenchida
        pygame.draw.rect(self.screen, self.GREEN, (barra_x, barra_y, largura_preenchida, altura))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_game_board()
        self.draw_goal(self.game_state.goal_board, self.game_state.N_CELLS)
        self.draw_points(self.game_state.N_CELLS, self.game_state.points)

    # ##################################### CONTROLLER #########################################

    def process_click(self, x, y):
        if self.cond1(y):  # Linhas
            index = self.get_index(y)
            if self.cond2(x):  # Botão esquerdo
                self.game_state = self.game_state.move(index, enums.Direction.RIGHT)
            elif self.cond3(x):  # Botão direito
                self.game_state = self.game_state.move(index, enums.Direction.LEFT)
        elif self.cond1(x):  # Colunas
            index = self.get_index(x)
            if self.cond2(y):  # Botão superior
                self.game_state = self.game_state.move(index, enums.Direction.DOWN)
            elif self.cond3(y):  # Botão inferior
                self.game_state = self.game_state.move(index, enums.Direction.UP)
        pygame.mixer.Sound('Files/click_music.wav').play()

    def get_index(self, c):
        return (c - (2 * self.EDGE_SIZE)) // CogitoGame.CELL_SIZE

    def cond1(self, c):  # TODO LOOK FOR A BETTER NAME
        return 2 * self.EDGE_SIZE < c < self.BOARD_SIZE + 2 * self.EDGE_SIZE

    def cond2(self, c):
        return self.EDGE_SIZE < c < 2 * self.EDGE_SIZE

    def cond3(self, c):
        return self.BOARD_SIZE + (2 * self.EDGE_SIZE) < c < self.BOARD_SIZE + (3 * self.EDGE_SIZE)
