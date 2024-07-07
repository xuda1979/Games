import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 60, 60
AMMO_WIDTH, AMMO_HEIGHT = 10, 20
PLAYER_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)
AMMO_COLOR = (0, 0, 255)
AWARD_COLORS = [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 128, 128), (128, 0, 128)]
BACKGROUND_COLOR = (255, 255, 255)
OBSTACLE_SPEED = 5
AWARD_SPEED = 3
AMMO_SPEED = 10
INVINCIBILITY_TIME = 2  # 2 seconds of invincibility

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Plane Game')

# Font for score and game over text
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.draw_player()
        self.invincible = False
        self.invincibility_start_time = 0

    def draw_player(self):
        # Drawing a simple plane-like shape facing upward
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        # Body
        pygame.draw.polygon(self.image, PLAYER_COLOR, [(30, 0), (40, 20), (30, 15), (20, 20)])
        # Wings
        pygame.draw.rect(self.image, PLAYER_COLOR, (10, 20, 40, 10))
        # Tail
        pygame.draw.polygon(self.image, PLAYER_COLOR, [(25, 20), (35, 20), (30, 40)])

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 5

    def make_invincible(self):
        self.invincible = True
        self.invincibility_start_time = time.time()

    def check_invincibility(self):
        if self.invincible and (time.time() - self.invincibility_start_time > INVINCIBILITY_TIME):
            self.invincible = False

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.draw_obstacle()

    def draw_obstacle(self):
        # Drawing a simple plane-like shape facing downward
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        # Body
        pygame.draw.polygon(self.image, OBSTACLE_COLOR, [(30, 60), (40, 40), (30, 45), (20, 40)])
        # Wings
        pygame.draw.rect(self.image, OBSTACLE_COLOR, (10, 30, 40, 10))
        # Tail
        pygame.draw.polygon(self.image, OBSTACLE_COLOR, [(25, 40), (35, 40), (30, 20)])

    def update(self):
        self.rect.y += OBSTACLE_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT)

# Award class
class Award(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.y += AWARD_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), -self.rect.height)

# Ammo class
class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((AMMO_WIDTH, AMMO_HEIGHT))
        self.image.fill(AMMO_COLOR)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def update(self):
        self.rect.y -= AMMO_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Create player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT)
player_group = pygame.sprite.Group()
player_group.add(player)

# Create obstacles
obstacles = pygame.sprite.Group()
for _ in range(10):
    x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
    y = random.randint(-SCREEN_HEIGHT, 0)
    obstacle = Obstacle(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacles.add(obstacle)

# Create awards
awards = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH)
    y = random.randint(-SCREEN_HEIGHT, 0)
    color = random.choice(AWARD_COLORS)
    award = Award(x, y, PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2, color)
    awards.add(award)

# Create ammo group
ammo_group = pygame.sprite.Group()

# Initialize score and lives
score = 0
lives = 5

# Main game loop
running = True
game_over = False
game_over_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                ammo = Ammo(player.rect.centerx, player.rect.top)
                ammo_group.add(ammo)

    keys = pygame.key.get_pressed()
    if not game_over:
        player.update(keys)
        obstacles.update()
        awards.update()
        ammo_group.update()

        player.check_invincibility()

        # Check for collisions with obstacles
        if not player.invincible and pygame.sprite.spritecollideany(player, obstacles):
            lives -= 1
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT)  # Reset player position
            player.make_invincible()
            if lives == 0:
                game_over = True
                game_over_time = time.time()

        # Check for collisions with awards
        award_collisions = pygame.sprite.spritecollide(player, awards, dokill=True)
        for award in award_collisions:
            score += 10
            x = random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, 0)
            color = random.choice(AWARD_COLORS)
            new_award = Award(x, y, PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2, color)
            awards.add(new_award)

        # Check for collisions between ammo and obstacles
        ammo_obstacle_collisions = pygame.sprite.groupcollide(ammo_group, obstacles, True, True)
        for collision in ammo_obstacle_collisions:
            x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, 0)
            new_obstacle = Obstacle(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            obstacles.add(new_obstacle)

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    player_group.draw(screen)
    obstacles.draw(screen)
    awards.draw(screen)
    ammo_group.draw(screen)

    # Draw score and lives
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
    lives_text = font.render(f'Lives: {lives}', True, (0, 0, 0))
    screen.blit(lives_text, (10, 10))

    if game_over:
        game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        if time.time() - game_over_time > 3:
            running = False

    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()



