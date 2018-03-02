import pygame, sys
import tileClass
import characters

def interaction(screen, player, total_frames, FPS):

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:#this will be for cycling through guns by pressing e
			if event.key == pygame.K_e:
				player.current_gun += 1
				player.current_gun %= 3 #this will get it to go back to 0 after 2
				sound = pygame.mixer.Sound("../Audio/inventory_sound_effects/cloth-inventory.wav")
				sound.play()
				sound.set_volume(0.1)

			if event.key == pygame.K_SPACE:
				sound = pygame.mixer.Sound("../Audio/gunReload.wav")
				sound.play()
				sound.set_volume(0.4)

	keys = pygame.key.get_pressed()

	if keys[pygame.K_w]: #UP
		future_tile_number = player.get_number() - tileClass.Tile.V        #set the future tile number as the one we are going to walk to
		if future_tile_number in range(1, tileClass.Tile.total_tiles + 1): #this will prevent us from walking off the screen
			future_tile = tileClass.Tile.get_tile(future_tile_number)      #get this tile
			if future_tile.walkable:
				player.set_target(future_tile)                             #set the target tile as the future tile
				player.rotate("n")                                         #rotate player to face north
				#player.y -= player.height

	if keys[pygame.K_s]: #Down
		future_tile_number = player.get_number() + tileClass.Tile.V        #set the future tile number as the one we are going to walk to
		if future_tile_number in range(1, tileClass.Tile.total_tiles + 1): #this will prevent us from walking off the screen
			future_tile = tileClass.Tile.get_tile(future_tile_number)      #get this tile
			if future_tile.walkable:
				player.set_target(future_tile)                             #set the target tile as the future tile
				player.rotate("s")                                         #rotate player to face south
				#player.y += player.height

	if keys[pygame.K_a]: #Left
		future_tile_number = player.get_number() - tileClass.Tile.H        #set the future tile number as the one we are going to walk to
		if future_tile_number in range(1, tileClass.Tile.total_tiles + 1): #this will prevent us from walking off the screen
			future_tile = tileClass.Tile.get_tile(future_tile_number)      #get this tile
			if future_tile.walkable:
				player.set_target(future_tile)                             #set the target tile as the future tile
				player.rotate("w")                                         #rotate the player to face west
				#player.x -= player.width

	if keys[pygame.K_d]: #Right
		future_tile_number = player.get_number() + tileClass.Tile.H        #set the future tile number as the one we are going to walk to
		if future_tile_number in range(1, tileClass.Tile.total_tiles + 1): #this will prevent us from walking off the screen
			future_tile = tileClass.Tile.get_tile(future_tile_number)      #get this tile
			if future_tile.walkable:
				player.set_target(future_tile)                             #set the target tile as the future tile
				player.rotate("e")                                         #rotate the player to face east
				#player.x += player.width
                               
	if keys[pygame.K_LEFT]:                                                #Character rotation with arrow keys
		player.rotate("w")

	elif keys[pygame.K_RIGHT]:
		player.rotate("e")

	elif keys[pygame.K_UP]:
		player.rotate("n")

	elif keys[pygame.K_DOWN]:
		player.rotate("s")

	if keys[pygame.K_SPACE]: #shoot
		proj_type = player.get_projectile_type()                #get projectile type

		if proj_type == "pistol" and total_frames%(FPS*3//4) == 0: #pistols can shoot every .75 second

			if player.pistol_ammo <= 0: #check if out of ammo 
				return
			player.pistol_ammo -= 1 #subtract ammo

			if player.direction == "w" :
				characters.Projectile(player.centerx, player.centery, -10, 0, "w", proj_type)
			elif player.direction == "e":
				characters.Projectile(player.centerx, player.centery, 10, 0, "e", proj_type)
			elif player.direction == "n":
				characters.Projectile(player.centerx, player.centery, 0, -10, "n", proj_type)
			elif player.direction == "s":
				characters.Projectile(player.centerx, player.centery, 0, 10, "s", proj_type)

		elif proj_type == "shotgun" and total_frames%(FPS*6//5) == 0: #shotgun can shoot every 1.2 second

			if player.shotgun_ammo <= 0: #check if out of ammo
				return			
			player.shotgun_ammo -= 1 #subtract ammo

			if player.direction == "w" :
				characters.Projectile(player.centerx, player.centery, -10, 0, "w", proj_type)
			elif player.direction == "e":
				characters.Projectile(player.centerx, player.centery, 10, 0, "e", proj_type)
			elif player.direction == "n":
				characters.Projectile(player.centerx, player.centery, 0, -10, "n", proj_type)
			elif player.direction == "s":
				characters.Projectile(player.centerx, player.centery, 0, 10, "s", proj_type)

		elif proj_type == "automatic" and total_frames%(FPS//5) == 0: #automatic can pretty much spam
			
			if player.automatic_ammo <= 0: #check if out of ammo
				return
			player.automatic_ammo -= 1 #subtract ammo

			if player.direction == "w" :
				characters.Projectile(player.centerx, player.centery, -10, 0, "w", proj_type)
			elif player.direction == "e":
				characters.Projectile(player.centerx, player.centery, 10, 0, "e", proj_type)
			elif player.direction == "n":
				characters.Projectile(player.centerx, player.centery, 0, -10, "n", proj_type)
			elif player.direction == "s":
				characters.Projectile(player.centerx, player.centery, 0, 10, "s", proj_type)


def text_to_screen(screen, text, x, y, size = 10, color = (255,255,255), font_type = "lucidahandwriting"):

	try:

		text = str(text)
		font = pygame.font.SysFont(font_type, size) #choose the font
		text = font.render(text, True, color)       #render the text
		screen.blit(text, (x, y))                   #blit to screen at xy position

	except Exception(e):
		print("Font Error, saw it coming")
		raise e