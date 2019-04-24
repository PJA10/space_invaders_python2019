from MapObject import *
import pygame

class Missile(MapObject):
    hight, width = 0, 0
    y_speed = 0
    direction = None

    def __init__(self, x, y, img=None):
        super().__init__(x,y)


    def advance(self):
        if self.direction == "up":
            return self.move_up()
        elif self.direction == "down":
            return self.move_down()
