from enum import Enum

class EnemyMoveStates(Enum) :
    IDLE = 1
    ATTACK = 2
    DEATH = 3
    HURT = 4
    WALK = 5
    
class EnemyBehaviorStates(Enum) :
    IDLE = 1
    CHASE = 2
    ATTACK = 3
    HURT = 4
    DEATH = 5
    
class PlayerStates(Enum) :
    HURT = 1
    IDLE = 2
    KICK = 3
    RUN = 4
    WALK = 5
    
class GameStates(Enum) :
    MENU = 1
    MAIN_GAME = 2
    GAME_OVER = 3