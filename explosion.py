import pygame

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 20  # Duration of the explosion (in frames)

    def draw(self, screen):
        if self.timer > 0:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 30 - self.timer // 2)  # Red color
            self.timer -= 1
