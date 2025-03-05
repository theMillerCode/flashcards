import pygame

class Asteroid:
    def __init__(self, x, y, problem, answer):
        self.x = x
        self.y = y
        self.problem = problem
        self.answer = answer
        self.speed = 1
        self.small_font = pygame.font.Font(None, 36)

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        problem_text = self.small_font.render(self.problem, True, (0, 0, 0))  # Black color
        screen.blit(problem_text, (self.x, self.y))
