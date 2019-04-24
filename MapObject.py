import Globals
import pygame

class MapObject:

    img = None
    width, hight = 0, 0
    speed = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x, self.y, self.width, self.hight)

    def draw(self):
        Globals.screen.blit(self.img, (self.x, self.y))
        # print (self)

    def __str__(self):
        return "creature is in (%s,%s)" % (self.x, self.y)


    def move_left(self):
        self.x = self.x - self.speed
        if self.x < 0:
            return True


    def move_right(self):
        self.x = self.x + self.speed
        if self.x + self.width > Globals.display_width:
            return True


    def move_down(self):
        self.y = self.y + self.y_speed
        if self.y > Globals.display_height + self.hight:
            return True


    def move_up(self):
        self.y = self.y - self.y_speed
        if self.y < 0 - self.hight:
            return True


    def update_hit_box(self):
        if 'hit_box' in vars(self).keys():
            self.hit_box.x = self.x
            self.hit_box.y = self.y


    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key == "x" or key == "y":
            self.update_hit_box()

