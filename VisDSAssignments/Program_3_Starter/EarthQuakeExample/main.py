import pygame
import sys,os
import json

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

if __name__=='__main__':

    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Earthquakes 1960 -2017 of magnitude 7 or more')
    screen.fill(background_colour)

    bg = pygame.image.load('C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\4553-Spatial-DS\\Resources\\Program_3_Starter\\EarthQuakeExample\\1024x512.png')
    pygame.display.flip()
    for x in range(1960,2017):
        f = open('quake-'+str(x)+'-adjusted.json','r')
        points = json.loads(f.read())
    
    count = 0
    running = True
    while running:
        screen.blit(bg, (0, 0))
        #for i in range(0,len(points)):  
        for p in points[count :5]:
            #count+=1
            pygame.draw.circle(screen, (225,165,0), p, 1,0)
            count+=5
            """if count == 5:
                pygame.time.delay(5000)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
        pygame.display.flip()
        pygame.time.delay(3000)
            
        pygame.image.save(screen, 'C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\VisDSAssignments\\Program_3_Starter\\display_quakes_screenshot.png')
   