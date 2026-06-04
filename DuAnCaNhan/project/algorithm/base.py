# Ninh Nguyễn Minh Tuyên - 24110372

import random
from re import I
import collections
import heapq

class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state  # state = ((x, y), tuple_of_dirties)
        self.parent = parent
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)


def normalize_dirties(dirties):
    return tuple(sorted(dirties))


def get_neighbors(state, cols, rows):
    (x, y), dirties = state
    neighbors = []

    directions = [
        (0, -1),  # Lên
        (0, 1),   # Xuống
        (-1, 0),  # Trái
        (1, 0)    # Phải
    ]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < cols and 0 <= ny < rows:
            new_pos = (nx, ny)

            # Nếu đi vào ô có rác thì xóa rác đó
            new_dirties = tuple(d for d in dirties if d != new_pos)

            neighbors.append((new_pos, new_dirties))

    return neighbors


# truy vết đường đi
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state[0])
        node = node.parent
    return path[::-1]


def is_in_frontier(state, frontier):
    return any(node.state == state for node in frontier)


# heuristic function (Manhattan distance)
def h(position, dirties):
    if not dirties:
        return 0
    
    # tính khoảng cách từ vị trí hiện tại đến ô rác gần nhất 
    x, y = position

    nearest = min(
        abs(x - dx) + abs(y - dy)
        for dx, dy in dirties
    )

    return nearest + len(dirties)


FOUND = "FOUND"
INF = float("inf")
