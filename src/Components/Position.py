import pygame


class Position:
    def __init__(self, pos, dim, scale=1,speed=1):
        self.velocity = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = speed
        self.dim = pygame.math.Vector2(dim)
        self.scale = scale

    def update(self):
        if self.velocity.magnitude() :
            self.pos += self.velocity.normalize()*self.speed
        self.clipPos()

    def setPos(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.clipPos()

    def setScale(self, scale):
        self.scale = scale

    def setDim(self, dim):
        self.dim = dim

    def updateVelocity(self,velocity) :
        self.velocity = velocity
        
    def clipPos(self) :
        self.pos.x = min(max(self.pos.x,32),960-32)
        self.pos.y = min(max(self.pos.y,32),640-32)
        
    def setSpeed(self,speed) :
        self.speed = speed
        