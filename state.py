import csv
import random
from copy import deepcopy

import enums


def ciclo_lista(lista):
    return lista[-1:] + lista[:-1]


def load_board(file_name):
    board = []
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            int_row = [int(char) for char in row]
            board.append(int_row)
    return board


def random_board(n):
    tab = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        while True:
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
            if tab[x][y] == 0:
                tab[x][y] = 1
                break
    return tab


class State:
    level_size = {1: 9}

    def __init__(self, level, random_start, difficulty):
        self.difficulty = difficulty
        self.N_CELLS = self.level_size[level]
        if random_start:
            self.board = random_board(self.N_CELLS)
        else:
            self.board = load_board(f"levels/level{level}/start.csv")
        self.goal_board = load_board(f"levels/level{level}/goal.csv")
        self.points = self.evaluate_board()

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

    def move(self, index, direction1):
        state_copy = deepcopy(self)

        direction2 = {enums.Direction.UP: enums.Direction.RIGHT,
                      enums.Direction.DOWN: enums.Direction.LEFT,
                      enums.Direction.RIGHT: enums.Direction.UP,
                      enums.Direction.LEFT: enums.Direction.DOWN
                      }[direction1]

        if state_copy.difficulty == enums.Difficulty.EASY:
            if direction1 == enums.Direction.RIGHT or direction1 == enums.Direction.LEFT:
                state_copy.move_line(index, direction1)
            elif direction1 == enums.Direction.UP or direction1 == enums.Direction.DOWN:
                state_copy.move_column(index, direction1)
        elif state_copy.difficulty == enums.Difficulty.MEDIUM:
            if direction1 == enums.Direction.RIGHT or direction1 == enums.Direction.LEFT:
                state_copy.move_column(index, direction2)
            if direction1 == enums.Direction.UP or direction1 == enums.Direction.DOWN:
                state_copy.move_line(index, direction2)
        elif state_copy.difficulty == enums.Difficulty.HARD:
            if direction1 == enums.Direction.RIGHT or direction1 == enums.Direction.LEFT:
                state_copy.move_line(index, direction1)
                state_copy.move_column(index, direction2)
            if direction1 == enums.Direction.UP or direction1 == enums.Direction.DOWN:
                state_copy.move_column(index, direction1)
                state_copy.move_line(index, direction2)
        return state_copy

    def evaluate_board(self):
        points = 0
        for x in range(self.N_CELLS):
            for y in range(self.N_CELLS):
                if self.goal_board[x][y] == 1 and self.board[x][y] == 1:
                    points += 1
        return points

    def check_win(self):
        return self.evaluate_board() == self.N_CELLS
