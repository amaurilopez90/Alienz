import pygame 
import tileClass
from baseClasses import Consumables
from random import randint
from characters import Player

class healthUPS(Consumables):
	List = []

	spawn_tiles = (49, 439)
	healthUPS_boosts = {"apple" : 200,
                      "potion" : 400}

	def __init__(self, x, y, type_):
		Consumables.__init__(self, x, y, type_)
		if self not in healthUPS.List:  #only add health up to the list if it doesn't already exist there
			healthUPS.List.append(self) #we don't want stacking health ups during respawn

	@staticmethod
	def update(screen, player):
		if player.health > 1000:
			player.health = 1000
			
		for consumable in healthUPS.List:

			screen.blit(consumable.img, (consumable.x, consumable.y))

			if consumable.colliderect(player):
				sound = pygame.mixer.Sound("../Audio/heal.ogg") #play heal sound
				sound.play()
				sound.set_volume(0.06)
				player.health += healthUPS.healthUPS_boosts[consumable.type]
				healthUPS.List.remove(consumable)
				break

	@staticmethod
	def spawn():

		for r in range(0, len(healthUPS.healthUPS_boosts)):
			healthUp_types = list(healthUPS.healthUPS_boosts.keys())

			p = randint(0, len(healthUPS.healthUPS_boosts) - 1)

			tile_num = healthUPS.spawn_tiles[r-1]             #make it the tile number
			spawn_node = tileClass.Tile.get_tile(tile_num)        #get the object tile for that number
			healthUPS(spawn_node.x, spawn_node.y, healthUp_types[p]) #create consumable on that tile 	

class ammoPacks(Consumables):
	List = []

	spawn_tiles = (12, 307, 450)
	ammoPacks_boosts = {"pistol_b" : 15,
                      "shotgun_b" : 10,
                      "automatic_b" : 30}

	def __init__(self, x, y, type_):
		Consumables.__init__(self, x, y, type_)
		if self not in ammoPacks.List:  #only add ammo packs to the list if it doesn't already exist there
			ammoPacks.List.append(self) #we don't want stacking ammo packs during respawn

	@staticmethod
	def update(screen, player):
		if player.pistol_ammo > 70: #max ammo for pistol is 50
			player.pistol_ammo = 75
		if player.shotgun_ammo > 55: #max ammo for shotgun is 40
			player.shotgun_ammo = 55
		if player.automatic_ammo > 200: #max ammo for autmatic is 200
			player.automatic_ammo = 200
			
		for consumable in ammoPacks.List:

			screen.blit(consumable.img, (consumable.x, consumable.y))

			if consumable.colliderect(player):
				sound = pygame.mixer.Sound("../Audio/gotammo.wav") #play gotammo sound
				sound.play()
				sound.set_volume(0.8)
				if consumable.type == "pistol_b":
					player.pistol_ammo += ammoPacks.ammoPacks_boosts["pistol_b"]
				if consumable.type == "shotgun_b":
					player.shotgun_ammo += ammoPacks.ammoPacks_boosts["shotgun_b"]
				if consumable.type == "automatic_b":
					player.automatic_ammo += ammoPacks.ammoPacks_boosts["automatic_b"]

				ammoPacks.List.remove(consumable)
				break

	@staticmethod
	def spawn():

		for r in range(0, len(ammoPacks.ammoPacks_boosts)):
			ammoPacks_types = list(ammoPacks.ammoPacks_boosts.keys())

			p = randint(0, len(ammoPacks.ammoPacks_boosts) - 1)

			tile_num = ammoPacks.spawn_tiles[r-1]             #make it the tile number
			spawn_node = tileClass.Tile.get_tile(tile_num)        #get the object tile for that number
			ammoPacks(spawn_node.x, spawn_node.y, ammoPacks_types[p]) #create consumable on that tile 