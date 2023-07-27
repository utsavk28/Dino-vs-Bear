import os
import pygame

class Sprite :
    def __init__(self,path,pos,scale=1,speed=0.1) :
        self.frames = list(map(lambda x:f"{path}/{x}",os.listdir(path)))
        self.frames_len = len(self.frames)
        self.frame_idx = 0
        self.animation_speed = speed
        self.image = None
        self.rect_size = (32*scale,32*scale)
        self.images = {}
        for frame_idx in range(self.frames_len) :
            self.images[frame_idx] = pygame.transform.scale(pygame.image.load(self.frames[frame_idx]).convert_alpha(),self.rect_size)
        self.load_image()
        self.rect = self.image.get_rect(center=pos)
        self.screen = pygame.display.get_surface()
        # self.health_rect.
        
    def clear(self) :
        self.reset_frame_idx()

    def load_image(self) :
        self.image = self.images[int(self.frame_idx)]
        
    def reset_frame_idx(self) :
        self.frame_idx = 0
        
    def animate(self,direction) :
        self.frame_idx += self.animation_speed
        if int(self.frame_idx) >= self.frames_len :
            self.reset_frame_idx()

        self.load_image()
        # pygame.draw.circle(self.screen,"#ffffff",self.rect.center,96,1)
        # pygame.draw.circle(self.screen,"#ffffff",self.rect.center,192,1)
        # pygame.draw.rect(self.screen,"#ffffff",self.full_health)
        # pygame.draw.rect(self.screen,"#8a0303",self.red_health)
        image = pygame.transform.flip(self.image,direction == -1,False)
        self.screen.blit(image,self.rect)
        
    def render(self,direction=1) :
        self.animate(direction)
        
