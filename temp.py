class Base :
    def __init__(self) :
        pass
    
    def entry(self,**kwargs) :
        print("Base")
        
class Impl(Base) :
    def __init__(self):
        super().__init__()
        
imp = Impl()
imp.entry()