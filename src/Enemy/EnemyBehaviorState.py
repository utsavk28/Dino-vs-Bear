from src.utils.constants import ZERO_VECTOR
from ..StateMachine.State import State
from ..enum import EnemyBehaviorStates
from .EnemyMoveState import *
from ..utils.utils import distance2v, random_pos_in_radius
import random
import pygame


empty_res = {
    'velocity': pygame.Vector2(),
    'kwargs': {}
}


class EnemyBehaviourIdleState(State):
    def __init__(self):
        super().__init__(EnemyBehaviorStates.IDLE, [
            EnemyBehaviorStates.CHASE, EnemyBehaviorStates.HURT, EnemyBehaviorStates.ATTACK])
        self.states = {
            'idle': False,
            'walk': False
        }
        self.idleStateCounter = None
        self.walkingDest = None
        self.runIdleState()

    def entry(self, **kwargs):
        self.idleStateCounter = random.randint(3, 5)
        self.walkingDest = None
        self.states = {
            'idle': True,
            'walk': False
        }

    def runIdleState(self):
        self.turnStateOnAndOthersOff('idle')
        self.idleStateCounter = random.randint(3, 5)

    def runWalkState(self, pos):
        self.turnStateOnAndOthersOff('walk')
        self.walkingDest = random_pos_in_radius(pos)

    def turnStateOnAndOthersOff(self, onState):
        for state in self.states.keys():
            self.states[state] = False
        self.states[onState] = True

    def internalStateUpdate(self, pos):
        kwargs = {}
        velocity = pygame.math.Vector2()
        if self.states['idle']:
            if self.idleStateCounter > 0:
                self.idleStateCounter -= 0.05
            else:
                self.runWalkState(pos)
                kwargs["isWalking"] = True
        elif self.states['walk']:
            velocity = self.walkingDest - pos
            if velocity.magnitude() < 0.5:
                velocity = pygame.math.Vector2()
                self.runIdleState()
                kwargs["isDoneWalking"] = True
        return {
            "velocity": velocity,
            "kwargs": kwargs
        }

    def stateChangeUpdate(self, pos, player_pos):
        dist = distance2v(pos, player_pos)
        isPlayerInChaseRadius = False
        isPlayerInAttackRadius = False
        if dist < 100:
            isPlayerInAttackRadius = True
        elif dist < 200:
            isPlayerInChaseRadius = True
        self.done = isPlayerInChaseRadius or isPlayerInAttackRadius
        if isPlayerInAttackRadius:
            self.next_state = EnemyBehaviorStates.ATTACK
        elif isPlayerInChaseRadius:
            self.next_state = EnemyBehaviorStates.CHASE

    def update(self, pos, player_pos, isHurt=False, **kwargs):
        self.done = isHurt
        if self.done:
            self.next_state = EnemyBehaviorStates.HURT
        else:
            self.stateChangeUpdate(pos, player_pos)
        if self.done:
            return empty_res
        res = self.internalStateUpdate(pos)
        return res


class EnemyBehaviourChaseState(State):
    def __init__(self):
        super().__init__(EnemyBehaviorStates.CHASE, [
            EnemyBehaviorStates.IDLE, EnemyBehaviorStates.ATTACK])

    def internalStateUpdate(self, pos, player_pos):
        kwargs = {
            'isWalking': True
        }
        velocity = player_pos - pos
        return {
            "velocity": velocity,
            "kwargs": kwargs
        }

    def stateChangeUpdate(self, pos, player_pos):
        dist = distance2v(pos, player_pos)
        isPlayerOutOfChaseRadius = False
        isPlayerInAttackRadius = False
        if dist < 75:
            isPlayerInAttackRadius = True
        elif dist > 250:
            isPlayerOutOfChaseRadius = True
        self.done = isPlayerOutOfChaseRadius or isPlayerInAttackRadius
        if isPlayerInAttackRadius:
            self.next_state = EnemyBehaviorStates.ATTACK
        elif isPlayerOutOfChaseRadius:
            self.next_state = EnemyBehaviorStates.IDLE

    def update(self, pos, player_pos, isHurt=False, **kwargs):
        self.done = isHurt
        if self.done:
            self.next_state = EnemyBehaviorStates.HURT
        else:
            self.stateChangeUpdate(pos, player_pos)
            if self.done:
                return {
                    'velocity': ZERO_VECTOR,
                    'kwargs': {
                        'isDoneWalking': True
                    }
                }
        res = self.internalStateUpdate(pos, player_pos)
        return res


class EnemyBehaviourAttackState(State):
    def __init__(self):
        super().__init__(EnemyBehaviorStates.ATTACK,
                         [EnemyBehaviorStates.CHASE])
        self.enter = True

    def update(self, isPlayerInChaseRadius):
        self.done = isPlayerInChaseRadius
        if isPlayerInChaseRadius:
            self.next_state = EnemyBehaviorStates.CHASE

    def internalStateUpdate(self, pos, player_pos, **kwargs):
        dist = distance2v(pos, player_pos)
        velocity = player_pos - pos
        # print(velocity,dist)
        if dist < 64:
            velocity.x = 0
        kwargs = {}
        if self.enter:
            self.enter = False
            kwargs = {
                'isAttacking': True
            }

        return {
            "velocity": velocity,
            "kwargs": kwargs
        }

    def exit(self, **kwargs):
        self.enter = True

    def stateChangeUpdate(self, pos, player_pos):
        dist = distance2v(pos, player_pos)
        isPlayerInChaseRadius = False
        if dist > 125:
            isPlayerInChaseRadius = True
        self.done = isPlayerInChaseRadius
        if isPlayerInChaseRadius:
            self.next_state = EnemyBehaviorStates.CHASE

    def update(self, pos, player_pos, isHurt=False, **kwargs):
        self.done = isHurt
        if self.done:
            self.next_state = EnemyBehaviorStates.HURT
        else:
            self.stateChangeUpdate(pos, player_pos)
        if self.done:
            return {
                'velocity': ZERO_VECTOR,
                'kwargs': {
                    'isChasing': True,
                    'isDoneAttacking': True
                }
            }
        res = self.internalStateUpdate(pos, player_pos)
        return res


class EnemyBehaviourHurtState(State):
    def __init__(self):
        super().__init__(EnemyBehaviorStates.HURT,
                         [EnemyBehaviorStates.IDLE])
        self.cooldown = None
        self.enter = True
        self.direction = None

    def entry(self, **kwargs):
        self.direction = kwargs['direction']
        self.cooldown = 3

    def exit(self, **kwargs):
        self.enter = True
        return {}

    def update(self, **kwargs):
        res = {
            'velocity': pygame.math.Vector2(self.direction, 0),
            'bypass_direction': True,
            'speed': 5,
            'kwargs': {}
        }
        if self.enter:
            self.enter = False
            res['kwargs'] = {
                'isHurt': True
            }
        self.cooldown -= 0.05
        if self.cooldown < 0:
            self.done = True
            self.next_state = EnemyBehaviorStates.IDLE
            res['kwargs']['isDoneBeingHurt'] = True

        return res
