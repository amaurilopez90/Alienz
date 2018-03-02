import pygame
import tileClass
from baseClasses import BaseCharacter
from random import randint
import processing

class Enemy(BaseCharacter):

	List = []    #enemy list
	spawn_tiles = (28,448,459)             #where the enemies will spawn from
	original_img = pygame.image.load("../Images/creature.png")
	health = 100

	def __init__(self, x, y):

		self.direction = "n"
		self.img = Enemy.original_img
		self.health = Enemy.health
		BaseCharacter.__init__(self, x, y) #call BaseCharacter constructor
		Enemy.List.append(self)            #add enemy to the list

	@staticmethod
	def update(screen, player, FPS, total_frames, kill_count):
		for enemy in Enemy.List:           #draw enemy to the screen
			screen.blit(enemy.img, (enemy.x, enemy.y))

			if player.x % tileClass.Tile.width == 0 and player.y % tileClass.Tile.height == 0: #check if enemy and player are both on x positions that are evenly divisible by 32
				if enemy.x % tileClass.Tile.width == 0 and enemy.y % tileClass.Tile.height == 0:

					tn = player.get_number()       #current tile number

					N = tn + -(tileClass.Tile.V)   #define tiles directly North, South, East, and West of player, this will be vulnerability field
					S = tn + (tileClass.Tile.V)
					E = tn + (tileClass.Tile.H)
					W = tn + -(tileClass.Tile.H)

					vulnerability_field = [N, S, E, W, tn]        #all current tiles around our player

					if enemy.get_number() in vulnerability_field: #if enemy is in our vulnerability field, start subtracting health
						player.health -= 5
						sound = pygame.mixer.Sound("../Audio/playerBeingHit.ogg")
						if total_frames%(FPS/2) == 0:
							sound.play()
							sound.set_volume(0.1) 

			if enemy.health <= 0:
				Enemy.List.remove(enemy)    #remove enemy from list if dead
				sound = pygame.mixer.Sound("../Audio/enemyDeath.wav")
				sound.play()
				sound.set_volume(0.1)
				player.enemies_killed += 1

			if enemy.tx != None and enemy.ty != None: #Target is set
				X = enemy.x - enemy.tx
				Y = enemy.y - enemy.ty

				vel = 2

				if kill_count >= 10:
					vel *= 2
				if kill_count >= 30:
					vel *= 4
				if kill_count >= 60:
					vel *= 8

				if X < 0: #right
					enemy.x += vel
					enemy.rotate("e", Enemy.original_img)
				elif X > 0: #left
					enemy.x -= vel 
					enemy.rotate("w", Enemy.original_img)

				if Y > 0: #up
					enemy.y -= vel
					enemy.rotate("n", Enemy.original_img)
				elif Y < 0: #down
					enemy.y += vel
					enemy.rotate("s", Enemy.original_img)

				if X==0 and Y==0:
					enemy.tx, enemy.ty = None, None
		
	@staticmethod
	def spawn(total_frames, FPS, kill_count):
		spawn_rate = FPS*5

		if kill_count > 10:
			spawn_rate = FPS*4
		if kill_count > 20:
			spawn_rate = FPS*3
		if kill_count > 30:
			spawn_rate = FPS*2
		if kill_count > 40:
			spawn_rate = (FPS)

		if total_frames % (spawn_rate) == 0:      #every spawn rate

			# if total_frames % (FPS*6) == 0:     #sounds might overlap, so I do this less often
			sound = pygame.mixer.Sound("../Audio/enemySpawn.wav")
			sound.play() #play enemySpawn sounds
			sound.set_volume(0.1)

			r = randint(0, len(Enemy.spawn_tiles) - 1)  #get psuedo random index
			tile_num = Enemy.spawn_tiles[r]             #make it the tile number
			spawn_node = tileClass.Tile.get_tile(tile_num)        #get the object tile for that number
			Enemy(spawn_node.x, spawn_node.y)           #create the enemy at that tile


class Player(BaseCharacter):

	guns_img = [pygame.image.load("../Images/pistol.png"),
				pygame.image.load("../Images/shotgun.png"),
				pygame.image.load("../Images/automatic.png")]

	guns_ammo = {"pistol" : 30, 
                   "shotgun" : 25,
                   "automatic" : 100}

	health = 1500

	def __init__(self,x,y):

		#get ammo
		self.pistol_ammo = Player.guns_ammo["pistol"]
		self.shotgun_ammo = Player.guns_ammo["shotgun"]
		self.automatic_ammo = Player.guns_ammo["automatic"]

		self.health = Player.health
		self.enemies_killed = 0
		self.current_gun = 0 #0 = pistol, 1 = shotgun, 2 = automatic
		self.direction = "n"
		self.img = pygame.image.load("../Images/Sim_n.png")

		BaseCharacter.__init__(self, x, y)

	def get_projectile_type(self): #get which gun player is holding, to return the proj type

		if self.current_gun == 0:
			return "pistol"
		elif self.current_gun == 1:
			return "shotgun"
		elif self.current_gun == 2:
			return "automatic"


	def draw(self, screen): #draws player and gun to screen

		h = self.width // 2
		img_for_gun = Player.guns_img[self.current_gun]

		if self.direction == "n":                                         #if facing north or west, blit the gun first, then the player
			screen.blit(img_for_gun, (self.x + h, self.y))

		if self.direction == "w":
			img_for_gun = pygame.transform.rotate(img_for_gun, 90)        #CCW turn
			screen.blit(img_for_gun, (self.x - 5, self.y + h - 2))

		screen.blit(self.img, (self.x, self.y))

		if self.direction == "e":
			west = pygame.transform.rotate(img_for_gun, 90)
			img_for_gun = pygame.transform.flip(west, True, False)
			screen.blit(img_for_gun, (self.x + h, self.y + h + 2))

		if self.direction == "s":
			img_for_gun = pygame.transform.flip(img_for_gun, False, True) #Flip the orientation of the gun from north to south
			screen.blit(img_for_gun, (self.x, self.y + h))

	def rotate(self, direction):                                          #rotates player to the direction we input

		path = "../Images/Sim_"
		png = ".png"

		if direction == "n":
			if self.direction != "n":                                     #check if not already in this direction
				self.direction = "n"
				self.img = pygame.image.load(path + direction + png)

		if direction == "s":
			if self.direction != "s": #check if not already in this direction
				self.direction = "s"
				self.img = pygame.image.load(path + direction + png)

		if direction == "e":
			if self.direction != "e": #check if not already in this direction
				self.direction = "e"
				self.img = pygame.image.load(path + direction + png)

		if direction == "w": 
			if self.direction != "w": #check if not already in this direction
				self.direction = "w"
				self.img = pygame.image.load(path + direction + png)

	def movement(self): #smooth player movement

		if self.tx != None and self.ty != None: #Target is set
			X = self.x - self.tx                #Find x difference between player and target (next tile)
			Y = self.y - self.ty                #Find y difference between player and target (next tile)

			vel = 8                             #this will be players movement speed

			if X < 0: #right
				self.x += vel
			elif X > 0: #left
				self.x -= vel 

			if Y > 0: #up
				self.y -= vel
			elif Y < 0: #down
				self.y += vel

			if X==0 and Y==0:
				self.tx, self.ty = None, None

class Projectile(pygame.Rect):

	width, height = 7, 10 #edit this later
	List = []

	projectile_img_collection = {"pistol" : pygame.image.load("../Images/pistol_b.png"),
							"shotgun" : pygame.image.load("../Images/shotgun_b.png"),
							"automatic" : pygame.image.load("../Images/automatic_b.png")}

	projectile_dmg = {"pistol" : (Enemy.health // 4),
						"shotgun" : Enemy.health // 2,
						"automatic" : (Enemy.health // 7) + 1}

	def __init__(self, x, y, velx, vely, direction, type_):

		self.type = type_
		self.direction = direction
		self.velx, self.vely = velx, vely

		if direction == "n":
			self.img = Projectile.projectile_img_collection[type_]

		if direction == "s":
			self.img = pygame.transform.flip(Projectile.projectile_img_collection[type_], False, True)

		if direction == "e":
			west = pygame.transform.rotate(Projectile.projectile_img_collection[type_], 90) 
			self.img = pygame.transform.flip(west, True, False)

		if direction == "w": 
			self.img = pygame.transform.rotate(Projectile.projectile_img_collection[type_], 90) #CCW

		pygame.Rect.__init__(self, x, y, Projectile.width, Projectile.height)
		Projectile.List.append(self)

	def offscreen(self, screen):

		if self.x < 0:
			return True
		elif self.y < 0:
			return True
		elif self.x + self.width > screen.get_width():
			return True
		elif self.y + self.height > screen.get_height():
			return True
		else:
			return False

	@staticmethod
	def update_thenDraw_thenDetectCollision_loop(screen):

		for projectile in Projectile.List:

			#update projectile position
			projectile.x += projectile.velx
			projectile.y += projectile.vely

			screen.blit(projectile.img, (projectile.x, projectile.y)) #draw projectile to screen

			if projectile.type == "pistol":
				sound = pygame.mixer.Sound("../Audio/pistolFire.wav")
			elif projectile.type == "shotgun":
				sound = pygame.mixer.Sound("../Audio/shotgunFire.wav")
			elif projectile.type == "automatic":
				sound = pygame.mixer.Sound("../Audio/automaticFire.wav")

			sound.play()
			sound.set_volume(0.02)

			if projectile.offscreen(screen): #if projectile if off the screen, remove it from list of projectiles
				sound.stop()
				Projectile.List.remove(projectile)
				continue #skip the rest

			for enemy in Enemy.List:

				if projectile.colliderect(enemy): #see if projectile has collided with enemy
					enemy.health -= Projectile.projectile_dmg[projectile.type]
					sound.stop()
					Projectile.List.remove(projectile) #remove projectile from list
					break

			for tile in tileClass.Tile.List:

				if projectile.colliderect(tile) and not(tile.walkable):
					try:
						sound.stop()
						Projectile.List.remove(projectile)
					except:
						pass #Projectile not in list
