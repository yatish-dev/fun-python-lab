import pygame
import random
import sys
import math

# === INIT ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧀 Cheese Escape!")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 36)

# === COLORS ===
WHITE = (255, 255, 255)
YELLOW = (255, 240, 100)
GHOST = (200, 255, 255)
RED = (255, 0, 0)

# === GAME OBJECTS ===
cheese = pygame.Rect(100, 100, 40, 40)
ghost = pygame.Rect(600, 400, 50, 50)
speed = 5
ghost_speed = 2
game_over = False

# === SOUNDS ===
try:
    caught_sound = pygame.mixer.Sound("caught.wav")  # optional funny sound
except:
    caught_sound = None  # sound is optional

# === DRAWING ===
def draw_cheese():
    pygame.draw.polygon(screen, YELLOW, [
        (cheese.x, cheese.y),
        (cheese.x + 40, cheese.y + 20),
        (cheese.x, cheese.y + 40)
    ])

def draw_ghost():
    pygame.draw.ellipse(screen, GHOST, ghost)
    eye1 = pygame.Rect(ghost.x + 10, ghost.y + 15, 10, 10)
    eye2 = pygame.Rect(ghost.x + 30, ghost.y + 15, 10, 10)
    pygame.draw.ellipse(screen, RED, eye1)
    pygame.draw.ellipse(screen, RED, eye2)

def move_ghost():
    dx = cheese.centerx - ghost.centerx
    dy = cheese.centery - ghost.centery
    dist = math.hypot(dx, dy)
    if dist != 0:
        ghost.x += int(ghost_speed * dx / dist)
        ghost.y += int(ghost_speed * dy / dist)

# === MAIN LOOP ===
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]: cheese.x -= speed
        if keys[pygame.K_RIGHT]: cheese.x += speed
        if keys[pygame.K_UP]: cheese.y -= speed
        if keys[pygame.K_DOWN]: cheese.y += speed

        move_ghost()

        draw_cheese()
        draw_ghost()

        if cheese.colliderect(ghost):
            game_over = True
            if caught_sound:
                caught_sound.play()
    else:
        msg = font.render("NOOOO DAIRY! I'M INTOLERANT!", True, RED)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))

    pygame.display.flip()
    clock.tick(60)
