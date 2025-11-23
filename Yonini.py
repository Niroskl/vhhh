import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("משחק יריות פשוט")

clock = pygame.time.Clock()

# צבעים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# שחקן
player_pos = [WIDTH // 2, HEIGHT - 50]
player_speed = 5
player_size = 50

# כדורים
bullets = []
bullet_speed = 7
bullet_size = 5

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE]:
        # ליצור כדור חדש
        bullets.append([player_pos[0] + player_size // 2, player_pos[1]])

    # לעדכן ולשרטט כדורים
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_size, bullet_size))

    # שרטוט השחקן
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], player_size, player_size))

    pygame.display.flip()
    clock.tick(60)
