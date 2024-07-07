import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
BALL_COLOR = (200, 200, 200)
PADDLE_COLOR = (0, 200, 200)
BUTTON_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
AWARD_COLOR = (0, 255, 0)
AWARD_SHINE_COLOR = (0, 200, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout Game')

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Paddle
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(SCREEN_WIDTH // 2 - paddle_width // 2, SCREEN_HEIGHT - 30, paddle_width, paddle_height)
paddle_speed = 10

# Balls
ball_radius = 10
balls = [pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
ball_speeds = [[5, -5]]

# Awards
awards = []
award_speed = 5

# Grid layout
def create_grid(level):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    hits_needed = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    colors = [YELLOW, GREEN, ORANGE, PINK]

    # Add more bricks and increase difficulty with level
    for i in range(level * 4 + 10):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT // 2 - 1)
        color = random.choice(colors)
        grid[y][x] = color
        hits_needed[y][x] = level

    return grid, hits_needed

level = 1
grid, hits_needed = create_grid(level)

# Lives
lives = 5

# Button
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
game_active = False

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
            game_active = True
            lives = 5
            level = 1
            grid, hits_needed = create_grid(level)
            balls = [pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
            ball_speeds = [[5, -5]]
            awards = []

    if game_active:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.move_ip(paddle_speed, 0)

        # Ball movement
        for i, ball in enumerate(balls):
            ball.move_ip(ball_speeds[i])

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_speeds[i][0] = -ball_speeds[i][0]
            if ball.top <= 0:
                ball_speeds[i][1] = -ball_speeds[i][1]
            if ball.bottom >= SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    balls = [pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
                    ball_speeds = [[5, -5]]
                    break
                else:
                    game_active = False

            # Ball collision with paddle
            if ball.colliderect(paddle):
                ball_speeds[i][1] = -ball_speeds[i][1]

            # Ball collision with bricks
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if grid[y][x] != BLACK:
                        brick_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        if ball.colliderect(brick_rect):
                            ball_speeds[i][1] = -ball_speeds[i][1]
                            hits_needed[y][x] -= 1
                            if hits_needed[y][x] <= 0:
                                grid[y][x] = BLACK
                                if random.random() < 0.1:  # 10% chance to drop an award
                                    awards.append(pygame.Rect(brick_rect.x, brick_rect.y, GRID_SIZE, GRID_SIZE))

        # Move awards
        for award in awards:
            award.move_ip(0, award_speed)
            if award.colliderect(paddle):
                awards.remove(award)
                new_balls = []
                new_speeds = []
                for ball in balls:
                    for _ in range(10):
                        new_balls.append(ball.copy())
                        new_speeds.append([ball_speeds[0][0] * random.choice([-1, 1]), ball_speeds[0][1] * random.choice([-1, 1])])
                balls.extend(new_balls)
                ball_speeds.extend(new_speeds)
            elif award.bottom >= SCREEN_HEIGHT:
                awards.remove(award)

        # Check if all bricks are cleared
        if all(grid[y][x] == BLACK for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)):
            level += 1
            if level > 10:
                level = 1
            grid, hits_needed = create_grid(level)
            balls = [pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
            ball_speeds = [[5, -5]]
            awards = []

        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = grid[y][x]
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, rect)

        # Draw paddle
        pygame.draw.rect(screen, PADDLE_COLOR, paddle)

        # Draw balls
        for ball in balls:
            pygame.draw.ellipse(screen, BALL_COLOR, ball)

        # Draw awards
        for award in awards:
            pygame.draw.rect(screen, AWARD_COLOR, award)
            pygame.draw.rect(screen, AWARD_SHINE_COLOR, award, 3)

        # Draw lives
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        # Draw level
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH - 120, 10))
    else:
        # Draw start button
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        button_text = font.render("Start", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text, (button_rect.x + 50, button_rect.y + 10))

        # Draw game over text if lives are exhausted
        if lives <= 0:
            game_over_text = large_font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()


