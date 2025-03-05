import pygame

class Missile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target  # Store the target asteroid
        self.speed = 5  # Speed of the missile

    def move(self):
        # Calculate horizontal and vertical distance to target
        dx = self.target.x - self.x
        dy = self.target.y - self.y

        # Calculate the direction to move
        distance = (dx**2 + dy**2)**0.5  # Pythagorean theorem for distance
        if distance != 0:  # Avoid division by zero
            self.x += self.speed * (dx / distance)  # Normalize dx
            self.y += self.speed * (dy / distance)  # Normalize dy

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 5, 10))  # Red color
