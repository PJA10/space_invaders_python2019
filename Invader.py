from MapObject import *
import pygame
from Missile import *
from TShoot import *

class Invader(MapObject):

    width, hight = 30, 30
    img = pygame.image.load('space-invaders-icons/RegInvader.png')
    img = pygame.transform.scale(img, (width, hight))
    speed = 7
    y_speed = 30

    def __init__(self, x, y):
        super().__init__(x, y)
        Globals.invaders_list.append(self)

    def shoot(self):
        return TShoot(self)


    def __str__(self):
        return "invader %s" % super().__str__()


class MidInvader(Invader):
    width, hight = 30, 30
    img = pygame.image.load('space-invaders-icons/saucer2b.ico')
    img = pygame.transform.scale(img, (width, hight))
    score = 20


class EasyInvader(Invader):
    width, hight = 30, 30
    img = pygame.image.load('space-invaders-icons/saucer1b.ico')
    img = pygame.transform.scale(img, (width, hight))
    score = 10


class HardInvader(Invader):
    width, hight = 30, 30
    img = pygame.image.load('space-invaders-icons/saucer3b.ico')
    img = pygame.transform.scale(img, (width, hight))
    score = 30




class MysteryShip(Invader):
    width, hight = 45, 20
    img = pygame.image.load('space-invaders-icons/MysteryShip.png')
    img = pygame.transform.scale(img, (width, hight))
    score = 50
    speed = 4

    def __init__(self, x, y):
        super().__init__(x, y)
        Globals.invaders_list.remove(self)

    def move_left(self):
        super().move_left()
        if self.x + self.width < 0:
            return True

    def move_right(self):
        super().move_right()
        if self.x > Globals.display_width:
            return True