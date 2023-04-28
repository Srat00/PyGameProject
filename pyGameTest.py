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

# 객체 정의
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.angle = 0
        self.speed = 5
        
        self.image = pygame.image.load("image/player.png").convert_alpha()
        self.rotated_image = pygame.transform.rotate(self.image, self.angle).convert_alpha()
        
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.rect = self.rotated_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def rotate(self, angle):
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    def draw(self):
        screen.blit(self.rotated_image, (self.x + self.image.get_width() // 2 - self.rotated_image.get_width() // 2,
                                         self.y + self.image.get_height() // 2 - self.rotated_image.get_height() // 2))
    
    def move_up(self):
        self.y -= self.speed
    
    def move_down(self):
        self.y += self.speed
        
    def move_left(self):
        self.x -= self.speed
        
    def move_right(self):
        self.x += self.speed
        
class Zombie:
    def __init__(self):
        self.angle = 0
        self.speed = 2
        self.x = random.randrange(SCREEN_WIDTH)
        self.y = random.randrange(SCREEN_HEIGHT)
        
        self.image = pygame.image.load("image/zombie.png").convert_alpha()
        self.rotated_image = pygame.transform.rotate(self.image, self.angle).convert_alpha()
        
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.rect = self.rotated_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self):
        screen.blit(self.rotated_image, (self.x + self.image.get_width() // 2 - self.rotated_image.get_width() // 2,
                                         self.y + self.image.get_height() // 2 - self.rotated_image.get_height() // 2))
        
    def move_up(self):
        self.y -= self.speed
    
    def move_down(self):
        self.y += self.speed
        
    def move_left(self):
        self.x -= self.speed
        
    def move_right(self):
        self.x += self.speed


# 환경 변수
zombie_amount = 10
zombie_list = []


# 게임 루프
done = False
clock = pygame.time.Clock()

# 초기화

# 플레이어 생성
player = Player()
# 적 생성
for i in range(zombie_amount):
    zombie_list.append(Zombie())

#게임 루프
while not done:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    # 플레이어 이동 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.move_down()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.move_up()
        
    # 종합 좀비 이벤트 처리
    for i in range(zombie_amount):
        # 좀비 이동 처리
        if player.x > zombie_list[i].x:
            zombie_list[i].move_right()
        if player.x < zombie_list[i].x:
            zombie_list[i].move_left()
        if player.y > zombie_list[i].y:   
            zombie_list[i].move_down()
        if player.y < zombie_list[i].y:
            zombie_list[i].move_up()
            
        # 좀비 충돌 처리
        if pygame.sprite.collide_mask(player, zombie_list[i]):
            print("HIT")
            zombie_list[i].x = random.randrange(SCREEN_WIDTH)
            zombie_list[i].y = random.randrange(SCREEN_HEIGHT)


    # 업데이트
    screen.fill(WHITE)
    
    player.draw()
    
    for i in range(zombie_amount):
        zombie_list[i].draw()
   
    pygame.display.update()

    # 초당 프레임 수 설정
    clock.tick(60)

# Pygame 종료
pygame.quit()
