import pygame
import random
import sys
import time
import os
print("Current directory:", os.getcwd())

# === CONFIG ===
WIDTH, HEIGHT = 900, 600
JUMPSCARE_DURATION = 1.5  # seconds
GLITCH_SOUND_FILE = "glitch.wav"
SCREAM_SOUND_FILE = "scream.wav"
IMAGE_FILE = "jumpscare.png"

# === INIT ===
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Gl!tch - Press SPACE to Die :)")
    return screen

def load_resources():
    try:
        glitch = pygame.mixer.Sound(GLITCH_SOUND_FILE)
        scream = pygame.mixer.Sound(SCREAM_SOUND_FILE)
        image = pygame.image.load(IMAGE_FILE)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        return glitch, scream, image
    except Exception as e:
        print(f"❌ Media Load Error: {e}")
        sys.exit()

def draw_glitch_text(screen, text, font, pos):
    flicker = random.randint(-2, 2)
    col = random.choice([(255, 0, 0), (0, 255, 0), (255, 255, 255)])
    t = font.render(text, True, col)
    screen.blit(t, (pos[0] + flicker, pos[1] + flicker))

def draw_scanlines(screen):
    for y in range(0, HEIGHT, 4):
        line = pygame.Surface((WIDTH, 2), pygame.SRCALPHA)
        line.fill((0, 255, 0, random.randint(20, 60)))
        screen.blit(line, (0, y))

def draw_glitch_boxes(screen):
    for _ in range(10):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        w, h = random.randint(10, 60), random.randint(2, 20)
        color = random.choice([(255, 0, 0), (0, 255, 255), (255, 255, 0)])
        pygame.draw.rect(screen, color, (x, y, w, h))

# === MAIN ===
def main():
    screen = init_pygame()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 42, bold=True)
    small_font = pygame.font.SysFont("Courier", 24)

    glitch_sound, scream_sound, jumpscare_img = load_resources()

    error_msgs = [
        "SYSTEM OVERRIDE", "RECOGNITION FAILURE", "AI ERROR", 
        "REBOOT LOOP", "INTERRUPTED THOUGHT", "SIGNAL LOST"
    ]

    jumpscare_active = False
    jumpscare_start = 0

    next_glitch = time.time() + random.uniform(3, 6)

    running = True
    while running:
        screen.fill((0, 0, 0))
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 🎯 Spacebar = trigger jumpscare
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jumpscare_active = True
                    scream_sound.play()
                    jumpscare_start = now

        # 🧟 Jumpscare logic
        if jumpscare_active:
            screen.blit(jumpscare_img, (0, 0))
            if now - jumpscare_start > JUMPSCARE_DURATION:
                jumpscare_active = False
        else:
            # Normal glitch screen
            draw_scanlines(screen)
            draw_glitch_boxes(screen)

            if random.random() < 0.07:
                msg = random.choice(error_msgs)
                draw_glitch_text(screen, msg, font, (WIDTH//2 - 200, HEIGHT//2 - 30))

            if random.random() < 0.25:
                warning_text = small_font.render("PRESS SPACE BAR TO DIE", True, (255, 0, 0))
                x = WIDTH // 2 - warning_text.get_width() // 2
                y = HEIGHT - 50
                screen.blit(warning_text, (x + random.randint(-2, 2), y + random.randint(-2, 2)))

            if now > next_glitch:
                glitch_sound.play()
                next_glitch = now + random.uniform(3, 6)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
