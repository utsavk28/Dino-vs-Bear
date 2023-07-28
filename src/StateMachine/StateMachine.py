class StateMachine :
    def __init__(self,states,current_state) :
        self.states = states
        self.current_state = current_state
        self.current_state_exec = self.states[self.current_state]
        self.isStateChanged = False
        
    def update(self,**kwargs) :
        self.isStateChanged = False
        res = self.current_state_exec.update(**kwargs)
        if self.current_state_exec.done :
            res_exit = self.current_state_exec.exit(**kwargs)
            if res_exit is None :
                res_exit = {}
            self.switch_state()    
            self.current_state_exec.entry(**res_exit,**kwargs)
            
        return res
    
    def switch_state(self) :
        self.current_state_exec.done = False
        self.current_state = self.current_state_exec.next_state
        self.current_state_exec = self.states[self.current_state]
        self.isStateChanged = True
