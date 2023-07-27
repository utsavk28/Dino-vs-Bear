import sys
import pygame
from .MainGame import MainGame
from .Menu import Menu
from .GameOver import GameOver
from .StateMachine.StateMachine import StateMachine
from .enum import GameStates

class Game:
    def __init__(self):
        pygame.init()
        self.width = 960
        self.height = 640
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("DINO Vs BEAR")
        self.clock = pygame.time.Clock()
        self.state_machine = StateMachine(
            {
                GameStates.MENU : Menu(),
                GameStates.MAIN_GAME : MainGame(),
                GameStates.GAME_OVER : GameOver(),
            },
            GameStates.MENU
        )

    def run(self):
        while True:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.state_machine.update()
            pygame.display.update()
            self.clock.tick(self.FPS)
