class State :
    def __init__(self,current_state,options) :
        self.current_state = current_state
        self.options = options
        self.next_state = None
        self.done = False
    
    def update(self) :
        pass
    
    def entry(self,**kwargs) :
        return {}
    
    def exit(self,**kwargs) :
        return {}