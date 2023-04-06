import pygame
import random
import math

# Pygame 초기화
pygame.init()

# 게임 화면 설정
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 타이틀 설정
pygame.display.set_caption("Survival Game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 플레이어 설정
player_image = pygame.image.load("image/player.png").convert()
player_image.set_colorkey(WHITE)
player_rect = player_image.get_rect()
player_rect.centerx = SCREEN_WIDTH / 2
player_rect.bottom = SCREEN_HEIGHT / 2
player_speed = 5

# 좀비 설정
zombie_image = pygame.image.load("image/zombie.png").convert()
zombie_image.set_colorkey(WHITE)
zombie_list = []
zombie_rect_list = []
for i in range(10):
    print("zombie", i)
    zombie_rect = zombie_image.get_rect()
    zombie_rect.x = random.randrange(player_rect.x - 1000, player_rect.x + 1000)
    zombie_rect.y = random.randrange(player_rect.y - 1000, player_rect.y + 1000)
    zombie_speed = 2
    zombie_list.append({'rect': zombie_rect, 'speed': zombie_speed})
    zombie_rect_list.append(zombie_rect)

# 게임 루프
done = False
clock = pygame.time.Clock()

while not done:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 플레이어 이동 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_rect.y += player_speed    
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_rect.y -= player_speed

    for zombie in zombie_list:
        # 좀비 이동 처리
        dx = player_rect.centerx - zombie['rect'].centerx
        dy = player_rect.centery - zombie['rect'].centery
        dist = math.hypot(dx, dy)
        dx = dx / dist
        dy = dy / dist
        zombie_rect = zombie['rect'].copy()
        zombie_rect.x += dx * zombie['speed']
        zombie_rect.y += dy * zombie['speed']
        

    # 충돌 검사
    for zombie in zombie_list:
        if player_rect.colliderect(zombie['rect']):
            done = True

    # 그리기
    screen.fill(WHITE)
    screen.blit(player_image, player_rect)
    for zombie in zombie_list:
        screen.blit(zombie_image, zombie['rect'])

    # 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)

# Pygame 종료
pygame.quit()
