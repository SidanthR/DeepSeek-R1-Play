import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (198, 197, 232)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Game")

# Clock
clock = pygame.time.Clock()

# Load images
drone_img = pygame.image.load('drone.png')  # You need to have a drone image named 'drone.png'
enemy_img = pygame.image.load('enemy.png')  # You need to have an enemy drone image named 'enemy.png'

# drone class
class Drone:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.width = img.get_width()
        self.height = img.get_height()
        self.speed = 5

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

# Enemy class
class Enemy:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.width = img.get_width()
        self.height = img.get_height()
        self.speed = random.randint(3, 6)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, WIDTH - self.width)
            self.speed = random.randint(3, 6)

# Create player drone
player = Drone(WIDTH // 2 - 25, HEIGHT - 100, drone_img)

# Create enemies
enemies = [Enemy(random.randint(0, WIDTH - 50), random.randint(-HEIGHT, 0), enemy_img) for _ in range(5)]

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player drone
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Update enemies
    for enemy in enemies:
        enemy.move()

    # Check for collisions
    for enemy in enemies:
        if (player.x < enemy.x + enemy.width and
            player.x + player.width > enemy.x and
            player.y < enemy.y + enemy.height and
            player.y + player.height > enemy.y):
            print("Game Over!")
            running = False

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    player.draw()
    for enemy in enemies:
        enemy.draw()

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()