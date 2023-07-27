import pygame

class Controller :
    def __init__(self) :
        self.direction = pygame.math.Vector2()
        self.boost = False
        self.attack = False
    
    def input(self) :
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT] :
            self.boost = True
        else :
            self.boost = False  
            
        if keys[pygame.K_SPACE] :
            self.attack = True
        else :
            self.attack = False 

    def update(self) :
        self.input()
        
    def reset_direction(self) :
        self.direction.x = 0
        self.direction.y = 0