from ..StateMachine.StateMachine import StateMachine
from ..StateMachine.State import State
from .EnemyMoveState import *
from ..enum import EnemyMoveStates, EnemyBehaviorStates
from ..Sprite.SpriteManager import SpriteManager
from ..Components.Position import Position
from .EnemyBehaviorState import *
import random
from ..Components.Stats import Stats
from ..utils.constants import ENEMY_CONSTANTS, SPRITE_DIM
random.seed(5)


class Enemy:
    def __init__(self, sprite_path, pos, scale=1):
        enemyMoveState = {
            EnemyMoveStates.IDLE: EnemyIdleState(),
            EnemyMoveStates.ATTACK: EnemyAttackState(),
            EnemyMoveStates.HURT: EnemyHurState(),
            EnemyMoveStates.WALK: EnemyWalkState(),
        }
        self.moveState2sprite = {
            EnemyMoveStates.IDLE: "Idle",
            EnemyMoveStates.ATTACK: "Attack1",
            EnemyMoveStates.HURT: "Hurt",
            EnemyMoveStates.WALK: "Walk",
        }
        enemyBehaviorState = {
            EnemyBehaviorStates.IDLE: EnemyBehaviourIdleState(),
            EnemyBehaviorStates.ATTACK: EnemyBehaviourAttackState(),
            EnemyBehaviorStates.CHASE: EnemyBehaviourChaseState(),
            EnemyBehaviorStates.HURT: EnemyBehaviourHurtState(),
        }

        self.move_state_machine = StateMachine(
            enemyMoveState, EnemyMoveStates.IDLE)
        self.behavior_state_machine = StateMachine(
            enemyBehaviorState, EnemyBehaviorStates.IDLE)

        self.pos = Position(pos, SPRITE_DIM, scale)
        self.sprite_manager = SpriteManager(
            sprite_path, self.moveState2sprite[self.move_state_machine.current_state], pos, scale)
        self.rect = self.sprite_manager.current_sprite.rect
        self.speed = self.pos.speed
        self.direction = 1
        self.speed_counter = 0
        self.stats = Stats(
            ENEMY_CONSTANTS['health'], ENEMY_CONSTANTS['damage'])

    def set_direction(self, direction):
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1
        if direction:
            self.direction = direction

    def render(self):
        self.sprite_manager.render()

    def update(self, player_pos):
        behaviour_kwargs = {'pos': self.pos.pos, 'player_pos': player_pos}
        res = self.behavior_state_machine.update(**behaviour_kwargs)
        self.move_state_machine.update(**res['kwargs'])

        self.pos.updateVelocity(res['velocity'])
        self.pos.update()

        if 'speed' in res.keys():
            self.pos.setSpeed(res['speed'])

        if 'bypass_direction' in res.keys():
            if not res['bypass_direction']:
                self.set_direction(self.pos.velocity.x)
                self.speed = 1
                self.speed_counter = 0
            else:
                self.speed_counter -= 1
                if self.speed_counter < 0:
                    self.speed_counter = 10
                    self.speed -= 0.025
        else:
            self.set_direction(self.pos.velocity.x)
            self.speed = 1
            self.speed_counter = 0
        self.pos.setSpeed(self.speed)

        newState = None
        if self.move_state_machine.isStateChanged:
            newState = self.moveState2sprite[self.move_state_machine.current_state]
        self.sprite_manager.update(pos=self.pos.pos, new_state=newState,
                                   direction=self.direction, health_percent=self.stats.health_percent)
