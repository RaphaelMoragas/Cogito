import pygame
import heapq

from game import Game, Direction
from copy import deepcopy
from collections import deque


class TreeNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []

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

    for dir in [Direction.UP, Direction.DOWN]:
        for index in list(range(9)):
            state_tmp = Game(font=pygame.font.Font(None, 50))

            state_tmp.board = deepcopy(state.board)
            state_tmp.points = deepcopy(state.points)
            state_tmp.move_column(index, dir)
            new_states.append((state_tmp, (dir,index)))
    for dir in [Direction.LEFT, Direction.RIGHT]:
        for index in list(range(9)):
            state_tmp = Game(font=pygame.font.Font(None, 50))

            state_tmp.board = deepcopy(state.board)
            state_tmp.points = deepcopy(state.points)
            state_tmp.move_column(index, dir)
            new_states.append((state_tmp, (dir,index)))

    return new_states


def goal_state_func(state):
    return state.board == state.goal_board

# Heuristicas
def h1(state):
    """
    Missmatch heuristic
    :return: Numero das pecas nas posisoes erradas.
    """
    return (state.N_CELLS - state.evaluate_board())

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

def greedy_search(problem, heuristic):
    setattr(TreeNode, "__lt__", lambda self, other: heuristic(self.state) < heuristic(other.state))
    states = [TreeNode(problem)]
    visited = set()
    visited.add(problem)

    while states:

        node = heapq.heappop(states)

        if goal_state_func(node.state):
            return node
        
        for (child, move) in child_game_states(node.state):
            if not child in visited:
                childNode = TreeNode(child, move=move)

                node.add_child(childNode)

                heapq.heappush(states, childNode)

                visited.add(child)

    return None
