import pygame
import random

pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Math Missile Command")

# Set up fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variablessource
clock = pygame.time.Clock()
running = True
user_input = ''
asteroids = []
missiles = []
base_x, base_y = 400, 550
score = 0

# Asteroid class
class Asteroid:
    def __init__(self, x, y, problem, answer):
        self.x = x
        self.y = y
        self.problem = problem
        self.answer = answer
        self.speed = 1

    def move(self):
        self.y += self.speed

    def draw(self):
        problem_text = small_font.render(self.problem, True, BLACK)
        screen.blit(problem_text, (self.x, self.y))

# Missile class
class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 5, 10))

# Function to create a random math problem
def generate_problem():
    num1 = random.randint(0, 12)
    num2 = random.randint(0, 12)
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        problem = f"{num1} + {num2}"
        answer = str(num1 + num2)
    elif operation == '-':
        problem = f"{num1} - {num2}"
        answer = str(num1 - num2)
    elif operation == '*':
        problem = f"{num1} * {num2}"
        answer = str(num1 * num2)
    else:
        problem = f"{num1} / {num2}"
        answer = str(num1 // num2)  # Use integer division for simplicity
    return problem, answer

# Main game loop
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for asteroid in asteroids:
                    if user_input == asteroid.answer:
                        missiles.append(Missile(base_x, base_y))
                        asteroids.remove(asteroid)
                        score += 1
                        break
                user_input = ''
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

    # Spawn new asteroids
    if random.random() < 0.01:
        problem, answer = generate_problem()
        x = random.randint(50, 750)
        asteroids.append(Asteroid(x, 0, problem, answer))

    # Move and draw asteroids
    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw()

    # Move and draw missiles
    for missile in missiles:
        missile.move()
        missile.draw()
        if missile.y < 0:
            missiles.remove(missile)

    # Render user input
    input_text = font.render(user_input, True, BLACK)
    screen.blit(input_text, (350, 500))

    # Display score
    score_text = small_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
