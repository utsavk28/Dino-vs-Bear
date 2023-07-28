import pygame
from ..StateMachine.StateMachine import StateMachine
from ..Sprite.SpriteManager import SpriteManager
from ..enum import PlayerStates
from .PlayerState import *
from ..Components.Controller import Controller
from ..Components.Position import Position
from ..Components.Stats import Stats
from .PlayerHealthBar import PlayerHealthBar
from ..utils.constants import PLAYER_CONSTANTS


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
        self.pos = Position(
            PLAYER_CONSTANTS['pos'], PLAYER_CONSTANTS['dim'], self.scale, PLAYER_CONSTANTS['speed'])
        self.state_machine = StateMachine(playerState, PlayerStates.IDLE)
        self.sprite_manager = SpriteManager(
            path, self.state2sprite[PlayerStates.IDLE], self.pos.pos, self.scale, 0.1, False)
        self.rect = self.sprite_manager.current_sprite.rect
        self.stats = Stats(
            PLAYER_CONSTANTS['health'], PLAYER_CONSTANTS['damage'])
        self.direction = 1
        self.player_health_bar = PlayerHealthBar(self.stats.health_percent)

    def set_direction(self, direction):
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1
        if direction:
            self.direction = direction

    def render(self):
        self.sprite_manager.render()
        self.player_health_bar.render()

    def update(self):
        self.controller.update()
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
        self.player_health_bar.update(self.stats.health_percent)
