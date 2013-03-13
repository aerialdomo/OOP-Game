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

# if GAME_WIDTH > 7 and GAME_HEIGHT > 7:

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


# class Character_Change(Character):
# 	IMAGE = "Horns"

# 	def __init__(self):
# 		GameElement.__init__(self)
# 		GAME_BOARD.register(self)
# 		GAME_BOARD.set_el(4, 4, self)

class Gem(GameElement):
	SOLID = False	

	# def interact(self):
	# 	pass # Do stuff

class BlueGem(Gem):
	IMAGE="BlueGem"

	#changes gem to another thing
	def interact(self, player):
		player.inventory.append(self)
		GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))

# class EvilBlueGem(Gem):
# 	IMAGE="BlueGem"

# 	def interact(self, new_char):
# 		#change into Horns
# 		# NEW_CHAR = Character_Change()
# 		# GAME_BOARD.del_el(player.x, player.y)
# 		# GAME_BOARD.register(NEW_CHAR)
# 		# GAME_BOARD.set_el(4, 4, NEW_CHAR)
# 		new_char.IMAGE = "RedGem"
# 		print new_char.IMAGE
	
class OrangeGem(Gem):
	IMAGE = "OrangeGem"
# class Gem_Props(Gem, ):
	
	#adds things to inventory
	def interact(self, player):
		player.inventory.append(self)
		GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))
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

	#Initializing Horns
	# global NEW_CHAR
	# NEW_CHAR = Character_Change()
	# if NEW_CHAR == (5,5, PLAYER):
	# 	GAME_BOARD.register(NEW_CHAR)
	# 	GAME_BOARD.del_el(5, 5)
	# 	GAME_BOARD.set_el(5, 5, NEW_CHAR)
	# 	print NEW_CHAR.IMAGE

	#message from our sponsors
	GAME_BOARD.draw_msg("The cake is a lie.")

	#gem code
	gem_orange = OrangeGem()
	GAME_BOARD.register(gem_orange)
	GAME_BOARD.set_el(3, 1, gem_orange)

	gem_blue = BlueGem()
	GAME_BOARD.register(gem_blue)
	GAME_BOARD.set_el(1, 1, gem_blue)
	# print "Blue gem", gem_blue.IMAGE

	# evil_blue_gem = EvilBlueGem()
	# GAME_BOARD.register(evil_blue_gem)
	# GAME_BOARD.set_el(4,4, evil_blue_gem)
	# PLAYER.interact
	# GAME_BOARD.del_el(4,4)
	# evil_blue_gem.interact
	# # GAME_BOARD.register(NEW_CHAR)
	# # GAME_BOARD.set_el(4, 4, NEW_CHAR)
	# 


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

	# elif KEYBOARD[key.SPACE]:
	# 	GAME_BOARD.erase_msg()

	if direction:
		next_location = PLAYER.next_pos(direction)
		next_x = next_location[0]
		next_y = next_location[1]

		existing_el = GAME_BOARD.get_el(next_x, next_y)

		if existing_el:
			existing_el.interact(PLAYER)

		# if existing_el

		if existing_el is None or not existing_el.SOLID:
			GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
			GAME_BOARD.set_el(next_x, next_y, PLAYER)


