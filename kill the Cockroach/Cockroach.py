import pygame
import random
import sys
import time

# === INIT ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐞 Cockroach Killer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 32)

# === LOAD IMAGE ===
try:
    roach_img = pygame.image.load("cockroach.png").convert_alpha()
    roach_img = pygame.transform.scale(roach_img, (100, 100))
except:
    print("Missing cockroach.png")
    pygame.quit()
    sys.exit()

# === LOAD SOUND ===
try:
    squish_sound = pygame.mixer.Sound("squish.wav")
except:
    squish_sound = None
    print("Missing squish.wav")

# === BLOOD SPLAT ===
class Blood:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(15, 30)
        self.lifetime = 1.0  # seconds
        self.spawn_time = time.time()

    def draw(self):
        alpha = 255 - int(255 * ((time.time() - self.spawn_time) / self.lifetime))
        if alpha < 0: alpha = 0
        blood_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(blood_surf, (0, 200, 0, alpha), (self.radius, self.radius), self.radius)
        screen.blit(blood_surf, (self.x - self.radius, self.y - self.radius))

    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime

# === ROACH ===
class Cockroach:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 100)
        self.y = random.randint(0, HEIGHT - 100)
        self.speed = random.uniform(1.5, 3.5)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

        if self.x < 0 or self.x > WIDTH - 100:
            self.dir_x *= -1
        if self.y < 0 or self.y > HEIGHT - 100:
            self.dir_y *= -1

    def draw(self):
        screen.blit(roach_img, (self.x, self.y))

    def is_clicked(self, mx, my):
        return self.x <= mx <= self.x + 100 and self.y <= my <= self.y + 100

# === GAME VARS ===
roaches = []
blood_splats = []
score = 0
spawn_delay = 2
last_spawn = time.time()
spawn_count = 3
game_timer = 30
start_time = time.time()

# === GAME LOOP ===
running = True
while running:
    now = time.time()
    screen.fill((240, 240, 240))
    elapsed = int(now - start_time)
    time_left = max(0, game_timer - elapsed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for roach in roaches[:]:
                if roach.is_clicked(mx, my):
                    roaches.remove(roach)
                    blood_splats.append(Blood(roach.x + 50, roach.y + 50))
                    score += 1
                    if squish_sound: squish_sound.play()

    # Spawn multiple roaches every few seconds
    if now - last_spawn > spawn_delay and time_left > 0:
        for _ in range(spawn_count):
            roaches.append(Cockroach())
        last_spawn = now

    # Update and draw roaches
    for roach in roaches:
        roach.move()
        roach.draw()

    # Draw and update blood splats
    for splat in blood_splats[:]:
        splat.draw()
        if splat.is_expired():
            blood_splats.remove(splat)

    # UI
    screen.blit(font.render(f"Score: {score}", True, (0, 100, 0)), (20, 20))
    screen.blit(font.render(f"Time Left: {time_left}s", True, (200, 0, 0)), (WIDTH - 220, 20))

    if time_left <= 0:
        over = font.render("Game Over! Press R to Restart", True, (180, 0, 0))
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score = 0
            roaches.clear()
            blood_splats.clear()
            start_time = time.time()
            last_spawn = time.time()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
