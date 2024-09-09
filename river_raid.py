import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_BASE_SPEED = 5
PLAYER_BOOSTED_SPEED = 8
BULLET_SPEED = 7

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced River Raid")

# Setup clock for FPS
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, [(15, 0), (0, 30), (30, 30)])  # Triangle representing the plane
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = PLAYER_BASE_SPEED
        self.fuel = 100  # Starting fuel

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Increase speed when Shift key is held down
            self.speed = PLAYER_BOOSTED_SPEED
        else:
            self.speed = PLAYER_BASE_SPEED

        if keys[pygame.K_LEFT] and self.rect.left > 100:  # Limit movement to within the riverbanks
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 100:
            self.rect.x += self.speed

    def refuel(self):
        self.fuel = min(100, self.fuel + 30)  # Refill fuel

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()

# Obstacle class (representing ships)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        pygame.draw.rect(self.image, GREEN, [0, 0, 40, 20])  # Simple rectangle for a ship
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(2, 5)  # Random speed for each obstacle

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = -60
            self.rect.x = random.randint(100, WIDTH - 140)

# Fuel class (representing fuel stations)
class Fuel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        pygame.draw.rect(self.image, YELLOW, [0, 0, 30, 40])  # Yellow rectangle for a fuel station
        pygame.draw.line(self.image, RED, (15, 0), (15, 40), 3)  # Vertical red line to resemble a fuel symbol
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2  # Speed for fuel stations

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = -30
            self.rect.x = random.randint(100, WIDTH - 130)

# Bridge class
class Bridge(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((WIDTH - 200, 20))
        pygame.draw.rect(self.image, DARK_GREEN, [0, 0, WIDTH - 200, 20])  # Bridge representation
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Fixed position to match river width
        self.rect.y = y
        self.speed = 2  # Bridge speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = -20

# Function to create game objects
def create_game_objects():
    player = Player()
    obstacles = pygame.sprite.Group()
    fuels = pygame.sprite.Group()
    bridges = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create obstacles, fuel, and bridges
    for i in range(5):
        x = random.randint(100, WIDTH - 140)  # Place within riverbanks
        y = random.randint(-100, -40)
        obstacle = Obstacle(x, y)
        obstacles.add(obstacle)

    for i in range(3):  # Adding fewer fuels and bridges for balance
        fuel_x = random.randint(100, WIDTH - 130)
        fuel_y = random.randint(-300, -40)
        fuel = Fuel(fuel_x, fuel_y)
        fuels.add(fuel)

    # Group all sprites together
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(obstacles)
    all_sprites.add(fuels)
    all_sprites.add(bridges)
    all_sprites.add(bullets)

    return player, obstacles, fuels, bridges, bullets, all_sprites

# Game over function
def game_over(screen, score, successful_shots):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render('Game Over', True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    shots_text = font.render(f'Successful Shots: {successful_shots}', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(shots_text, (WIDTH // 2 - shots_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
def main():
    player, obstacles, fuels, bridges, bullets, all_sprites = create_game_objects()
    
    # Score, level, and successful shots
    score = 0
    level = 1
    successful_shots = 0
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot a bullet when Space key is pressed
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        # Update all sprites
        all_sprites.update()

        # Check for collisions
        if pygame.sprite.spritecollide(player, obstacles, False) or pygame.sprite.spritecollide(player, bridges, False):
            game_over(screen, score, successful_shots)
            running = False

        # Check if player refuels
        if pygame.sprite.spritecollide(player, fuels, True):
            player.refuel()

        # Check if bullets hit obstacles
        hits = pygame.sprite.groupcollide(bullets, obstacles, True, True)
        for hit in hits:
            successful_shots += 1  # Increment the successful shots counter
            score += 10
            # Optionally, add new obstacles
            x = random.randint(100, WIDTH - 140)
            y = random.randint(-100, -40)
            obstacle = Obstacle(x, y)
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        # Decrease fuel over time
        player.fuel -= 0.05  # Slower fuel consumption
        if player.fuel <= 0:
            game_over(screen, score, successful_shots)
            running = False

        # Update score
        score += 1

        # Draw everything
        screen.fill(BLUE)  # Blue background to represent the river

        # Draw the riverbanks
        pygame.draw.rect(screen, DARK_GREEN, [0, 0, 100, HEIGHT])  # Left bank
        pygame.draw.rect(screen, DARK_GREEN, [WIDTH - 100, 0, 100, HEIGHT])  # Right bank

        all_sprites.draw(screen)

        # Display score, fuel, level, and successful shots
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        fuel_text = font.render(f'Fuel: {int(player.fuel)}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        shots_text = font.render(f'Successful Shots: {successful_shots}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(fuel_text, (10, 50))
        screen.blit(level_text, (10, 90))
        screen.blit(shots_text, (10, 130))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
