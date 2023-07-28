import pygame
import random

random.seed(5)


class Map:
    def __init__(self):
        self.tiles = []
        self.tileSize = 32
        self.scale = 2
        self.rect_size = (self.tileSize*self.scale, self.tileSize*self.scale)
        self.tile_path = "res/graphics/Tiles"
        self.screen = pygame.display.get_surface()
        self.generate_tiles()

    def generate_tiles(self):
        for i in range(10):
            temp = []
            for j in range(15):
                count = random.randint(1, 8)
                tile_image = pygame.image.load(f"{self.tile_path}/{count}.png")
                tile_image = pygame.transform.scale(tile_image, self.rect_size)
                tile_rect = tile_image.get_rect(
                    topleft=(j*self.tileSize*self.scale, i*self.tileSize*self.scale))
                temp.append({
                    'image': tile_image,
                    'rect': tile_rect
                })
            self.tiles.append(temp)

    def render(self):
        for i in range(10):
            for j in range(15):
                self.screen.blit(
                    self.tiles[i][j]['image'], self.tiles[i][j]['rect'])

    def update(self):
        pass
