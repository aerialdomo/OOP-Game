import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####

class Rock(GameElement):
	IMAGE = "Rock"
	SOLID = True

class Character(GameElement):
	IMAGE = "Cat"
	SOLID = True
	def next_pos(self, direction):
		if direction == "up":
			return (self.x, self.y -1)
		elif direction == "down":
			return (self.x, self.y + 1)
		elif direction == "left":
			return (self.x-1, self.y)
		elif direction == "right":
			return (self.x+1, self.y)
		return None	

	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []	


class NewChar(Character):
	IMAGE = "Horns"

	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []

	def interact(self):
		pass	

class Gem(GameElement):
	SOLID = False	

class BlueGem(Gem):
	IMAGE="BlueGem"

	def interact(self, player):
		player.inventory.append(self)
		GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))

class Heart(Gem):
	IMAGE="Heart"

	def interact(self, player):
		#change into Horns
		GAME_BOARD.del_el(player.x,player.y)
		HORNS = NewChar()
		GAME_BOARD.register(HORNS)
		GAME_BOARD.set_el(player.x, player.y, HORNS)	
		#set HORNS inventory to be the same as PLAYER
		HORNS.inventory = PLAYER.inventory
		#in game, PLAYER cannot change image mid game unless a new char is created
		global PLAYER
		PLAYER = HORNS	

	
class OrangeGem(Gem):
	IMAGE = "OrangeGem"
	
	#adds things to inventory
	def interact(self, player):
		player.inventory.append(self)
		GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))

class DoorClosed(GameElement):
	IMAGE = "DoorClosed"
	SOLID = True

	def interact(self, player):
		GAME_BOARD.draw_msg("You need 2 Gems to open this door")

		if len(PLAYER.inventory) == 2: 
			GAME_BOARD.del_el(5,5)
			door_open = DoorOpen()
			GAME_BOARD.register(door_open)
			GAME_BOARD.set_el(5,5, door_open)
			GAME_BOARD.draw_msg("Winner Winner Chicken Dinner!")

class DoorOpen(GameElement):
	IMAGE = "DoorOpen"
	SOLID = True

	def interact(self, player):
		pass

# ####   End class definitions    ####

#### Game initialization code here
def initialize():
	rock_positions = [
		(2, 1),
		(1, 2),
		(3, 2),
		(2, 3),
		# (0, 1)
	]

	rocks = []

	for pos in rock_positions:
		#Initialize and register rock
		rock = Rock()
		GAME_BOARD.register(rock)
		GAME_BOARD.set_el(pos[0], pos[1], rock)
		rocks.append(rock)

	rocks[-1].SOLID = False

	for rock in rocks:
		print rock

	# Initializing Girl
	global PLAYER
	PLAYER = Character()
	GAME_BOARD.register(PLAYER)
	GAME_BOARD.set_el(2, 2, PLAYER)
	print PLAYER

	# Initializing Horns
	global HORNS
	HORNS = NewChar()
	GAME_BOARD.register(HORNS)

	#message from our sponsors
	GAME_BOARD.draw_msg("The heart is a lie.")

	#gem code
	gem_orange = OrangeGem()
	GAME_BOARD.register(gem_orange)
	GAME_BOARD.set_el(3, 1, gem_orange)

	gem_blue = BlueGem()
	GAME_BOARD.register(gem_blue)
	GAME_BOARD.set_el(1, 1, gem_blue)
	# print "Blue gem", gem_blue.IMAGE

	heart = Heart()
	GAME_BOARD.register(heart)
	GAME_BOARD.set_el(4, 4, heart)

	door_closed = DoorClosed()
	GAME_BOARD.register(door_closed)
	GAME_BOARD.set_el(5,5, door_closed)


def keyboard_handler():
	direction = None

	if KEYBOARD[key.UP]:
		direction = "up"
	if KEYBOARD[key.DOWN]:
		direction = "down"
	if KEYBOARD[key.LEFT]:
		direction = "left"
	if KEYBOARD[key.RIGHT]:
		direction = "right"

	if direction:
		next_location = PLAYER.next_pos(direction)
		next_x = next_location[0]
		next_y = next_location[1]

		#makes the girl not fall off the map
		if next_x <0 or next_x >= GAME_WIDTH or next_y <0 or next_y >= GAME_HEIGHT:
			return None

		#checking to see if there is already something there
		existing_el = GAME_BOARD.get_el(next_x, next_y)

		if existing_el:
			existing_el.interact(PLAYER)

		#moves the girl	
		if existing_el is None or not existing_el.SOLID:
			GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
			GAME_BOARD.set_el(next_x, next_y, PLAYER)
