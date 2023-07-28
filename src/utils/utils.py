import pygame 
import random 

def distance2v(v1,v2) :
    return v1.distance_to(v2)

def random_pos_in_radius(pos) :
    temp = [[50, 850, 150], [50, 550, 100]]
    newPos = [0, 0]
    for i in range(len(newPos)):
        l, h, r = temp[i]
        r1, r2 = int(pos[i]-r), int(pos[i]+r)
        r1 = max(min(r1, h), l)
        r2 = max(min(r2, h), l)
        newPos[i] = random.randint(r1, r2)
    return pygame.math.Vector2(newPos)