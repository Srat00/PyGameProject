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
from tkinter import *
from tkinter import messagebox
import time
#====================================================================================================
#상수 정의
#====================================================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ROOM_WIDTH = 1024*3
ROOM_HEIGHT = 1024*3
GROUND_WIDTH = 1824
GROUND_HEIGHT= 1600

BLACK = (0, 0, 0)

#====================================================================================================
# 객체 정의
#====================================================================================================

# 주인공 객체
class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group) # super()는 부모 클래스의 생성자를 호출한다.

		self.direction = pygame.math.Vector2() # (x, y) 형식의 벡터
		self.status = 'right' # 주인공의 방향
		self.apply_status()
		self.image = pygame.image.load('graphics/stay_right/0.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.speed = 10
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]
		self.speed = 5
		#주인공 쿨타임을 위한 변수
		self.cool = 0
		#주인공 성장구현을 위한 스코어 변수
		self.score = 0
		self.health = 200

	def take_damage(self, damage):
		self.health -= damage
		if self.health <= 0:
			self.health = 0

	def apply_status(self):
		self.sprites = []
		if self.status == 'right': #오른쪽을 보면서
			if abs(self.direction[0]) + abs(self.direction[1]) == 0: #움직임이 없으면
				self.sprites.append(pygame.image.load('graphics/stay_right/0.png'))
				self.sprites.append(pygame.image.load('graphics/stay_right/1.png'))
				self.sprites.append(pygame.image.load('graphics/stay_right/2.png'))
				self.sprites.append(pygame.image.load('graphics/stay_right/3.png'))
	
			else: #움직임이 없으면
				self.sprites.append(pygame.image.load('graphics/move_right/0.png'))
				self.sprites.append(pygame.image.load('graphics/move_right/1.png'))
				self.sprites.append(pygame.image.load('graphics/move_right/2.png'))
				self.sprites.append(pygame.image.load('graphics/move_right/3.png'))

		if self.status == 'left': #오른쪽을 보면서
			if abs(self.direction[0]) + abs(self.direction[1]) == 0: #움직임이 없으면
				self.sprites.append(pygame.image.load('graphics/stay_left/0.png'))
				self.sprites.append(pygame.image.load('graphics/stay_left/1.png'))
				self.sprites.append(pygame.image.load('graphics/stay_left/2.png'))
				self.sprites.append(pygame.image.load('graphics/stay_left/3.png'))
			else: #움직임이 있으면
				self.sprites.append(pygame.image.load('graphics/move_left/0.png'))
				self.sprites.append(pygame.image.load('graphics/move_left/1.png'))
				self.sprites.append(pygame.image.load('graphics/move_left/2.png'))
				self.sprites.append(pygame.image.load('graphics/move_left/3.png'))
	
	# 주인공 이동
	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			if self.rect.center[1] - 192 < 0:	 # y좌표가 0보다 작으면(위로 나가려고 하면)y의 방향값을 0으로 바꿔
				self.direction.y = 0		# update함수의 self.rect.center += self.direction * self.speed 계산에서 y값이 0이 된다.
			else:
				self.direction.y = -1 		#그렇지 않을 때는 전의 코드와 같음
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			if self.rect.center[1] + 32 > GROUND_HEIGHT:
				self.direction.y = 0
			else:
				self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			if self.rect.center[0] + 90 > GROUND_WIDTH:
				self.direction.x = 0
			else:
				self.direction.x = 1
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			if self.rect.center[0] - 90 < 0:
				self.direction.x = 0
			else:
				self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.apply_status()
		self.current_sprite += 0.1
		if int(self.current_sprite) >= len(self.sprites):
			self.current_sprite = 0
		self.image = self.sprites[int(self.current_sprite)]

		if self.direction != pygame.Vector2(0,0): # 방향이 정해져 있을 때만 이동
			new_rect = self.rect.move(self.direction *self.speed)
			self.rect = new_rect

		# 모든 장애물과 충돌 검사 (각 장애물의 충돌 영역인 collision_rect와 플레이어의 충돌 영역인 rect를 이용)
		for obstacle in obstacles:
			if self.rect.colliderect(obstacle.collision_rect):
				if self.direction.x > 0:
					if self.rect.right<=obstacle.collision_rect.left+player.speed:
						self.rect.right = obstacle.collision_rect.left  # 오른쪽으로 이동 중이면 충돌한 장애물의 왼쪽으로 위치 고정
				if self.direction.x < 0:
					if self.rect.left >= obstacle.collision_rect.right-player.speed:
						self.rect.left = obstacle.collision_rect.right  # 왼쪽으로 이동 중이면 충돌한 장애물의 오른쪽으로 위치 고정
				if self.direction.y > 0:
					if self.rect.bottom <= obstacle.collision_rect.top+player.speed:
						self.rect.bottom = obstacle.collision_rect.top  # 아래쪽으로 이동 중이면 충돌한 장애물의 위쪽으로 위치 고정
				if self.direction.y < 0:
					if self.rect.top >= obstacle.collision_rect.bottom-player.speed:
						self.rect.top = obstacle.collision_rect.bottom  # 위쪽으로 이동 중이면 충돌한 장애물의 아래쪽으로 위치 고정
		

	def collision(self):
		pass
	

	#성장 구현을 위한 발사 속도 추가
	def fire(self):
		if(player.score < 10):
			if(player.cool > 30):
				player.cool = 0
				bullet_group.add(Bullet(self.rect.center, BulletSpeed, camera_group))
				attack_sound.play()

		elif(10 <= player.score < 20):
			if(player.cool > 25):
				player.cool = 0
				bullet_group.add(Bullet(self.rect.center, BulletSpeed, camera_group))
				attack_sound.play()
		
		elif(20 <= player.score < 30):
			if(player.cool > 20):
				player.cool = 0
				bullet_group.add(Bullet(self.rect.center, BulletSpeed, camera_group))
				attack_sound.play()

		elif(30 <= player.score < 40):
			if(player.cool > 15):
				player.cool = 0
				bullet_group.add(Bullet(self.rect.center, BulletSpeed, camera_group))
				attack_sound.play()
		
		elif(40 <= player.score < 50):
			if(player.cool > 10):
				player.cool = 0
				bullet_group.add(Bullet(self.rect.center, BulletSpeed, camera_group))
				attack_sound.play()

def draw_health_bar():
	bar_height = 20  # 체력바의 높이
	bar_x=20
	bar_y=20
	pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, player.health, bar_height))

def draw_time_background():
	color=(187,50,250)

	pygame.draw.rect(screen, (0,255,255), (496, 0, 276, 120), 5)
	rect_surface = pygame.Surface((276, 120))
	rect_surface.set_alpha(128)
	rect_surface.fill(color)
	screen.blit(rect_surface, (496,0))

# 장애물 객체
class Tree(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/box.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.collision_rect = pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2, self.rect.width, self.rect.height // 2-10)  # 충돌 박스 크기 수정
		self.colliding = False # 지금까지 만들어진 tree 객체들과의 충돌 검사를 위한 변수

		while pygame.sprite.spritecollide(self,obstacles,False):
				self.rect.topleft = (randint(200, GROUND_WIDTH - 200), randint(200, GROUND_HEIGHT - 200))
				self.collision_rect.topleft = (self.rect.left, self.rect.top + self.rect.height // 2)

	def update(self):
		pass

# 적 객체
class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/enemy.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

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
		player.take_damage(10)
		# 충돌시 랜덤 좌표로 이동.
		self.x = randint(1000,2000)
		self.y = randint(1000,2000)
		# 충돌 기준 보정.
		self.set_rect_center(self.x, self.y)

	def collision_bullet(self):
		# 충돌시 랜덤 좌표로 이동.
		self.x = randint(1000,2000)
		self.y = randint(1000,2000)
		# 충돌 기준 보정.
		self.set_rect_center(self.x, self.y)

# 적2 객체
class Enemy2(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image1 = pygame.image.load('graphics/enemy2_1.png').convert_alpha()
		self.image2 = pygame.image.load('graphics/enemy2_2.png').convert_alpha()
		self.image = self.image1
		self.rect = self.image.get_rect(topleft = pos)
		self.direction = pygame.math.Vector2()
		# 이동속도 3
		self.speed = 3
		#적 체력 추가
		self.hp = 1

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
    
	# 적2 체력 감소 추가
	def collision(self):
		# 충돌시 랜덤 좌표로 이동.
		player.take_damage(10)
		self.x = randint(1000,2000)
		self.y = randint(1000,2000)
		# 충돌 기준 보정.
		self.set_rect_center(self.x, self.y)

	def collision_bullet(self):
		# 충돌시 랜덤 좌표로 이동.
		self.x = randint(1000,2000)
		self.y = randint(1000,2000)
		# 충돌 기준 보정.
		self.set_rect_center(self.x, self.y)

	# 적2 분노 모드 추가
	def angry(self):
		self.hp = 0
		self.speed = 7
		self.image = self.image2

	def release(self):
		self.hp = 1
		self.speed = 3
		self.image = self.image1


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
		w = self.display_surface.get_size()[0]- (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.display_surface.get_size()[1]- (self.camera_borders['top'] + self.camera_borders['bottom'])
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
		if self.offset.x < 0 - 600: #player의 크기 64 고려
			self.offset.x = 0 - 600 #더 이상 안움직이게(조건과 똑같은 값) #!!!!플레이어 속도의 영향을 받음!!!!
		if self.offset.x > GROUND_WIDTH - SCREEN_WIDTH + 680:
			self.offset.x = GROUND_WIDTH - SCREEN_WIDTH + 680

		self.offset.y = target.rect.centery - self.half_h
		if self.offset.y < 0 - 320:
			self.offset.y = 0 - 320
		if self.offset.y > GROUND_HEIGHT - SCREEN_HEIGHT + 320:
			self.offset.y = GROUND_HEIGHT - SCREEN_HEIGHT + 320

	# 카메라 업데이트
	def custom_draw(self,player):
		
		# 어떤 유형을 사용할지 선택

		self.center_target_camera(player)
		#self.box_target_camera(player)
		# self.keyboard_control()
		#self.mouse_control()
		#self.zoom_keyboard_control()

		self.internal_surf.fill('#000000') # 기본 배경 색상 설정

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
# 함수정의
#====================================================================================================

# 마우스 위치 반환
def get_normalized_mouse_pos():
	direction = pygame.math.Vector2(pygame.mouse.get_pos()) - (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # 마우스 좌표를 벡터로 변환 >> 마우스 좌표 - 화면 중심 좌표
	normal_direction = direction.normalize() # 방향을 단위 벡터로 설정함 (캐릭터 이동 방식과 동일)
	return normal_direction

def game_start():
	start_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	start_image = pygame.image.load('graphics/start.png')

	while True:
		for event in pygame.event.get():
			# 종료 조건
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				return
		start_screen.fill((255,255,255))
		start_screen.blit(start_image, (0,0))

		pygame.display.update()


#====================================================================================================
# 구동부
#====================================================================================================
pygame.init()

game_start()
start_time = time.time() # 시작시간 확인
time_limit=5*60 # 제한시간 30분
elapsed_time=0
time_font = pygame.font.SysFont("malgungothic", 36)

attack_sound = pygame.mixer.Sound('sound/attack_sound.wav')
attack_sound.set_volume(0.3)
bgm = pygame.mixer.Sound('sound/temp_BGM.mp3')
bgm.set_volume(0.3)
bgm.play(-1)

screen = pygame.display.set_mode((1280,720)) # 화면 설정
clock = pygame.time.Clock()
pygame.event.set_grab(False) # 마우스 포커스 설정 (True : 마우스 커서가 화면 밖으로 나가지 못하게 함)

# 환경변수 설정
ObstacleCount = 20 # 장애물 개수
EnemyCount = 5 # 적 개수
EnemyList = [] # 적 리스트
BulletSpeed = 25 # 총알 속도

# 적2 추가
Enemy2Count = 5 # 적2 개수
Enemy2List = [] # 적2 리스트

# 객체 생성 및 설정
camera_group = CameraGroup() # 카메라 객체 생성
bullet_group = pygame.sprite.Group() # 총알 그룹 생성
obstacles = pygame.sprite.Group()#tree를 넣을 스프라이트 그룹 생성

player = Player((640,360),camera_group) # 주인공 객체 생성, 카메라 그룹에 속함 

moving_sprites = pygame.sprite.Group()
moving_sprites.add(player)

for i in range(ObstacleCount): # 장애물 객체 생성
	random_x = randint(200,GROUND_WIDTH - 200)
	random_y = randint(200,GROUND_HEIGHT - 200)
	tree=Tree((random_x,random_y),camera_group) # 장애물 객체 생성, 카메라 그룹에 속함
	obstacles.add(tree) # 생성된 Tree 객체를 obstale 스프라이트 그룹에 추가한다.

for i in range(EnemyCount): # 적 객체 생성
	random_x = randint(1000,2000)
	random_y = randint(1000,2000)
	EnemyList.append(Enemy((random_x,random_y),camera_group)) # 적 객체 생성, 카메라 그룹에 속함
done=False
for i in range(Enemy2Count): # 적2 객체 생성
	random_x = randint(1000,2000)
	random_y = randint(1000,2000)
	Enemy2List.append(Enemy2((random_x,random_y),camera_group)) # 적2 객체 생성, 카메라 그룹에 속함



while elapsed_time < time_limit:
	while True:
		for event in pygame.event.get():
		# 종료 조건
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if get_normalized_mouse_pos().x > 0:
				player.status = 'right'
			else:
				player.status = 'left'
				
			# 적군 처리
			for i in range(EnemyCount):
				#플레이어와 충돌 처리
				if EnemyList[i].rect.colliderect(player.rect):
					EnemyList[i].collision()
				#총알과 충돌 처리
				if pygame.sprite.spritecollide(EnemyList[i], bullet_group, True):
					EnemyList[i].collision_bullet()
				
				# 마우스 왼쪽 버튼으로 총알 발사
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					player.fire()
				
			if player.health<=0:
				# 알림창 띄우기. tkinter를 사용함.
				if time_score >= 400 and time_score < 500:
					real_score='F'
				elif time_score >= 300 and time_score < 400:
					real_score='D'
				elif time_score >= 200 and time_score < 300:
					real_score='C'
				elif time_score >= 100 and time_score < 200:
					real_score='B'
				elif time_score >= 1 and time_score < 100:
					real_score='A'
				elif time_score < 0:
					real_score='S'
				Tk().wm_withdraw()
				messagebox.showinfo("PyGameTest", f"당신의 점수는 {real_score} 입니다~ ")
				pygame.quit()
				sys.exit()

			#충돌 처리를 for문 밖으로 내보냄
			#충돌처리 원활하게 하기 위함 
			# 적군 처리
			for i in range(EnemyCount):
				#플레이어와 충돌 처리
				if EnemyList[i].rect.colliderect(player.rect):
					EnemyList[i].collision()
				#총알과 충돌 처리
				if pygame.sprite.spritecollide(EnemyList[i], bullet_group, True):
					EnemyList[i].collision_bullet()
					

			# 적2 처리 추가
			for i in range(Enemy2Count):
				#총알과 충돌 처리
				if pygame.sprite.spritecollide(Enemy2List[i], bullet_group, True):
					if (Enemy2List[i].hp == 1):
						Enemy2List[i].angry()
					else:
						Enemy2List[i].release()
						Enemy2List[i].collision_bullet()
					#성장 구현을 위한 스코어 추가
					player.score += 1

				#플레이어와 충돌 처리
				if Enemy2List[i].rect.colliderect(player.rect):
					Enemy2List[i].collision()

			#쿨타임 구현
			player.cool += 1

		# 객체 업데이트

		screen.fill('#71ddee')

		camera_group.update()
		camera_group.custom_draw(player)
		player.update()
		draw_health_bar() # 체력 표시
		draw_time_background()
		# 플레이 시간 표시
		current_time = time.time()
		elapsed_time = current_time - start_time

		remaining_time = max(time_limit - elapsed_time, 0)
		minutes = int(remaining_time // 60)
		seconds = int(remaining_time % 60)
		time_score = minutes * 60 + seconds # 점수 로직 ( 우선 남은 초 만큼 점수를 지정 )
		time_text = time_font.render(f"남은 시간: {minutes:02d}:{seconds:02d}", True, (14, 244, 246))
		score_text = time_font.render(f"점수: {player.score}", True, (14, 244, 246))
			
		screen.blit(time_text, (500, 10))
		screen.blit(score_text, (500, 60))
			

		pygame.display.update()
		clock.tick(60)
