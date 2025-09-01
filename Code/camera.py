#Libraries
import pygame
vec = pygame.math.Vector2

#This is the camera class
class Camera:
    #The __init__ method: contains the self parameter - initialises the attributes 
    def __init__(self):
        self.zoom_scale = 1 #Tells the level of zoom

    #zoom_ket method - checks if the zoom in/out keys were pressed 
    def zoom_key(self):
        input = pygame.key.get_pressed() #Checks the inputs
        
        if input[pygame.K_i]: #Checks if the i key was pressed
            self.zoom_scale += 0.1 #Zooms the screen by 0.1
        if input[pygame.K_o]: #Checks if the o keys was pressed
            self.zoom_scale += 0.1 #Zooms outs the screen by 0.1

'''
#The second camera class
class Camera2:
    #The __init__ method: Contains the self and player parameters - initialises the attributes
    def __init__(self, player):
        self.player = player #Sets the player
        self.offset = vec(0, 0) #Sets the offset to vector coordinates 0,0
        self.offset_float = vec(0, 0) #Sets the offset float to vector coordates 0,0
        self.NEW_WIDTH, self.NEW_HEIGHT = 480, 270 #Sets the new window size
        self.contsant = vec(-self.NEW_WIDTH / 2 + player.rect.w / 2, 0) #Changes the constant ot the vector new width

    #set_method method: Contains the parameters self and methods - sets the method
    def set_method(self, method):
        self.method = method

class CamScroll():
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player

class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.contsant.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.contsant.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.contsant.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.contsant.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)
'''