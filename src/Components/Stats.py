class Stats:
    def __init__(self, health, damage):
        self.total_health = health
        self.health = health
        self.damage = damage
        self.health_percent = None
        self.calc_health_percent()
        
    def calc_health_percent(self) :
        self.health_percent = int(100*self.health//self.total_health)
    
    def update(self, damage=0):
        self.health = max(self.health-damage,0)
        self.calc_health_percent()
    
