import pygame
import random
import sys
import time

# Initialize
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI GL!TCH")
clock = pygame.time.Clock()

# Load glitch sound
try:
    glitch_sound = pygame.mixer.Sound("glitch.wav")
except:
    print("⚠️ 'glitch.wav' not found. Please add a glitch sound.")
    sys.exit()

# Fonts
font = pygame.font.SysFont("Consolas", 42, bold=True)
small_font = pygame.font.SysFont("Courier", 24)

# Error messages
messages = [
    "RECOGNITION FAILURE",
    "SYSTEM CORRUPTION",
    "REBOOTING...",
    "MEMORY LEAK DETECTED",
    "INPUT SIGNAL LOST",
    "ERROR 0xAI013",
    "OVERRIDE REJECTED"
]

def draw_rgb_text(text, x, y):
    base = font.render(text, True, (255, 255, 255))
    red = font.render(text, True, (255, 0, 0))
    green = font.render(text, True, (0, 255, 0))
    blue = font.render(text, True, (0, 0, 255))

    screen.blit(red, (x + random.randint(-2, 2), y))
    screen.blit(green, (x, y + random.randint(-2, 2)))
    screen.blit(blue, (x + random.randint(-2, 2), y + random.randint(-2, 2)))
    screen.blit(base, (x, y))

def draw_scanlines():
    for i in range(0, HEIGHT, 4):
        opacity = random.randint(20, 60)
        line = pygame.Surface((WIDTH, 2), pygame.SRCALPHA)
        line.fill((0, 255, 0, opacity))
        screen.blit(line, (0, i))

def draw_glitch_boxes():
    for _ in range(10):
        w = random.randint(10, 60)
        h = random.randint(2, 20)
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 200, 255)])
        pygame.draw.rect(screen, color, (x, y, w, h))

# Timing glitch sounds
next_glitch = time.time() + random.uniform(3, 7)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Glitch effects
    draw_scanlines()
    draw_glitch_boxes()

    # Flashing message
    if random.random() < 0.08:
        msg = random.choice(messages)
        draw_rgb_text(msg, WIDTH//2 - len(msg)*10, HEIGHT//2 - 20)

    # Sound effect
    if time.time() > next_glitch:
        glitch_sound.play()
        next_glitch = time.time() + random.uniform(3, 6)

    # Footer text
    if random.random() < 0.1:
        flicker_text = small_font.render(">> SYSTEM MONITORING AI CORE...", True, (0, 255, 0))
        screen.blit(flicker_text, (30, HEIGHT - 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
