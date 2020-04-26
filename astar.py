import numpy as np
import pygame
import queue

import math
import time

row_count = 30
column_count = 40
squaresize = 20
start = (0,0)
end = (12,13)
srcy = squaresize * start[0]
srcx = squaresize * start[1]
desy = squaresize * end[0]
desx = squaresize * end[1]

pygame.init()

width = column_count * squaresize
height = row_count * squaresize
size = (width, height)
flag = True

#animates the node
def animate(node):
    if node!=start and node!=end:
        pygame.draw.rect(screen,(0,255,255),(node[1]*squaresize,node[0]*squaresize,squaresize-1,squaresize-1))

def create_board():
    board = np.full((row_count,column_count),0)
    board[start] = 0
    board[end] = 0
    return board

def draw_board(board):
    screen.fill((128,206,255))
    pygame.display.set_caption('Pathfinding visualiser')
    for c in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, (128, 206, 255), (c * squaresize, r * squaresize , squaresize, squaresize))
            pygame.draw.rect(screen, (255, 255, 255),(c * squaresize, r * squaresize , squaresize - 1, squaresize - 1))
    pygame.draw.rect(screen, (119, 221, 119), (srcx, srcy, squaresize - 1, squaresize - 1))
    pygame.draw.rect(screen, (225, 105, 97), (desx, desy, squaresize - 1, squaresize - 1))

visit = np.full((row_count, column_count),False)
stack = []





class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)

        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            animate(node_position)
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)








screen = pygame.display.set_mode(size)
board = create_board()

draw_board(board)
while(flag):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    path = astar(board)


    pygame.display.update()
print(path)