import pygame
import random
import sys
import time

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎭 Random Mask Generator")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MASK_COLORS = [(255, 200, 200), (180, 255, 220), (240, 240, 150), (220, 180, 255)]

# Face parts
def draw_face():
    shape = random.choice(['circle', 'square', 'oval'])
    color = random.choice(MASK_COLORS)
    x, y = WIDTH // 2, HEIGHT // 2

    if shape == 'circle':
        pygame.draw.circle(screen, color, (x, y), 200)
    elif shape == 'square':
        pygame.draw.rect(screen, color, (x - 150, y - 150, 300, 300), border_radius=60)
    elif shape == 'oval':
        pygame.draw.ellipse(screen, color, (x - 130, y - 180, 260, 360))

def draw_eyes():
    style = random.choice(['dots', 'cross', 'rects'])
    eye_y = HEIGHT // 2 - 60
    spacing = 80

    for side in [-1, 1]:
        cx = WIDTH // 2 + side * spacing
        cy = eye_y

        if style == 'dots':
            pygame.draw.circle(screen, BLACK, (cx, cy), 20)
        elif style == 'cross':
            pygame.draw.line(screen, BLACK, (cx - 15, cy - 15), (cx + 15, cy + 15), 3)
            pygame.draw.line(screen, BLACK, (cx + 15, cy - 15), (cx - 15, cy + 15), 3)
        elif style == 'rects':
            pygame.draw.rect(screen, BLACK, (cx - 15, cy - 15, 30, 30), border_radius=5)

def draw_mouth():
    style = random.choice(['smile', 'line', 'frown', 'x'])
    x, y = WIDTH // 2, HEIGHT // 2 + 80

    if style == 'smile':
        pygame.draw.arc(screen, BLACK, (x - 60, y - 30, 120, 60), 3.14, 0, 3)
    elif style == 'line':
        pygame.draw.line(screen, BLACK, (x - 40, y), (x + 40, y), 4)
    elif style == 'frown':
        pygame.draw.arc(screen, BLACK, (x - 60, y - 10, 120, 60), 0, 3.14, 3)
    elif style == 'x':
        pygame.draw.line(screen, BLACK, (x - 25, y - 15), (x + 25, y + 15), 3)
        pygame.draw.line(screen, BLACK, (x + 25, y - 15), (x - 25, y + 15), 3)

def generate_mask():
    screen.fill(WHITE)
    draw_face()
    draw_eyes()
    draw_mouth()

# === MAIN LOOP ===
next_mask_time = time.time()
running = True
while running:
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if now >= next_mask_time:
        generate_mask()
        next_mask_time = now + 3  # new mask every 3 sec

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
