import numpy as np
import pygame
import queue
import math
import time


row_count = 30
column_count = 40
start = (12,11)
end = (12,30)
squaresize = 20


#animate nodes
def animatetemp(temp):
    if not temp == column_count*start[0] + start[1]:
        if not temp == column_count*end[0] + end[1]:
            x = int(temp/column_count)* squaresize
            y = int(temp%column_count) * squaresize
            pygame.draw.rect(screen, (0, 255, 255), (y , x + 100, squaresize - 1, squaresize - 1))


#define the board matrix
def create_board():
    board = np.full((row_count, column_count),0)
    board[start] = 1
    board[end] = 9
    return board


#gives closest node
def minver(mindis, visit):
    min = 10000
    for i in range(row_count * column_count):
        if mindis[i] < min and visit[i] == False:
            min = i
    return min


# update left, right, top, bottom
def updateneighbours(mindis, visit, u, nodes):

    #top
    if 0< u - column_count < row_count*column_count and  mindis[u- column_count] >= mindis[u] + 1 and not mindis[u - column_count] == 10001:
        mindis[u - column_count] = mindis[u] + 1
        nodes.put(u - column_count)


    #bottom
    if 0< u + column_count < row_count*column_count and mindis[u + column_count] >= mindis[u] + 1 and not mindis[u + column_count] == 10001:
        mindis[u + column_count] = mindis[u] + 1
        nodes.put(u + column_count)

    #left
    if 0< u - 1 < row_count*column_count and mindis[u - 1] > mindis[u] + 1 and not mindis[u - 1] == 10001:
        if int(u/ column_count) == int((u-1)/column_count):
            mindis[u - 1] = mindis[u] + 1
            nodes.put(u-1)

     #right
    if 0< u + 1 < row_count*column_count and mindis[u + 1] > mindis[u] + 1 and not mindis[u + 1] == 10001:
        if int(u / column_count) == int((u -1)/ column_count):
            mindis[u + 1] = mindis[u] + 1
            nodes.put(u + 1)



visit = []
mindis = []
for i in range(row_count * column_count) :
    visit.append(False)
    mindis.append(10000)

# dijsktra algorithm
def dijsktra(board):

    mindis[column_count*start[0] + start[1]] = 0
    print(mindis)

    print(visit)
    count = 0
    nodes = queue.Queue()


    u = minver(mindis,visit)

    nodes.put(u)
    while not nodes.empty():
        temp = nodes.get()
        if not temp == column_count * end[0] + end[1]:
            visit[temp] = True
            animatetemp(temp)
            updateneighbours(mindis,visit,temp,nodes)
        else:
            visit[temp] = True
            break

    solution = np.full((row_count, column_count),0)
    for i in range(row_count * column_count):
        x = int(i/column_count)
        y = int(i % column_count)
        solution[(x,y)] = mindis[i]
    print(visit)
    print(solution)

#creating window

pygame.init()
width = column_count * squaresize
height = row_count * squaresize
size = (width, height)
srcy = squaresize * start[0]
srcx = squaresize * start[1]
desy = squaresize * end[0]
desx = squaresize * end[1]

def draw_board(board):
    screen.fill((128, 206, 255))
    pygame.display.set_caption('Pathfinding visualiser')
    for c in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, (128, 206, 255), (c * squaresize, r * squaresize + 100, squaresize, squaresize))
            pygame.draw.rect(screen, (255, 255, 255),(c * squaresize , r * squaresize + 100, squaresize - 1 , squaresize - 1))

    pygame.draw.rect(screen, (119, 221, 119), (srcx, srcy + 100, squaresize - 1, squaresize - 1))
    pygame.draw.rect(screen, (225, 105, 97), (desx, desy + 100, squaresize - 1, squaresize - 1))
    pygame.draw.rect(screen, (119, 221, 119), (600, 60, squaresize - 1, squaresize - 1))
    srcText = pygame.font.Font('freesansbold.ttf',12)
    TextSurf = srcText.render('source',True,(255,255,255))
    screen.blit(TextSurf,(630,65))
    pygame.draw.rect(screen, (225, 105, 97), (500, 60, squaresize - 1, squaresize - 1))
    desText = pygame.font.Font('freesansbold.ttf', 12)
    TextSurf2 = desText.render('destination', True, (255, 255, 255))
    screen.blit(TextSurf2, (530, 65))

board = create_board()

screen = pygame.display.set_mode(size)
flag = True
draw_board(board)
#dijsktra(board)
play = pygame.image.load('play.png')
play = pygame.transform.scale(play,(40,40))

while(flag):

    screen.blit(play, (700,50))

    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        posx = mouse[0]
        posy = mouse[1]

        if event.type == pygame.QUIT:
                flag = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            print(posx)
            if posy > 100:
                    row = int(math.floor(posx/squaresize)) * squaresize
                    col = int(math.floor(posy/squaresize)) * squaresize
                    wallx = int(row / squaresize)
                    wally = int(col / squaresize) - 5
                    print(wallx,wally)
                    mindis[column_count * wally + wallx] = 10001
                    pygame.draw.rect(screen, (0, 0, 0), (row, col, squaresize - 1, squaresize - 1))
                    #print(event.pos)

            if 700 + 40 > mouse[0] > 700 and 50 + 40 > mouse[1] > 50:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dijsktra(board)


    pygame.display.update()


