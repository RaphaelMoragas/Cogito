import pygame
import heapq

from enums import Direction
from state import State
from copy import deepcopy
from collections import deque


class TreeNode:
    def __init__(self, state, parent=None, move=None, n_moves=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.n_moves = n_moves

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def print_solution(self):
        if self.parent is not None:
            self.parent.print_solution()

        if self.move is not None:
            print(f"move {str(self.move[0]).split('.')[1]} by {self.move[1]}")
        return


def child_game_states(state):
    new_states = []
    for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
        for index in list(range(9)):
            state_tmp = State()

            state_tmp.board = deepcopy(state.board)
            state_tmp.points = deepcopy(state.points)
            state_tmp = state_tmp.move(index, direction)
            new_states.append((state_tmp, (direction, index)))

    return new_states


def goal_state_func(state):
    return state.board == state.goal_board


# Heuristicas
def h1(state):
    """
    Missmatch heuristic
    :return: Numero das pecas nas posisoes erradas.
    """
    return state.N_CELLS - state.evaluate_board()


def a_star(node, heuristic):
    if node.parent is None:
        node.n_moves = 0
        return heuristic(node.state)
    else:
        node.n_moves = node.parent.n_moves + 1
        return heuristic(node.state) + node.n_moves


# Algorithms
def breadth_first_search(initial_state):
    root = TreeNode(initial_state)
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if goal_state_func(node.state):
            return node

        for (state, move) in child_game_states(node.state):
            child_node = TreeNode(state, move=move)

            node.add_child(child_node)

            queue.append(child_node)

    return None


def greedy_search(problem, heuristic=h1, a_star_on=False):
    if a_star_on:
        setattr(TreeNode, "__lt__", lambda self, other: a_star(self, heuristic) < a_star(other, heuristic))
    else:
        setattr(TreeNode, "__lt__", lambda self, other: heuristic(self.state) < heuristic(other.state))
    states = [TreeNode(problem)]
    visited = set()
    visited.add(problem)

    while states:

        node = heapq.heappop(states)

        if goal_state_func(node.state):
            return node
        child_move = child_game_states(node.state)
        for (child, move) in child_move:
            if child not in visited:
                childNode = TreeNode(child, move=move)

                node.add_child(childNode)

                heapq.heappush(states, childNode)

                visited.add(child)

    return None


def next_move(state, algorithm):
    tmp_state = deepcopy(state)
    final_node = algorithm(tmp_state)
    while final_node.parent.state.board != state.board:
        final_node = final_node.parent
    return final_node.move
