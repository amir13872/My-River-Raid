import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load and play background music
#music_background
music_path = "C:/Users/209/OneDrive/Desktop/project/river raid/photo/sounds.mp3"
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  # Play music in a loop

# Load shooting sound
#shot_sound
shoot_sound = pygame.mixer.Sound("C:/Users/209/OneDrive/Desktop/project/river raid/photo/shut.mp3")
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
FUEL_DECREASE_RATE = 0.05
POWER_UP_DURATION = 5000  # milliseconds

# Colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River Raid Inspired Game")

# Setup clock for FPS
clock = pygame.time.Clock()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #player_logo
        player = "C:/Users/209/OneDrive/Desktop/project/river raid/photo/airplan.png"
        self.image = pygame.image.load(player).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = PLAYER_SPEED
        self.fuel = 100
        self.invulnerable = False


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 100:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 100:
            self.rect.x += self.speed

    def refuel(self):
        self.fuel = min(100, self.fuel + 30)

    def activate_power_up(self, power_type):
        if power_type == "shield":
            self.invulnerable = True

    def deactivate_power_up(self):
        self.invulnerable = False

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
        if self.rect.bottom < 0:
            self.kill()

# Boat class
class Boat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #boat_logo
        boat = "C:/Users/209/OneDrive/Desktop/project/river raid/photo/boat.png"
        self.image = pygame.image.load(boat).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 25))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Helicopter class
class Helicopter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #helicopter_logo
        helicopter = "C:/Users/209/OneDrive/Desktop/project/river raid/photo/helicopter.png"
        self.image = pygame.image.load(helicopter).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 40))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(3, 6)


    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = -20
            self.rect.x = random.randint(100, WIDTH - 140)

# Bridge class
class Bridge(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((WIDTH - 200, 40))
        pygame.draw.rect(self.image, BROWN, [0, 0, WIDTH - 200, 40])
        pygame.draw.rect(self.image, DARK_GREEN, [0, 0, WIDTH - 200, 10])
        pygame.draw.rect(self.image, BROWN, [0, 10, WIDTH - 200, 30])
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = y

    def update(self):
        pass

# Fuel class
class Fuel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the fuel station image 
        #fuel_logo
        fuel_image_path = "C:/Users/209/OneDrive/Desktop/project/river raid/photo/fuel.png"
        self.image = pygame.image.load(fuel_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 40))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()


# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.power_type = power_type
        if power_type == "shield":
            self.image.fill(WHITE)
        elif power_type == "speed":
            self.image.fill(GREEN)
        elif power_type == "multi-shot":
            self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()

# Function to create game objects
def create_game_objects(level):
    player = Player()
    boats = pygame.sprite.Group()
    helicopters = pygame.sprite.Group()
    fuels = pygame.sprite.Group()
    bridges = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    # Generate boats
    for i in range(level + 4):
        x = random.randint(100, WIDTH - 140)
        y = random.randint(-100, -40)
        boat = Boat(x, y)
        boats.add(boat)

    # Generate helicopters
    for i in range(level + 2):
        x = random.randint(100, WIDTH - 140)
        y = random.randint(-300, -40)
        helicopter = Helicopter(x, y)
        helicopters.add(helicopter)

    # Generate fuel depots
    # for i in range(level + 2):
    for i in range(3):
        fuel_x = random.randint(100, WIDTH - 130)
        fuel_y = random.randint(-300, -40)
        fuel = Fuel(fuel_x, fuel_y)
        fuels.add(fuel)

    # Generate power-ups
    for i in range(2 + (level // 5)):
        power_up_x = random.randint(100, WIDTH - 130)
        power_up_y = random.randint(-300, -40)
        power_type = random.choice(["shield", "speed", "multi-shot"])
        power_up = PowerUp(power_up_x, power_up_y, power_type)
        power_ups.add(power_up)

    # Generate bridges
    bridge_y = -40
    bridge = Bridge(bridge_y)
    bridges.add(bridge)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(boats)
    all_sprites.add(helicopters)
    all_sprites.add(fuels)
    all_sprites.add(bridges)
    all_sprites.add(bullets)
    all_sprites.add(power_ups)

    return player, boats, helicopters, fuels, bridges, bullets, power_ups, all_sprites

# Game over function
def game_over(screen, score, kills):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render('Game Over', True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    kills_text = font.render(f'Enemies Destroyed: {kills}', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(kills_text, (WIDTH // 2 - kills_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
# Main game loop
def main():
    level = 1
    player, boats, helicopters, fuels, bridges, bullets, power_ups, all_sprites = create_game_objects(level)

    score = 0
    kills = 0
    fuel_spawn_kill_threshold = 15  # The next milestone for fuel station spawn

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Play shooting sound when spacebar is pressed
                    shoot_sound.play()

                    # Existing shooting logic
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        all_sprites.update()

        if pygame.sprite.spritecollide(player, helicopters, False) or pygame.sprite.spritecollide(player, boats, False):
            if not player.invulnerable:
                game_over(screen, score, kills)
                running = False

        for bridge in pygame.sprite.spritecollide(player, bridges, False):
            if pygame.sprite.spritecollide(player, bridges, False):
                bridge.kill()
                score += 50

        fuel_hits = pygame.sprite.spritecollide(player, fuels, True)
        for fuel in fuel_hits:
            player.refuel()

        power_up_hits = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in power_up_hits:
            player.activate_power_up(power_up.power_type)
            pygame.time.set_timer(pygame.USEREVENT + 1, POWER_UP_DURATION)  # Power-up duration
            player.power_up = power_up.power_type

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                player.deactivate_power_up()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        hits = pygame.sprite.groupcollide(bullets, boats, True, True)
        for hit in hits:
            score += 10
            kills += 1  # Increment kill counter
            x = random.randint(100, WIDTH - 140)
            y = random.randint(-100, -40)
            boat = Boat(x, y)
            boats.add(boat)
            all_sprites.add(boat)

        hits = pygame.sprite.groupcollide(bullets, helicopters, True, True)
        for hit in hits:
            #score_increase
            score += 20
            kills += 1  # Increment kill counter
            x = random.randint(100, WIDTH - 140)
            y = random.randint(-100, -40)
            helicopter = Helicopter(x, y)
            helicopters.add(helicopter)
            all_sprites.add(helicopter)

        # Check if kills reached the threshold for spawning fuel stations
        if kills >= fuel_spawn_kill_threshold:
            # Spawn n new fuel stations
            #fuel_number
            for i in range(3):
                fuel_x = random.randint(100, WIDTH - 130)
                fuel_y = random.randint(-300, -40)
                fuel = Fuel(fuel_x, fuel_y)
                fuels.add(fuel)
                all_sprites.add(fuel)

            # Increase the threshold for the next batch of fuel stations
            #fuel_increase
            fuel_spawn_kill_threshold += 15

        player.fuel -= FUEL_DECREASE_RATE
        if player.fuel <= 0:
            game_over(screen, score, kills)
            running = False

        score += 1

        if not boats and not helicopters:
            level += 1
            player, boats, helicopters, fuels, bridges, bullets, power_ups, all_sprites = create_game_objects(level)

        screen.fill(BLUE)
        pygame.draw.rect(screen, DARK_GREEN, [0, 0, 100, HEIGHT])
        pygame.draw.rect(screen, DARK_GREEN, [WIDTH - 100, 0, 100, HEIGHT])
        all_sprites.draw(screen)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        fuel_text = font.render(f'Fuel: {int(player.fuel)}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        kills_text = font.render(f'Enemies Destroyed: {kills}', True, WHITE)  # Display kills
        screen.blit(score_text, (10, 10))
        screen.blit(fuel_text, (10, 50))
        screen.blit(level_text, (10, 90))
        screen.blit(kills_text, (10, 130))  # Update kills display

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
