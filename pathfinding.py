import pygame
import time
import threading
import math
import subprocess
pygame.init()
clock=pygame.time.Clock()
surface = pygame.display.set_mode((1025,525))
FPS=60

RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY1 = (50,50,50)
GRAY2 = (25,25,25)
GREEN = (0,255,0)
BLUE = (0, 0, 255)

D = 50

(mouse_x, mouse_y) = pygame.mouse.get_pos()
forbidden_block = []
black_blocks = []
running = True
keys=pygame.key.get_pressed()
ab = -1
a = (0,0)
b= (0,0)

smallfont = pygame.font.SysFont('Corbel',35) 
text = smallfont.render('Settings' , True , RED) 


def draw_black_blocks():
    for i in black_blocks:
        pygame.draw.rect(surface, BLACK, pygame.Rect(i[0]-D/2, i[1]-D/2, D, D))
     
def gui():
    gui = True
    while gui:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                gui = False
            if event.type == pygame.QUIT:           
                pygame.display.update() 
                gui = False

        pygame.draw.rect(surface, GRAY2, pygame.Rect(200,100,600,300))

        sf = pygame.font.SysFont('Corbel',20)
        text_list = ["SPACE = run the A* pathfinding","M = switch between block and A&B points",
                     "in this program you click to add indestructible blocks,", "then you place the points A (departure) and B (arrival),", 
                     "finally you launch the pathfinding AI"]
        for i in range(len(text_list)):
            text2 = sf.render(text_list[i], True,RED)
            surface.blit(text2,(250,i*25+125))

        clock.tick(FPS)
        pygame.display.update()

def draw(surface):
    surface.fill(GRAY1)
    for i in range(int(1000/D)):
        pygame.draw.line(surface,BLACK, (i*D+D/2, 0), (i*D+D/2, 525),3)
    for i in range(int(500/D)):
        pygame.draw.line(surface,BLACK, (0, i*D+D/2), (1025, i*D+D/2),3)
    if not a == (0,0):
        pygame.draw.rect(surface, GREEN, pygame.Rect(a[0]-D/2, a[1]-D/2, D, D))
    if not b == (0,0):
        pygame.draw.rect(surface, RED, pygame.Rect(b[0]-D/2, b[1]-D/2, D, D))
    pygame.draw.rect(surface, GRAY2, pygame.Rect(900,25,120,40))
    surface.blit(text,(900,25))
def braining(pos):
    time.sleep(0.05)
    b_test = []
    f_list = []
    forbid_block = forbidden_block+black_blocks
    for i in range(1, -2, -1):
        for j in range(1, -2, -1):
            pos_x = i*D +pos[0]
            pos_y = j*D +pos[1]
            g_cost = math.sqrt((pos_x-a[0])**2 + (pos_y-a[1])**2)
            h_cost = math.sqrt((pos_x-b[0])**2 + (pos_y-b[1])**2)
            f_cost = g_cost+h_cost
            if g_cost != 0 and not (pos_x, pos_y) in forbid_block:
                b_test.append([(pos_x, pos_y), g_cost, h_cost, f_cost])
                f_list.append(f_cost)
    test2 = sorted(f_list)
    if len(test2) == 0:
        print('error')
        return 'out of range', test2[0]
    index = f_list.index(test2[0])
    if len(test2) != 0: return b_test[index][0], test2[0]
    
def AI():
    sf = pygame.font.SysFont('Corbel',round(20*50/D))
    new_pos, f = braining(a)
    test = 0
    poss = [new_pos]
    fcost_list = [f]
    while new_pos != b and test < 100000:
        test += 1
        forbidden_block.append(new_pos)
        pygame.draw.rect(surface, BLUE, pygame.Rect(new_pos[0]-D/2, new_pos[1]-D/2, D, D))
        surface.blit(sf.render(str(round(f)), True,RED),(new_pos[0]-D/2, new_pos[1]-D/2))
        pygame.display.flip()
        new_pos, f = braining(new_pos)
        fcost_list.append(f)
        poss.append(new_pos)
        if new_pos == 'out of range':
            poss.pop()
            poss.pop()
            new_pos = poss[len(poss)-1]
            print('error fixed')
    reversing(poss, fcost_list)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                subprocess.run(["python", "pathfinding.py"])
                run = False
    pygame.quit()
def reversing(posse, fcl):
    sf = pygame.font.SysFont('Corbel',round(20*50/D))
    fc = fcl
    pos = posse
    poss = posse[len(posse)-1]
    index = reversing2(poss, fc, pos)
    fc.pop(pos.index(index))
    pos.pop(pos.index(index))
    poss = index
    while poss != 'finished':
        time.sleep(0.05)

        pygame.draw.rect(surface, WHITE, pygame.Rect(poss[0]-D/2, poss[1]-D/2, D, D))
        #surface.blit(sf.render(str(round(fposs)), True,RED),(poss[0]-D/2, poss[1]-D/2)) under maintenance
        pygame.display.flip()
        index = reversing2(poss, fc, pos)
        if index == 'finished': 
            pass
        else:
            fc.pop(pos.index(index))
            pos.pop(pos.index(index))

        poss = index
    print('finished')
def reversing2(poss, fc, pos):
        fposs = 100000
        poss2 = 0
        index = 0
        list1 = [[], []]
        if math.sqrt((poss[0]-a[0])**2 + (poss[1]-a[1])**2) < 1.5*D: return 'finished'
        for i in range(1, -2, -1):
            for j in range(1, -2, -1):
                if (poss[0]+i*D, poss[1]+j*D) in pos and not i == j == 0:
                    if (poss[0]+i*D, poss[1]+j*D) != b :
                        print(fc[pos.index((poss[0]+i*D, poss[1]+j*D))], (poss[0]+i*D, poss[1]+j*D))
                        index = (poss[0]+i*D, poss[1]+j*D)
                        poss2 = pos[pos.index(index)]
                        fposs = fc[pos.index(index)]
                        list1[0].append(fposs)
                        list1[1].append(poss2)
        print('list : ', list1)
        list3 = sorted(list1[0])
        if len(list3) == 1: return list1[1][0]
        if len(list3) == 0:
            print('error line 167 list index out of range')
            return 'finished'
        print('index : ', list1[1][list1[0].index(list3[0])])
        poss2 = list1[1][list1[0].index(list3[0])]
        
        return poss2
                        
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:           
                pygame.display.update() 
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 875 < mouse_x < 1020 and 0 < mouse_y < 75:
                    gui(surface)
                else:
                    if ab == -1:
                        black_blocks.append((mouse_x, mouse_y))
                    elif ab == 0:
                        a = (mouse_x,mouse_y)
                        ab += 1
                    elif ab == 1:
                        b = (mouse_x,mouse_y)
                        ab += 1
                    else:
                        AI()
            if event.type == pygame.KEYDOWN:
                if ab > 0: ab = -1
                else: ab += 1
    draw(surface)
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    draw_black_blocks()
    mouse_x = round(mouse_x/D) * D
    mouse_y = round(mouse_y/D) * D
    if not (875 < mouse_x < 1020 and 0 < mouse_y < 75):
        if not (ab == -1):
            if ab == 0:
                pygame.draw.rect(surface, GREEN, pygame.Rect(mouse_x-D/2, mouse_y-D/2, D, D))
            elif ab <2:
                pygame.draw.rect(surface, RED, pygame.Rect(mouse_x-D/2, mouse_y-D/2, D, D))
        else:
            pygame.draw.rect(surface, BLACK, pygame.Rect(mouse_x-D/2, mouse_y-D/2, D, D))
    
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
