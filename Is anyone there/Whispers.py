import pygame
import random
import sys
import time
import math

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whispers in the Void")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 36, bold=True)

# Load whisper sound
try:
    whisper = pygame.mixer.Sound("whisper.wav")
except:
    print("⚠️ Missing 'whisper.wav'. Please add it.")
    sys.exit()

# Orb class
class Orb:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.randint(10, 30)
        self.opacity = 0
        self.fade_speed = random.uniform(0.5, 1)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.2, 0.5)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.opacity = (self.opacity + self.fade_speed) % 255

    def draw(self):
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, int(abs(math.sin(self.opacity / 255 * math.pi)) * 80)), (self.radius, self.radius), self.radius)
        screen.blit(s, (self.x - self.radius, self.y - self.radius))

# Create orbs
orbs = [Orb() for _ in range(50)]

# Whisper timer
next_whisper = random.randint(5, 15)
last_whisper = time.time()

# Flicker text
def draw_glitch_text(text, base_x, base_y):
    flicker = random.randint(-2, 2)
    offset_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    text1 = font.render(text, True, offset_color)
    text2 = font.render(text, True, (255, 255, 255))
    screen.blit(text1, (base_x + flicker, base_y + flicker))
    screen.blit(text2, (base_x, base_y))

# Main loop
running = True
while running:
    screen.fill((5, 5, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw orbs
    for orb in orbs:
        orb.update()
        orb.draw()

    # Whisper sound
    now = time.time()
    if now - last_whisper > next_whisper:
        whisper.play()
        last_whisper = now
        next_whisper = random.randint(6, 14)

    # Glitchy text
    draw_glitch_text("Nothing is real", WIDTH//2 - 130, HEIGHT//2 - 20)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
