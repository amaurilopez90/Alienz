import pygame
from characters import *
from tileClass import Tile

def A_Star(screen, player, total_frames, FPS):

	half = Tile.width // 2

	N = -25 #up 25 tiles
	S = 25  #down 25 tiles
	W = -1  #left 1 tile
	E = 1   #right 1 tile

	NW = -26 #up 25 tiles then to the right 1
	NE = -24 #up 25 tiles then to the left 1
	SE = 26  #down 25 tiles then to the right 1
	SW = 24  #down 25 tiles then to the left 1

	for tile in Tile.List:                  #reset our tiles. This will make it so that if we are boxed in an obstacle, the enemy will not find us
		tile.parent = None                  
		tile.H, tile.G, tile.F = 0, 0, 0

	def block_movement(tiles, diagonals, adjacent_tile): #prevents the enemies from moving diagonally. Otherwise they might be able to cut through obstacles
		if adjacent_tile.number not in diagonals:        #only add non-diagonal tiles to the list of valid tiles
			tiles.append(adjacent_tile)
		return tiles

	def get_adjacent_tiles(current_node):
		
		array = (                          #array of all adjacent (surrounding) tile's numbers
			(current_node.number + N),
			(current_node.number + NE),
			(current_node.number + E),
			(current_node.number + SE),
			(current_node.number + S),
			(current_node.number + SW),
			(current_node.number + W),
			(current_node.number + NW),
			)

		tiles = []                         #contains all valid tiles that are around our current_node

		original_node_number = current_node.number
		diagonals = [original_node_number + NE, original_node_number + NW, original_node_number + SE, original_node_number + SW]

		for tile_number in array:          #go through all tiles in above array

			adjacent_tile = Tile.get_tile(tile_number)                       #get the tile
			if adjacent_tile == None:
				continue
				
			if tile_number not in range(1, Tile.total_tiles + 1):            #if surround tiles happen to be off the screen
				continue

			if adjacent_tile.walkable and adjacent_tile not in closed_list:  #if this tile meets our criteria (walkable and not already in closed list)
				#tiles.append(adjacent_tile) #Diagonal movement              #add this tile to the list of all valid tiles that are around our current_node
				tiles = block_movement(tiles, diagonals, adjacent_tile) #Blocky movement

		return tiles                                                         #return this list

	def G(tile):
		difference = tile.number - tile.parent.number 

		if difference in (N,S,E,W):
			#10
			tile.G = tile.parent.G + 10
		elif difference in (NE,NW,SW,SE):
			#14
			tile.G = tile.parent.G + 14
		

	def H():
		for tile in Tile.List:
			tile.H = 10*(abs(tile.x - player.x) + abs(tile.y - player.y)) // Tile.width   #H = x difference + y difference between the tile and our player, times 10

	def F(tile):
		#F = G + H
		tile.F = tile.G + tile.H

	def swap(tile):              #swap the tile from the open list to the closed list
		open_list.remove(tile)
		closed_list.append(tile)

	def get_LFT():               #get lowest F value tile
		F_values = []
		for tile in open_list:
			F_values.append(tile.F)     #load F tiles in list

		reverse = open_list[::-1]       #takes the open list and reverses it

		for tile in reverse:
			if tile.F == min(F_values): #check for lowest F tile. If two are the same, return the last one
				return tile             #which is why we reverse the open list, for speed

	def move_to_G_cost(lowest_F_tile, tile):
		Gvalue = 0
		difference = lowest_F_tile.number - tile.number

		if difference in (N,S,E,W):
			Gvalue = lowest_F_tile.G + 10

		elif difference in (NE,NW,SE,SW):
			Gvalue = lowest_F_tile.G + 14

		return Gvalue

	def loop():
		lowest_F_tile = get_LFT()
		swap(lowest_F_tile)
		adjacent_nodes = get_adjacent_tiles(lowest_F_tile) #find this tile's adjacent nodes

		for node in adjacent_nodes:                                #add adjacent node to open list if not already there
			if node not in open_list:                              #and assign the parent node to the one with lowest F value
				open_list.append(node)
				node.parent = lowest_F_tile

			elif node in open_list:
				#G check                                            #if adjacent node is already in the open list
				calculated_G = move_to_G_cost(lowest_F_tile, node)  #find G cost
				if calculated_G < node.G:                           #if alternative is not worth it
					node.parent = lowest_F_tile                     #parent should be lowest_F_tile
					G(node)
					F(node)

		if open_list == [] or player.get_tile() in closed_list:    #if open list is empty, there is no solution for a path from enemy to player
			return

		for node in open_list:
			G(node)
			F(node)


		loop()
		

	for enemy in Enemy.List:
		if enemy.tx != None or enemy.ty != None:
			continue                  #Enemy is set and has a target tile

		open_list = []                #all the tiles we want to consider
		closed_list = []              #all tiles that are not accessible and we have already checked

		enemy_tile = enemy.get_tile()
		open_list.append(enemy_tile)  #first, add current tile to the open list

		adjacent_nodes = get_adjacent_tiles(enemy_tile) #find current tile's adjacent nodes

		for node in adjacent_nodes:    #scroll through adjacent nodes
			node.parent = enemy_tile   #assign their parent to the current tile
			open_list.append(node)     #add these nodes to the open list

		swap(enemy_tile)               #swap this tile from the open list to the closed list

		H()                            #find the Heuristic values of all tiles relative to our player

		for node in adjacent_nodes:    #scroll through adjacent nodes again 
			G(node)                    #find G value 
			F(node)                    #find F value

		loop()                         #recursive, find lowest F value

		return_tiles = []              #return tiles list

		parent = player.get_tile()

		while True:
			return_tiles.append(parent)

			parent = parent.parent     #get parent's parent, grandparent? Because the very very first tile does not have a parent
			if parent == None:
				break
			if parent.number == enemy.get_number():
				break


		if len(return_tiles) > 1:
			next_tile = return_tiles[-1] #grab the last tile, the tile we want the enemy to move to
			enemy.set_target(next_tile)






