import pygame


class PlayerHealthBar:
    def __init__(self, health_percent=100):
        self.full_health_info = {
            'points': [[10, 10], [300, 10], [260, 30], [10, 30]],
        }
        self.curr_health_info = {
            'points': [[10, 10], [300, 10], [260, 30], [10, 30]],
            'offset': [[2, 1], [-8, 1], [-2, -1], [2, -1]],
        }
        self.screen = pygame.display.get_surface()
        self.calc_health(health_percent)

    def calc_health(self, health_percent=100):
        for i in range(4):
            for j in range(2):
                self.curr_health_info['points'][i][j] = self.full_health_info['points'][i][j] + \
                    self.curr_health_info['offset'][i][j]
        for i in range(1, 3):
            self.curr_health_info['points'][i][0] *= health_percent/100

    def render(self):
        pygame.draw.polygon(self.screen, "#ffffff",
                            self.full_health_info['points'])
        pygame.draw.polygon(self.screen, "#8a0303",
                            self.curr_health_info['points'])

    def update(self, health_percent):
        self.calc_health(health_percent)
