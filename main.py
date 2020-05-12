import numpy as np
import pygame
import queue
import math
import time


row_count = 30
column_count = 40
start = (20,35)
end = (12,11)
squaresize = 20

choice = 0

pygame.init()
width = column_count * squaresize
height = row_count * squaresize
size = (width, height)
srcy = squaresize * start[0]
srcx = squaresize * start[1]
desy = squaresize * end[0]
desx = squaresize * end[1]

#
#
#
#
#
#animate nodes for dikstra
def animatetemp(temp):
    if not temp == column_count*start[0] + start[1]:
        if not temp == column_count*end[0] + end[1]:
            x = int(temp/column_count)* squaresize
            y = int(temp%column_count) * squaresize
            pygame.draw.rect(screen, (0, 255, 255), (y , x + 100, squaresize - 1, squaresize - 1))

#animates the node
def animate(node):
    if node!=start and node!=end:
        pygame.draw.rect(screen,(0,255,255),(node[1]*squaresize,node[0]*squaresize + 100,squaresize-1,squaresize-1))

#
#
#
#
#

#define the board matrix
def create_board():
    board = np.full((row_count, column_count),0)
    board[start] = 1 #starting
    board[end] = 9   #end
    return board


def draw_board(board):
    screen.fill((128, 206, 255))
    pygame.display.set_caption('Pathfinding visualiser')
    for c in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, (128, 206, 255), (c * squaresize, r * squaresize + 100, squaresize, squaresize))
            pygame.draw.rect(screen, (255, 255, 255),(c * squaresize , r * squaresize + 100, squaresize - 1 , squaresize - 1))

    pygame.draw.rect(screen, (119, 221, 119), (srcx, srcy + 100, squaresize - 1, squaresize - 1))
    pygame.draw.rect(screen, (225, 105, 97), (desx, desy + 100, squaresize - 1, squaresize - 1))
    #the green source block
    pygame.draw.rect(screen, (119, 221, 119), (600, 60, squaresize - 1, squaresize - 1))
    srcText = pygame.font.Font('freesansbold.ttf',12)
    TextSurf = srcText.render('source',True,(255,255,255))
    screen.blit(TextSurf,(630,65))
    #the red destination block
    pygame.draw.rect(screen, (225, 105, 97), (500, 60, squaresize - 1, squaresize - 1))
    desText = pygame.font.Font('freesansbold.ttf', 12)
    TextSurf2 = desText.render('destination', True, (255, 255, 255))
    screen.blit(TextSurf2, (530, 65))
    #dikstra text
    dikstraText = pygame.font.Font('freesansbold.ttf', 12)
    dikstraSurf = dikstraText.render('Dikstra', True, (255, 255, 255))
    screen.blit(dikstraSurf, (50, 65))
    # dfs text
    dfsText = pygame.font.Font('freesansbold.ttf', 12)
    dfsSurf = dfsText.render('DFS', True, (255, 255, 255))
    screen.blit(dfsSurf, (150, 65))
    # a star text
    astarText = pygame.font.Font('freesansbold.ttf', 12)
    astarSurf = astarText.render('A star', True, (255, 255, 255))
    screen.blit(astarSurf, (250, 65))
#
#
#
#
#

"""  dijktra algorithm stuff  """
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






# dijsktra algorithm
mindis = []
for i in range(row_count * column_count):
    mindis.append(10000)


def dijsktra(board):
    visit = []

    for i in range(row_count * column_count):
        visit.append(False)
        mindis.append(10000)

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
            #time.sleep(0.01)
        else:
            visit[temp] = True
            break

    solution = np.full((row_count, column_count),0)
    for i in range(row_count * column_count):
        x = int(i/column_count)
        y = int(i % column_count)
        solution[(x,y)] = mindis[i]
#
#
#
#



"""dfs algorithm stuff"""
visit = np.full((row_count, column_count),False)
stack = []

#depth first naive search
def dfs(board, node):


        visit[node] = True
        print(visit)
        animate(node)
        stack.append(node)
        if(node==end):
            return
        else:
            top = stack[-1] #top most element
            print(top)
            if top[1] + 1 < column_count and visit[top[0],top[1]+1] == False and board[top[0],top[1]+1]!=10001:
                dfs(board,(top[0],top[1]+1))
            elif top[1] -1 >=0 and visit[top[0],top[1]-1] == False and board[top[0],top[1]-1]!=10001:
                dfs(board,(top[0],top[1]-1))
            elif top[0] + 1 < row_count and visit[top[0] + 1,top[1]] == False and board[top[0] + 1,top[1]]!=10001:
                dfs(board,(top[0] + 1,top[1]))
            elif top[0] - 1 >= 0 and visit[top[0] -1 ,top[1]] == False and board[top[0] -1 ,top[1]]!=10001:
                dfs(board,(top[0] - 1,top[1]))

            stack.pop()




#
#
#
#
"""a star algorithm stuff"""
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







####creating the window###




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

            #print(posx)
            if posy > 100:
                    row = int(math.floor(posx/squaresize)) * squaresize
                    col = int(math.floor(posy/squaresize)) * squaresize
                    wallx = int(row / squaresize)
                    wally = int(col / squaresize) - 5
                    #print(wallx,wally)
                    mindis[column_count * wally + wallx] = 10001
                    board[wally][wallx] = 10001
                    pygame.draw.rect(screen, (0, 0, 0), (row, col, squaresize - 1, squaresize - 1))
                    #print(event.pos)
            if 50 + 60 > mouse[0] > 50 and 65 + 30 > mouse[1] > 65:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = 0
            if 150 + 50 > mouse[0] > 150 and 65 + 30 > mouse[1] > 65:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = 1
                    print(choice)
            if 250 + 50 > mouse[0] > 250 and 65 + 30 > mouse[1] > 65:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = 2
                    print(choice)

            if 700 + 40 > mouse[0] > 700 and 50 + 40 > mouse[1] > 50:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if choice == 0:
                        dijsktra(board)
                    if choice == 1:
                        dfs(board,start)
                    if choice == 2:
                        board[start]=board[end] = 0
                        path = astar(board)


    pygame.display.update()


