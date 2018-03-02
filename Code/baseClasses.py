import pygame
import tileClass

class BaseCharacter(pygame.Rect):

	width, height = 32, 32

	def __init__(self, x, y):

		self.tx, self.ty = None, None #target tile's x and y 
		pygame.Rect.__init__(self, x, y, BaseCharacter.width, BaseCharacter.height)

	def get_number(self):
		return int(((self.x / self.width) + tileClass.Tile.H) + ((self.y / self.height)*tileClass.Tile.V))  #finds tile number that our character is on

	def get_tile(self):
		return tileClass.Tile.get_tile(self.get_number())

	def set_target(self, next_tile):  #set the target tile as the next tile
		if self.tx == None and self.ty == None:
			self.tx = next_tile.x
			self.ty = next_tile.y

	def rotate(self, direction, original_img): #rotates player to the direction we input

		if direction == "n":
			if self.direction != "n": #check if not already in this direction
				self.direction = "n"
				self.img = original_img

		if direction == "s":
			if self.direction != "s": #check if not already in this direction
				self.direction = "s"
				self.img = pygame.transform.flip(original_img, False, True)

		if direction == "e":
			if self.direction != "e": #check if not already in this direction
				self.direction = "e"
				west = pygame.transform.rotate(original_img, 90) 
				self.img = pygame.transform.flip(west, True, False)

		if direction == "w": 
			if self.direction != "w": #check if not already in this direction
				self.direction = "w"
				self.img = pygame.transform.rotate(original_img, 90) #CCW

class Consumables(pygame.Rect):

	width, height = 16, 16
	List = [] #list of all consumables

	consumables_img_collection = {"apple" : pygame.image.load("../Images/apple.png"),
							"potion" : pygame.image.load("../Images/potion.png"),
							"pistol_b" : pygame.image.load("../Images/pistol_b.png"),
							"shotgun_b" : pygame.image.load("../Images/shotgun_b.png"),
							"automatic_b" : pygame.image.load("../Images/automatic_b.png")}

	# consumable_boosts = {"apple" : (Player.health // 4),
	#                       "potion" : (Player.health // 2)}

	def __init__(self, x, y, type_):

		self.type = type_
		self.img = Consumables.consumables_img_collection[type_]
		pygame.Rect.__init__(self, x, y, Consumables.width, Consumables.height)
		Consumables.List.append(self)

	def get_number(self):
		return int(((self.x / self.width) + tileClass.Tile.H) + ((self.y / self.height)*tileClass.Tile.V))  #finds tile number that our character is on

	def get_tile(self):
		return tileClass.Tile.get_tile(self.get_number())

	# @staticmethod
	# def update(screen, player):
	# 	for consumable in Consumables.List:

	# 		screen.blit(consumable.img, (consumable.x, consumable.y))

	# 		if consumable.colliderect(player):
	# 			player.health += Consumables.consumable_boosts[consumable.type]
	# 			Consumables.List.remove(consumable)
	# 			break
