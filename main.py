from pygame import *
import pygame_menu as pm
from random import *
from math import *
from time import time as timer
import os
import json

init()

available_blocks = 7

subticking = 0

animation_ticks = 10
animation_stop_ticks = 1
animation_direction = []
subticking_title = ""
animation_ticks_title = ""
animation_stop_ticks_title = ""
#waiting_parameter = 0

cell_x = 50
cell_y = 50

direction = 0
generated = 0
numeric_crutch = 0

field_x = 5
field_y = 3
wall_checking_data = []
level_checking_data = []
wall_direction_x_data = []
wall_direction_y_data = []

level_data = {}
level = 1

available = []

level_file = {
    "x":0,
    "y":0,
    "data":[
    ]
}

font.init()
font1 = font.SysFont('Arial', 24)
font2 = font.SysFont('Arial', 48)


def developers_asking():
    print("You've launched developer's game version. Current mode: level editing")
    return int(input("Please enter an index of the level to be edited:"))


def printMatrix ( matrix ): 
   for i in range ( len(matrix) ): 
      for j in range ( len(matrix[i]) ): 
          print ( "{:4d}".format(matrix[i][j]), end = "" ) 
      print ()


#TODO Анимации можно сделать с помощью time.wait(милисекунды). Тогда после каждого изменения положения блоков можно покадрово отрисовывать их с помощью drawing(), после чего делать time.wait(). Тогда лучше объединять обновляемые блоки в группы для лучшей картинки


def Scene_loader(level_name):
    global field_x, field_y
    global wall_checking_data, level_checking_data
    global wall_direction_x_data, wall_direction_y_data
    global available
    try:
        with open(level_name, 'r', encoding='utf-8') as file:
            level_data = json.load(file)
        field_x = level_data["x"]
        field_y = level_data["y"]
        wall_checking_data.clear()
        wall_checking_data = [[0] * field_x for i in range(field_y)]
        level_checking_data.clear()
        level_checking_data = [[0] * field_x for i in range(field_y)]
        wall_direction_x_data.clear()
        wall_direction_x_data = [[0] * field_x for i in range(field_y)]
        wall_direction_y_data.clear()
        wall_direction_y_data = [[0] * field_x for i in range(field_y)]
        for i in range(len(level_data["data"])):
            wall_checking_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["wcd"]
            level_checking_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["wcd"]
            wall_direction_x_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["dir_x"]
            wall_direction_y_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["dir_y"]
        available = level_data["available"]
        if len(available) < available_blocks:
            for i in range(available_blocks - len(available)):
                available.append(0)
    except FileNotFoundError:
        print('')
        print('FileNotFoundError: There is no such file as', level_name)
        a = input('Press Enter to create it.')
        field_x, field_y = map(int, input('Enter the length and width of the field to be created (two integer values separated by a space).').split())
        wall_checking_data = [[0] * field_x for i in range(field_y)]
        level_checking_data = [[0] * field_x for i in range(field_y)]
        wall_direction_x_data = [[0] * field_x for i in range(field_y)] 
        wall_direction_y_data = [[0] * field_x for i in range(field_y)]
        available = [0, 0, 0, 0, 0, 0, 0]
    except KeyError:
        print('')
        print('KeyError: the', level_name, 'file containing the level has not been generated correctly or is corrupted.')
        a = input('Press enter to close the programme.')


def available_update():
    global available
    global marker_x, marker_y
    global available_moving, available_moveable, available_generating, available_rotating, available_boosting, available_rail, available_spike
    try:
        available_b.remove(moving_marker, moveable_marker, generating_marker, rotating_marker, boosting_marker)
    except UnboundLocalError:
        pass
    if available[0] >= 1:
        moving_marker = StableGameSprite("sprites\moving.png", marker_x, marker_y)
        available_moving = True
    else:
        available_moving = False
        moving_marker = StableGameSprite("sprites\wall.png", marker_x, marker_y)
    available_b.add(moving_marker)
    if available[1] >= 1:
        moveable_marker = StableGameSprite("sprites\moveable.png", marker_x + cell_x, marker_y)
        available_moveable = True
    else:
        available_moveable = False
        moveable_marker = StableGameSprite("sprites\wall.png", marker_x + cell_x, marker_y)
    available_b.add(moveable_marker)
    if available[2] >= 1:
        generating_marker = StableGameSprite("sprites\generating.png", marker_x + 2 *cell_x, marker_y)
        available_generating = True
    else:
        available_generating = False
        generating_marker = StableGameSprite("sprites\wall.png", marker_x + 2 *cell_x, marker_y)
    available_b.add(generating_marker)
    if available[3] >= 1:
        rotating_marker = StableGameSprite("sprites\sprite_rotating.png", marker_x + 3 * cell_x, marker_y)
        available_rotating = True
    else:
        available_rotating = False
        rotating_marker = StableGameSprite("sprites\wall.png", marker_x + 3 * cell_x, marker_y)
    available_b.add(rotating_marker)
    if available[4] >= 1:
        boosting_marker = StableGameSprite("sprites\sprite_boosting.png", marker_x + 4 * cell_x, marker_y)
        available_boosting = True
    else:
        available_boosting = False
        boosting_marker = StableGameSprite("sprites\wall.png", marker_x + 4 * cell_x, marker_y)
    available_b.add(boosting_marker)
    if available[5] >= 1:
        rail_marker = StableGameSprite("sprites\sprite_railed_moveable.png", marker_x + 5 * cell_x, marker_y)
        available_rail = True
    else:
        available_rail = False
        rail_marker = StableGameSprite("sprites\wall.png", marker_x + 5 * cell_x, marker_y)
    available_b.add(rail_marker)
    if available[6] >= 1:
        spike_marker = StableGameSprite("sprites\spike.png", marker_x + 6 * cell_x, marker_y)
        available_spike = True
    else:
        available_spike = False
        spike_marker = StableGameSprite("sprites\wall.png", marker_x + 6 * cell_x, marker_y)
    available_b.add(spike_marker)


def colliding(i, direction):
    global development_mode, finish
    if sprite.spritecollide(i, moving_b, False):
        for j in moving_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    j.kill()
                else:
                    j.moved(direction)
    if sprite.spritecollide(i, moveable_b, False):
        for j in moveable_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    j.kill()
                else:
                    j.moved(direction)
    if sprite.spritecollide(i, generating_b, False):
        for j in generating_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    j.kill()
                else:
                    j.moved(direction)
    if sprite.spritecollide(i, rotating_b, False):
        for j in rotating_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    j.kill()
                else:
                    j.moved(direction)
    if sprite.spritecollide(i, boosting_b, False):
        for j in boosting_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    j.kill()
                else:
                    j.moved(direction)
    if sprite.spritecollide(i, railed_moveable_b, False):
        for j in railed_moveable_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    j.kill()
                #if direction == abs(j.direction_x):
                #    j.moved(direction)
                #elif direction == abs(j.direction_y) * 2:
                #    j.moved(direction)
    if sprite.spritecollide(i, spike_b, False):
        for j in spike_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if direction == j.direction_x:
                    #j.moved(direction)
                    pass
                elif direction == j.direction_y * 2:
                    #j.moved(direction)
                    pass
                else:
                    i.kill()
                    wall_checking_data[j.rect.y // cell_y][j.rect.x // cell_x] = 6
                    j.health -= 1
                    if j.health <= 0:
                        j.kill()
                        wall_checking_data[j.rect.y // cell_y][j.rect.x // cell_x] = 0
    if sprite.spritecollide(i, enemy_b, True):
        if i.wcd != 7:
            i.health -= 1
            if i.health <= 0:
                wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                i.kill()
        else:
            i.health -= 1
            if i.health <= 0:
                i.kill()
                wall_checking_data[j.rect.y // cell_y][j.rect.x // cell_x] = 0
            wall_checking_data[j.rect.y // cell_y][j.rect.x // cell_x] = 0
        if len(enemy_b.sprites()) == 0:
            development_mode = False
            finish = True
    if sprite.spritecollide(i, mirror_b, False):
        for j in mirror_b.sprites():
            if (sprite.collide_rect(i, j)) and (i != j):
                if i.wcd == 7:
                    wall_checking_data[i.rect.y // cell_y][i.rect.x // cell_x] = 0
                    i.kill()
                if (direction == j.direction_x * -1):
                    i.rect.y = j.rect.y + j.direction_y * cell_y
                    i.direction_x = 0
                    i.direction_y = j.direction_y * 1
                    i.rotated()
                    wall_checking_data[j.rect.y // cell_y][j.rect.x // cell_x] = -2
                    colliding(i, j.direction_y * 2)
                elif (direction == j.direction_y * -2):
                    i.rect.x = j.rect.x + j.direction_x * cell_x
                    i.direction_y = 0
                    i.direction_x = j.direction_x * 1
                    i.rotated()
                    wall_checking_data[j.rect.y // cell_y][j.rect.x // cell_x] = -2
                    colliding(i, j.direction_x * 1)
                else:
                    #j.moved(direction)
                    pass


def object_generating(x, y, wcd, dir_x, dir_y, is_placed, *args):
    if wcd == 1:
        moving = Moving("sprites\moving.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        moving.start()
        moving_b.add(moving)
    elif wcd == 2:
        moveable = Moveable("sprites\moveable.png", x * cell_x + 1, y * cell_y + 1, 0, 0, 1, wcd, is_placed)
        moveable.start()
        moveable_b.add(moveable)
    elif wcd == 3:
        generating = Generating("sprites\generating.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        generating.start()
        generating_b.add(generating)
    elif wcd == 4:
        rotating = Rotating("sprites\sprite_rotating.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        rotating.start()
        rotating_b.add(rotating)
    elif wcd == 5:
        boosting = Boosting("sprites\sprite_boosting.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        boosting.start()
        boosting_b.add(boosting)
    elif wcd == 6:
        railed_moveable = Railed_moveable("sprites\sprite_railed_moveable.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        railed_moveable.start()
        railed_moveable_b.add(railed_moveable)
    elif wcd == 7:
        spike = Spike("sprites\spike.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 5, wcd, is_placed)
        spike.start()
        spike_b.add(spike)
    elif wcd == 8:
        enemy = Enemy("sprites\enemy.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        enemy.start()
        enemy_b.add(enemy)
    elif wcd == 9:
        wall = Wall("sprites\wall.png", x * cell_x + 1, y * cell_y + 1, 0, 0, 1, wcd, False)
        wall.start()
        wall_b.add(wall)
    elif wcd == 10:
        wall = Wall("sprites\spiked_wall.png", x * cell_x + 1, y * cell_y + 1, 0, 0, 1, 9, False)
        wall.start()
        wall_b.add(wall)
    elif wcd == -1:
        locateable_cell = Locateable_cell("sprites\locateable_cell.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, False)
        locateable_cell.start()
        locateable_cell_b.add(locateable_cell)
    elif wcd == -2:
        mirror = Mirror("sprites\mirror.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, -2, False)
        mirror.start()
        mirror_b.add(mirror)
    elif wcd == -3:
        unexplored = Unexplored("sprites\sprite_unexplored.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, args[0], False, False)
        unexplored.start()
        unexplored_b.add(unexplored)


def object_seeking(x, y, wcd, action, *args): 
    if wcd == 1:
        for i in moving_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":                          #rotating *args: direction_x from rotating block (1 or -1)
                    if i.direction_x == 1:
                        i.direction_x = 0
                        i.direction_y = args[0] * (-1)
                    elif i.direction_x == -1:
                        i.direction_x = 0
                        i.direction_y = args[0]
                    elif i.direction_y == 1:
                        i.direction_y = 0
                        i.direction_x = args[0]
                    elif i.direction_y == -1:
                        i.direction_y = 0
                        i.direction_x = args[0] * (-1)
                    i.rotated()
                    break
                elif action == "boosting":                          #rotating *args: direction_x, direction_y from boosting block (1 or -1)
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 2:
        for i in moveable_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "boosting":
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 9:
        for i in wall_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "seeking":
                    return i

    elif wcd == 3:
        for i in generating_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":
                    if i.direction_x == 1:
                        i.direction_x = 0
                        i.direction_y = args[0] * (-1)
                    elif i.direction_x == -1:
                        i.direction_x = 0
                        i.direction_y = args[0]
                    elif i.direction_y == 1:
                        i.direction_y = 0
                        i.direction_x = args[0]
                    elif i.direction_y == -1:
                        i.direction_y = 0
                        i.direction_x = args[0] * (-1)
                    i.rotated()
                    break
                elif action == "boosting":
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 4:
        for i in rotating_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":
                    i.rotated()
                    break
                elif action == "boosting":
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 5:
        for i in boosting_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":
                    if i.direction_x == 1:
                        i.direction_x = 0
                        i.direction_y = args[0] * (-1)
                    elif i.direction_x == -1:
                        i.direction_x = 0
                        i.direction_y = args[0]
                    elif i.direction_y == 1:
                        i.direction_y = 0
                        i.direction_x = args[0]
                    elif i.direction_y == -1:
                        i.direction_y = 0
                        i.direction_x = args[0] * (-1)
                    i.rotated()
                    break
                elif action == "boosting":
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 8:
        for i in enemy_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "boosting":
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i
    elif wcd == -1:
        for i in locateable_cell_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "seeking":
                    return i
    elif wcd == -2:
        for i in mirror_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":
                    pass
                    if i.direction_x == -1:
                        if i.direction_y == -1:
                            if args[0] == 1:
                                i.direction_y = 1
                            else:
                                i.direction_x = 1
                        else:
                            if args[0] == 1:
                                i.direction_x = 1
                            else:
                                i.direction_y = -1
                    else:
                        if i.direction_y == -1:
                            if args[0] == 1:
                                i.direction_x = -1
                            else:
                                i.direction_y = 1
                        else:
                            if args[0] == 1:
                                i.direction_y = -1
                            else:
                                i.direction_x = -1
                    i.rotated()
                    break
                elif action == "boosting":
                    wall_checking_data[y][x] = 0
                    i.rect.x += cell_x * 3 * args[0]
                    i.rect.y += cell_y * 3 * args[1]
                    i.start()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 7:
        for i in spike_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":
                    if i.direction_x == 1:
                        i.direction_x = 0
                        i.direction_y = args[0] * (-1)
                    elif i.direction_x == -1:
                        i.direction_x = 0
                        i.direction_y = args[0]
                    elif i.direction_y == 1:
                        i.direction_y = 0
                        i.direction_x = args[0]
                    elif i.direction_y == -1:
                        i.direction_y = 0
                        i.direction_x = args[0] * (-1)
                    i.rotated()
                    break
                elif action == "seeking":
                    return i

    elif wcd == 6:
        for i in railed_moveable_b:
            if (i.rect.x // cell_x == x) and (i.rect.y // cell_y == y):
                if action == "generating":
                    return (i.direction_x), (i.direction_y)
                elif action == "rotating":
                    if i.direction_x == 1:
                        i.direction_x = 0
                        i.direction_y = args[0] * (-1)
                    elif i.direction_x == -1:
                        i.direction_x = 0
                        i.direction_y = args[0]
                    elif i.direction_y == 1:
                        i.direction_y = 0
                        i.direction_x = args[0]
                    elif i.direction_y == -1:
                        i.direction_y = 0
                        i.direction_x = args[0] * (-1)
                    i.rotated()
                    break
                elif action == "seeking":
                    return i



def block_information(x, y):
    i = -2
    while i <= 9:
        j = object_seeking(x, y, i, "seeking", 0)
        if i != -1:
            try:
                print("wcd:", j.wcd)
                print("x:", j.rect.x // cell_x)
                print("y:", j.rect.y // cell_y)
                print("dir_x:", j.direction_x)
                print("dir_y:", j.direction_y)
                print("is_placed:", j.is_placed)
                break
            except AttributeError:
                pass
        i += 1



def drawing():
    global marker_x, marker_y
    window.blit(background, (0, 0))
    cells.draw(window)
    available_b.draw(window)
    moving_b.draw(window)
    moveable_b.draw(window)
    generating_b.draw(window)
    rotating_b.draw(window)
    boosting_b.draw(window)
    railed_moveable_b.draw(window)
    spike_b.draw(window)
    enemy_b.draw(window)
    mirror_b.draw(window)
    unexplored_b.draw(window)
    wall_b.draw(window)
    for i in range(len(available)):
        available_count = font1.render(str(available[i]), 1, (0, 0, 0))
        window.blit(available_count, (marker_x + cell_x * i + cell_x // 3, marker_y + cell_y))
    level_count = font1.render(str(level), 1, (0, 0, 0))
    window.blit(level_count, (win_width // 2 - 5, marker_y - cell_y // 2))
    buttons.draw(window)


def menu_drawing():
    global marker_x, marker_y
    global game_started
    window.blit(background, (0, 0))
    cells.draw(window)
    available_b.draw(window)
    if not game_started:
        locateable_cell_b.draw(window)
    moving_b.draw(window)
    moveable_b.draw(window)
    generating_b.draw(window)
    rotating_b.draw(window)
    boosting_b.draw(window)
    railed_moveable_b.draw(window)
    spike_b.draw(window)
    enemy_b.draw(window)
    mirror_b.draw(window)
    unexplored_b.draw(window)
    wall_b.draw(window)
    for i in range(len(available)):
        available_count = font1.render(str(available[i]), 1, (0, 0, 0))
        window.blit(available_count, (marker_x + cell_x * i + cell_x // 3, marker_y + cell_y))
    level_count = font1.render(str(level), 1, (0, 0, 0))
    window.blit(level_count, (win_width // 2 - 5, marker_y - cell_y // 2))
    buttons.draw(window)


def waiter():
    pass
    #global waiting_parameter    


class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, direction_x, direction_y, health, wcd, is_placed, *args):
        super().__init__()
        self.size = [cell_x, cell_y]
        self.health = health
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.wcd = wcd
        self.is_placed = is_placed
        #if self.direction_x == 1:
        self.image_main = transform.scale(image.load(player_image), (cell_x - 2, cell_y - 2))
        self.image = transform.scale(image.load(player_image), (cell_x - 2, cell_y - 2))
        if len(args) > 0:
            self.found = args[0]
        if self.wcd != -2:
            if self.direction_x == 1:
                self.image = self.image_main
            elif self.direction_x == -1:
                self.image = transform.rotate(self.image_main, 180)
            elif self.direction_y == 1:
                self.image = transform.rotate(self.image_main, -90)
            elif self.direction_y == -1:
                self.image = transform.rotate(self.image_main, 90)
        else:
            if (self.direction_x == 1) and (self.direction_y == 1):
                self.image = self.image_main
            elif (self.direction_x == 1) and (self.direction_y == -1):
                self.image = transform.rotate(self.image_main, 90)
            elif (self.direction_x == -1) and (self.direction_y == -1):
                self.image = transform.rotate(self.image_main, 180)
            elif (self.direction_x == -1) and (self.direction_y == 1):
                self.image = transform.rotate(self.image_main, -90)
        self.player_image = image.load(player_image)
        self.rect = self.image.get_rect()
        self.rect[0] += player_x
        self.rect[1] += player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def moved(self, direction):
        if abs(direction) == 1:
            self.rect.x += cell_x * direction
        if abs(direction) == 2:
            self.rect.y += cell_y * (direction / 2)
        self.start()
        colliding(self, direction)
    def start(self):
        wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x] = self.wcd
    def rotated(self):
        if self.wcd == 4:
            if self.direction_x == 1:
                self.direction_x = -1
                self.image = transform.flip(self.image_main, True, False)
            elif self.direction_x == -1:
                self.direction_x = 1
                self.image = self.image_main
        elif self.wcd == -2:
            if (self.direction_x == 1) and (self.direction_y == 1):
                self.image = self.image_main
            elif (self.direction_x == 1) and (self.direction_y == -1):
                self.image = transform.rotate(self.image_main, 90)
            elif (self.direction_x == -1) and (self.direction_y == -1):
                self.image = transform.rotate(self.image_main, 180)
            elif (self.direction_x == -1) and (self.direction_y == 1):
                self.image = transform.rotate(self.image_main, -90)
        else:
            if self.direction_x == 1:
                self.image = self.image_main
            elif self.direction_x == -1:
                self.image = transform.rotate(self.image_main, 180)
            elif self.direction_y == 1:
                self.image = transform.rotate(self.image_main, -90)
            elif self.direction_y == -1:
                self.image = transform.rotate(self.image_main, 90)


class StableGameSprite(sprite.Sprite):
    def __init__(self, available_image, x, y):
        super().__init__()
        self.image = transform.scale(image.load(available_image), (cell_x - 2, cell_y - 2))
        self.player_image = image.load(available_image)
        self.rect = self.image.get_rect()
        self.rect[0] += x
        self.rect[1] += y


class NedoButton(sprite.Sprite):
    def __init__(self, available_image, x, y, index):
        super().__init__()
        self.image = transform.scale(image.load(available_image), (cell_x - 2, cell_y - 2))
        self.player_image = image.load(available_image)
        self.rect = self.image.get_rect()
        self.rect[0] += x
        self.rect[1] += y
        self.i = index 
    def update(self, event_list):
        for e in event_list:
            if e.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(e.pos):
                    return self.i


class Cell(sprite.Sprite):
    def __init__(self, cell_image, x, y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(cell_image), (size_x, size_y))
        self.player_image = image.load(cell_image)
        self.rect = self.image.get_rect()
        self.rect[0] += x
        self.rect[1] += y
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Unobtainable(GameSprite):
    pass
class Player(GameSprite):
    pass
class Locateable_cell(GameSprite):
    pass

class Black_hole(Unobtainable):
    pass

class Unexplored(GameSprite):
    def update():
        if not self.found:
            for i in range(3):
                for j in range(3):
                    wcd = wall_checking_data[self.rect.y // cell_y + (i - 1)][self.rect.x // cell_x + (j - 1)]
                    if (wcd > 0) and (wcd < 8):
                        exploring = object_seeking(self.rect.x // cell_x + (j - 1), self.rect.y // cell_y + (i - 1), wcd, "seeking", None)
                        if exploring.is_placed:
                            self.found = True
                            break
        if self.found:
            object_generating(self.rect.x // cell_x, self.rect.y // cell_y, self.wcd, self.direction_x, self.direction_y, False)
            self.kill()
                    

class Enemy(GameSprite):
    pass
        
class Mirror(Unobtainable):
    pass

class Spike(GameSprite):
    pass


class Wall(Unobtainable):
    def update(self):
        wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x] = 9


class Moving(GameSprite):
    def update(self):
        x = self.rect.x + cell_x * self.direction_x
        y = self.rect.y + cell_y * self.direction_y
        global direction, animation_group
        if subticking == 1:
            animation_group = []
        if (x <= win_width - cell_x) and (x >= cell_x) and (y <= win_height - cell_y * (1 + 3)) and (y >= cell_y):
            s = 1
            deleted = False
            while True:
                pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y * s][self.rect.x // cell_x + self.direction_x * s]
                if (pushed == 0) or (pushed >= 8) or (pushed == -1):
                    break
                elif pushed == 6:
                    pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 6, "seeking", 0)
                    if (self.direction_x != abs(pushed_block.direction_x)) and (self.direction_y != abs(pushed_block.direction_y)):
                        break
                    else:
                        #if self.direction_x == 1:
                        #    for i in range(field_x - self.rect.x // cell_x - 1):
                        #        if wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x + i + 1] == 9:
                        #            break
                        #elif self.direction_x == -1:
                        #    for i in range(self.rect.x // cell_x):
                        #        if wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x - i - 1]
                        #elif self.direction_y == 1:
                        #    for i in range(field_y - self.rect.y // cell_y - 1):
                        #        if wall_checking_data[self.rect.y // cell_y + i + 1][self.rect.x // cell_x]
                        #elif self.direction_y == -1:
                        #    for i in range(self.rect.y // cell_y):
                        #        if wall_checking_data[self.rect.y // cell_y - i - 1][self.rect.x // cell_x]
                        pass
                elif pushed == -2:
                    pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, -2, "seeking", 0)
                    if (self.direction_x == pushed_block.direction_x * -1) or (self.direction_y == pushed_block.direction_y * -1):
                        break
                elif pushed == 7:
                    pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 7, "seeking", 0)
                    if ((self.direction_x == pushed_block.direction_x) and (self.direction_x != 0)) or ((self.direction_y == pushed_block.direction_y) and (self.direction_y != 0)):
                        if wall_checking_data[self.rect.y // cell_y + self.direction_y * (s + 1)][self.rect.x // cell_x + self.direction_x * (s + 1)] == 9:
                            wall_check = object_seeking(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 9, "seeking", 0)
                            wall_check.kill()
                            pushed_block.kill()
                            object_generating(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 10, 0, 0, False)
                            deleted = True
                        s += 1
                        break
                    else:
                        break
                s += 1
            if (pushed != 9) and (pushed != 6):
                #waiting_parameter += 1
                if deleted:
                    s -= 1
                for i in range(s):
                        pushed_x = (self.rect.x + self.direction_x * cell_x * i) // cell_x
                        pushed_y = (self.rect.y + self.direction_y * cell_y * i) // cell_y
                        try:
                            pushed_object = object_seeking(pushed_x, pushed_y, wall_checking_data[pushed_y][pushed_x], "seeking", None)
                            print("pushed_object", pushed_object)
                            animation_group.append(pushed_object)
                            animation_direction.append([self.direction_x, self.direction_y])
                        except AttributeError:
                            pass
                wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x] = 0
                for block in animation_group:
                    wall_checking_data[block.rect.y // cell_y + self.direction_y][block.rect.x // cell_x + self.direction_x] = block.wcd
                for i in range(animation_ticks * subticking):
                    for block in animation_group:
                        try:
                            block.rect.x += cell_x // animation_ticks * self.direction_x
                            block.rect.y += cell_y // animation_ticks * self.direction_y
                        except AttributeError:
                            pass
                    #animation_group.draw(window)
                    drawing()
                    display.update()
                    time.wait(animation_stop_ticks)
                if subticking == 1:
                    if self.direction_x != 0:
                        direction = 1 * self.direction_x
                    elif self.direction_y != 0:
                        direction = 2 * self.direction_y
                    for block in animation_group:
                        colliding(block, direction)
                        if block.health > 0:
                            block.start()
                    #wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x] = 1
    def invisible_update(self):
        x = self.rect.x + cell_x * self.direction_x
        y = self.rect.y + cell_y * self.direction_y
        global direction
        if (self.direction_x != 0):
            self.rect.x = x
            direction = 1 * self.direction_x
        elif (self.direction_y != 0):
            self.rect.y = y
            direction = 2 * self.direction_y
        colliding(self, direction)



class Moveable(Player):
    def update(self):
        colliding(self, 0)

class Railed_moveable(Player): #TODO В данном случае, в связи с вызовом функции коллайда после апдейта данный блок будет удаляться со сцены при попытке толкнуть его в сторону, перпендикулярную возможной
    def update(self):
        colliding(self, 0)



class Generating(Player):
    def update(self): 
        x = self.rect.x + cell_x * self.direction_x
        y = self.rect.y + cell_y * self.direction_y
        global direction, animation_group
        if subticking == 1:
            animation_group = []
        if (x <= win_width - cell_x * self.direction_x * 2) and (x >= cell_x * self.direction_x * 2) and (y <= win_height - cell_y * self.direction_y * (1 + 3)) and (y >= cell_y * self.direction_y * 2):
            pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x]
            copied = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x]
            s = 1
            already = False
            if (copied > 0) and (copied < 7):
                while True:
                    pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y * s][self.rect.x // cell_x + self.direction_x * s]
                    if (pushed == 0) or (pushed >= 8) or (pushed == -1):
                        break
                    elif pushed == 6:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 6, "seeking", 0)
                        if (self.direction_x != abs(pushed_block.direction_x)) and (self.direction_y != abs(pushed_block.direction_y)):
                            break
                        else:
                            #if self.direction_x == 1:
                            #    for i in range(field_x - self.rect.x // cell_x - 1):
                            #        if wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x + i + 1] == 9:
                            #            break
                            #elif self.direction_x == -1:
                            #    for i in range(self.rect.x // cell_x):
                            #        if wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x - i - 1]
                            #elif self.direction_y == 1:
                            #    for i in range(field_y - self.rect.y // cell_y - 1):
                            #        if wall_checking_data[self.rect.y // cell_y + i + 1][self.rect.x // cell_x]
                            #elif self.direction_y == -1:
                            #    for i in range(self.rect.y // cell_y):
                            #        if wall_checking_data[self.rect.y // cell_y - i - 1][self.rect.x // cell_x]
                            pass
                    elif pushed == -2:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, -2, "seeking", 0)
                        if (self.direction_x == pushed_block.direction_x * -1) or (self.direction_y == pushed_block.direction_y * -1):
                            break
                    elif pushed == 7:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 7, "seeking", 0)
                        if ((self.direction_x == pushed_block.direction_x) and (self.direction_x != 0)) or ((self.direction_y == pushed_block.direction_y) and (self.direction_y != 0)):
                            if wall_checking_data[self.rect.y // cell_y + self.direction_y * (s + 1)][self.rect.x // cell_x + self.direction_x * (s + 1)] == 9:
                                wall_check = object_seeking(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 9, "seeking", 0)
                                wall_check.kill()
                                pushed_block.kill()
                                object_generating(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 10, 0, 0, False)
                            s += 1
                            break
                        else:
                            break
                    s += 1
                    #pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y * s][self.rect.x // cell_x + self.direction_x * s]
                    #if (pushed >= 8) or (pushed == 0) or (pushed == -1):
                    #    break
                    #elif pushed == 6:
                    #    pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 6, "seeking", 0)
                    #    if ((self.direction_x != abs(pushed_block.direction_x)) and (self.direction_x != 0)) and ((self.direction_y != abs(pushed_block.direction_y)) and (self.direction_y != 0)):
                    #        break
                    #elif pushed == -2:
                    #    pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, -2, "seeking", 0)
                    #    if (self.direction_x == pushed_block.direction_x * -1) or (self.direction_y == pushed_block.direction_y * -1):
                    #        invisible_piston = Moving("sprites\cell.jpg", self.rect.x, self.rect.y, self.direction_x, self.direction_y, 1, 1, False)
                    #        invisible_piston.invisible_update()
                    #        invisible_piston.kill()
                    #        dir_x, dir_y = object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, copied, "generating", 1)
                    #        object_generating(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, copied, dir_x, dir_y, False)
                    #        already = True
                    #        break
                    #elif pushed == 7:
                    #    pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 7, "seeking", 0)
                    #    if ((self.direction_x == pushed_block.direction_x) and (self.direction_x != 0)) or ((self.direction_y == pushed_block.direction_y) and (self.direction_y != 0)):
                    #        if wall_checking_data[self.rect.y // cell_y + self.direction_y * (s + 1)][self.rect.x // cell_x + self.direction_x * (s + 1)] == 9:
                    #            wall_check = object_seeking(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 9, "seeking", 0)
                    #            wall_check.kill()
                    #            pushed_block.kill()
                    #            object_generating(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 10, 0, 0, False)
                    #        break
                    #    else:
                    #        break
                    #s += 1
                if (pushed != 9) and not already and (pushed != 6):
                    fake_image = transform.scale(object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, copied, "seeking", None).image, (cell_x - 2, cell_y - 2))
                    for i in range(s - 1):
                        pushed_x = (self.rect.x + self.direction_x * cell_x * (i + 1)) // cell_x
                        pushed_y = (self.rect.y + self.direction_y * cell_y * (i + 1)) // cell_y
                        try:
                            pushed_object = object_seeking(pushed_x, pushed_y, wall_checking_data[pushed_y][pushed_x], "seeking", None)
                            animation_group.append(pushed_object)
                            animation_direction.append([self.direction_x, self.direction_y])
                        except AttributeError:
                            break
                    for block in animation_group:
                        wall_checking_data[block.rect.y // cell_y + self.direction_y][block.rect.x // cell_x + self.direction_x] = block.wcd
                    for i in range(animation_ticks * subticking):
                        for block in animation_group:
                            try:
                                block.rect.x += cell_x // animation_ticks * self.direction_x
                                block.rect.y += cell_y // animation_ticks * self.direction_y
                            except AttributeError:
                                pass
                        #animation_group.draw(window)
                        drawing()
                        window.blit(fake_image, (self.rect.x + self.direction_x * cell_x, self.rect.y + self.direction_y * cell_y))
                        display.update()
                        time.wait(animation_stop_ticks)
                    if subticking == 1:
                        if self.direction_x != 0:
                            direction = 1 * self.direction_x
                        elif self.direction_y != 0:
                            direction = 2 * self.direction_y
                        for block in animation_group:
                            colliding(block, direction)
                            if block.health > 0:
                                block.start()
                    dir_x, dir_y = object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, copied, "generating", 1)
                    object_generating(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, copied, dir_x, dir_y, False)



class Rotating(Player):
    def update(self): 
        x = self.rect.x // cell_x
        y = self.rect.y // cell_y
        if (wall_checking_data[y][x + 1] != 0) and (wall_checking_data[y][x + 1] != 9):
            object_seeking(x + 1, y, wall_checking_data[y][x + 1], "rotating", self.direction_x)
            #waiting_parameter += 1
        if (wall_checking_data[y + 1][x] != 0) and (wall_checking_data[y + 1][x] != 9):
            object_seeking(x, y + 1, wall_checking_data[y + 1][x], "rotating", self.direction_x)
            #waiting_parameter += 1
        if (wall_checking_data[y][x - 1] != 0) and (wall_checking_data[y][x - 1] != 9):
            object_seeking(x - 1, y, wall_checking_data[y][x - 1], "rotating", self.direction_x)
            #waiting_parameter += 1
        if (wall_checking_data[y - 1][x] != 0) and (wall_checking_data[y - 1][x] != 9):
            object_seeking(x, y - 1, wall_checking_data[y - 1][x], "rotating", self.direction_x)
            #waiting_parameter += 1




class Boosting(Player):
    def update(self):
        x = self.rect.x
        y = self.rect.y
        if (x <= win_width - self.direction_x * cell_x * 2) and (x >= self.direction_x * cell_x * 2) and (y <= win_height - self.direction_y * cell_y * (2 + 3)) and (y >= self.direction_y * cell_y * 2):
            boosted = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x]
            pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y * 2][self.rect.x // cell_x + self.direction_x * 2]
            s = 2
            if (boosted > 0) and (boosted < 7):
                while True:
                    pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y * s][self.rect.x // cell_x + self.direction_x * s]
                    if (pushed == 9) or (pushed <= 0) or (pushed == 8):
                        break
                    elif pushed == 6:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 6, "seeking", 0)
                        if ((self.direction_x != abs(pushed_block.direction_x)) and (self.direction_x != 0)) and ((self.direction_y != abs(pushed_block.direction_y)) and (self.direction_y != 0)):
                            break
                    elif pushed == -2:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, -2, "seeking", 0)
                        if (self.direction_x == pushed_block.direction_x * -1) or (self.direction_y == pushed_block.direction_y * -1):
                            break
                    elif pushed == 7:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x * s, self.rect.y // cell_y + self.direction_y * s, 7, "seeking", 0)
                        if ((self.direction_x == pushed_block.direction_x) and (self.direction_x != 0)) or ((self.direction_y == pushed_block.direction_y) and (self.direction_y != 0)):
                            if wall_checking_data[self.rect.y // cell_y + self.direction_y * (s + 1)][self.rect.x // cell_x + self.direction_x * (s + 1)] == 9:
                                wall_check = object_seeking(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 9, "seeking", 0)
                                wall_check.kill()
                                pushed_block.kill()
                                object_generating(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 10, 0, 0, False)
                            break
                        else:
                            break
                    s += 1
                if (pushed != 9) and (pushed != 6):
                    #waiting_parameter += 1
                    #invisible_piston = Moving("sprites\cell.jpg", self.rect.x + cell_x * self.direction_x, self.rect.y + cell_y * self.direction_y, self.direction_x, self.direction_y, 1, 1, False)
                    #invisible_piston.invisible_update()
                    #invisible_piston.kill()
                    wcd = wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x]
                    wcd_boosted = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x]
                    #for i in range(s - 1):
                    #    pushed_x = (self.rect.x + self.direction_x * cell_x * (i + 1)) // cell_x
                    #    pushed_y = (self.rect.y + self.direction_y * cell_y * (i + 1)) // cell_y
                    #    animation_group.add(object_seeking(pushed_x, pushed_y, wall_checking_data[pushed_y][pushed_x], "seeking", None))
                    #for j in range(animation_ticks):
                    #    for i in animation_group:
                    #        i.rect.x += cell_x // animation_ticks * self.direction_x
                    #        i.rect.y += cell_y // animation_ticks * self.direction_y
                    #    animation_group.draw(window)
                    #    display.update()
                    #    time.wait(5)
                    if (wcd == 0) or (wcd == -1):
                        wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                        object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "boosting", self.direction_x, self.direction_y)
                        return wcd_boosted, 0
                    elif wcd == -2:
                        mirror = object_seeking(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, -2, "seeking", 0)
                        if (self.direction_x == mirror.direction_x * -1) or (self.direction_y == mirror.direction_y * 1):
                            wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                            boosted = object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "seeking", None)
                            boosted.rect.x += cell_x * 2 * self.direction_x
                            boosted.rect.y += cell_y * 2 * self.direction_y
                            return wcd_boosted, 1
                        else:
                            object_seeking(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, wcd, "seeking", 0).kill()
                            wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x] = 0
                            wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                            object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "boosting", self.direction_x, self.direction_y)
                            return wcd_boosted, 0
                    elif wcd == 9:
                        object_seeking(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, wcd, "seeking", 0).kill()
                        wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x] = 0
                        object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "seeking", 0).kill()
                        wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                        return wcd_boosted, 0
                    elif wcd == 7:
                        pushed_block = object_seeking(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, wcd, "seeking", 0)
                        if ((self.direction_x == pushed_block.direction_x) and (self.direction_x != 0)) or ((self.direction_y == pushed_block.direction_y) and (self.direction_y != 0)):
                            wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                            object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "boosting", self.direction_x, self.direction_y)
                            return wcd_boosted, 0
                        else:
                            object_seeking(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, wcd, "seeking", 0).kill()
                            wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x] = 0
                            object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "seeking", 0).kill()
                            wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                            return wcd_boosted, 0
                    else:
                        object_seeking(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, wcd, "seeking", 0).kill()
                        wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x] = 0
                        wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x] = 0
                        object_seeking(self.rect.x // cell_x - self.direction_x, self.rect.y // cell_y - self.direction_y, wcd_boosted, "boosting", self.direction_x, self.direction_y)
                        return wcd_boosted, 0
                else: 
                    return 0, 0
            else: 
                return 0, 0
        else: 
            return 0, 0
        

win_width, win_height = 600, 400
window = display.set_mode((win_width, win_height), RESIZABLE)
display.toggle_fullscreen()
display.set_caption('game.exe')
background = transform.scale(image.load("sprites\level_background.png"), (win_width, win_height))
buttons = sprite.Group()

files = len(os.listdir(path="levels"))

clock = time.Clock() 

run = True
finish = False
finished = False
work_time = False
every_move = False
development_mode = False
game_started = False
FPS = 25

available_moving = True
available_moveable = True
available_generating = True
available_rotating = True
available_boosting = True
available_rail = True
available_spike = True


available_b = sprite.Group()
locateable_cell_b = sprite.Group()
wall_b = sprite.Group()
moving_b = sprite.Group()
moveable_b = sprite.Group()
generating_b = sprite.Group()
rotating_b = sprite.Group()
boosting_b = sprite.Group()
enemy_b = sprite.Group()
mirror_b = sprite.Group()
spike_b = sprite.Group()
railed_moveable_b = sprite.Group()
unexplored_b = sprite.Group()
buttons = sprite.Group()
cells = sprite.Group()
#animation_group = sprite.Group()

marker_x, marker_y = 0, 0
level_name = ''

def starting():
    global available_b, locateable_cell_b, wall_b, moving_b, moveable_b, generating_b, rotating_b, boosting_b, railed_moveable_b, spike_b, unexplored_b, enemy_b, mirror_b, buttons, cells
    global marker_x, marker_y
    global level_name, level
    global win_height, win_width, window, background
    global field_x, field_y
    global run, game_started
    global subticking

    #sprite.Group.empty(animation_group)
    sprite.Group.empty(available_b)
    sprite.Group.empty(locateable_cell_b)
    sprite.Group.empty(wall_b)
    sprite.Group.empty(moving_b)
    sprite.Group.empty(moveable_b)
    sprite.Group.empty(generating_b)
    sprite.Group.empty(rotating_b)
    sprite.Group.empty(boosting_b)
    sprite.Group.empty(enemy_b)
    sprite.Group.empty(mirror_b)
    sprite.Group.empty(spike_b)
    sprite.Group.empty(railed_moveable_b)
    sprite.Group.empty(unexplored_b)
    sprite.Group.empty(buttons)
    sprite.Group.empty(cells)

    level_name = 'levels\level_' + str(level) + '.json'

    Scene_loader(level_name)
    print("Searching for levels to load...")
    print('Scene generating started...')
    for x in range(field_x):
        for y in range(field_y):
            object_generating(x, y, wall_checking_data[y][x], wall_direction_x_data[y][x], wall_direction_y_data[y][x], False)
    print('Scene generating finished.')


    win_width, win_height = cell_x * field_x, cell_y * (field_y + 3)
    window = display.set_mode((win_width, win_height), RESIZABLE)
    display.toggle_fullscreen()
    display.set_caption('Cell Automata.exe')
    background = transform.scale(image.load("sprites\level_background.png"), (win_width, win_height))
    for i in range(field_x - 1):
        a = Cell("sprites\cell.jpg", cell_x * (i + 1) - 1, 0, 2, win_height - cell_y * 3)
        cells.add(a)
    for i in range(field_y - 1):
        a = Cell("sprites\cell.jpg", 0, cell_x * (i + 1) - 1, win_width, 2)
        cells.add(a)
    marker_x = (field_x * cell_x - 7 * cell_x) // 2
    marker_y = (field_y + 2) * cell_y - cell_y // 2 * 3
    available_update()

    back_button = NedoButton("buttons\level_options.png", 2, win_height - cell_y, 'back')
    buttons.add(back_button)
    restart_button = NedoButton("buttons\level_restart.png", cell_x + 4, win_height - cell_y, 'restart')
    buttons.add(restart_button)

    run = True
    game_started = False



def main_menu():
    global display
    menu = pm.Menu("Cell Automata", 400, 400, onclose=level_selection)
    menu.add.button('Play', pm.events.CLOSE)
    menu.add.button('Options', options())
    menu.add.button('Quit', exit)
    menu.mainloop(window)

def level_selection():
    global level, run
    win_width, win_height = 600, 400
    window = display.set_mode((win_width, win_height), RESIZABLE)
    display.toggle_fullscreen()
    display.set_caption('game.exe')
    background = transform.scale(image.load("buttons\menu_background.png"), (win_width, win_height))
    buttons = sprite.Group()
    x = (win_width - 7 * cell_x) / 8
    y = (win_height - ((files + 6) // 7) * cell_y) / ((files + 6) // 7 + 1)
    for i in range ((files + 6) // 7):
        if files - 7 * i >= 7:
            for j in range(7):
                button = NedoButton("buttons\level_selection_button.png", x + j * (x + cell_x), y + i * (y + cell_y), i * 7 + j + 1)
                buttons.add(button)
        else:
            for j in range(files - 7 * i):
                button = NedoButton("buttons\level_selection_button.png", x + j * (x + cell_x), y + i * (y + cell_y), i * 7 + j + 1)
                buttons.add(button)
    
    lvl_selection = True
    while lvl_selection:
        window.blit(background, (0, 0))
        clock.tick(12) 
        buttons.draw(window)
        for button in buttons:
            selected_level_name = font2.render(str(button.i), 1, (0, 0, 0))
            window.blit(selected_level_name, (button.rect.centerx - font2.size(str(button.i))[0] // 2, button.rect.centery - font2.size(str(button.i))[1] // 2))
        event_list = event.get()
        for button in buttons:
            i = button.update(event_list)
            if i != None:
                lvl_selection = False
                level = i
                run = True
                #try:
                starting()
                #except NameError:
                #    pass
                break
        for e in event_list:
            if e.type == QUIT:
                lvl_selection = False
                main_menu()
        display.update()

def settings(action):
    global subticking, subticking_title
    global animation_ticks, animation_ticks_title
    if action == "subticking_title":
        if subticking == 0:
            subticking_title = "Subticking: Off"
        else:
            subticking_title = "Subticking: On"
    elif action == "subticking":
        if subticking == 0:
            subticking = 1
        else:
            subticking = 0
        settings("subticking_title")
    elif action == "animation_ticks_title": 
        animation_ticks_title = "Animation ticks: " + str(animation_ticks)
    elif action == "animation_ticks":
        if animation_ticks == 50:
            animation_ticks = 25
        if animation_ticks == 25:
            animation_ticks = 10
        if animation_ticks == 10:
            animation_ticks = 5
        if animation_ticks == 5:
            animation_ticks = 1
        if animation_ticks == 1:
            animation_ticks = 50
        settings("animation_ticks_title")
    elif action == "animation_stop_ticks_title": 
        animation_ticks_title = "Animation sleep ticks: " + str(animation_stop_ticks)
    elif action == "animation_stop_ticks":
        if animation_ticks == 50:
            animation_ticks = 10
        if animation_ticks == 10:
            animation_ticks = 5
        if animation_ticks == 5:
            animation_ticks = 2
        if animation_ticks == 2:
            animation_ticks = 1
        if animation_ticks == 1:
            animation_ticks = 50
        settings("animation_stop_ticks_title")
    
def options():
    global subticking_title, subticking
    global animation_ticks_title, animation_ticks
    global animation_stop_ticks_title, animation_stop_ticks
    global cell_x, cell_y
    option = pm.Menu("Options", 400, 400, onclose=main_menu)
    settings("subticking_title")
    settings("animation_ticks_title")
    settings("animation_stop_ticks_title")
    #button_a = pm.widgets.Button(subticking_title, onreturn=settings("subticking"))
    #button_b = pm.widgets.Button(animation_ticks_title, onreturn=settings("animation_ticks"))
    #button_c = pm.widgets.Button(animation_stop_ticks_title, onreturn=settings("animation_stop_ticks"))
    


#window.blit(background, (0, 0))
#cells.draw(window)
display.toggle_fullscreen()

main_menu()


while run:
    #waiting_parameter = 0
    window.blit(background, (0, 0))
    cells.draw(window)
    clock.tick(FPS) 
    menu_drawing()
    if finish:
        next_button = NedoButton("buttons\level_next.png", win_width - (cell_x + 2), win_height - cell_y, 'next')
        buttons.add(next_button)
        finished = True

    if (work_time or every_move) and not finished:
        if development_mode:
            print("lcd:")
            printMatrix(level_checking_data)
            print("wcd:")
            printMatrix(wall_checking_data)
            print("FPS:", FPS)
        clock.tick(FPS)

        # boosting update and animation
        for i in boosting_b.sprites():
            wcd_boosted, mirrored = i.update()
            colliding_x = i.rect.x // cell_x + i.direction_x * 2
            colliding_y = i.rect.y // cell_y + i.direction_y * 2
            if (wall_checking_data[colliding_y][colliding_x] != 0) and (wall_checking_data[colliding_y][colliding_x] != -1) and (wall_checking_data[colliding_y][colliding_x] != 9):
                colliding(object_seeking(colliding_x, colliding_y, wall_checking_data[colliding_y][colliding_x], "seeking", None), 0)
            if i.direction_x != 0:
                direction = i.direction_x
            else:
                direction = i.direction_y * 2
            try:
                if wcd_boosted != 0:
                    if mirrored == 1:
                        colliding(object_seeking(i.rect.x // cell_x + i.direction_x, i.rect.y // cell_y + i.deriction_y, wcd_boosted, "seeking", None), direction)
                    else:
                        colliding(object_seeking(i.rect.x // cell_x + i.direction_x * 2, i.rect.y // cell_y + i.deriction_y * 2, wcd_boosted, "seeking", None), direction)
            except AttributeError:
                pass

        #generating update and animation
        animation_group = []
        animation_direction = []
        generators = len(generating_b.sprites())
        j = 1
        for i in generating_b.sprites():
            if j <= generators:
                i.update()
                colliding(i, 0)
                j += 1
            else:
                break
        if subticking == 0:
            for i in range(animation_ticks):
                s = 0
                for block in animation_group:
                    block.rect.x += cell_x // animation_ticks * animation_direction[s][0]
                    block.rect.y += cell_y // animation_ticks * animation_direction[s][1]
                    s += 1
                drawing()
                display.update()
                time.wait(animation_stop_ticks)
            s = 0
            for block in animation_group:
                if animation_direction[s][0] != 0:
                    direction = 1 * animation_direction[s][0]
                elif animation_direction[s][1] != 0:
                    direction = 2 * animation_direction[s][1]
                colliding(block, direction)
                if block.health > 0:
                    block.start()
                s += 1

        #moving update and animation
        animation_group = []
        animation_direction = []
        for i in moving_b.sprites():
            i.update()
        print("animation_group", animation_group)
        if subticking == 0:
            for i in range(animation_ticks):
                s = 0
                for block in animation_group:
                    print("animation_group", animation_group)
                    print("block", block)
                    block.rect.x += cell_x // animation_ticks * animation_direction[s][0]
                    block.rect.y += cell_y // animation_ticks * animation_direction[s][1]
                    s += 1
                drawing()
                display.update()
                time.wait(animation_stop_ticks)
            s = 0
            for block in animation_group:
                if animation_direction[s][0] != 0:
                    direction = 1 * animation_direction[s][0]
                elif animation_direction[s][1] != 0:
                    direction = 2 * animation_direction[s][1]
                colliding(block, direction)
                if block.health > 0:
                    block.start()
                s += 1

        #rotating update and animation
        for i in rotating_b.sprites():
            i.update()
        every_move = False
        drawing()

        if (work_time or every_move) and not finished:
            if development_mode:
                print("lcd:")
                printMatrix(level_checking_data)
                print("wcd:")
                printMatrix(wall_checking_data)
                print("FPS:", FPS)
            clock.tick(FPS)

    
    keys = key.get_pressed()
    if (keys[K_1]) and not work_time and not game_started and (available_moving or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 1, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 1, 1, 0, True)
                    available[0] -= 1
                    available_update()
    elif (keys[K_2]) and not work_time and not game_started and (available_moveable or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 2, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 2, 1, 0, True)
                    available[1] -= 1
                    available_update()
    elif (keys[K_3]) and not work_time and not game_started and (available_generating or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 3, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 3, 1, 0, True)
                    available[2] -= 1
                    available_update()
    elif (keys[K_4]) and not work_time and not game_started and (available_rotating or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 4, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 4, 1, 0, True)
                    available[3] -= 1
                    available_update()
    elif (keys[K_5]) and not work_time and not game_started and (available_boosting or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 5, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 5, 1, 0, True)
                    available[4] -= 1
                    available_update()
    elif (keys[K_6]) and not work_time and not game_started and (available_rail or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 6, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 6, 1, 0, True)
                    available[5] -= 1
                    available_update()
    elif (keys[K_7]) and not work_time and not game_started and (available_spike or development_mode):
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if (lcd == -1) or (development_mode):
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    if not development_mode:
                        available[wcd - 1] += 1
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                if development_mode:
                    object_generating(x // cell_x, y // cell_y, 7, 1, 0, False)
                else:
                    object_generating(x // cell_x, y // cell_y, 7, 1, 0, True)
                    available[6] -= 1
                    available_update()
    elif (keys[K_8]) and not work_time and not game_started and development_mode:
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if lcd != -1:
                if wcd == 0:
                    pass
                else:
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                object_generating(x // cell_x, y // cell_y, 8, 1, 0, False)
    elif (keys[K_9]) and not work_time and not game_started and development_mode:
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            lcd = level_checking_data[y // cell_y][x // cell_x]
            if lcd != -1:
                if wcd == 0:
                    pass
                else:
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                object_generating(x // cell_x, y // cell_y, 9, 1, 0, False)
    elif (keys[K_0]) and not work_time and not game_started and development_mode:
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            if wcd == 0:
                pass
            else:
                object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                wall_checking_data[y // cell_y][x // cell_x] = 0
            object_generating(x // cell_x, y // cell_y, -1, 1, 0, False)
    elif (keys[K_z]) and not work_time and not game_started and development_mode:
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            if wcd == 0:
                pass
            else:
                object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                wall_checking_data[y // cell_y][x // cell_x] = 0
            object_generating(x // cell_x, y // cell_y, -2, 1, 1, False)
    elif (keys[K_x]) and not work_time and not game_started and development_mode:
        x, y = mouse.get_pos()
        if y < (field_y * cell_y):
            wcd = wall_checking_data[y // cell_y][x // cell_x]
            if (wcd != 0) and (wcd != 1):
                explored = object_seeking(x // cell_x, y // cell_y, wcd, "seeking")
                object_generating(x // cell_x, y // cell_y, -3, explored.direction_x, explored.direction_x, False, wcd)
    elif ((keys[K_BACKSPACE]) or (keys[K_DELETE])) and not work_time and not game_started:
        x, y = mouse.get_pos()
        if y < (field_y * cell_x):
            if not development_mode:
                for i in range(7):
                    try:
                        if level_checking_data[y // cell_y][x // cell_x] == -1:
                            deleted = object_seeking(x // cell_x, y // cell_y, i + 1, "seeking", None)
                            if deleted.is_placed:
                                deleted.kill()
                                available[wall_checking_data[y // cell_y][x // cell_x] - 1] += 1
                                available_update()
                                wall_checking_data[y // cell_y][x // cell_x] = 0
                                break
                    except AttributeError:
                        pass
            else:
                for i in range(12):
                    try:
                        deleted = object_seeking(x // cell_x, y // cell_y, i - 2, "seeking", None)
                        deleted.kill()
                        wall_checking_data[y // cell_y][x // cell_x] = 0
                        break
                    except AttributeError:
                        pass
    
    event_list = event.get()
    for e in event_list:
        for button in buttons:
            i = button.update(event_list)
            if i == "back":
                finished = False
                finish = False
                run = False
                work_time = False
                FPS = 60
                level_selection()
            elif i == "next":
                finished = False
                finish = False
                work_time = False
                FPS = 60
                level += 1
                level_name = 'levels\level_' + str(level) + '.json'
                starting()
                break
            elif i == "restart":
                finished = False
                finish = False
                work_time = False
                FPS = 60
                starting()
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                game_started = True
                if work_time:
                    work_time = False
                else:
                    work_time = True

            elif e.key == K_DOWN:
                if FPS >= 5:
                    FPS /= 5

            elif e.key == K_UP:
                if FPS <= 25:
                    FPS *= 5

            elif e.key == K_e:
                every_move = True
                game_started = True

            elif (e.key == K_r) and not work_time and not game_started:
                x, y = mouse.get_pos()
                for i in range(7):
                    if (level_checking_data[y // cell_y][x // cell_x] == -1) or (development_mode):
                        found = object_seeking(x // cell_x, y // cell_y, i + 1, "seeking", 0)
                        try:
                            if found.is_placed or development_mode:
                                object_seeking(x // cell_x, y // cell_y, i + 1, "rotating", -1)
                                wall_direction_x_data[y // cell_y][x // cell_x] = found.direction_x
                                wall_direction_y_data[y // cell_y][x // cell_x] = found.direction_y
                        except AttributeError:
                            pass
                if development_mode:
                    for i in range(2):
                        found = object_seeking(x // cell_x, y // cell_y, -2 - i, "seeking", 0)
                        try:
                            if found.is_placed or development_mode:
                                object_seeking(x // cell_x, y // cell_y, -2 - i, "rotating", -1)
                                wall_direction_x_data[y // cell_y][x // cell_x] = found.direction_x
                                wall_direction_y_data[y // cell_y][x // cell_x] = found.direction_y
                        except AttributeError:
                            pass


            elif (e.key == K_s) and not work_time and not finish:
                level_data.clear()
                level_data = level_file
                level_data["x"] = field_x
                level_data["y"] = field_y
                for x in range(field_x):
                    for y in range(field_y):
                        #saving = object_seeking(x, y, -3, "seeking")
                        #try:
                        #    level_data["data"].append({"wcd":-3, "wcd_extra":wall_checking_data[y][x], "x":x, "y":y, "dir_x":saving.direction_x, "dir_y":saving.direction_y})
                        #except AttributeError:
                        level_data["data"].append({"wcd":wall_checking_data[y][x], "x":x, "y":y, "dir_x":wall_direction_x_data[y][x], "dir_y":wall_direction_y_data[y][x]})
                print("Please enter the number of available units of each type.")
                available[0] = int(input("Moving blocks:    "))
                available[1] = int(input("Moveable blocks:    "))
                available[2] = int(input("Generating blocks:    "))
                available[3] = int(input("Rotating blocks:    "))
                available[4] = int(input("Boosting blocks:    "))
                available[5] = int(input("Railed moveable blocks:    "))
                available[6] = int(input("Spike blocks:    "))
                level_data["available"] = available
                with open(level_name, 'w', encoding='utf-8') as file:
                    json.dump(level_data, file)
                print(level_name, "Has been saved succesfully!")

            elif (e.key == K_a) and not work_time:
                if development_mode:
                    development_mode = False
                    level_checking_data = wall_checking_data
                    print("development_mode = False")
                else:
                    development_mode = True
                    print("development_mode = True")
            elif (e.key == K_d) and not work_time:
                finished = False
                finish = False
                work_time = False
                FPS = 60
                level = files + 1
                level_name = 'levels\level_' + str(level) + '.json'
                starting()
            elif (e.key == K_i) and development_mode:
                x, y = mouse.get_pos()
                block_information(x // cell_x, y // cell_y)


    display.update()