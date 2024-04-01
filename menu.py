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
                 difficulty=enums.Difficulty.EASY,
                 heuristic=enums.Heuristic.MISMATCHED_PIECES,
                 algorithm=enums.Algorithm.GREEDY
                 ):
        self.font = font
        self.width = width
        self.height = height
        self.screen = screen
        self.background = background
        self.random_start = random_start
        self.level = level
        self.difficulty = difficulty
        self.menu_options = ["Play", "Difficulty", "Jogador", "Quit"]
        self.difficulty_options = [difficulty.name.capitalize() for difficulty in enums.Difficulty]
        self.selected_option = 0
        self.selected_difficulty = 0
        self.in_difficulty_menu = False

        # Opções jogador oi AI
        self.heuristic = heuristic
        self.algorithm = algorithm
        self.player_options = ["Pessoa", "AI"]
        self.ai_options = ["Heurística", "Algoritmo"]
        self.heuristic_options = ["Mismatched Pieces", "Manhattan Distance"]
        self.algorithm_options = ["BFS", "Greedy", "A Star"]
        self.selected_player_option = 0
        self.selected_ai_option = 0
        self.selected_heuristic_option = 0
        self.selected_algorithm_option = 0
        self.in_player_menu = False
        self.in_ai_menu = False
        self.in_heuristic_menu = False
        self.in_algorithm_menu = False

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

    def draw_player_menu(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.player_options):
            color = RED if i == self.selected_player_option else BLACK
            self.draw_text(option, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

    def draw_ai_menu(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.ai_options):
            color = RED if i == self.selected_ai_option else BLACK
            self.draw_text(option, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

    def draw_heuristic_menu(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.heuristic_options):
            color = RED if i == self.selected_heuristic_option else BLACK
            self.draw_text(option, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

    def process_heuristic_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_heuristic_option = (self.selected_heuristic_option - 1) % len(self.selected_heuristic_option)
            elif event.key == pygame.K_DOWN:
                self.selected_heuristic_option = (self.selected_heuristic_option + 1) % len(self.selected_heuristic_option)
            elif event.key == pygame.K_RETURN:
                if self.selected_heuristic_option == 0:
                    self.heuristic = enums.Heuristic.MISMATCHED_PIECES
                elif self.selected_heuristic_option == 1:
                    self.heuristic = enums.Heuristic.MANHATTAN_DISTANCE
                self.in_heuristic_menu = False

    def draw_algorithm_menu(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.algorithm_options):
            color = RED if i == self.selected_algorithm_option else BLACK
            self.draw_text(option, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

    def process_algorithm_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_algorithm_option = (self.selected_algorithm_option - 1) % len(self.selected_algorithm_option)
            elif event.key == pygame.K_DOWN:
                self.selected_algorithm_option = (self.selected_algorithm_option + 1) % len(self.selected_algorithm_option)
            elif event.key == pygame.K_RETURN:
                if self.selected_algorithm_option == 0:
                    self.algorithm = enums.Algorithm.BFS
                if self.selected_algorithm_option == 1:
                    self.algorithm = enums.Algorithm.GREEDY
                elif self.selected_algorithm_option == 2:
                    self.algorithm = enums.Algorithm.A_STAR
                self.in_heuristic_menu = False

    def menu_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                running = self.process_event(event)
            if self.in_difficulty_menu:
                self.draw_difficulty_menu()
            elif self.in_player_menu:
                self.draw_player_menu()
            elif self.in_ai_menu:
                self.draw_ai_menu()
            elif self.in_heuristic_menu:
                self.draw_heuristic_menu()
            elif self.in_algorithm_menu:
                self.draw_algorithm_menu()
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
        # Checa se ocorre o fechamento do jogo
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Dentro do menu de seleção de dificuldade
            if self.in_difficulty_menu:
                self.process_difficulty_selection(event)
            # Dentro do menu de seleção do tipo de jogador (Pessoa ou AI)
            elif self.in_player_menu:
                # Navega pelas opções do menu Jogador
                if event.key == pygame.K_UP:
                    self.selected_player_option = (self.selected_player_option - 1) % len(self.player_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_player_option = (self.selected_player_option + 1) % len(self.player_options)
                # Confirma a seleção do tipo de jogador
                elif event.key == pygame.K_RETURN:
                    if self.selected_player_option == 1:  # AI foi selecionado
                        self.in_player_menu = False
                        self.in_ai_menu = True  # Abre o submenu de AI
                    else:  # Pessoa foi selecionada
                        self.in_player_menu = False
            # Dentro do submenu de AI
            elif self.in_ai_menu:
                # Navega pelas opções de AI
                if event.key == pygame.K_UP:
                    self.selected_ai_option = (self.selected_ai_option - 1) % len(self.ai_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_ai_option = (self.selected_ai_option + 1) % len(self.ai_options)
                # Confirma a seleção do tipo de AI
                elif event.key == pygame.K_RETURN:
                    if self.selected_ai_option == 0:  # Heurística selecionada
                        self.in_ai_menu = False
                        self.in_heuristic_menu = True
                    if self.selected_ai_option == 1:  # Algoritmo selecionado
                        self.in_ai_menu = False
                        self.in_algorithm_menu = True
            elif self.in_heuristic_menu:
                if event.key == pygame.K_UP:
                    self.selected_heuristic_option = (self.selected_heuristic_option - 1) % len(self.heuristic_options)
                if event.key == pygame.K_DOWN:
                    self.selected_heuristic_option = (self.selected_heuristic_option + 1) % len(self.heuristic_options)
                elif event.key == pygame.K_RETURN:
                    self.in_heuristic_menu = False  # Pode iniciar o jogo ou voltar ao menu
                    self.heuristic = list(enums.Algorithm)[self.selected_heuristic_option]
            elif self.in_algorithm_menu:
                if event.key == pygame.K_UP:
                    self.selected_algorithm_option = (self.selected_algorithm_option - 1) % len(self.algorithm_options)
                if event.key == pygame.K_DOWN:
                    self.selected_algorithm_option = (self.selected_algorithm_option + 1) % len(self.algorithm_options)
                elif event.key == pygame.K_RETURN:
                    self.in_algorithm_menu = False  # Pode iniciar o jogo ou voltar ao menu
                    self.algorithm = list(enums.Algorithm)[self.selected_algorithm_option]
            # Navegação no menu principal
            else:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                # Ações baseadas na opção selecionada
                elif event.key == pygame.K_RETURN:
                    # Inicia o jogo
                    if self.selected_option == 0:
                        print("Start game!")
                        game = CogitoGame(font=self.font, difficulty=self.difficulty)
                        game.play()
                    # Abre o menu de dificuldade
                    elif self.selected_option == 1:
                        self.in_difficulty_menu = True
                    # Abre o menu de seleção do tipo de jogador
                    elif self.selected_option == 2:
                        self.in_player_menu = True
                    # Sai do jogo
                    elif self.selected_option == 3:
                        print("Quit selected!")
                        running = False
        return running

# if __name__ == "__main__":
#    MainMenu(font=pygame.font.Font(None, 50)).menu_loop()
