from Missile import *
import Globals
import pygame
import copy


def hit(invader):
    Globals.invaders_list.remove(invader)
    Globals.cannon.laser = None
    Globals.score += invader.score
    Globals.sounds_libary['invaderkilled'].play()
    print("%s is dead by laser" % invader)


class Laser(Missile):
    hight, width = 8, 3
    y_speed = 10
    direction = "up"
    color = Globals.neon

    def __init__(self, x, y):
        super().__init__(x, y)

    def __init__(self, cannon):
        super().__init__(cannon.x + cannon.width/2, cannon.y)

    def draw(self):
        pygame.draw.rect(Globals.screen, self.color, [self.x, self.y, self.width, self.hight])


    def is_hit_invaders(self):
        for invader in copy.copy(Globals.invaders_list):
            if self.is_hit(invader):
                print("%s is hit by laser %s" % (invader, self))
                return invader


    def is_hit(self, map_object):
        if self.hit_box.colliderect(map_object.hit_box):
            return True


