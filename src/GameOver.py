import os
import pygame
import random
from .StateMachine.State import State
from .Sprite.Sprite import Sprite
from .enum import GameStates
random.seed(42)


class GameOver(State):
    def __init__(self):
        super().__init__(GameStates.MENU, [GameStates.MAIN_GAME])
        self.title_font = pygame.font.Font('res/font/GravityBold8.ttf', 56)
        self.score_font = pygame.font.Font('res/font/GravityRegular5.ttf', 48)
        self.screen = pygame.display.get_surface()
        self.title1 = self.title_font.render("GAME", True, "#BC4D4F")
        self.title2 = self.title_font.render(" ", True, "#0696DB")
        self.title3 = self.title_font.render("OVER", True, "#BC4D4F")
        self.score = self.score_font.render("Score", True, "#0696DB")
        self.title_rect2 = self.title2.get_rect(center=(480, 200))
        self.title_rect1 = self.title1.get_rect(
            midright=self.title_rect2.midleft)
        self.title_rect3 = self.title3.get_rect(
            midleft=self.title_rect2.midright)
        self.score_rect = self.score.get_rect(center=(480, 276))

        self.bg_img = pygame.transform.scale(pygame.image.load(
            "res/graphics/background/back.png"), (960, 640))
        self.bg_rect = self.bg_img.get_rect(topleft=(0, 0))
        self.ground_sprite = self.load_sprites(
            "res/graphics/background/ground")
        self.surface_sprite = self.load_sprites(
            "res/graphics/background/surface")
        self.grass_sprite = self.load_sprites("res/graphics/background/grass")
        self.blocks = []
        for i in range(6, 10):
            for j in range(15):
                sprite = None
                if i == 6:
                    if random.random() < 0.3:
                        sprite = random.choice(self.grass_sprite)
                elif i == 7:
                    sprite = self.surface_sprite[j % 3]
                    if j == 0:
                        sprite = self.surface_sprite[0]
                    elif j == 14:
                        sprite = self.surface_sprite[2]
                    else:
                        sprite = self.surface_sprite[1]
                elif i == 8:
                    sprite = self.ground_sprite[j % 3]
                else:
                    sprite = self.ground_sprite[3+j % 3]
                if sprite:
                    block = {
                        'rect': pygame.Rect(j*64, i*64, 64, 64),
                        'sprite': sprite
                    }
                    self.blocks.append(block)

        self.player_sprites = ['doux', 'mort', 'tard', 'vita']
        self.enemy_sprites = ['Pink_Monster', 'Owlet_Monster', 'Dude_Monster']
        self.players = []
        self.enemies = []
        self.switch_btn = False

    def load_sprites(self, path):
        sprite_paths = list(map(lambda x: f'{path}/{x}', os.listdir(path)))
        sprite_paths.sort()
        sprites = list(map(lambda x: pygame.image.load(x), sprite_paths))
        sprites = list(
            map(lambda x: pygame.transform.scale(x, (64, 64)), sprites))
        return sprites

    def player_update(self):
        if random.randint(1, 1000) <= 3:
            self.players.append(Sprite(
                f"res/graphics/characters/{random.choice(self.player_sprites)}/run", (-64, 6*64+16), scale=4))

        for player in self.players:
            speed = random.randint(1, 5)
            animation_speed = speed/20
            player.rect.x += speed
            player.animation_speed = animation_speed
            player.render()

        self.players = list(filter(lambda x: x.rect.x < 1000, self.players))

    def enemy_update(self):
        if random.randint(1, 1000) > 997:
            enemy_name = random.choice(self.enemy_sprites)
            self.enemies.append(Sprite(
                f"res/graphics/characters/{enemy_name}/{enemy_name}_Walk", (1000, 6*64), scale=4))

        for enemy in self.enemies:
            speed = random.randint(1, 5)
            animation_speed = speed/20
            enemy.rect.x -= speed
            enemy.animation_speed = animation_speed
            enemy.render(direction=-1)

        self.enemies = list(filter(lambda x: x.rect.x > -100, self.enemies))

    def handle_mouse(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.switch_btn = True
            self.play_icon_rect.centery = 298
            if pygame.mouse.get_pressed()[0]:
                self.play = True
                self.next_state = GameStates.MAIN_GAME
                self.done = True
        else:
            self.switch_btn = False
            self.play_icon_rect.centery = 295

    def entry(self, score=0):
        self.score = self.score_font.render(f"Score:{score}", True, "#0696DB")
        self.score_rect = self.score.get_rect(center=(480, 276))

    def update(self,**kwargs):
        # self.entry()
        self.screen.blit(self.bg_img, self.bg_rect)
        for block in self.blocks:
            self.screen.blit(block['sprite'], block['rect'])

        self.player_update()
        self.enemy_update()

        self.screen.blit(self.title1, self.title_rect1)
        self.screen.blit(self.title2, self.title_rect2)
        self.screen.blit(self.title3, self.title_rect3)
        self.screen.blit(self.score, self.score_rect)
        # self.handle_mouse()
        
        
