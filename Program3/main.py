# Rephael Edwards
# Program 3
import pygame
import sys,os
import json
import time

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

if __name__=='__main__':

    pointlist = []
    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Earthquakes 1960 -2017 of magnitude 7 or more')
    screen.fill(background_colour)    
    
    count = 5
    folder = 'C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\VisDSAssignments\\Program3\\JsonFilesCreated\\'
    bg = pygame.image.load('C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\VisDSAssignments\\Program3\\1024x512.png')
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    
    f = open(folder+'quake-adjusted.json','r')
    points = json.loads(f.read())
        
    running = True
    while running: 
        for p in points[:count]:
            pygame.draw.circle(screen, (225,165,0), p, 1,0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.image.save(screen, 'C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\VisDSAssignments\\Program3\\display_quakes_screenshot.png')
                pygame.display.flip()
            pygame.time.wait(10)
            count+=5