#Libraries
from turtle import left
import pygame
pygame.mixer.init()
import math
from settings import * #Imports contents from the settings file

#A class: Contains no parameters - extracts files from their location and allows them to be used
class SpriteSheet:
    #A __init__ (initialise) method: Containing the parameters self, filename - sets the variables
    def __init__(self, filename):
        self.filename = filename
        self.sheet = pygame.image.load(self.filename).convert_alpha() #Loads the game faster by loading the files quickly
    
    #Sprite_get method: Contains the parameters self, x, y, width, height - Cuts out individual sprites from the spritesheet and gets the corresponding sprite
    def sprite_get(self, x, y, width, height):
        sprite = pygame.Surface([width, height]) #Creating the surface of the sprites with the width and height  
        sprite.blit(self.sheet, (0, 0), (x, y, width, height)) #The third parameter creates a cut out of the sprite sheet so that only the selected sections are used to make the sprite animated. 
        #Blit is a function to draw an image loaded in 
        sprite.set_colorkey(BLACK) #Setting the sprite background colour to black
        return sprite #Returns the sprite to draw on the screen

#A class: containing no parameter - It creates the player
class Player:
    #A __init__ (initialise) method: Contains the parameters: self, x, y, data, sprite_sheet, animations - This sets the main variables that will be continuously used 
    def __init__(self, x, y, data, sprite_sheet, animations):
        self.x = x #Defines x
        self.y = y #Defines y

        self.x_change = 0 #Sets the value of the player movement of the x coordinate to 0
        self.y_change = 0 #Sets the value of the player movement of the y coordinate to 0

        self.velocity = 0 #Creating velocity and setting it to 0, which is how fast the player jumps into the air
        self.gravity = 2.2 #Gravity tells us the rate at which we falls back down to the ground surface, as the setting 2.2

        self.jump = False #Creating jump state and setting to false
        self.super_jump = False
        self.super_jump_uses = 10

        self.attacking = False #The player attacking is set to condition False
        self.attack_cooldown = 0

        self.facing = 'idle' #Creating a facing state, telling us the which way the player is facing. For now, it is set to idle
        self.target_lock = False #Facing the enemy is set to false

        self.run = False

        #Gets the data from the CHARATER_DATA in settings.py
        self.size = data[0] #Gets the character size from position 0 from the list CHARACTER_DATA
        self.scale = data[1] #Gets the character scale from position 1 from the list CHARACTER_DATA
        self.animation_list = self.sprite_animation(sprite_sheet, animations) #Makes a list of animation where it runs through the sprite sheet
        self.action = 0 #The specific action done by the sprite: 0:idle, 1:Left/Right run, 2:Jump, 3:Attack
        self.frame_index = 0 #Sets a frame_index to 0, indicating the entites animation frame in order to loop through the animation
        self.image = self.animation_list[self.action][self.frame_index] #The image stores the animation list of the action and frame index

        self.time = pygame.time.get_ticks() #From the pygame module, where it sets a timer. This is used for the animation loop

        self.rect = pygame.Rect((x, y, 80, 80)) #Drawing the image react for the player

        self.health = 200 #Sets the health value to 200
        self.hit = False #Sets hit as false
        self.life = True #Sets the life to true

        #Player Sound
        self.sword_slash = pygame.mixer.Sound('Music/Sword Strike.wav')
        self.sword_slash.set_volume(0.6)

        self.jump_sound = pygame.mixer.Sound('Music/Jump.wav')
        self.jump_sound.set_volume(1)

    #Update method which updates the other functions
    def update(self):
        self.movement() #Calls movement method
    
    #sprite_animation method: containing the sprite_sheet and animation method - This method draws the animation from the list on to the surface of the screen
    def sprite_animation(self, sprite_sheet, animations):
        animation_list = [] #The main list of the animations
        for y, animation in enumerate(animations): #A nested for loop that goes down the sprite sheet columns to load the sprites
            sprite_list = [] #A list containing the sprties
            #This loop goes through the rows of the sprite sheet
            for x in range(animation): #A loop that goes through the animation of the rows
                sprite = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size) #Gets the single image for the sprite
                sprite_list.append(sprite) #Appends sprites onto the sprite list
            animation_list.append(sprite_list) #Appends the sprite list into the animation list
        return animation_list #Returns the animation list

    #animation method - This method run the animation of the player during certain actions
    def animation(self):
        if self.life == True: #Checks if the player is alive
            if self.hit == True: #Checks if the player has been hit
                self.action_update(4) #Does action 4
                if self.health <= 0: #Checks if the players health is less than or equal to 0
                    self.health = 0 #Sets the health to 0
                    self.life = False #Sets the life to false as the player has died
                    self.collide = False #Sets collide to false, so the player is not colliding with the enemy
                    self.action_update(5)
            elif self.run == True: #Checks if the run state is true
                self.action_update(1) #Updates the action to 1
            elif self.jump == True: #Checks if the player is jumpong
                self.action_update(2) #Does the action of index 2
            elif self.attacking == True: #Checks if attacking is true
                self.action_update(3) #Does the action of index 3
            elif self.health <= 0: #Checks if the players health is less than or equal to 0
                self.health = 0 #Sets the health to 0
                self.life = False #Sets the life to false
                self.action_update(5) #Does action 5
            else:
                self.action_update(0) #Updates action 0
        else:
            self.hit = False #Sets hit to false as the player is no longer hit
            self.collide = False #Sets the collide to false as the player is no longer is colliding

        cooldown = 100 #A cooldown timer set to 150
        self.image = self.animation_list[self.action][self.frame_index] #Sets the image to the animation list with the action an frame index
        if pygame.time.get_ticks() - self.time > cooldown: #A tick system where it checks if the tick subtracted by time is greater than the cooldown
            self.frame_index += 1 #Increments the frame index by 1
            self.time = pygame.time.get_ticks() #Sets the time to tick
        if self.frame_index >= len(self.animation_list[self.action]): #Checks if the frame index is greater or equal to the length of the animation list and action
            if self.life == False: #Checks if the player is alive
                self.frame_index = len(self.animation_list[self.action]) - 1 #Sets the frame index to the length of the animation list and the action
            else:
                #reset conditions
                self.frame_index = 0 #Sets the frame index back to 0
                if self.action == 3: #Checks if the action is attack
                    self.attacking = False #Sets attacking to false
                    self.attack_cooldown = 10 #Sets the cooldown to 10
                if self.action == 4: #Checks if the action is 4
                    self.hit = False #Sets hit to false
                    self.attacking = False #Sets attacking to false
                    self.attack_cooldown = 10 #Sets the cooldown back to 10

    #movement method: containing the parameters self, width, height, surface and enemies - dedicated for all the movement function of the game.
    def movement(self, width, height, enemies):
        input = pygame.key.get_pressed() #input is assinged to the pygame module, where it checks if keyboard keys are pressed

        self.run = False

        #Prevent other actions from colliding from each other
        if self.attacking == False and self.life == True:

            if input[pygame.K_a]: #Checks if the input is 'a' key
                self.x_change = -PLAYER_SPEED #The player movement of the x coordinate is subtracted by the player speed, making the sprite move left
                self.run = True
                self.facing = 'left' #Tells the code the sprite is facing left
            else:
                self.x_change = 0 #This stops the player from continously moving, so it is set to 0
            
            if input[pygame.K_d]: #Checks if the input is the 'd' key
                self.x_change = +PLAYER_SPEED #The player movement of the x coordinate is added by player speed, making it move right
                self.run = True
                self.facing = 'right' #Tells the code the sprite is facing right
            
            if input[pygame.K_p]: #Checks if the key pressed is p
                self.attacks(enemies) #Attacks the enemies on the screen
                self.sword_slash.play()

            if input[pygame.K_w] and self.jump == False: #Checks if the input is the 'w' key and if the the self.jump condition is false 
                self.jump_sound.play()
                self.velocity = -13  #Changes the velocity from 0 to -11
                self.facing = 'up' #Tells the code that the sprite is facing up
                self.jump = True #When 'w' keys is pressed, changes the jump state to true

            #The same setup as the 'w' key, but for SPACE
            if self.super_jump_uses != 0: #Checks if the super jumpes the player has is not equal to 0 
                if input[pygame.K_SPACE] and self.super_jump == False:
                    self.jump_sound.play()
                    self.velocity = -20
                    self.facing = 'up'
                    self.super_jump = True
                    self.super_jump_uses -= 1 #Subtracts the super juper by 1
      
        self.velocity += self.gravity #Adds velocity to gravity, so that gravity can pull down the sprite back to the ground surface
        self.y_change += self.velocity #Adds the y change to velocity to tell the code the change in the y coordinate
        
        self.rect.x += self.x_change #Adds a rectangle to the player x change
        self.rect.y += self.y_change #Adds a rectangle to the player y chnage
        
        if self.attack_cooldown > 0: #Check if the cooldown is greater than 0
            self.attack_cooldown -= 1 #Subtracts the cooldown by 1

        #Checks if the player is jumping
        if (self.rect.bottom + self.y_change) > height - 26: #Checks if the bottom of the player rect plus the change in y coordinate is greater than the height - 131(the ground level)
            self.velocity = 0 #Sets the velocity back to 0
            self.jump = False #Sets the jump condition back to false
            self.super_jump = False
            self.y_change = height - 26 - self.rect.bottom #Sets the y change to height substracted by the 131 and the players bottom rect
            
        #Checks for collision with border
        if (self.rect.left + self.x_change) < 0: #Checks whether the left rectangle added with the x change is less than 0
            self.x_change = 0 - self.rect.left #When the sprite's left rectangle side touches the border, it stops the player from moving off the screen
            self.rect.left = 0 #Resetting the left rectangle to 0 to stop player going past border
        if (self.rect.right + self.x_change) > width: #Checks whether the right rectangle added with the x change is less than the screen width (1280)
            self.x_change = width - self.rect.right #When the sprite's right rectangle side touches the border, it stops the player from movign off the screen
            self.rect.right = width #Resets the right rectangle back to width to prevent player going past the border

        '''
        cooldown = 125
        cool = False
        if pygame.time.get_ticks() - self.time > cooldown: 
            if (self.rect.bottom + self.y_change) > height - 26: #Checks if the bottom of the player rect plus the change in y coordinate is greater than the height - 131(the ground level)
                self.velocity = 0 #Sets the velocity back to 0
                self.super_jump = False #Sets the jump condition back to false
                self.y_change = height - 26 - self.rect.bottom #Sets the y change to height substracted by the 131 and the players bottom rect
                cool = True
        if cool == False:
            cooldown -= 1
        '''

        #Player faces the enemy
        if enemies.rect.centerx > self.rect.centerx: #Checks is the enemy x center rect is greater than the player center x rect
            self.target_lock = False #If true, player is facing right of the enemy
        else:
            self.target_lock = True #If false, player is facing left of the enemy

    #Attack method: Conains self, surface and enemies as parameters. Allows the player to attack the enemy
    def attacks(self, enemies):
        if self.attack_cooldown == 0:
            self.attacking = True #Sets the self.attacking to true
            self.attack_rect = pygame.Rect(self.rect.centerx - (self.rect.width * 1.2 * self.target_lock), self.rect.y, self.rect.width * 0.8, self.rect.height) #Sets the attack rectangle, 
            #where the attack_rect is at the center of the player rect. 
            #This is subtracted by times 0.5 width and target lock to flip the sprite of where the enemies are. 
            #The self.rect.y is then called and self.width is multiplied by 0.3 to create the width of the attack_rect. The height is also called
            if self.attack_rect.colliderect(enemies.rect): #Checks whether the self.attack_rect is colliding with the enemy rect          
                enemies.hit = True
                enemies.health -= 20 #Reduces the enemy health by 20

    #action_update method: Containing the self and new_action parameters - It checks whether there is a new action done
    def action_update(self, new_action):
        self.new_action = new_action #Defines new_action as self

        if self.new_action != self.action: #Checks if new_action is not equal to action
            self.action = self.new_action #action is set to the new_action
            self.frame_index = 0 #Sets the frame index to 0
            self.time = pygame.time.get_ticks() #Resets the timer

    #draw method: Containing the parameters self and surface - Draws the player on the screen.
    def draw(self, surface):
        playerLock = pygame.transform.flip(self.image, True, False) #This flips the player (self.image) dependng on the way the player is facing. 
        #True indicates the player is flipped and false stops the player and False preventing the sprite flipping up or down      
        if self.facing == 'left':
            surface.blit(playerLock, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y)) #Draws the playerLock with the rect x and y on the surface

#Enemy Class - no inheritance
class Enemy:
    #A __init__ (initialise) method: Contains the parameters: self, x, y, data, sprite_sheet, animations - This sets the main variables that will be continously used
    def __init__(self, x, y, data, sprite_sheet, animations):
        self.x = x #Defines x as self
        self.y = y #Defines y as self

        self.x_change = 0 #Sets the change in the x coordinate to 0
        self.y_change = 0 #Sets the chnage in the y coordinate to 0

        self.target_lock = False #A condition set to false where it checks if the enemy is facing the player
        
        self.run = False

        #Gets the data from the ENEMY_DATA in settings.py
        self.size = data[0] #Gets the size of the enemy from index postiion 0
        self.scale = data[1] #Gets the scale of the enemy from index position 1
        self.offset = data[2] #Gets the offset of the enemy from the index position 2
        self.animation_list = self.sprite_animation(sprite_sheet, animations) #Makes a list of animations to run through
        self.action = 0 #0:idle, 1:run_right, 2:run_left
        self.frame_index = 0 #Setting the frame index to 0
        self.image = self.animation_list[self.action][self.frame_index] #Sets the image to the animation list where it contains the action and frame index

        self.time = pygame.time.get_ticks() #From the pygame module, where it sets a timer. This is used for the animation loop
    
        self.rect = pygame.Rect((x, y, 60, 30)) #Drawing the image react for the enemy

        self.collide = False
        self.attacking = False

        self.run = False

        self.health = 100 #Sets enemy health to 0
        self.hit = False
        self.life = True
        
        #Sound
        self.hurt_sound = pygame.mixer.Sound('Music/Hurt.wav')
        self.hurt_sound.set_volume(1)

        self.enemy_death_sound = pygame.mixer.Sound('Music/Enemy Death.wav')
        self.enemy_death_sound.set_volume(2)

    #sprite_animation method: containing the sprite_sheet and animation method - This method draws the animation from the list on to the surface of the screen
    def sprite_animation(self, sprite_sheet, animations):
        animation_list = [] #The main list contianing the main animations
        for y, animation in enumerate(animations): #A nested for loop that goes down the sprite sheet columns to load the sprites
            sprite_list = [] #A list containing the sprites
            #This loop goes through the rows of the sprite sheet
            for x in range(animation): #A loop through the animation of the eenmy
                sprite = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size) #Gets the single image for the sprite
                sprite_list.append(pygame.transform.scale(sprite, (self.size * self.scale, self.size * self.scale))) #Gets the single image from the sprite sheet
            animation_list.append(sprite_list) #Appends the sprite list into the animation list
        return animation_list #Returns the animation list
 
    #animation method - This method run the animation of the enemy during certain actions
    def animation(self):
        if self.life == True:
            if self.collide == True: #Checks if attacking is true
                self.action_update(2) #Does the action of index 3
                self.attacking = True
                self.run = False
            elif self.hit == True: #Checks if the enemy has been hit
                self.action_update(3) #Does action 3
            elif self.health <= 0: #Checks if the enemy health is less than or equal to 0
                self.health = 0 #Sets the health to 0
                self.enemy_death_sound.play()
                self.hit = False #Sets hit to false
                self.life = False #Sets the life to false
                self.action_update(4) #The enemy does action 4
            elif self.run == True: #Checks if the run state is true
                self.action_update(1) #Updates the action to 1
            else :
                self.action_update(0) #Updates the action to 0

        cooldown = 100 #A cooldown timer which conuntdown from 100
        self.image = self.animation_list[self.action][self.frame_index] #Sets the image to the animation list with the action and frame index
        if pygame.time.get_ticks() - self.time > cooldown: #A tick system where it checks if the tick subtracted by time is greated than the cooldown
            self.frame_index += 1 #Increments the frame index by 1
            self.time = pygame.time.get_ticks() #Resets the timer
        if self.frame_index >= len(self.animation_list[self.action]): #Checks if the frame index if greater or equal to the length of the animation list and action
            if self.life == False: #Checks if the enemies life is false 
                self.frame_index = len(self.animation_list[self.action]) - 1 #Sets the frame index to the length of the animation list and the action all subtracted by 1
            else:
                #reset conditions
                self.frame_index = 0 #Sets the frame index back to 0
                if self.action == 3: #Chekcs if the action by the enemyt is 3
                    self.hit = False #sets hit to false
                    self.attacking = False #Sets attacking to false
                    self.run = False
                if self.action == 4: #Checks if the action is 4
                    self.life = False #Sets life to false
                    self.collide = False #Sets collision to false
                    self.hit = False #Sets the hit to false
                if self.action == 2:
                    self.collide = False
                    self.run = False 
                if self.action == 1:
                    self.attacking = False
                    self.hit = False

    #movement method: Containing the parameters self and player: This allows the enemy to move
    def movement(self, player):
        self.attack(player) #Attakc the player

        if player.rect.centerx > self.rect.centerx: #Cheks if the player centre rect is greater than the enemy rect 
            self.target_lock = False #Sets targelock to false
        else:
            self.target_lock = True #Sets target_lock to true - faces the player   

        try:
            self.x_change = player.rect.x - self.rect.x #Sets the x change to player rect subtracted by the x rect
            #self.y_change = player.rect.y - self.rect.y #Sets the y change to the player rect subtracted by the y rect
            
            if self.rect.x <= player.rect.x: #Checks if the enemy x position is less than or equal to the player rect x coordinate
                self.x_change = ENEMY_SPEED #Sets the enemy x change to the enemy speed. This means the enemy move left
                self.run = True #Sets te run condition to true
           
            if self.rect.x >= player.rect.x: #Checks if the enemey x position is greater than or equal to the player rect x coordinate
                self.x_change = -ENEMY_SPEED #Sets the enemy x change to negative enemy speed. This means the enemy move right
                self.run = True
            
            if self.attacking == True or self.hit == True or self.health <= 0: #Checks if the enemy is attacking or is being hit
                self.x_change = 0 #Sets the x change to 0

            if player.health <= 0:
                self.x_changed = 0
                self.run = False
           
            distance = math.hypot(self.x_change) #Sets the distace and returns the Euclidean norm. This is the orginal distance.
            #distance = math.hypot(self.x_change, self.y_change) #Sets the distace and returns the Euclidean norm. This is the orginal distance.
            self.x_change - self.x_change / distance #Sets the x change and y chnage divided by distance
            #self.y_change - self.y_change / distance
        except ZeroDivisionError: #The code above expects to have a zero division error
            result = 0 #Sets the result to 0

        self.rect.x += self.x_change #The rect x is added to the x change
        #self.rect.y += self.y_change #The rect y is added to the y change

    #A methods which allows the enemy to attack
    def attack(self, player):
      if self.rect.colliderect(player.rect): #Checks if the enemy rectangle collides with the player rectangle
          self.collide = True #Sets the collide variable to true
          if self.collide and self.life == True: #Checks if collide is true and the enemy is alive
              self.attacking = True
              player.hit = True
              player.health -= 0.8 #The player loses 0.8 health
          else:
              player.health -= 0 #Player loses no health
    
    #action_update method: Containing the self and new_action parameters - It checks whether there is a new action done
    def action_update(self, new_action):
        self.new_action = new_action #Defines new_action as self

        if self.new_action != self.action: #Checks if new_action is not equal to action
            self.action = self.new_action #action is set to the new_action
            self.frame_index = 0 #Sets the frame index to 0
            self.time = pygame.time.get_ticks() #Resets the timer

    #draw method - Containing the parameters self and surface - Draws the enemy on the screen and locks the enemies sight on the player     
    def draw(self, surface):
        enemyLock = pygame.transform.flip(self.image, self.target_lock, False) #Flips the enemy sprite to face the enemy. False preventing the sprite flipping up or down 
        surface.blit(enemyLock, (self.rect.x - (self.offset[0] * self.scale), self.rect.y - (self.offset[1] * self.scale))) #Draws the enemy on the screen, where it can flip, sets the offset to the scale of the x and y coordinate

#Surface class: containing the parameter pygame.sprite.Sprite. This is part of the pygame module which allows manipulation of sprites - Makes it load the in-game surface for entities to stand on
class Surface(pygame.sprite.Sprite):
    #__init__ method: Contains the parameters self, x, y - stores the variables
    def __init__(self, x, y):
        self.x = x * SPRITE_SIZE #Multiplies x with the sprite size (in settings.py)
        self.y = y * SPRITE_SIZE #Multiplies y with the sprite size (in settings.py)
        self.width = SPRITE_SIZE #Sets the width to sprite size of 80
        self.height = SPRITE_SIZE #Sets the height to sprite size of 80

        self.image = self.game.surface.sprite_get(300, 600, self.width, self.height) #Gets the image and places to the game surface 

        self.rect = self.image.get_rect() #The image is set to self.rect
        self.rect.x = self.x #Sets the rect of x to self.x
        self.rect.y = self.y #Sets the rect of y to self.y

#Button class - no inheritance needed
class Button:
    #__init__ (Initialises) method - Contains the parameters self, info, x, y, width, height, fg, bg, fontsize - Stores all the variables for the button
    def __init__(self, info, x, y, width, height, fg, bg, fontsize):
        self.font = pygame.font.Font('Pixeltype.ttf', fontsize) #Sets the font and font size for the game

        self.x = x #Sets the x cords of the button
        self.y = y #Sets the y cords of the button

        self.width = width #Set the width of the button
        self.height = height #Sets the height of the button

        self.fg = fg #Sets the fore ground for the text
        self.bg = bg #Sets the background colour for the button

        self.info = info #Sets the information which contains the text in the button

        self.image = pygame.Surface((self.width, self.height)) #Calls image variable which sets the width and height
        self.image.fill(self.bg) #Fills the image rectangle with the background colour
        self.rect = self.image.get_rect() #Creates a rectangle around the image

        self.rect.x = self.x #Creates a rectangle hitbox for the x coordinate
        self.rect.y = self.y #Cretaes a rectangle hitbox for the y coordinate

        self.text = self.font.render(self.info, True, self.fg) #Renders the font, which is stated at the self.font line and the content(info). The True indicates whether anti-aliasing should be on. This makes the font smoother
        self.text_rect = self.text.get_rect(center = (self.width / 2, self.height / 2)) #Puts the text in the middle of the button, being exactly half the button size
        self.image.blit(self.text, self.text_rect) #Draws the image text and rect

    #Clicked function -containing self, pos being the position of the mouse and pressed which checks if the mouse has been pressed
    def clicked(self, pos, pressed):
        if self.rect.collidepoint(pos): #Gets the position of the mouse and checks whether it is collding with the button
            if pressed[0]: #Checks whether the left click (which is 0) is pressed
                return True #If pressed returns True
            return False #If not pressed return False
        return False #If the rectangle of the mouse does not collide, then return false