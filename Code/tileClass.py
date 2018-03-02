import pygame, processing

class Tile(pygame.Rect):   #this class IS a rectangle so, inherit from Rect class
	List = []              #List of tiles
	width, height = 32, 32 #tile width and height
	total_tiles = 1
	H, V = 1, 25           #horizontal and vertical differences in tile numbers


	invalidTiles = (1,2,3,4,5,6,7,8,9,10,16,17,18,19,20,21,22,   #All invalid tiles on the game map
	            26,27,29,30,31,32,51,52,54,55,56,57,76,77,79,80,81,82,
	            83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,100,
	            101,102,104,105,106,107,108,112,113,114,115,116,117,118,
	            119,120,121,122,123,125,126,127,145,146,147,148,150,151,
	            156,157,158,162,162,163,164,165,166,167,168,170,171,172,173,175,
	            176,182,183,184,186,187,188,189,190,191,192,193,195,196,197,198,
	            200,201,207,208,209,211,212,213,214,215,216,222,223,225,226,
	            233,234,236,237,238,239,240,241,247,248,250,251,258,259,261,
	            262,263,264,265,266,272,273,275,276,283,284,286,287,288,289,290,291,
	            300,301,308,309,311,312,313,314,315,316,325,326,330,331,332,333,334,349,350,
	            351,372,373,374,375,376,377,378,379,380,381,382,397,398,399,400,
	            401,402,403,404,405,406,407,422,423,424,425,426,427,428,429,430,431,432,
	            451,452,453,454,455,456,457,458,460,461,462,463,464,465,466,467,472,473,
	            474,475)


                                                                       
	def __init__(self, x, y, Type): #Tile constructor

		self.parent = None                  #What we need for the A* algorithm
		self.H, self.G, self.F = 0, 0, 0    #I will be using F = G + H

		self.type = Type
		self.number = Tile.total_tiles #assign each tile a number. So the first tile will be tile 1, then tile 2, etc.
		Tile.total_tiles += 1

		if Type == "empty": #if empty tile, then you can walk on it
			self.walkable = True
		else:
			self.walkable = False

		pygame.Rect.__init__(self, (x, y), (Tile.width, Tile.height)) #call Rect constructor

		Tile.List.append(self) #add created tile to the list
	@staticmethod
	def get_tile(number):
		for tile in Tile.List: #scroll through each tile in list
			if tile.number == number: #if tile is the one we are looking for, then return that tile
				return tile

	# def draw_tiles(screen):
	# 	half_width = Tile.width // 2
	# 	for tile in Tile.List:
	# 		pass
			# if not(tile.type == "empty"):
			# 	pygame.draw.rect(screen, [40, 40, 40], tile )

			# if tile.G != 0 :
			# 	processing.text_to_screen(screen, tile.G, tile.x, tile.y + half_width, color = [120, 157, 40]) #only important tile information is displayed
			# if tile.H != 0 :
			# 	processing.text_to_screen(screen, tile.H, tile.x + half_width, tile.y + half_width, color = [20, 67, 150])
			# if tile.F != 0 :
			# 	processing.text_to_screen(screen, tile.F, tile.x + half_width, tile.y, color = [56, 177, 177])

			#processing.text_to_screen(screen, tile.number, tile.x, tile.y)                        #after tiles are drawn, add the tile number as text
