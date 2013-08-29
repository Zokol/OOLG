"""
# Object-Oriented Labyrinth Generator -- OOLG
# Author: Heikki Juva, heikki@juva.lu
# Date: 29.08.2013
# License: MIT, http://opensource.org/licenses/MIT
"""

import os, sys, getopt
import pygame
import random
from pygame.locals import *

class Room:
	opposite = {'n': 's', 'e': 'w', 'w':'e', 's': 'n'} # Define opposite doors, used when connecting rooms together, so that going out from north-door will make you come out from south-door of other room.

	def __init__(self, color, doors = {'n': None, 'e': None, 's': None, 'w': None}):
		self.color = color 	# Pygame.Color-object
		self.drawn = False 	# Flag that is set when draw_room processes this object
		self.doors = doors	# Dictionary that contains information of what doors are connected, default is that all doors are connected to None

	# Function that connects this object to other object, if direction si not specified, it selects free direction to connect to
	def connect(self, room, direction=None):
		if self == room: return False 					# Check that we are not trying to connect room to itself
		if room in self.doors.values(): return False 			# Check that this room does not already connect to the room we are trying to connect 
		if direction == None:							# If direction is not specified
			for d in self.doors.keys():					# Iterate door directions
				if self.doors[d] == None:				# If door is not connected
					if room.doors[self.opposite[d]] == None: 	# If the target room has open door at this direction (opposite to our door)
						self.doors[d] = room			# Connect out door to target
						room.doors[self.opposite[d]] = self	# Connect target door to our room
						return True				# All is fine, return True
			return False	# No free door found
		if direction in self.doors:	# If direction was specified, check that we have door in that direction
			if room.doors[self.opposite[d]] == None:	# Check that target has free door at this direction (opposite to our door)
				self.doors[d] = room			# Connect our door to target
				room.doors[self.opposite[d]] = self	# Connect target door to our room
				return True				# All is fine
		return False	# Invalid direction or non-free door

def main(argv):
	labyrinth = []
	
	# Get user provided params for labyrinth size
	try:
		opts, args = getopt.getopt(argv,'s:',["size="])
	except getopt.GetoptError:
		print 'labyrinth.py -s <number_of_rooms>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-s', '--size'):
			labyrinth_size = int(arg)

	# Check if labyrinth size was provided, give warning if not
	try: 
		labyrinth_size
	except NameError:
		print "Didn't specify labyrinth size, defaulting to 1000"
		labyrinth_size = 8000

	# Create given number of rooms, with various colors
	for i in range(labyrinth_size):
		r = lambda: random.randint(0,200)
		color = pygame.Color(r(), r(), r())
		labyrinth.append(Room(color, {'n': None, 'e': None, 's': None, 'w': None}))

	
	# Connect rooms together
	for room_a in labyrinth:
		room_b = random.choice(labyrinth)
		i = 0
		while not room_a.connect(room_b):
			if i < 10: i += 1
			else: break
			room_b = random.choice(labyrinth)
	
	# Do graphics
	if not pygame.font: print "Warning, no fonts"
	if not pygame.mixer: print "Warning, no sound"
	pygame.init()
	screen = pygame.display.set_mode((1000, 1000))
	pygame.display.set_caption('Object Oriented Labyrinth')
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((255,255,255))
	
	# First room is on the center of window
	x = 500
	y = 500

	# Iterate through labyrinth, draw_room runs the same draw_room function for rooms connected
	for room in labyrinth: 
		draw_room(room, [x, y], background)

	# Update background with all the rooms drawn to screen
	screen.blit(background, (0,0))
	pygame.display.flip()
	
	clock = pygame.time.Clock()

	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

def draw_room(room, coords, surface):
	# Sizes of room and corridors
	r_w = 8
	r_h = 8
	c_w = 2
	c_h = 2
	
	# Spacing between rooms, defined by size of corridors 
	dir_spacing = {'n': [-10, 0], 'e': [0, 10], 'w': [0, -10], 's': [10, 0]}

	# Corridor color
	corr_color = pygame.Color(100,100,100)
	
	# Draw room to surface
	pygame.draw.rect(surface, room.color, (coords[0], coords[1], r_w, r_h))

	# Draw corridors
	pygame.draw.rect(surface, corr_color, (coords[0]-2, coords[1]+3, c_w, c_h))
	pygame.draw.rect(surface, corr_color, (coords[0]+3, coords[1]-2, c_w, c_h))
	pygame.draw.rect(surface, corr_color, (coords[0]+3, coords[1]+8, c_w, c_h))
	pygame.draw.rect(surface, corr_color, (coords[0]+8, coords[1]+3, c_w, c_h))
	
	# Tell room-object that it has been drawn, so that the room is not drawn again
	room.drawn = True

	# Iterate the connecting rooms, and run draw_room if some connecting room has not been drawn
	for direction in room.doors:
		if room.doors[direction] != None: # Check if the 'door' is connected to a room
			if not room.doors[direction].drawn: # Check if room has already been drawn
				draw_room(room.doors[direction], [coords[0] + dir_spacing[direction][0], coords[1] + dir_spacing[direction][1]], surface)
	
if __name__ == "__main__":
	main(sys.argv[1:])
