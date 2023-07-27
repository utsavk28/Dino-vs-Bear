import os
import pygame
from .Sprite import Sprite


class SpriteManager:
    def __init__(self, path, current_state, pos, scale=1, speed=0.1,show_health=True):
        self.path = path
        self.sprites = {}
        self.current_sprite_name = current_state
        for sprite_path in os.listdir(path):
            sprite_name = sprite_path.split("_")[-1]
            self.sprites[sprite_name] = Sprite(
                f"{path}/{sprite_path}", pos, scale, speed)
        self.screen = pygame.display.get_surface()
        self.current_sprite = self.sprites[self.current_sprite_name]
        self.direction = 1
        self.full_health_info = {
            'pos': None,
            'dim': [60, 10],
            'offset': [22, 0]
        }
        self.curr_health_info = {
            'pos': None,
            'dim': [58, 8],
            'offset': [1, 1],
        }
        self.show_health = show_health
        self.calc_health(list(self.current_sprite.rect.topleft))
        self.full_health = pygame.Rect(
            self.full_health_info['pos'], self.full_health_info['dim'])
        self.curr_health = pygame.Rect(
            self.curr_health_info['pos'], self.curr_health_info['dim'])

    def calc_health(self, pos, health_percent=100):
        self.full_health_info['pos'] = pos.copy()
        self.curr_health_info['pos'] = pos.copy()
        for i in range(2):
            self.full_health_info['pos'][i] += (
                self.full_health_info['offset'][i] + (i == 0)*self.direction*6)
            self.curr_health_info['pos'][i] = self.full_health_info['pos'][i] + \
                self.curr_health_info['offset'][i]
            self.curr_health_info['dim'][i] = self.full_health_info['dim'][i] - \
                2*self.curr_health_info['offset'][i]
            if i == 0:
                self.curr_health_info['dim'][i] *= health_percent/100

    def update_health_pos(self):
        self.full_health.x = self.full_health_info['pos'][0]
        self.full_health.y = self.full_health_info['pos'][1]
        self.curr_health.x = self.curr_health_info['pos'][0]
        self.curr_health.y = self.curr_health_info['pos'][1]
        self.curr_health.w = self.curr_health_info['dim'][0]


    def update(self, pos=None, new_state=None, direction=0, health_percent=100):
        self.direction = direction
        if pos:
            self.current_sprite.rect.center = pos
        if new_state:
            self.current_sprite.clear()
            self.change_sprite(new_state, pos)
        self.calc_health(
            list(self.current_sprite.rect.topleft), health_percent)
        self.update_health_pos()

    def change_sprite(self, sprite_name, pos):
        self.current_sprite_name = sprite_name
        self.current_sprite = self.sprites[self.current_sprite_name]
        self.current_sprite.rect.center = pos

    def render(self):
        self.current_sprite.render(self.direction)
        if self.show_health :
            pygame.draw.rect(self.screen, "#ffffff", self.full_health)
            pygame.draw.rect(self.screen, "#8a0303", self.curr_health)
