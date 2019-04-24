import sys
import pygame
from Cannon import *
from Invader import *
import Globals
import random
import time
from TShoot import *
import math

def game_loop():
    print ("start game")
    pygame.init()
    pygame.mixer.init(buffer=1)
    Globals.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((Globals.display_width, Globals.display_height))
    Globals.screen = screen
    pygame.display.set_caption('SpaceInvaders')

    Globals.sounds_libary['shoot'] = pygame.mixer.Sound('sounds//shoot.wav')
    Globals.sounds_libary['invaderkilled'] = pygame.mixer.Sound('sounds//invaderkilled.wav')
    Globals.sounds_libary['explosion'] = pygame.mixer.Sound('sounds//explosion.wav')
    for sound in Globals.sounds_libary:
        Globals.sounds_libary[sound].set_volume(0.25)

    game_icon = pygame.image.load('space-invaders-icons/Icon.png')
    pygame.display.set_icon(game_icon)

    pressed_left, pressed_right, pressed_space = False, False, False

    done = False
    quit = False

    Globals.cannon = Cannon(Globals.display_width/2-(Cannon.width/2), Globals.display_height*(5/6))
    cannon = Globals.cannon
    invaders_list = Globals.invaders_list
    direction = "right"
    shoots = []
    turn_count = 0
    health_left = 2
    num_invaders_cols = 11
    for row in range(5):
        for col in range(num_invaders_cols):
            invaders_space_distance_ratio = 6/4
            x = (Globals.display_width - (invaders_space_distance_ratio * Invader.width * num_invaders_cols))/2   + invaders_space_distance_ratio * Invader.width*col
            y = (1/6)*Globals.display_height + invaders_space_distance_ratio * Invader.hight*row
            if 3 <= row <= 4:
                new_invader = EasyInvader(x, y)
            elif 1 <= row <= 2:
                new_invader = MidInvader(x, y)
            else:
                new_invader = HardInvader(x, y)
    frequency = 37
    mystery_ship = None

    while not done and not quit:
        turn_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

            elif event.type == pygame.KEYDOWN:  # check for key presses
                if event.key == pygame.K_LEFT:  # left arrow turns left
                    pressed_left = True
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    pressed_right = True
                elif event.key == pygame.K_SPACE:  # up arrow goes up
                    pressed_space = True
            elif event.type == pygame.KEYUP:  # check for key releases
                if event.key == pygame.K_LEFT:  # left arrow turns left
                    pressed_left = False
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    pressed_right = False
                elif event.key == pygame.K_SPACE:  # up arrow goes up
                    pressed_space = False

        if pressed_left:
            cannon.move_left()
        if pressed_right:
            cannon.move_right()
        if pressed_space:
            cannon.shoot()
        if turn_count % frequency == 0:
            move_row = False
            for invader in invaders_list:

                if direction == "right":
                    if invader.x + invader.speed > Globals.display_width - invader.width:
                        move_row = True
                    invader.move_right()
                elif direction == "left":
                    if invader.x < invader.speed:
                        move_row = True
                    invader.move_left()

            if move_row:
                for invader in invaders_list:
                    if invader.x == 0 or invader.x == Globals.display_width - invader.width:
                        pass
                    elif direction == "right":
                        invader.move_left()
                    elif direction == "left":
                        invader.move_right()
                    invader.move_down()

                if direction == "right":
                    direction = "left"
                elif direction == "left":
                    direction = "right"

                frequency = math.ceil(frequency *0.75)

        advance_missiles(cannon)
        if cannon.laser:
            dead_invader = cannon.laser.is_hit_invaders()
            if dead_invader:
                hit(dead_invader)
            elif mystery_ship and cannon.laser.is_hit(mystery_ship):
                Globals.score += mystery_ship.score
                cannon.laser = None
                mystery_ship = None
                Globals.sounds_libary['invaderkilled'].play()

        cols = []
        for invader in invaders_list:
            if invader.x not in cols:
                cols.append(invader.x)

        for col in cols:
            first_col_invader = max([invader for invader in invaders_list if invader.x == col], key=lambda invader: invader.y)
            if random.randint(0, 500) == 1:
                shoots.append(first_col_invader.shoot())

        sleep = False
        for shoot in shoots:
            shoot.advance()
            if shoot.is_hit():
                "cannon is heat"
                if not health_left:
                    done = True
                else:
                    health_left -= 1
                    cannon.x = Globals.display_width/2-(Cannon.width/2)
                    shoots = []
                    cannon.laser = None
                    mystery_ship = None
                    sleep = True
                    Globals.sounds_libary['explosion'].play()

        if not invaders_list:
            done = True

        for invader in invaders_list:
            if invader.y + invader.hight > cannon.y:
                done = True

        if mystery_ship:
            if mystery_ship.move_left():
                mystery_ship = None
        else:
            if random.randint(0, 800) == 1:
                mystery_ship = MysteryShip(Globals.display_width + MysteryShip.width, (1/11) * Globals.display_height)

        if not done:
            draw_game(shoots, health_left, mystery_ship)

        clock.tick(60)
        if sleep:
            sleep_start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() < sleep_start_time + 1200:
                pygame.display.flip()
                clock.tick(60)
    if quit:
        sys.exit()
    done = False
    screen.fill((0, 0, 0))
    game_over()
    text = ''
    font = pygame.font.SysFont('comicsansms',20)
    width, hight= 200, 32
    input_box = pygame.Rect(Globals.display_width/2, Globals.display_height* (4/5) - hight, width, hight)
    color = Globals.white
    while not done and not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open('leader_board.txt', 'a') as file:
                        file.write("{}: {}\n".format(text[:20], Globals.score))
                    with open('leader_board.txt', 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            print(int(line.split()[-1]))
                        lines = sorted(lines, key=lambda line: int(line.split()[-1]))
                    with open('leader_board.txt', 'w') as file:
                        file.writelines(reversed(lines))
                    text = ''
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(Globals.black)
        message_display("Name: ", Globals.display_width * (3 / 7), Globals.display_height * (77 / 100), 25)
        game_over()
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x, input_box.y))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(60)
    if quit:
        sys.exit()
    done = False

    screen.fill(Globals.black)
    message_display("score board", Globals.display_width/2 , Globals.display_height*(1/11), 45)
    with open('leader_board.txt', 'r') as file:
        for i in range(10):
            line = file.readline()
            message_display(line[:-1], Globals.display_width/2 , Globals.display_height * (2 / 11) + Globals.display_height* (1/12) * i, 35)
    pygame.display.flip()

    while not done and not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True


def draw_game(shoots, health_left, mystery_ship):
    screen = Globals.screen
    cannon = Globals.cannon
    invaders_list = Globals.invaders_list
    screen.fill((0, 0, 0))

    cannon.draw()
    for invader in invaders_list:
        invader.draw()
    if cannon.laser:
        cannon.laser.draw()
    for shoot in shoots:
        shoot.draw()
    heart_img = pygame.image.load('space-invaders-icons/pixel-heart.png')
    heart_img = pygame.transform.scale(heart_img, (40, 40))
    for i in range(health_left + 1):
        Globals.screen.blit(heart_img, (20 + i * 50, Globals.display_height / 12 - 20))
    if mystery_ship:
        mystery_ship.draw()
    message_display("score: %s" % Globals.score, 6 / 7 * Globals.display_width, Globals.display_height / 12, 30)
    pygame.display.flip()


def advance_missiles(cannon):
    if cannon.laser:
        if cannon.laser.advance():
            cannon.laser = None


def game_over():
    message_display("score: %s" % Globals.score, Globals.display_width/2, Globals.display_height*(8/12), 60)
    message_display("Game Over")


def text_objects(text, font):
    text_surface = font.render(text, True, Globals.white)
    return text_surface, text_surface.get_rect()


def message_display(text, x=Globals.display_width/2, y=Globals.display_height/2, size=100):
    large_text = pygame.font.SysFont('comicsansms',size)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (x, y)
    Globals.screen.blit(text_surf, text_rect)



if __name__ == "__main__":
    game_loop()

