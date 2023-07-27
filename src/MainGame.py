import sys
import copy
import pygame
import random
from src.Enemy.Enemy import Enemy
from src.Player.Player import Player
from src.Map import Map
from .enum import PlayerStates, EnemyBehaviorStates, GameStates
from .StateMachine.State import State

random.seed(5)


class MainGame(State):
    def __init__(self):
        super().__init__(GameStates.MAIN_GAME, [GameStates.GAME_OVER])
        self.screen = pygame.display.get_surface()
        self.enemies_sprite = [
            "res/graphics/characters/Pink_Monster",
            "res/graphics/characters/Owlet_Monster",
            "res/graphics/characters/Dude_Monster",
        ]
        self.enemies = [
            Enemy("res/graphics/characters/Pink_Monster", (445, 332), 3),
        ]
        self.player = Player("res/graphics/characters/mort", scale=2)
        self.map = Map()
        self.enemy_count = len(self.enemies)
        self.score = 0

    def game_update(self):
        while len(self.enemies) < self.enemy_count:
            self.enemies.append(Enemy(random.choice(
                self.enemies_sprite), (random.randint(100, 860), random.randint(100, 540)), 3))

        self.map.update()
        for enemy in self.enemies:
            enemy.update(self.player.pos.pos)
        self.player.update()

    def render(self):
        self.map.render()
        for enemy in self.enemies:
            enemy.render()
        self.player.render()

    def interaction_update(self):
        curr_state = {
            'player': self.player.state_machine.current_state,
            'enemies': list(map(lambda x: x.behavior_state_machine.current_state, self.enemies))
        }
        new_state = copy.deepcopy(curr_state)

        for i, enemy in enumerate(self.enemies):
            if curr_state['player'] == PlayerStates.KICK and self.player.rect.colliderect(enemy.rect):
                direction = 1 if self.player.rect.x < enemy.rect.x else -1
                if self.player.direction == direction:
                    new_state['enemies'][i] = EnemyBehaviorStates.HURT

        for i, enemy in enumerate(self.enemies):
            if new_state['enemies'][i] == EnemyBehaviorStates.ATTACK and self.player.rect.colliderect(enemy.rect):
                direction = 1 if enemy.rect.x < self.player.rect.x else -1
                if enemy.direction == direction:
                    new_state['player'] = PlayerStates.HURT
                    break

        for i, enemy in enumerate(self.enemies):
            if new_state['enemies'][i] == EnemyBehaviorStates.HURT and curr_state['enemies'][i] != new_state['enemies'][i]:
                behaviour_kwargs = {'pos': enemy.pos.pos,
                                    'player_pos': self.player.pos.pos, 'isHurt': True,
                                    'direction': self.player.direction}
                res = enemy.behavior_state_machine.update(**behaviour_kwargs)
                enemy.pos.updateVelocity(res['velocity'])
                enemy.move_state_machine.update(**res['kwargs'])
                newState = None
                if enemy.move_state_machine.isStateChanged:
                    newState = enemy.moveState2sprite[enemy.move_state_machine.current_state]
                enemy.stats.update(self.player.stats.damage)
                enemy.sprite_manager.update(
                    pos=enemy.pos.pos, new_state=newState, direction=enemy.direction, health_percent=enemy.stats.health_percent)

        if curr_state['player'] != new_state['player'] and new_state['player'] == PlayerStates.HURT:
            kwargs = {
                'velocity': self.player.controller.direction,
                'isHurt': True
            }
            self.player.state_machine.update(**kwargs)
            newState = None
            if self.player.state_machine.isStateChanged:
                newState = self.player.state2sprite[self.player.state_machine.current_state]
            self.player.sprite_manager.update(
                pos=self.player.pos.pos, new_state=newState, direction=self.player.direction)
            self.player.stats.update(enemy.stats.damage)
            if self.player.stats.health <= 0:
                self.done = True
                self.next_state = GameStates.GAME_OVER

    def clear(self):
        incr_count = len(self.enemies)
        self.enemies = list(filter(lambda x: x.stats.health >
                            0 or x.behavior_state_machine.current_state == EnemyBehaviorStates.HURT, self.enemies))
        incr_count -= len(self.enemies)
        self.score += incr_count
        self.enemy_count += incr_count*0.3

    def exit(self):
        return {
            'score': self.score
        }

    def update(self, **kwargs):
        self.game_update()
        self.interaction_update()
        self.render()
        self.clear()
