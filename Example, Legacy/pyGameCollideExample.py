# ================================================
# Original : https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
# Description : pygame.Rect.colliderect()를 사용해 충돌을 감지하는 예제. Collision이 어떻게 동작하는지 이해할 수 있다.
# ================================================
import pygame

pygame.init()
window = pygame.display.set_mode((250, 250))
# rect1 생성, 위치를 화면의 중심으로 설정. inflate()는 rect의 크기를 늘려줌.
rect1 = pygame.Rect(*window.get_rect().center, 0, 0).inflate(75, 75)
# rect2 생성
rect2 = pygame.Rect(0, 0, 75, 75)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # rect2의 위치를 마우스 위치로 설정
    rect2.center = pygame.mouse.get_pos()
    # rect1과 rect2가 충돌했는지 확인
    collide = rect1.colliderect(rect2)
    # 충돌했다면 rect1의 색상을 빨간색으로, 아니라면 흰색으로 설정
    color = (255, 0, 0) if collide else (255, 255, 255)

    window.fill(0)
    # rect1과 rect2를 그림
    pygame.draw.rect(window, color, rect1)
    pygame.draw.rect(window, (0, 255, 0), rect2, 6, 1)
    pygame.display.flip()

pygame.quit()
exit()