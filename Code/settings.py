WIDTH = 1280 #A constant for width of screen 
HEIGHT = 615 #A constant for height of screen

FPS = 60 #The frame rate per second
SPRITE_SIZE = 80 #The box of the SPRITE_SIZE

CHARACTER_SIZE = 80 #Gets the character sprite size
CHARACTER_SCALE = 1 #Sets the character scale to 1
CHARACTER_DATA = [CHARACTER_SIZE, CHARACTER_SCALE] #A list containing the character data to be called

ENEMY_SIZE = 80 #Gets the enemy sprite size
ENEMY_SCALE = 3 #Sets the character scale to 3
ENEMY_OFFSET = [30, 36] #Changes the offset of the enemy when scaling. This makes the enemy stand on the surface/platform layer
ENEMY_DATA = [ENEMY_SIZE, ENEMY_SCALE, ENEMY_OFFSET] #A list containing the enemy data to be called

#Speed - A constant speed of the entites
PLAYER_SPEED = 7
ENEMY_SPEED = 2.3

#Animation - How many individual sprites there are within the sprite sheets that makes up the animation
CHARACTER_ANIMATION = [4, 8, 4, 4, 3, 10]
ENEMY_ANIMATION = [9, 6, 12, 5, 23]

#Colour (red, green, blue)
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)
GREY = (188, 188, 188)
LIGHT_GREEN = (19, 203, 118)
LIME = (34, 218, 116)
YELLOW = (203, 173, 19)
RED = (203, 19, 41)