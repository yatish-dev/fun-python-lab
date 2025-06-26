import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floating Bubbles Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Colors
BLUE = (0, 200, 255)
BACKGROUND = (10, 10, 30)
WHITE = (255, 255, 255)

# Bubble class
class Bubble:
    def __init__(self):
        self.radius = random.randint(15, 40)
        self.x = random.randint(0 + self.radius, WIDTH - self.radius)
        self.y = HEIGHT + self.radius
        self.speed = random.uniform(1, 3)

    def move(self):
        self.y -= self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)

    def is_clicked(self, pos):
        mx, my = pos
        return (self.x - mx)**2 + (self.y - my)**2 < self.radius**2

# Bubble list and counter
bubbles = []
popped_count = 0
spawn_timer = 0

# Game loop
while True:
    screen.fill(BACKGROUND)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for b in bubbles[:]:
                if b.is_clicked(pos):
                    bubbles.remove(b)
                    popped_count += 1
                    break  # Only pop one bubble per click

    # Spawn bubbles every 20 frames
    spawn_timer += 1
    if spawn_timer > 20:
        bubbles.append(Bubble())
        spawn_timer = 0

    # Move and draw bubbles
    for bubble in bubbles[:]:
        bubble.move()
        bubble.draw(screen)
        if bubble.y + bubble.radius < 0:
            bubbles.remove(bubble)

    # Draw popped count
    counter_text = font.render(f"Bubbles Popped: {popped_count}", True, WHITE)
    screen.blit(counter_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)
