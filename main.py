import pygame
from pygame.locals import *
import random



# My friend challenged me to make this in one evening.
# This is a very simple version of a guitar hero clone.
# No music or anything, just a minimal implementation.

class presscube:
    def __init__(self, sizex, sizey, x, y, button):
        self.rect = pygame.Rect(x, y, sizex, sizey)
        self.rect.centerx = x
        self.rect.centery = y
        self.button = button
        self.color = (0, 50, 50, 120)
        self.colors = [(0, 50, 50, 120), (50,0, 100, 120)]
        self.counter = 0
        

    def press(self, notes, event):
        points = 0
        if event.key == self.button:
            if event.type == pygame.KEYDOWN:
                print("DOWN")
                self.color = self.colors[1]
                collided = False
                for n in notes:
                    if presscube.rect.colliderect(n.rect):
                        notes.remove(n)
                        points = 50
                        collided = True
                if not collided:
                    points = -25
            if event.type == pygame.KEYUP:
                self.color = self.colors[0]
        return points

    def update(self, notes, event): 
        return self.press(notes, event)

class note:
    def __init__(self, sizex, sizey, x, y, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sizex, sizey)
        self.rect.centerx = x
        self.rect.centery = y
        self.color = (255, 0, 0)
        self.active = True


    def update(self): 
        self.fall()
        if (self.rect.centery > height + self.rect.height):
            self.active = False

    def fall(self):
        self.rect.centery -= self.speed


def createNotes(x_positions, height, l):
    note_speed = -1
    chance1 = random.randint(0, 100)
    chance2 = random.randint(0, 100)
    chance3 = random.randint(0, 100)
    chance4 = random.randint(0, 100)
    if (chance1 > 90):
        l.append(note(note_size[0], note_size[1], x_positions[0], - note_size[1], note_speed))
    if (chance2 > 90):
        l.append(note(note_size[0], note_size[1], x_positions[1], - note_size[1], note_speed))
    if (chance3 > 90):
        l.append(note(note_size[0], note_size[1], x_positions[2], - note_size[1], note_speed))
    if (chance4 > 90):
        l.append(note(note_size[0], note_size[1], x_positions[3], - note_size[1], note_speed))
    
    
    

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    score = 0
    pygame.display.set_caption('Cube Catch')
    pygame.mouse.set_visible(1)
    width = 800
    height = 1000
    clock = pygame.time.Clock()
    dt = clock.tick(60)
    screen = pygame.display.set_mode([width, height])
    pygame.display.init()
    note_size = (50, 50)
    button_size = (100, 100)
    x_positions = [width/8, width/8 + width/5, width/8+ 2* width/5, width-width/8]
    
    
    presscube0 = presscube(button_size[0], button_size[1], x_positions[0], height-button_size[1], pygame.K_a)
    presscube1 = presscube(button_size[0], button_size[1], x_positions[1], height-button_size[1], pygame.K_s)
    presscube2 = presscube(button_size[0], button_size[1], x_positions[2], height-button_size[1], pygame.K_d)
    presscube3 = presscube(button_size[0], button_size[1], x_positions[3], height-button_size[1], pygame.K_j)

    presscubes = [presscube0, presscube1, presscube2, presscube3]
    pressed = []

    notes = []
    note_counter = 0

    myfont = pygame.font.SysFont("monospace", 25)

    while True:
        
        scoreboard = myfont.render(str(score), 1, (255, 255, 255))
        

        screen.fill((0, 0, 0))

        note_counter -= 1
        if note_counter <= 0:
            note_counter = 1/random.randint(1, 5) * 120
            createNotes(x_positions, height, notes)
        
        i = 0
        while i < len(notes):
            notes[i].update()
            pygame.draw.rect(screen, notes[i].color, notes[i].rect)
            if not notes[i].active:
                score -= 25
                del notes[i]
            else:
                i+=1
            

        events = pygame.event.get() 
        for event in events:
            if event.type == pygame.QUIT:  
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print("observed")
                for presscube in presscubes:
                    score += presscube.update(notes, event)
            if event.type == pygame.KEYUP:
                for presscube in presscubes:
                    score += presscube.update(notes, event)
        
        for presscube in presscubes:
            pygame.draw.rect(screen, presscube.color, presscube.rect)

        screen.blit(scoreboard, (width/2, height/2))
            

        


            
            
        
        
        pygame.display.flip()
        
