from ..StateMachine.State import State
from ..StateMachine.StateMachine import StateMachine
from ..enum import EnemyMoveStates


class EnemyIdleState(State):
    def __init__(self):
        super().__init__(EnemyMoveStates.IDLE, [
            EnemyMoveStates.ATTACK, EnemyMoveStates.HURT, EnemyMoveStates.WALK])

    def update(self, isHurt=False, isWalking=False, isAttacking=False, **kwargs):
        self.done = isHurt or isWalking or isAttacking
        if isHurt:
            self.next_state = EnemyMoveStates.HURT
        elif isAttacking:
            self.next_state = EnemyMoveStates.ATTACK
        elif isWalking:
            self.next_state = EnemyMoveStates.WALK


class EnemyAttackState(State):
    def __init__(self):
        super().__init__(EnemyMoveStates.ATTACK, [
            EnemyMoveStates.IDLE, EnemyMoveStates.HURT, EnemyMoveStates.WALK])

    def update(self, isHurt=False, isDoneAttacking=False, isChasing=False, **kwargs):
        self.done = isHurt or isDoneAttacking
        if isHurt:
            self.next_state = EnemyMoveStates.HURT
        elif isChasing:
            self.next_state = EnemyMoveStates.WALK
        elif isDoneAttacking:
            self.next_state = EnemyMoveStates.IDLE


class EnemyHurState(State):
    def __init__(self):
        super().__init__(EnemyMoveStates.HURT, [EnemyMoveStates.IDLE])

    def update(self, isDoneBeingHurt=False, **kwargs):
        self.done = isDoneBeingHurt
        if isDoneBeingHurt:
            self.next_state = EnemyMoveStates.IDLE


class EnemyWalkState(State):
    def __init__(self):
        super().__init__(EnemyMoveStates.WALK, [
            EnemyMoveStates.IDLE, EnemyMoveStates.ATTACK, EnemyMoveStates.HURT])

    def update(self, isHurt=False, isDoneWalking=False, isAttacking=False, **kwargs):
        self.done = isHurt or isDoneWalking or isAttacking
        if isHurt:
            self.next_state = EnemyMoveStates.HURT
        elif isAttacking:
            self.next_state = EnemyMoveStates.ATTACK
        elif isDoneWalking:
            self.next_state = EnemyMoveStates.IDLE
