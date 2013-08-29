"""
# Object-Oriented Labyrinth Generator -- OOGL
# Author: Heikki Juva, heikki@juva.lu
# Date: 29.08.2013
# License: MIT, http://opensource.org/licenses/MIT
"""

import os, sys, getopt
import pygame
import random
from pygame.locals import *

class Room:
	opposite = {'n': 's', 'e': 'w', 'w':'e', 's': 'n'}

	def __init__(self, color, doors = {'n': None, 'e': None, 's': None, 'w': None}):
		self.color = color
		self.drawn = False
		self.doors = doors

	def connect(self, room, direction=None):
		if self == room: return False
		if room in self.doors.values(): return False
		if direction == None:
			for d in self.doors.keys():
				if self.doors[d] == None:
					if room.doors[self.opposite[d]] == None:
						self.doors[d] = room
						room.doors[self.opposite[d]] = self
						return True
			return False
		if direction in self.doors:
			if room.doors[self.opposite[d]] == None:
				self.doors[d] = room
				room.doors[self.opposite[d]] = self
				return True
		return False

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

	
	# Connect rooms together, 
	"""
	i = 0
	while(i < len(labyrinth)):
		room_a = labyrinth[i]
		room_b = random.choice(labyrinth)
		if room_a != room_b:
			if room_a.connect(room_b):
				i = i + 1
			else:
				labyrinth[i+1].connect(room_b)
				i = i + 2
		else:
			room_b = random.choice(labyrinth)
	"""
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
