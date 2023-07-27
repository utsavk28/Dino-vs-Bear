from ..StateMachine.State import State
from ..enum import PlayerStates
from ..utils.constants import ZERO_VECTOR


class PlayerIdleState(State):
    def __init__(self):
        super().__init__(PlayerStates.IDLE, [
            PlayerStates.HURT, PlayerStates.KICK, PlayerStates.WALK])

    def update(self, velocity, isKicking=False, isHurt=False,**kwargs):
        isWalking = (velocity.magnitude() > 0)
        self.done = isHurt or isWalking or isKicking
        if isHurt:
            self.next_state = PlayerStates.HURT
        elif isKicking:
            self.next_state = PlayerStates.KICK
        elif isWalking:
            self.next_state = PlayerStates.WALK


class PlayerWalkState(State):
    def __init__(self):
        super().__init__(PlayerStates.WALK, [
            PlayerStates.HURT, PlayerStates.KICK, PlayerStates.IDLE])

    def update(self, velocity, isKicking=False, isHurt=False,**kwargs):
        isDoneWalking = (velocity.magnitude() == 0)
        self.done = isHurt or isDoneWalking or isKicking
        if isHurt:
            self.next_state = PlayerStates.HURT
        elif isKicking:
            self.next_state = PlayerStates.KICK
        elif isDoneWalking:
            self.next_state = PlayerStates.IDLE


class PlayerHurtState(State):
    def __init__(self):
        super().__init__(PlayerStates.HURT, [PlayerStates.IDLE])
        self.cooldown = 2
        
    def entry(self,**kwargs) :
        self.cooldown = 3
        
    def update(self,**kwargs):
        # print(self.cooldown)
        self.cooldown -= 0.05
        if self.cooldown < 0:
            self.done = True
            self.next_state = PlayerStates.IDLE

class PlayerKickState(State):
    def __init__(self):
        super().__init__(PlayerStates.KICK, [
            PlayerStates.IDLE, PlayerStates.HURT])

    def update(self, isDoneKicking=False, isHurt=None,**kwargs):
        self.done = isDoneKicking or isHurt
        if isHurt :
            self.next_state = PlayerStates.HURT
        elif isDoneKicking:
            self.next_state = PlayerStates.IDLE
