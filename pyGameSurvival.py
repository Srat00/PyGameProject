# Version: 1.1.0
# Log:
# 2023-04-28: Ver 1.0.0
# - Created [어록희]
# 2023-05-03: ver 1.0.1
# - Added Obstacle [강희수]
# 2023-05-08: ver 1.0.1_1
# - Added Bullet [어록희] 
# 2023-05-08: ver 1.1.0
# - Code Refactored
# - Added Camera
# - Reinforced Obstacle
# ================================================

#====================================================================================================
# 라이브러리 임포트
#====================================================================================================
import pygame, sys
from random import randint

#====================================================================================================
#상수 정의
#====================================================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ROOM_WIDTH = 1024*3
ROOM_HEIGHT = 1024*3
GROUND_WIDTH = 3648
GROUND_HEIGHT= 3200

BLACK = (0, 0, 0)

#====================================================================================================
# 객체 정의
#====================================================================================================

# 주인공 객체
class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group) # super()는 부모 클래스의 생성자를 호출한다.
		self.image = pygame.image.load('graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2() # (x, y) 형식의 벡터
		self.speed = 30

	# 주인공 이동
	def input(self): 
		keys = pygame.key.get_pressed()

		# 키보드 입력에 따라 방향을 설정한다.
		# 방향은 벡터로 표현한다. direction과 speed를 곱연산하여 최종 이동 속도를 구한다.
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			if self.rect.center[1] < 0:     #y좌표가 0보다 작으면(위로 나가려고 하면)  y의 방향값을 0으로 바꿔
				self.direction.y = 0		#update함수의 self.rect.center += self.direction * self.speed 계산에서 y값이 0이 된다.
			else:
				self.direction.y = -1 		#그렇지 않을 때는 전의 코드와 같음
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			if self.rect.center[1] > GROUND_HEIGHT:
				self.direction.y = 0
			else:
				self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			if self.rect.center[0] > GROUND_WIDTH:
				self.direction.x = 0
			else:
				self.direction.x = 1
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			if self.rect.center[0] < 0:
				self.direction.x = 0
			else:
				self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed # 캐릭터 이동


	def collision(self):
		pass
	
	def fire(self):
		bullet_group.add(Bullet(self.rect.center, BulletSpeed, camera_group))		
		

# 장애물 객체
class Tree(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

# 적 객체
class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/enemy.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 20

	def update(self):
		self.direction = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
		if self.direction.length() < 1000 and self.direction.length() > 15: #500에서 1000으로 더 멀리서도 캐릭터를 향해 찾아오게 함
			self.direction.scale_to_length(self.speed)
		else:
			self.direction.scale_to_length(0)
		self.rect.center += self.direction

	# 충돌 기준 중심 보정
	def set_rect_center(self, x, y):
		# 랜덤 좌표 이동시 충돌 기준이 따라가지 않으므로, 충돌 기준을 보정해줌.
		self.rect.center = (x + self.image.get_width() // 2, y + self.image.get_height() // 2)
   
	def collision(self):
		# 충돌시 랜덤 좌표로 이동.
		self.x = randint(1000,2000)
		self.y = randint(1000,2000)
		# 충돌 기준 보정.
		self.set_rect_center(self.x, self.y)


# 총알 객체
class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, speed, group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		# 마우스 방향으로 총알을 발사함.
		self.direction = pygame.math.Vector2(pygame.mouse.get_pos()) - (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # 마우스 좌표를 벡터로 변환 >> 마우스 좌표 - 화면 중심 좌표
		self.normal_direction = self.direction.normalize() # 방향을 단위 벡터로 설정함 (캐릭터 이동 방식과 동일)
		self.speed = speed
		#print(self.normal_direction)

	def update(self):
		# 화면 밖으로 나가면 총알을 제거함.
		if self.rect.centerx < 0 or self.rect.centerx > ROOM_WIDTH or self.rect.centery < 0 or self.rect.centery > ROOM_HEIGHT:
			self.kill()
		self.rect.center += self.normal_direction * self.speed

# 카메라 객체
class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		# 카메라 설정
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# 카메라 경계 설정
		self.camera_borders = {'left': 500, 'right': 500, 'top': 300, 'bottom': 300}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)

		# 배경 설정
		self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		# 카메라 이동 속도 설정
		self.keyboard_speed = 5
		self.mouse_speed = 0.2

		# 룸 설정
		self.zoom_scale = 1
		self.internal_surf_size = (ROOM_WIDTH,ROOM_HEIGHT)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	# 객체가 카메라의 중앙에만 있도록 함.
	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	# 객체가 카메라 경계 안에 있도록 함. (추천)
	def box_target_camera(self,target):

		if target.rect.left < self.camera_rect.left:
			self.camera_rect.left = target.rect.left
		if target.rect.right > self.camera_rect.right:
			self.camera_rect.right = target.rect.right
		if target.rect.top < self.camera_rect.top:
			self.camera_rect.top = target.rect.top
		if target.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = target.rect.bottom

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']
	
	# 키보드 입력으로 카메라를 이동함.
	def keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_j]: self.camera_rect.x -= self.keyboard_speed
		if keys[pygame.K_l]: self.camera_rect.x += self.keyboard_speed
		if keys[pygame.K_i]: self.camera_rect.y -= self.keyboard_speed
		if keys[pygame.K_j]: self.camera_rect.y += self.keyboard_speed

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']  
		
	# 마우스 입력으로 카메라를 이동함.
	def mouse_control(self):
		mouse = pygame.math.Vector2(pygame.mouse.get_pos())
		mouse_offset_vector = pygame.math.Vector2()

		left_border = self.camera_borders['left']
		top_border = self.camera_borders['top']
		right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
		bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

		if top_border < mouse.y < bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector.x = mouse.x - left_border
				pygame.mouse.set_pos((left_border,mouse.y))
			if mouse.x > right_border:
				mouse_offset_vector.x = mouse.x - right_border
				pygame.mouse.set_pos((right_border,mouse.y))
		elif mouse.y < top_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
				pygame.mouse.set_pos((left_border,top_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
				pygame.mouse.set_pos((right_border,top_border))
		elif mouse.y > bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
				pygame.mouse.set_pos((left_border,bottom_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
				pygame.mouse.set_pos((right_border,bottom_border))

		if left_border < mouse.x < right_border:
			if mouse.y < top_border:
				mouse_offset_vector.y = mouse.y - top_border
				pygame.mouse.set_pos((mouse.x,top_border))
			if mouse.y > bottom_border:
				mouse_offset_vector.y = mouse.y - bottom_border
				pygame.mouse.set_pos((mouse.x,bottom_border))

		self.offset += mouse_offset_vector * self.mouse_speed
		
	# 줌을 키보드 입력으로 조절함.
	def zoom_keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q]:
			self.zoom_scale += 0.1
		if keys[pygame.K_e]:
			self.zoom_scale -= 0.1

	# 카메라 업데이트
	def custom_draw(self,player):
		
		# 어떤 유형을 사용할지 선택

		self.center_target_camera(player)
		#self.box_target_camera(player)
		# self.keyboard_control()
		#self.mouse_control()
		#self.zoom_keyboard_control()

		self.internal_surf.fill('#71ddee') # 기본 배경 색상 설정

		# 배경 그리기
		ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset # 배경의 위치를 카메라에 맞게 설정
		self.internal_surf.blit(self.ground_surf, ground_offset) # 배경을 그림

		# 객체 그리기
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): # 객체를 y좌표 기준으로 정렬
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset # 객체의 위치를 카메라에 맞게 설정
			self.internal_surf.blit(sprite.image,offset_pos) # 객체를 그림

		scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale) # 줌을 적용함
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h)) # 줌을 적용한 후 카메라의 중심을 다시 설정함
		
		self.display_surface.blit(scaled_surf,scaled_rect) # 최종 업데이트 된 정보를 화면에 그림

#====================================================================================================
# 구동부
#====================================================================================================
pygame.init()
screen = pygame.display.set_mode((1280,720)) # 화면 설정
clock = pygame.time.Clock()
pygame.event.set_grab(False) # 마우스 포커스 설정 (True : 마우스 커서가 화면 밖으로 나가지 못하게 함)

# 환경변수 설정
ObstacleCount = 50 # 장애물 개수
EnemyCount = 5 # 적 개수
EnemyList = [] # 적 리스트
BulletSpeed = 25 # 총알 속도

# 객체 생성 및 설정
camera_group = CameraGroup() # 카메라 객체 생성
bullet_group = pygame.sprite.Group() # 총알 그룹 생성

player = Player((640,360),camera_group) # 주인공 객체 생성, 카메라 그룹에 속함 

for i in range(ObstacleCount): # 장애물 객체 생성
	random_x = randint(0,GROUND_WIDTH)
	random_y = randint(0,GROUND_HEIGHT)
	Tree((random_x,random_y),camera_group) # 장애물 객체 생성, 카메라 그룹에 속함

for i in range(EnemyCount): # 적 객체 생성
	random_x = randint(1000,2000)
	random_y = randint(1000,2000)
	EnemyList.append(Enemy((random_x,random_y),camera_group)) # 적 객체 생성, 카메라 그룹에 속함

while True:
	for event in pygame.event.get():
		# 종료 조건
		if event.type == pygame.QUIT: 
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		
		# 마우스 휠로 줌 조작
		#if event.type == pygame.MOUSEWHEEL:
		#	camera_group.zoom_scale += event.y * 0.03

	# 적군 처리
		for i in range(EnemyCount):
			#플레이어와 충돌 처리
			if EnemyList[i].rect.colliderect(player.rect):
				EnemyList[i].collision()
			#총알과 충돌 처리
			if pygame.sprite.spritecollide(EnemyList[i], bullet_group, True):
				EnemyList[i].collision()

		# 마우스 왼쪽 버튼으로 총알 발사
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				player.fire()


	# 객체 업데이트
	screen.fill('#71ddee')
	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(60)
