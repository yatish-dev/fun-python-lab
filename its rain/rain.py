import pygame
import random
import sys
import time

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Don't Expect Anything")
clock = pygame.time.Clock()

# Load thunder sound
try:
    thunder_sound = pygame.mixer.Sound("thunder.wav")
except:
    print("⚠️ Missing 'thunder.wav' file. Please add it to the folder.")
    sys.exit()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (10, 10, 30)
RAIN_COLOR = (180, 180, 255)

# Font
font = pygame.font.SysFont("Courier New", 36, bold=True)

# Rain drop class
class Raindrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.length = random.randint(5, 15)
        self.speed = random.uniform(4, 10)

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-20, -5)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.line(screen, RAIN_COLOR, (self.x, self.y), (self.x, self.y + self.length), 1)

# Create raindrops
raindrops = [Raindrop() for _ in range(150)]

# Thunder timer
next_thunder = random.randint(3, 8)
last_thunder_time = time.time()

# Main loop
running = True
while running:
    screen.fill(DARK_BLUE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rain logic
    for drop in raindrops:
        drop.fall()
        drop.draw()

    # Random lightning flash
    now = time.time()
    if now - last_thunder_time > next_thunder:
        screen.fill(WHITE)
        thunder_sound.play()
        pygame.display.flip()
        pygame.time.delay(100)
        last_thunder_time = now
        next_thunder = random.randint(3, 7)

    # Display message
    text = font.render("Don't expect anything", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
