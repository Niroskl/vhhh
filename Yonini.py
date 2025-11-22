pip install pygame
python unicorn.py
import pygame
import random

pygame.init()

# --- הגדרות חלון ---
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🦄 חד־קרן תינוק חמוד")

clock = pygame.time.Clock()

# --- צבעים ---
SKY = (190, 230, 255)
GROUND = (255, 240, 255)
UNICORN_COLOR = (255, 180, 255)
HORN_COLOR = (255, 220, 0)
STAR_COLOR = (255, 255, 100)

# --- מצב משחק ---
score = 0
lives = 3
gravity = 0.7

# --- חד קרן ---
unicorn = pygame.Rect(100, 350, 50, 50)
vel_y = 0
on_ground = True

# --- כוכבים לאיסוף ---
stars = []
STAR_TIME = pygame.USEREVENT + 1
pygame.time.set_timer(STAR_TIME, 1500)

# --- מכשולים ---
obstacles = []
OBS_TIME = pygame.USEREVENT + 2
pygame.time.set_timer(OBS_TIME, 1800)


def draw_unicorn(x, y):
    """חד־קרן חמוד"""
    # גוף
    pygame.draw.rect(screen, UNICORN_COLOR, (x, y, 50, 50), border_radius=14)
    # עין
    pygame.draw.circle(screen, (0, 0, 0), (x + 35, y + 20), 5)
    # קרן
    pygame.draw.polygon(screen, HORN_COLOR, [(x + 20, y - 10), (x + 30, y + 5), (x + 10, y + 5)])
    # זנב
    pygame.draw.circle(screen, (255, 150, 255), (x - 7, y + 35), 10)


def draw_star(rect):
    pygame.draw.circle(screen, STAR_COLOR, (rect.x + 10, rect.y + 10), 10)


def draw_obstacle(rect):
    pygame.draw.rect(screen, (255, 120, 120), rect, border_radius=8)


# --- לולאת המשחק ---
running = True
while running:
    clock.tick(60)
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, HEIGHT - 80, WIDTH, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # יצירת כוכבים
        if event.type == STAR_TIME:
            stars.append(pygame.Rect(WIDTH, random.randint(200, 380), 20, 20))

        # יצירת מכשולים
        if event.type == OBS_TIME:
            obstacles.append(pygame.Rect(WIDTH, 390, 40, 40))

    # --- קלט ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = -13
        on_ground = False

    # --- תנועה של החד קרן ---
    vel_y += gravity
    unicorn.y += vel_y

    if unicorn.y >= 350:
        unicorn.y = 350
        vel_y = 0
        on_ground = True

    # --- תנועה של כוכבים ---
    for star in stars[:]:
        star.x -= 5
        if star.colliderect(unicorn):
            score += 1
            stars.remove(star)
        elif star.x < -30:
            stars.remove(star)
        else:
            draw_star(star)

    # --- תנועה של מכשולים ---
    for obs in obstacles[:]:
        obs.x -= 7
        if obs.colliderect(unicorn):
            lives -= 1
            obstacles.remove(obs)
        elif obs.x < -40:
            obstacles.remove(obs)
        else:
            draw_obstacle(obs)

    # --- ציור חד קרן ---
    draw_unicorn(unicorn.x, unicorn.y)

    # --- טקסט ---
    font = pygame.font.SysFont("Comic Sans MS", 28)
    score_surf = font.render(f"⭐ ניקוד: {score}", True, (0, 0, 0))
    lives_surf = font.render(f"💗 חיים: {lives}", True, (0, 0, 0))
    screen.blit(score_surf, (20, 20))
    screen.blit(lives_surf, (20, 60))

    # --- סיום משחק ---
    if lives <= 0:
        over = font.render("💔 המשחק נגמר! לחץ R להתחיל מחדש", True, (200, 0, 0))
        screen.blit(over, (150, 200))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            lives = 3
            score = 0
            obstacles = []
            stars = []

    pygame.display.update()

pygame.quit()
