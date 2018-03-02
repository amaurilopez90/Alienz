import pygame, sys, processing
from tileClass import Tile
from characters import *
from processing import interaction
from A_Star import A_Star
from consumables import *
from time import sleep

pygame.init()
pygame.font.init() #initialize font module
pygame.mixer.init() #initialize mixer for music

pygame.mixer.music.load("../Audio/gameMusicHighAlert.ogg")   #set up the game's background music
pygame.mixer.music.set_volume(0.06)
pygame.mixer.music.play(-1)                               #keep the music playing on replay    

print(pygame.mixer.music.get_volume())

screen = pygame.display.set_mode((800, 608))
for y in range(0, screen.get_height(), 32): 
	for x in range(0, screen.get_width(), 32):
		if Tile.total_tiles in Tile.invalidTiles:         #total_tiles also keeps track of current tile number. So if the tile is in fact an invalid tile,
			Tile(x, y, "solid")                           #then make the tile a solid type (aka walkable = False)
		else:
			Tile(x, y, "empty")                           #if not then make the tile an empty type (aka walkable = True)


clock = pygame.time.Clock()
FPS = 32
total_frames = 0

gamemap = pygame.image.load("../Images/techbackground.jpg")

player = Player(64, 288)
healthUPS.spawn()
ammoPacks.spawn()
prev_enemies_killed = 0
healthUPS_respawn = False
ammoPacks_respawn = False
while True:

	if player.enemies_killed - prev_enemies_killed == 10:  #healthUPS respawn every time player kills 10 enemies
		healthUPS_respawn = True	
	if player.enemies_killed - prev_enemies_killed == 7: #ammoPacks respawn every time player kills 7 enemies
		ammoPacks_respawn = True

	screen.blit(gamemap, (0,0))                           #display game map
	Enemy.spawn(total_frames, FPS, player.enemies_killed) #start spawning enemies at a rate depending on the total kill count of enemy
	Enemy.update(screen, player, FPS, total_frames, player.enemies_killed)

	player.movement()                                     #start player movement method

	Projectile.update_thenDraw_thenDetectCollision_loop(screen)      #projectile process

	A_Star(screen, player, total_frames, FPS)             #Start A* algorithm
	
	interaction(screen, player, total_frames, FPS)        #start processing user-player interaction (aka translate button presses into actions)

	player.draw(screen)                                   #draw player to screen

	healthUPS.update(screen, player)                      #update consumables
	ammoPacks.update(screen, player)                      

	processing.text_to_screen(screen, "Health: {0}".format(player.health), 40, 520)
	processing.text_to_screen(screen, "Kill Count: {0}".format(player.enemies_killed), 40, 540)
	processing.text_to_screen(screen, "Ammo:", 360, 300)
	processing.text_to_screen(screen, "Pistol: {0}".format(player.pistol_ammo), 360, 320)
	processing.text_to_screen(screen, "Shotgun: {0}".format(player.shotgun_ammo), 360, 340)
	processing.text_to_screen(screen, "Automatic: {0}".format(player.automatic_ammo), 360, 360)

	if healthUPS_respawn == True:
		healthUPS.spawn()
		prev_enemies_killed = player.enemies_killed
		healthUPS_respawn = not(healthUPS_respawn)
	if ammoPacks_respawn == True:
		ammoPacks.spawn()
		prev_enemies_killed = player.enemies_killed
		ammoPacks_respawn = not(ammoPacks_respawn)

	pygame.display.flip()
	clock.tick(FPS)
	total_frames += 1

	if player.health <= 0:
		sleep(1)
		screen.blit(pygame.image.load("../Images/gameover.jpg"), (0,0))
		pygame.display.update()
		break

sleep(4)