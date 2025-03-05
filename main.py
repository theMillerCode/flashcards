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

# Updated Missile class
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

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 5, 10))

# Explosion class
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 20  # Duration of the explosion (in frames)

    def draw(self):
        if self.timer > 0:
            pygame.draw.circle(screen, RED, (self.x, self.y), 30 - self.timer // 2)
            self.timer -= 1


# Function to create a random math problem
def generate_problem():
    num1 = random.randint(0, 12)
    num2 = random.randint(1, 12)  # Avoid zero for division
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        problem = f"{num1} + {num2}"
        answer = str(num1 + num2)
    elif operation == '-':
        num1, num2 = max(num1, num2), min(num1, num2)  # Ensure num1 >= num2
        problem = f"{num1} - {num2}"
        answer = str(num1 - num2)
    elif operation == '*':
        problem = f"{num1} * {num2}"
        answer = str(num1 * num2)
    else:  # Division
        num2 = random.randint(1, 12)  # Ensure divisor is not zero
        num1 = num2 * random.randint(1, 12)  # Make num1 a multiple of num2
        problem = f"{num1} / {num2}"
        answer = str(num1 // num2)  # Integer division
    return problem, answer


explosions = []

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
                        missiles.append(Missile(base_x, base_y, asteroid))  # Target this asteroid
                        user_input = ''
                        score += 1
                        break
                user_input = ''
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

    # Spawn new asteroids (only if fewer than 5 on screen)
    if len(asteroids) < 5 and random.random() < 0.01:
        problem, answer = generate_problem()
        x = random.randint(50, 750)
        asteroids.append(Asteroid(x, 0, problem, answer))

    # Move and draw asteroids
    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw()

    # Move and draw missiles
    for missile in missiles[:]:
        missile.move()
        missile.draw()
        # Check if the missile has reached its target
        if abs(missile.x - missile.target.x) < 5 and abs(missile.y - missile.target.y) < 5:
            explosions.append(Explosion(missile.target.x, missile.target.y))  # Create explosion
            missiles.remove(missile)  # Remove the missile
            if missile.target in asteroids:
                asteroids.remove(missile.target)  # Remove the asteroid

    # Move and draw explosions
    for explosion in explosions[:]:
        explosion.draw()
        if explosion.timer <= 0:  # Remove explosion once the timer ends
            explosions.remove(explosion)
    
    # Render user input
    input_text = font.render(user_input, True, BLACK)
    screen.blit(input_text, (350, 500))

    # Display score
    score_text = small_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
