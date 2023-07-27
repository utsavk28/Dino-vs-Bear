import pygame
from ..StateMachine.StateMachine import StateMachine
from ..Sprite.SpriteManager import SpriteManager
from ..enum import PlayerStates
from .PlayerState import *
from ..Components.Controller import Controller
from ..Components.Position import Position
from ..Components.Stats import Stats


class Player:
    def __init__(self, path, scale):
        self.scale = 1.5*scale
        playerState = {
            PlayerStates.IDLE: PlayerIdleState(),
            PlayerStates.HURT: PlayerHurtState(),
            PlayerStates.KICK: PlayerKickState(),
            PlayerStates.WALK: PlayerWalkState(),
        }
        self.state2sprite = {
            PlayerStates.IDLE: "idle",
            PlayerStates.HURT: "hurt",
            PlayerStates.KICK: "kick",
            PlayerStates.WALK: "walk",
        }
        self.screen = pygame.display.get_surface()
        self.controller = Controller()
        self.pos = Position((300, 400), (24, 24), self.scale, 2)
        self.state_machine = StateMachine(playerState, PlayerStates.IDLE)
        self.sprite_manager = SpriteManager(
            path, self.state2sprite[PlayerStates.IDLE], self.pos.pos, self.scale, 0.1, False)
        self.rect = self.sprite_manager.current_sprite.rect
        self.stats = Stats(1000, 50)
        self.direction = 1
        self.full_health_info = {
            'points': [[10, 10], [300, 10], [260, 30], [10, 30]],
        }
        self.curr_health_info = {
            'points': [[10, 10], [300, 10], [260, 30], [10, 30]],
            'offset': [[2, 1], [-8, 1], [-2, -1], [2, -1]],
        }
        self.calc_health(self.stats.health_percent)

    def calc_health(self, health_percent=100):
        for i in range(4):
            for j in range(2):
                self.curr_health_info['points'][i][j] = self.full_health_info['points'][i][j] + \
                    self.curr_health_info['offset'][i][j]
        for i in range(1, 3):
            self.curr_health_info['points'][i][0] *= health_percent/100

    def set_direction(self, direction):
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1
        if direction:
            self.direction = direction

    def render(self):
        self.sprite_manager.render()

        pygame.draw.polygon(self.screen, "#ffffff",
                            self.full_health_info['points'])
        pygame.draw.polygon(self.screen, "#8a0303",
                            self.curr_health_info['points'])

    def update(self):
        self.controller.update()

        # self.pos.updateVelocity(self.controller.direction)
        # self.pos.update()

        kwargs = {}
        if self.state_machine.current_state in [PlayerStates.WALK, PlayerStates.IDLE]:
            kwargs['isKicking'] = self.controller.attack
        elif self.state_machine.current_state == PlayerStates.KICK:
            if self.controller.attack == False:
                kwargs['isDoneKicking'] = True
            self.controller.reset_direction()

        kwargs['velocity'] = self.controller.direction
        self.pos.updateVelocity(self.controller.direction)
        self.pos.update()
        self.set_direction(self.pos.velocity.x)

        self.state_machine.update(**kwargs)
        newState = None
        if self.state_machine.isStateChanged:
            newState = self.state2sprite[self.state_machine.current_state]
        self.sprite_manager.update(pos=self.pos.pos, new_state=newState,
                                   direction=self.direction, health_percent=self.stats.health_percent)
        self.calc_health(self.stats.health_percent)
        # self.calc_health(50)
        # print(self.state_machine.current_state)
