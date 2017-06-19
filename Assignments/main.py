#Rephael Edwards
#Assignment 2
import pygame
import random
from dbscan import *
import sys,os
import pprint as pp


keys = []
bronx_crimes = []
manhatten_crimes = []
queens_crimes = []
brooklyn_crimes = []
staten_island_crimes = []
# maxX = 1067226
# minX = 271820
# maxY = 913357
# minY = 121250
DIRPATH = os.path.dirname(os.path.realpath(__file__))    

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)


def create_list(filename):
    
    scaled_points = []
    crimes = []
    all_crimes = []
    xlist = []
    ylist = []
    newxlist = []
    newylist = []

    #DIRPATH = os.path.dirname(os.path.realpath(__file__))    

    got_keys = False
    #with open(DIRPATH+'/'+'nypd_small_data.txt') as f:
    with open(DIRPATH+ filename) as f:
        print(f)
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not got_keys:
                keys = line
                #print(keys)
                got_keys = True
                continue

            crimes.append(line)
    print(len(crimes))
    for crime in crimes:
        if crime[19] != ("") and crime[20] != (""):
            if crime[19] != ("X_COORD_CD"):
                all_crimes.append((int(crime[19]),int(crime[20]))) 
    #print(crimes)
    
    for item in all_crimes:
        x = item[0]
        y = item[1]
        xlist.append(float(x))
        ylist.append(float(y))
    """
    maxX = max(xlist)
    minX = min(xlist)
    maxY = max(ylist)
    minY = min(ylist)"""

    maxX = float(1067226)
    minX = float(271820)
    maxY = float(913357)
    minY = float(121250)

    for x in xlist:
        #newx = ((float(x) - float(minX)) / (float(maxX) - float(minX))*1000.0) 
        tempx = x-minX
        denomX = (maxX - minX) 
        newx = (tempx / denomX) * 1000.0
        #newx = float(((x - minX) / (maxX - minX)) * 1000.0)
        newxlist.append(int(newx))
    for y in ylist:
        tepmy = y - minY
        denomY = maxY - minY
        newy = (1 - (tepmy / denomY)) * 1000.0
        #newy = ((1-(float(y) - float(minY)) / (float(maxY) - float(minY))*1000.0) 
        #newy = float((1-(y - minY)) / ((maxY - minY))) *1000.0
        newylist.append(int(newy))
    for r in range(len(all_crimes)-1):
        scaled_points.append((newxlist[r],newylist[r]))
        
    #print(scaled_points)  
    return scaled_points

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1000, 1000)

goldenrod = (253,182,50)
tomato = (255,99,71)
teal = (2,120,120)
firebrick = (194,35,38)
brown = (165,42,42)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Crime Clusters')
screen.fill(background_colour)
pygame.display.flip()


epsilon = 20
min_pts = 5.0

bronx_crimes = create_list('\\NYPD_CrimeData\\filtered_crimes_bronx.csv')
brooklyn_crimes = create_list('/../NYPD_CrimeData/filtered_crimes_brooklyn.csv')
manhatten_crimes = create_list('/../NYPD_CrimeData/filtered_crimes_manhattan.csv')
queens_crimes = create_list('/../NYPD_CrimeData/filtered_crimes_queens.csv')
staten_island_crimes = create_list('/../NYPD_CrimeData/filtered_crimes_staten_island.csv')
print("end of calls")


running = True
while running:
    for b in brooklyn_crimes:
        pygame.draw.circle(screen, (165,42,42), b, 3, 0)
    for p in bronx_crimes:
        pygame.draw.circle(screen, (2,120,120), p, 3, 0)
    print("brooklyn")
    for m in manhatten_crimes:
        pygame.draw.circle(screen, firebrick, m, 3, 0)
    print("manhatten")
    for q in queens_crimes:
        pygame.draw.circle(screen, tomato, q, 3, 0)
    print("queens")
    for s in staten_island_crimes:
        pygame.draw.circle(screen, goldenrod, s, 3, 0)
    print("staten Island")
    
    pygame.image.save(screen, 'C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\VisDSAssignments\\Assignment2\\all_boroughs_screen_shot.png')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     clean_area(screen,(0,0),width,height,(255,255,255))
        #     scaled_points.append(event.pos)
        #     mbrs = calculate_mbrs(scaled_points, epsilon, min_pts)
    pygame.display.flip()
