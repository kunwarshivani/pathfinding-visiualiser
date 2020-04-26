import numpy as np
import pygame
import queue

import math
import time

row_count = 30
column_count = 40
squaresize = 20
start = (12,11)
end = (12,30)
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
    board[start] = 1
    board[end] = 9
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

#depth first naive search
def dfs(board, node):

    if visit[node]==False and board[node]!=10001:
        visit[node] = True
        print(visit)
        animate(node)
        stack.append(node)
        if(node==end):
            return
        else:
            top = stack[-1] #top most element
            print(top)
            if top[1] + 1 < column_count and visit[top[0],top[1]+1] == False:
                dfs(board,(top[0],top[1]+1))
            elif top[1] -1 >=0 and visit[top[0],top[1]-1] == False:
                dfs(board,(top[0],top[1]-1))
            elif top[0] + 1 < row_count and visit[top[0] + 1,top[1]] == False:
                dfs(board,(top[0] + 1,top[1]))
            elif top[0] - 1 >= 0 and visit[top[0] -1 ,top[1]] == False:
                dfs(board,(top[0] - 1,top[1]))

            stack.pop()

    else:
        return




screen = pygame.display.set_mode(size)
board = create_board()

draw_board(board)
while(flag):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    dfs(board, start)

    pygame.display.update()
print(visit)