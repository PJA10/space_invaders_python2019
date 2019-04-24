from Missile import *


class TShoot(Missile):
    hight, width = 15,11
    y_speed = 5
    direction = "down"
    img = pygame.image.load('space-invaders-icons/Tshoot.png')
    img = pygame.transform.scale(img, (width, hight))

    def __init__(self, invader):
        super().__init__(invader.x + invader.width/2, invader.y + invader.hight)


    def is_hit(self):
        if self.hit_box.colliderect(Globals.cannon.hit_box):
            return True
