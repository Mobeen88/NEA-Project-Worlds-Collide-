#Libraries
import pygame
pygame.mixer.init()
import sys
import random
from sprites import * #Imports contents within the sprites python source code file
from settings import * #Impots contents within the settings python source code file
from camera import *

#Game class: No parameters - Is the main class for the game to run
class Game:
    #__init__ method: Contains the parameter self - Initialises attributes of the object game so it can run and display necessary sprites and backgrounds. 
    #All the methods will contain self, where I am able to recall variables with self to other methods
    def __init__(self): 
        pygame.init() #Initialises pygame in order to use
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Sets the window screen size to WIDTH and HEIGHT from settings file. 
        #The width and height of the screen is stored in an tuple. This is so that it doesn't change the screen size as tuple are unchangable
        self.caption = pygame.display.set_caption('Worlds Collide') #Adds a name to the window bar
        self.clock = pygame.time.Clock() #This is the FPS (Frames per second) which synchronises the game. This tells us the number of images/pixels constantly being displayed in a single second
        self.time = pygame.time.get_ticks() #From the pygame module, where it sets a timer. This is used for the animation loop
        
        self.running = True #Tells us the game is    running

        #The convert_alpha() fucntion matches the window screen. It does calculations which makes it easier for us to load the image without visual glitches
        #Loads spritesheets at png format
        self.entity = pygame.image.load('Graphics/Entity.png').convert_alpha() #Opens the character sprite sheet
        self.enemySprite = pygame.image.load('Graphics/Enemy.png').convert_alpha() #Opens the enemy sprite sheet
        self.surface = SpriteSheet('Graphics/Surface.png')

        #Loads the image backgrounds
        self.background = pygame.image.load('Graphics/Game Screen.png').convert_alpha() #Opens the background of the game.
        self.leftScreen = pygame.image.load('Graphics/Left Scene.png').convert_alpha()
        self.rightScreen = pygame.image.load('Graphics/Right Scene.png').convert_alpha()
        self.trainStation = pygame.image.load('Graphics/Train Station.png').convert_alpha()
        self.pyramid = pygame.image.load('Graphics/Pyramid.png').convert_alpha()

        #Moving images
        self.train = pygame.image.load('Graphics/Train.png').convert_alpha()
        self.train_rect = self.train.get_rect(topleft = (860, 530)) #Creates a rectangle of the train image, where the top left of the train image at coordinate 860, 530 and move the train left of the screen.

        self.player = Player(605, 420, CHARACTER_DATA, self.entity, CHARACTER_ANIMATION) #Creates the player from the player class and loads the character datad
        
        self.x_spawn = random.randint(0, WIDTH - 20) #A random function which selects any part of the map for the enemy to spawn
        self.enemy = Enemy(self.x_spawn, 510, ENEMY_DATA, self.enemySprite, ENEMY_ANIMATION) #Creates the enemy from the enemy class and loads the enemy data

        #Menus
        self.mainMenu = pygame.image.load('Graphics/Main Menu.png').convert() #Opens the main menu screen background
        self.controls_GUI = pygame.image.load('Graphics/Controls.png').convert_alpha()
        self.pauseMenu = pygame.image.load('Graphics/Pause.png').convert_alpha() #Opens the pause menu background
        self.gameOver = pygame.image.load('Graphics/Game Over.png').convert_alpha() #Opens the gameover background
        self.winner = pygame.image.load('Graphics/Winner.png').convert_alpha()

        #Music/Sound either mp3 or wav format
        self.background_music = pygame.mixer.Sound('Music/Background Music.mp3') #Loads the music
        self.background_music.play(-1) #This makes the music loop
        self.background_music.set_volume(0.3) #Sets the volumn of the music

        self.clicked_sound = pygame.mixer.Sound('Music/Click.wav')
        self.clicked_sound.set_volume(1)

        self.enemy_growl_sound = pygame.mixer.Sound('Music/Enemy Growl.wav')
        self.enemy_growl_sound.set_volume(2)

        self.death_sound = pygame.mixer.Sound('Music/Death.wav')
        self.death_sound.set_volume(2)

    #new_game method - Starts a new game
    def new_game(self):
        self.playing = True #If the player quit, then it should destory the interface
        self.all_sprites = pygame.sprite.LayeredUpdates() #An object containing all the sprites in the game making it easier to update the game

    #event method - It is an event loop, looping through the game. This allows the game to run continuously until a condition is met
    def event(self):
        for event in pygame.event.get(): #Gets the event from the pygame module
            if event.type == pygame.QUIT: #if the event is QUIT from the pygame module
                self.running = False #Sets the running state which was true to false to indicate the game has stopped running
                self.playing = False #Sets the playing state to false, indicating that there is no new game

        self.player.animation() #Calls the animation of the player
        self.enemy.animation() #Calls the animation of the enemy

    #update method - which updates the game sprites
    def update(self):
        self.all_sprites.update() #An object containing all the sprites in the game making it easier to update the game 

    #draw method - containing parameters self - draw everything on the screen
    def draw(self):
        self.screen.fill(BLACK) #Fills the screen background with black
        self.all_sprites.draw(self.screen) #Draws all the sprites from the all_spritess group to the screen
        if self.control == True:
            self.controls_screen() #Calls the control_screen method
            if self.returnScreen == True:
                self.screen.fill(BLACK) #Fills the screen black
                self.main_menu() #Calls the main_menu method
        else:
            self.game_screen()

        self.clock.tick(FPS) #Sets the FPS of the game to 60
        pygame.display.update() #Updates the display

    #game_screen method - display the content of the in game screen
    def game_screen(self):
        self.screen.blit(self.background, (0,0)) #Draws the background of tahe game at 0, 0 coordinate
        self.screen.blit(self.rightScreen, (636, 392)) #Draws the right hand of the screen

        self.train_rect.x -= 3 #Moves the rectangle of the train to the left of the x coordinate
        if self.train_rect.right < 400: #Once the trian rect reaches the 400 x coordinate
            self.train_rect.left = 2000 #It should move back to the 2000 x coordinate

        self.screen.blit(self.train, self.train_rect) #Draws both the train and the rectangle of the train

        self.screen.blit(self.leftScreen, (0, 392))
        self.screen.blit(self.trainStation, (646, 391))
        self.screen.blit(self.pyramid, (442, 290))

        self.health_bar(self.player.health, 10, 10) #Draws the players health bar at coordinates 10, 10
        #self.health_bar(self.enemy.health, 850, 10)

        self.enemy.draw(self.screen) #Draws the enemy on the screen
        self.enemy.movement(self.player) #Allows the enemy to move, where the player is the target

        if self.enemy.health <= 0:
            self.enemy
            for i in range(1):
                spawn_timer = 50
                if pygame.time.get_ticks() - self.time > spawn_timer:
                    self.enemy.draw(self.screen)
                    self.enemy.movement(self.player)
                    pygame.time.get_ticks() + self.time < spawn_timer
            i += i

        #Draws and allows the player to move
        self.player.draw(self.screen) #Draws the player on the screen
        self.player.movement(WIDTH, HEIGHT, self.enemy) #Allows the player to move, and do certain action by calling the movement method

        input = pygame.key.get_pressed() #Sets input variable to a pygame function to check is a key is pressed

        if input[pygame.K_ESCAPE]: #Checks if the key pressed is ESCAPE
            self.pause_screen()

        self.clock.tick(FPS)
        pygame.display.update()
    

    #health_bar method: containing the parameters self, health, x and y - it creates the entity health for both player and enemies.
    def health_bar(self, health, x, y):
        health_ratio = health / 200 #A ratio, where the health is divides by 200. This makes it easier to see the visuals of the player losing health

        pygame.draw.rect(self.screen, BLACK, (x - 4, y - 4, 405, 35)) #Draws a black outline of the health bar

        pygame.draw.rect(self.screen, WHITE, (x, y, 400, 30)) #Draws the health bar

        if health >= 150: #Checks if health is greater than 150
            pygame.draw.rect(self.screen, LIGHT_GREEN, (x, y, 400 * health_ratio, 30)) #Draws a green health bar
        elif health >= 100: #Checks if health is greater that 100
            pygame.draw.rect(self.screen, YELLOW, (x, y, 400 * health_ratio, 30)) #Draws an orange health bar
        elif health >= 1: #Checks if health is greater than 1 
            pygame.draw.rect(self.screen, RED, (x, y, 400 * health_ratio, 30)) #Draws a red health bar
        else: #If neither condition is met
            pygame.draw.rect(self.screen, WHITE, (x, y, 400, 30)) #Draws the original white health bar
        
        seconds = 12000 #A variable set to 5000
        if health <= 0: #Checks if the player's health is 0
            self.death_sound.play()
            if pygame.time.get_ticks() - self.time > seconds: #Checks the time is less than the seconds
                self.game_over()
        
        seconds2 = 14000
        if self.enemy.health <= 0:
            if pygame.time.get_ticks() - self.time > seconds2: #Checks the time is less than the seconds
                self.win_screen()

    #control_screen method - Display the control screen
    def controls_screen(self):
        self.screen.blit(self.controls_GUI, (0,0))
        self.return_button() #Calls the return button
      
    #return_button method - Displays and creates the return button
    def return_button(self):
        self.returnScreen = False #Sets this condition to false
        returnButton = Button('Click anywhere to return to main menu', 450, 580, 520, 40, WHITE, BLACK, 45)
      
        while self.control == True: #While main is set to True, it will keep on looping
            for control_event in pygame.event.get(): #Gets the event using the controlEvent variable
                if control_event.type == pygame.MOUSEBUTTONDOWN: #If the event type is clicking the mouse it will set a control to false
                    self.clicked_sound.play()
                    self.returnScreen = True #Sets the returnScreen condition to true
                    self.control = False
                    self.main = True

            #Draw
            self.screen.blit(returnButton.image, returnButton.rect) #Draws the return button image and hitbox 
            self.clock.tick(FPS)
            pygame.display.update()
        
    #loop function - This loops through the events of the game
    def loop(self):
        while self.playing: #As the self.playing condition is True, it will keep on running
            self.event() #Runs all the event occuring. (E.g. Pressing of a certain key or clicking of the mouse) 
            self.update() #Updates the games so it is animated and not a still image
            self.draw() #Displays the sprutes on the screen
        
        self.clock.tick(FPS)
        pygame.display.update()

    #Methods which displays the pause screen
    def pause_screen(self):
        self.paused = True #Setting the paused condition to true 
        returnButton1 = Button('Return', 395, 218, 479, 124, WHITE, BLACK, 50) #Displays the return button
        quitButton1 = Button('QUIT', 395, 420, 479, 124, WHITE, BLACK, 50) #Displays a quit button

        while self.paused: #A loop which will run until paused condition is set to false
            #Similar setup to event function 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            #Gets the mouse and from the sprties.py, it gets the mouse position and pressed
            self.mouse_pos = pygame.mouse.get_pos() #Gets the mouse position
            self.mouse_pressed = pygame.mouse.get_pressed() #Checks if the mouse has been pressed

            if returnButton1.clicked(self.mouse_pos, self.mouse_pressed):
                self.clicked_sound.play()
                self.paused = False

            if quitButton1.clicked(self.mouse_pos, self.mouse_pressed):
                self.clicked_sound.play()
                pygame.time.delay(500) #Delays the program for 500 milliseconds
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
        
            self.screen.blit(self.pauseMenu, (0,0))
            self.screen.blit(returnButton1.image, returnButton1.rect) #Draws the control button image and hitbox
            self.screen.blit(quitButton1.image, quitButton1.rect) #Draws the quit button and hitbox

            self.clock.tick(FPS)
            pygame.display.update()
    
    #win_screen method: It opens the 'You Win' interface
    def win_screen(self):
        self.win = True
        returnButton3 = Button('Return to main menu', 73, 430, 479, 124, WHITE, LIME, 50) #Displays a pause button
        quitButton3 = Button('QUIT', 700, 430, 480, 124, WHITE, LIME, 50) #Displays a pause button      

        while self.win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            #Gets the mouse and from the sprties.py, it gets the mouse position and pressed
            self.mouse_pos = pygame.mouse.get_pos() #Gets the mouse position
            self.mouse_pressed = pygame.mouse.get_pressed() #Checks if the mouse has been pressed

            if returnButton3.clicked(self.mouse_pos, self.mouse_pressed):
                self.clicked_sound.play()
                self.screen.fill(BLACK)
                self.win = False
                self.main = True
                self.main_menu()
            
            if quitButton3.clicked(self.mouse_pos, self.mouse_pressed):
                self.screen.fill(BLACK)
                self.clicked_sound.play()
                pygame.time.delay(500) #Delays the program
                self.win = False
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
            
            #Draws images. blit is a function in the pygame module that draws images to the screen
            self.screen.blit(self.winner, (0,0)) #Draws the main menu screen at the position of 0,0
            self.screen.blit(returnButton3.image, returnButton3.rect) #Draws the control button image and hitbox
            self.screen.blit(quitButton3.image, quitButton3.rect) #Draws the quit button and hitbox
            self.clock.tick(FPS)
            pygame.display.update() #When the menu screen stops, then the in-game screen appears      

    #main_menu method - Displays the main menu screen and draws the buttons to be clicked
    def main_menu(self):
        self.main = True #main is a variable set to true
        self.control = False #control variable is set to false
        self.gameover = False
        playGameButton = Button('Start Game', 480, 239, 361, 89, WHITE, LIGHT_GREEN, 49) #The playGameButton variable is set to the Button class, where the parameters are in use
        controlsButton = Button('Controls', 480, 360, 361, 89, WHITE, YELLOW, 50) #The controlsButton variable is set to the Button class, where the parameters are in use
        quitButton = Button('Quit', 480, 482, 361, 89, WHITE, RED, 50) #The quitButton variable is set to the Button class, where the parameters are in use
    
        while self.main: #While main is set to True, it will keep on looping
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main = False
                    self.running = False

            #Gets the mouse and from the sprties.py, it gets the mouse position and pressed
            self.mouse_pos = pygame.mouse.get_pos() #Gets the mouse position
            self.mouse_pressed = pygame.mouse.get_pressed() #Checks if the mouse has been pressed

            if playGameButton.clicked(self.mouse_pos, self.mouse_pressed): #Checks whether the mouse position is on the play game button and is the mouse clicks on the play game button
                self.clicked_sound.play()
                playGameButton = Button('Start Game', 480, 239, 361, 89, WHITE, GREY, 49) #Changes the button to grey once clicked
                self.enemy_growl_sound.play()
                self.gameover = False
                self.main = False #main set to false tells us the main menu should close

            if controlsButton.clicked(self.mouse_pos, self.mouse_pressed): #Checks whether the mouse position is on the controls button and is the mouse clicks on the controls button
                self.clicked_sound.play()
                controlsButton = Button('Controls', 480, 360, 361, 89, WHITE, GREY, 50) #Changes the button to grey once clicked
                self.gameover = False
                self.main = False
                self.control = True
          
            if quitButton.clicked(self.mouse_pos, self.mouse_pressed):
                self.screen.fill(BLACK)
                self.clicked_sound.play()
                quitButton = Button('Quit', 480, 482, 361, 89, WHITE, GREY, 50) #Changes the button to grey once clicked
                pygame.time.delay(500) #Delays the program
                self.playing = False
                self.running = False
                self.gameover = False
                self.main = False

            #Draws images. blit is a function in the pygame module that draws images to the screen
            self.screen.blit(self.mainMenu, (0,0)) #Draws the main menu screen at the position of 0,0
            self.screen.blit(playGameButton.image, playGameButton.rect) #Draws the play button image and hitbox
            self.screen.blit(controlsButton.image, controlsButton.rect) #Draws the control button image and hitbox
            self.screen.blit(quitButton.image, quitButton.rect) #Draws the quit button and hitbox
            self.clock.tick(FPS)
            pygame.display.update() #When the menu screen stops, then the in-game screen appears
    
    #game_over method - Displays the game over screen
    def game_over(self):
        self.gameover = True
        returnButton2 = Button('Return to main menu', 73, 430, 479, 124, WHITE, LIME, 50) #Displays a pause button
        quitButton2 = Button('QUIT', 700, 430, 480, 124, WHITE, LIME, 50) #Displays a pause button      
           
        while self.gameover: #This only occurs when gameover is set to true
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            #Similar to main_menu function
            self.mouse_pos = pygame.mouse.get_pos() #Gets the mouse position
            self.mouse_pressed = pygame.mouse.get_pressed() #Checks if the mouse has been pressed
        
            if returnButton2.clicked(self.mouse_pos, self.mouse_pressed):
                self.clicked_sound.play()
                returnButton2 = Button('Return to main menu', 73, 430, 479, 124, WHITE, LIGHT_GREEN, 50) #Changes the colour of the button when pressed
                self.gameover = False
                self.main = True
                self.main_menu()

            if quitButton2.clicked(self.mouse_pos, self.mouse_pressed):
                self.clicked_sound.play()
                quitButton2 = Button('QUIT', 700, 430, 480, 124, WHITE, LIGHT_GREEN, 50)
                pygame.time.delay(500) #Delays the program
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
        
            self.screen.blit(self.gameOver, (0,0))
            self.screen.blit(returnButton2.image, returnButton2.rect)
            self.screen.blit(quitButton2.image, quitButton2.rect)

            self.clock.tick(FPS)
            pygame.display.update()

#Converting class into object code
game = Game() #Creates the Game object
game.main_menu()
game.new_game()
while game.running:
    game.loop()

pygame.display.update()

#Stops the game from running
pygame.quit() #Quit the game
sys.exit() #Exits the system