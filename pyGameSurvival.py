# ================================================
# Description: PyGame을 이용한 간단한 피하기 게임
# Author: Rocky Eo
# Since: 2023-04-28

# Version: 1.0.1_1
# Log:
# 2023-04-28: Ver 1.0.0
# - Created [어록희]
# 2023-05-03: ver 1.0.1
# - Added Obstacle [강희수]
# 2023-05-08: ver 1.0.1_1
# - Added Bullet [어록희] 
# Comment : 좀 비효율적인 방법입니다. 일단은 작동은 되니 추후에 수정해보겠습니다. [어록희]
# ================================================

import pygame
import random
import math
import time

from tkinter import *
from tkinter import messagebox

# Pygame 초기화
pygame.init()

#font
game_font = pygame.font.Font(None, 40)

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

# 장애물 클래스 정의
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        # 장애물이 다른 장애물과 겹치지 않도록 생성
        while pygame.sprite.spritecollide(self, group, False):
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, SCREEN_HEIGHT - self.rect.height)

    def update(self):
        pass

# 장애물 그룹 생성
obstacle_group = pygame.sprite.Group()

# 객체 정의
# 주인공 객체
class Player(pygame.sprite.Sprite):
    # 초기 설정
    def __init__(self):
        # 좌표, 각도, 속도 설정
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.angle = 0
        self.speed = 5
        
        # 이미지 설정
        # 이미지 불러오기, convert_alpha()는 이미지의 배경을 투명하게 만듦
        self.image = pygame.image.load("image/player.png").convert_alpha() 
        # 이미지의 중심 좌표를 구함. 기본적으로 이미지의 좌상단이 기준이므로, 이미지의 크기의 반을 더해줌.
        self.center = (self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2) 
        # 객체 충돌 기준 설정
        self.rect = self.image.get_rect()
        self.rect.center = self.center

        # 이미지 회전용 이미지 생성
        self.image1 = self.image
        self.image2 = pygame.transform.rotate(self.image, 180).convert_alpha() 

    # 이미지 회전
    def rotate1(self):
        self.image = self.image1
    def rotate2(self):
        self.image = self.image2

    # 이미지 그리기
    def draw(self):
        # 객체의 충돌 기준을 그림 (디버그용)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        # 이미지를 그림
        screen.blit(self.image, (self.x, self.y))
    
    # 객체 이동, 객체의 충돌기준도 같이 움직이게 처리해줘야 함.
    def move_up(self):
        self.rect.centery -= self.speed
        self.y -= self.speed
    
    def move_down(self):
        self.rect.centery += self.speed
        self.y += self.speed
        
    def move_left(self):
        self.rect.centerx -= self.speed
        self.x -= self.speed
        
    def move_right(self):
        self.rect.centerx += self.speed
        self.x += self.speed
    def update(self):
        pass
        
        
# 적 개체
class Enemy:
    # 초기 설정
    def __init__(self):
        # 좌표, 각도, 속도 설정. 스폰은 랜덤으로 한다.
        self.x = random.randrange(SCREEN_WIDTH)
        self.y = random.randrange(SCREEN_HEIGHT)
        self.angle = 0
        self.speed = 2
        
        # 이미지 설정. 세부 사항은 주인공 객체와 동일함.
        self.image = pygame.image.load("image/enemy.png").convert_alpha()
        self.center = (self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2)
        
        # 객체 충돌 기준 설정
        self.rect = self.image.get_rect()
        self.rect.center = self.center
    
    # 이미지 그리기. 세부 사항은 주인공 객체와 동일함.
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect, 1)
        screen.blit(self.image, (self.x, self.y))
    
    # 객체 이동. 세부 사항은 주인공 객체와 동일함.
    def move_up(self):
        self.rect.centery -= self.speed
        self.y -= self.speed
    
    def move_down(self):
        self.rect.centery += self.speed
        self.y += self.speed
        
    def move_left(self):
        self.rect.centerx -= self.speed
        self.x -= self.speed
        
    def move_right(self):
        self.rect.centerx += self.speed
        self.x += self.speed

    # 충돌 기준 중심 보정
    def set_rect_center(self, x, y):
        # 랜덤 좌표 이동시 충돌 기준이 따라가지 않으므로, 충돌 기준을 보정해줌.
        self.rect.center = (x + self.image.get_width() // 2, y + self.image.get_height() // 2)

    # 적군 개체 충돌 이벤트 처리
    def collision(self):
        # 충돌시 랜덤 좌표로 이동.
        self.x = random.randrange(SCREEN_WIDTH)
        self.y = random.randrange(SCREEN_HEIGHT)
        # 충돌 기준 보정.
        self.set_rect_center(self.x, self.y)
        
# 장애물 클래스 정의
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        # 장애물이 다른 장애물과 겹치지 않도록 생성
        while pygame.sprite.spritecollide(self, group, False):
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, SCREEN_HEIGHT - self.rect.height)

    def update(self):
        pass

# 총알 개체
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((205, 205, 30))  # 총알 색상 설정
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20
        self.dx = math.cos(angle) * self.speed
        self.dy = -math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()
            
# 점수 개체
class Score:
    # 초기 설정
    def __init__(self):
        # 점수, 텍스트 변수 선언
        self.score = 0
        self.text = "Score: "

        # 폰트 설정 (폰트, 크기, 굵기, 기울임)
        self.scoreText = pygame.font.SysFont("Consolas", 25, True, False)

        # 텍스트 렌더 설정 (텍스트, 안티앨리어싱, 색상)
        self.render = self.scoreText.render(self.text + str(self.score), True, BLACK)

        # 텍스트 렌더의 중심 좌표 설정
        self.rect = self.render.get_rect()
        self.rect.center = (SCREEN_WIDTH // 20, 20)

    # 텍스트 그리기
    def draw(self):
        # 텍스트 렌더를 화면에 그림. render를 다시 설정해주는 이유는 점수가 바뀔 때마다 다시 렌더를 해줘야 하기 때문.
        self.render = self.scoreText.render(self.text + str(self.score), True, BLACK)
        screen.blit(self.render, self.rect)
    
    # 점수 설정. 점수를 가져와 더해줌.
    def setScore(self, score):
        self.score += score
        
# ================================================================================================  

# 환경 변수 설정
enemy_amount = 10 # 인 게임에서 변경 가능
enemy_list = []
last_shot_time = pygame.time.get_ticks()
fire_delay = 350

# 게임 루프
done = False
clock = pygame.time.Clock()

# 초기화

# 플레이어 생성
player = Player()
# 적 생성
for i in range(enemy_amount):
    enemy_list.append(Enemy())
# 점수 생성
score = Score()
score.setScore(100)
# 장애물 그룹 생성
obstacle_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# ================================================================================================  

#게임 루프

while not done:
    # 초당 프레임 수 설정
    clock.tick(60)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    # 플레이어 이동 처리. elif를 사용하지 않은 이유는 키를 동시에 누를 수 있기 때문.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.move_down()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.move_up()

    #플레이어 회전 처리
    mouseX, mouseY = pygame.mouse.get_pos()
    if(mouseX < player.x + 20):
        player.rotate1()
    else:
        player.rotate2()

    # 종합 좀비 이벤트 처리
    for i in range(zombie_amount):
        # 좀비 이동 처리. 플레이어와 좀비의 좌표를 비교해 좀비가 플레이어를 따라가도록 함.
        if player.x > zombie_list[i].x:
            zombie_list[i].move_right()
        if player.x < zombie_list[i].x:
            zombie_list[i].move_left()
        if player.y > zombie_list[i].y:   
            zombie_list[i].move_down()
        if player.y < zombie_list[i].y:
            zombie_list[i].move_up()
            
        # 좀비 충돌 처리
        if zombie_list[i].rect.colliderect(player.rect):
            # 충돌시 이벤트 처리
            zombie_list[i].collision()
            score.setScore(-5)
=======
    # 종합 적군 이벤트 처리
    for i in range(enemy_amount):
        # 적군 이동 처리. 플레이어와 적군의 좌표를 비교해 적군가 플레이어를 따라가도록 함.
        if player.x > enemy_list[i].x:
            enemy_list[i].move_right()
        if player.x < enemy_list[i].x:
            enemy_list[i].move_left()
        if player.y > enemy_list[i].y:   
            enemy_list[i].move_down()
        if player.y < enemy_list[i].y:
            enemy_list[i].move_up()
            
        # 주인공 충돌 처리
        if enemy_list[i].rect.colliderect(player.rect):
            # 충돌시 이벤트 처리
            enemy_list[i].collision()
            score.setScore(-5)
        # 총알 충돌 처리
        for k in range(len(bullet_group)):
            if bullet_group.sprites()[k].rect.colliderect(enemy_list[i].rect):
                enemy_list[i].collision()
                bullet_group.sprites()[k].kill()
            
    # 장애물 개수가 8개 이하일 때만 새로운 장애물 생성
    if len(obstacle_group) < 8:
        obstacle = Obstacle(obstacle_group)
        obstacle_group.add(obstacle)

    if pygame.sprite.spritecollide(player,obstacle_group, False):
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.move_right()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.move_left()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move_up()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move_down()

    # 총알 이벤트 처리
    if pygame.mouse.get_pressed()[0]:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time >= fire_delay:
            mx, my = pygame.mouse.get_pos()
            px, py = player.rect.center
            angle = math.atan2(my - py, mx - px)
            bullet = Bullet(px, py, -angle)
            bullet_group.add(bullet)
            last_shot_time = current_time

    # 게임 종료 조건 처리
    if score.score <= 0:
        # 알림창 띄우기. tkinter를 사용함.
        Tk().wm_withdraw()
        messagebox.showinfo("PyGameTest", "GAME OVER! ")
        done = True

    # 그리기
    screen.fill(WHITE)
    obstacle_group.draw(screen)
    bullet_group.draw(screen)
    player.draw()
    for i in range(enemy_amount):
        enemy_list[i].draw()
    score.draw()

    # 업데이트
    obstacle_group.update()
    bullet_group.update()

    pygame.display.flip()

# Pygame 종료
pygame.quit()
