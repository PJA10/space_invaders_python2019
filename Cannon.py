from MapObject import MapObject
import pygame
from Laser import *


class Cannon(MapObject):

    width, hight = 45, 35
    img = pygame.image.load("space-invaders-icons//CannonImg.png")
    img = pygame.transform.scale(img, (width, hight))
    speed = 5
    laser = None

    def __init__(self, x, y):
        super().__init__(x, y)


    def __str__(self):
        return "cannon %s" % super().__str__()


    def shoot(self):
        if not self.laser:
            Globals.sounds_libary['shoot'].play()
            self.laser = Laser(self)

    def move_right(self):
        if super().move_right():
            self.x = Globals.display_width - self.width


    def move_left(self):
        if super().move_left():
            self.x = 0

