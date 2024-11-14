# module imports ###########################################################################################################################################################################################################################################


from pickle import HIGHEST_PROTOCOL

import random
import math

import pygame
from pygame.locals import *

# Fix for screen_size

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()


# window settings ###########################################################################################################################################################################################################################################


screen_size = [int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)]

flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((screen_size), flags)

pygame.display.set_caption("Real Game")

### preloading background as base for display ratio

background=pygame.image.load('alpha_background.png').convert() 
background_width = background.get_width()
background_height = background.get_height()

win = pygame.Surface((background_width,background_height))


# loading assets ####################################################################################################################################################################################################################################################


player_Character = pygame.image.load('alpha_spaceship.png').convert_alpha()
bullet = pygame.image.load('alpha_bullet.png').convert_alpha()
alien = pygame.image.load('Enemy_Saucer.png').convert_alpha()
alien_s = pygame.image.load('Enemy_Saucer_s.png').convert_alpha()
score_display = pygame.image.load('score_display.png').convert_alpha()

one = pygame.image.load('One.png').convert_alpha()
two = pygame.image.load('Two.png').convert_alpha()
three = pygame.image.load('Three.png').convert_alpha()
four = pygame.image.load('Four.png').convert_alpha()
five = pygame.image.load('Five.png').convert_alpha()
six = pygame.image.load('Six.png').convert_alpha()
seven = pygame.image.load('Seven.png').convert_alpha()
eight = pygame.image.load('Eight.png').convert_alpha()
nine = pygame.image.load('Nine.png').convert_alpha()
zero = pygame.image.load('Zero.png').convert_alpha()

# classes/objects and methods #######################################################################################################################################################################################################################################


### object class

class object():
    
    def __init__(self, x, y, pic):

        self.x = x
        self.y = y
        self.pic = pic
        self.height = self.pic.get_height()
        self.width = self.pic.get_width()
    
    def display (self, l):  # prints image out on the display
        

        win.blit(self.pic,( self.x, self.y))    

    def collide(self,list): # return if object is colliding with any object from given list
        
        for o in list:

            if ((o.x + o.width > self.x) and (o.x < self.x + self.width)) and ((o.y + o.height > self.y) and (o.y < self.y + self.height)):
                return True
    
    def get_center(self):   # return x and y-coordinate of player as tuple
                
        center_x = self.x - self.width/2
        center_y = self.y - self.height/2
        
        return (center_x,center_y)

score_gui = object(8, 8, score_display)

### actor class

class actor(object):

    def __init__(self, x, y, pic, vel):
        super().__init__(x, y, pic)
        
        self.vel = vel

### player class                    

class player(actor):
    
    def __init__(self, x , y, pic, vel, hp):
        super().__init__(x, y, pic, vel)

        self.hp = hp
    
p1 = player(screen_size[0]/2, screen_size[1]/2, player_Character, 16, 6)

### background class 

class bg(object):
    
    def __init__(self, x, y, pic):
        super().__init__(x, y, pic)
     
bg1=bg(0,0, background)

### projectile class

class projectile(actor):

    def __init__(self,x,y, pic, vel, angle):
        super().__init__(x, y, pic, vel)
        
        self.angle = angle
        self.speed_x = self.vel * math.cos(self.angle)
        self.speed_y = self.vel * math.sin(self.angle)
    
bulletlist = []

### enemy class
  
class enemy(actor):

    def __init__(self,x,y, pic, vel, hp):
        super().__init__(x, y, pic, vel)

        self.hp = hp

enemylist = []

### stops actor from moving out of bounds

def keep_in_borders(entity,background):

    if entity.x < 0:
        entity.x += -(entity.x)

    if entity.x > background.width:
        entity.x -= entity.x - background.width

    if entity.y < 0:
        entity.y += -(entity.y)

    if entity.y > background.height:
        entity.y -= entity.y - background.height

### returns True if entity touched edges of background

def touched_borders(entity,background):

    if entity.x < 0:
        return True

    elif entity.x > background.width:
        return True

    elif entity.y < 0:
        return True

    elif entity.y > background.height:
        return True
    
    else:
        return False

### display rotated towards something

def display_rotated(entity, orientation):

    vec_x, vec_y = entity.x - orientation[0], entity.y - orientation[1]

    angle = math.degrees(math.atan2(-vec_y, vec_x)) - 270

    rot_entity = pygame.transform.rotate(entity.pic, angle)
    rect = rot_entity.get_rect(center=(entity.x,entity.y))
    win.blit(rot_entity,rect)


# random variables ##########################################################################################################################################################################################################################################

### stores cooldown for firing weapon

cooldown = 0    

# pygame.event.set_allowed([QUIT, KEYESCAPE, KEYLEFT, KEYRIGHT, KEYSPACE]) #Dont know how to properly use this yet :(

### stores offset to revert the scaling of the display

offset_x = screen_size[0] / background_width  
offset_y = screen_size[1] / background_height  

### player stats

invincibility = 0

### score

score = 0

# Start_of_Game_Loop #########################################################################################################################################################################################################################################


run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False

# set random variables #########################################################################################################################################################################################################################################


### get mouse postion and correct for scaling offset

    mx, my = pygame.mouse.get_pos()
    mx = mx / offset_x
    my = my / offset_y

### enemy stats

    ehp = 1

### player stats

    if invincibility > 0:
        invincibility -= 1

# enemy_spawning #########################################################################################################################################################################################################################################


    if random.randint(0,8) == 1:
        
        spawn_direction = random.randint(1,4)
        
        if spawn_direction == 1:
            enemylist.append(enemy(random.randint(0, background_width), 0, alien, 10, ehp))
        elif spawn_direction == 2:
            enemylist.append(enemy(0, random.randint(0, background_height), alien, 10, ehp))
        elif spawn_direction == 3:
            enemylist.append(enemy(background_width, random.randint(0, background_height), alien, 10, ehp))
        elif spawn_direction == 4:
            enemylist.append(enemy(random.randint(0, background_width), background_height, alien, 10, ehp))

    


# collision ####################################################################################################################################################################################################################################################


### checks collision of enemy with player projectiles
    
    if not bulletlist == []:
    
        for e in enemylist:
        
            if e.collide(bulletlist):

                e.hp -= 1
                if e.hp <= 0:

                    enemylist.pop(enemylist.index(e))
                    score += 1

### enemy collision with eachother

    for e in enemylist:
        
        temp_el = enemylist[:]
        temp_el.pop(temp_el.index(e))

        for oe in temp_el:
            
            if e.collide([oe]):
                
                e_vec_x = oe.x - e.x 
                e_vec_y = oe.y -e.y
            
                e_angle = math.atan2(e_vec_y, e_vec_x) 
                e.x += -(e.vel * math.cos(e_angle))
                e.y += -(e.vel * math.sin(e_angle))

### enemy collision with player

            if p1.collide([oe]):
                
                p_vec_x = oe.x - p1.x 
                p_vec_y = oe.y -p1.y
            
                p_angle = math.atan2(p_vec_y, p_vec_x) 
                p1.x += -(p1.vel * math.cos(p_angle))
                p1.y += -(p1.vel * math.sin(p_angle))

                if not invincibility > 0:
                    p1.hp -= 1
                    invincibility += 3

                if p1.hp <= 0:
                       p1.vel = 0 


# display ####################################################################################################################################################################################################################################################

      
### displays background

    bg1.display(bg1)
        
### displays player projectiles    
    
    for b in bulletlist:
    
        b.display(b)
        
        b.y += b.speed_y
        b.x += b.speed_x
        
        if touched_borders(b, bg1): # removes out of bounds projectiles
           
           bulletlist.pop(bulletlist.index(b))

### displays player   

    display_rotated(p1, [mx, my])

### displays enemys   

    for e in enemylist:      
        
        display_rotated(e, [p1.x, p1.y])

        vec_x = p1.x - e.x 
        vec_y = p1.y -e.y
        angle = math.atan2(vec_y, vec_x)
    
        speed_x = e.vel * math.cos(angle)
        speed_y = e.vel * math.sin(angle)

        e.x += speed_x
        e.y += speed_y

### display gui

    score_gui.display(score_gui)
    
    counter = 16
    
    for i in str(score):
        
        if i == "0":
            win.blit(zero, (counter+score_gui.width, 8)) 

        elif i == "1":
            win.blit(one, (counter+score_gui.width, 8)) 

        elif i == "2":
            win.blit(two, (counter+score_gui.width, 8)) 

        elif i == "3":
            win.blit(three, (counter+score_gui.width, 8)) 

        elif i == "4":
            win.blit(four, (counter+score_gui.width, 8)) 

        elif i == "5":
            win.blit(five, (counter+score_gui.width, 8)) 

        elif i == "6":
            win.blit(six, (counter+score_gui.width, 8)) 

        elif i == "7":
            win.blit(seven, (counter+score_gui.width, 8)) 

        elif i == "8":
            win.blit(eight, (counter+score_gui.width, 8)) 

        elif i == "9":
            win.blit(nine, (counter+score_gui.width, 8)) 

        counter += 16


# Scale display to screen_size ###################################################################################################################################################################################################################################################    


    scaled_win = pygame.transform.smoothscale(win,screen_size)
   
    screen.blit(scaled_win,(0,0))
    
    pygame.display.update()


# Controls ####################################################################################################################################################################################################################################################


### stores inputs from mouse and keyboard
    
    keys=pygame.key.get_pressed()
    mouse_input = pygame.mouse.get_pressed()
    
### player movement controls

    if not keys == []:

        if keys[pygame.K_ESCAPE]: 
            run = False    
    
        if keys[pygame.K_a]: 
            p1.x -= p1.vel
   
        if keys[pygame.K_d]:
            p1.x += p1.vel

        if keys[pygame.K_w]:
            p1.y -= p1.vel

        if keys[pygame.K_s]:
            p1.y += p1.vel

### player shooting controls     
    
    if not mouse_input == []:  
        
        if cooldown == 0 and mouse_input[0]:

            vec_x = mx - p1.x
            vec_y = my - p1.y
    
            angle = math.atan2(vec_y, vec_x)

            bulletlist.append(projectile(p1.x,p1.y, bullet,48,angle))
            cooldown += 4
    
        if not cooldown == 0:
            cooldown -=1
    
### keeps player from going out of bounds 
     
    keep_in_borders(p1, bg1)


# End of Game Loop ############################################################################################################################################################################################################################################   


### set frame rate

    pygame.time.delay(20) 

pygame.quit