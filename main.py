import pygame
import random
from asteroid import Asteroid
from missile import Missile
from explosion import Explosion
from utils import generate_problem

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

# Game variables
clock = pygame.time.Clock()
running = True
user_input = ''
asteroids = []
missiles = []
base_x, base_y = 400, 550
score = 0
explosions = []
countdown = 60

# game over function
def show_game_over():
    global running, game_running
    screen.fill(WHITE)
    game_over_text = font.render("GAME OVER", True, RED)
    final_score_text = small_font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (250, 250))
    screen.blit(final_score_text, (300, 350))
    pygame.display.flip()
    pygame.time.wait(3000)  # Show the Game Over screen for 3 seconds

    # Flashing "Press S to start a new game"
    restart = True
    while restart:
        screen.fill(WHITE)
        screen.blit(game_over_text, (250, 250))
        screen.blit(final_score_text, (300, 350))
        
        # Create a slow-flashing effect by alternating text visibility
        if pygame.time.get_ticks() // 500 % 2 == 0:  # Blinks every 500 ms
            restart_text = small_font.render("Press S to start a new game", True, BLACK)
            screen.blit(restart_text, (200, 450))
        
        pygame.display.flip()
        
        # Event handling for restarting or quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_running = False  # Exit the entire program
                restart = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    restart = False  # Exit the restart loop
                    running = True  # Reset the running flag
                    initialize_game()  # Reinitialize the game state

# Function to initialize or reset the game state
def initialize_game():
    global countdown, score, asteroids, missiles, user_input, explosions, running
    countdown = 60  # Reset the timer to 60 seconds
    score = 0  # Reset the score
    asteroids = []  # Clear the asteroid list
    missiles = []  # Clear the missile list
    explosions = []  # Clear the explosions
    user_input = ''  # Clear the user input
    running = True  # Set the running flag to True

# Initialize game
initialize_game()

# Main program loop
game_running = True
while game_running:
    # Main game loop
    while running:
        screen.fill(WHITE)
        
        # Decrement the timer
        if countdown > 0:
            countdown -= 1 / 60  # Decrease by one second per frame (assuming 60 FPS)
        else:
            running = False  # End the game when time runs out

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
            y = 0  # Always start at the top of the screen
            new_asteroid = Asteroid(x, y, problem, answer)
        
            # Check for overlap with existing asteroids
            overlap = False
            for asteroid in asteroids:
                if abs(new_asteroid.x - asteroid.x) < 50 and abs(new_asteroid.y - asteroid.y) < 50:
                    overlap = True
                    break

            # Add the asteroid only if there's no overlap
            if not overlap:
                asteroids.append(new_asteroid)

        # Move and draw asteroids
        for asteroid in asteroids[:]:
            asteroid.move()
            asteroid.draw(screen)

            # Check if asteroid reaches the bottom
            if asteroid.y > 600:  # Assuming screen height is 600
                explosions.append(Explosion(asteroid.x, 600))  # Explosion at the bottom
                asteroids.remove(asteroid)  # Remove the asteroid
                score -= 1  # Deduct a point

        # Move and draw missiles
        for missile in missiles[:]:
            missile.move()
            missile.draw(screen)

            # Check if the missile has reached its target
            if abs(missile.x - missile.target.x) < 5 and abs(missile.y - missile.target.y) < 5:
                explosions.append(Explosion(missile.target.x, missile.target.y))  # Create explosion
                missiles.remove(missile)  # Remove the missile
                if missile.target in asteroids:
                    asteroids.remove(missile.target)  # Remove the asteroid

        # Move and draw explosions
        for explosion in explosions[:]:
            explosion.draw(screen)
            if explosion.timer <= 0:  # Remove explosion once the timer ends
                explosions.remove(explosion)
        
        # Render user input
        input_text = font.render(user_input, True, BLACK)
        screen.blit(input_text, (350, 500))

        # Display score
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display countdown timer
        timer_text = small_font.render(f"Time: {int(countdown)}", True, BLACK)
        screen.blit(timer_text, (10, 50))  # Slightly below the score

        pygame.display.flip()
        clock.tick(60)
        
    # Call the Game Over function
    if game_running:
        show_game_over()

pygame.quit()
