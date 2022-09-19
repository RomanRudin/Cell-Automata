from pygame import *
from constants import *
import os
import json

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
        for i in range(len(level_data["data"])):
            wall_checking_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = object_generating(level_data["data"][i]["x"], level_data["data"][i]["y"], level_data["data"][i]["wcd"], level_data["data"][i]["dir_x"], level_data["data"][i]["dir_y"], False)
            #level_checking_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["wcd"]
            #wall_direction_x_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["dir_x"]
            #wall_direction_y_data[level_data["data"][i]["y"]][level_data["data"][i]["x"]] = level_data["data"][i]["dir_y"]
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


def Scene_saver(level_name):
    level_data.clear()
    level_data = level_file
    level_data["x"] = field_x
    level_data["y"] = field_y
    for x in range(field_x):
        for y in range(field_y):
            level_data["data"].append({"wcd":wall_checking_data[y][x].wcd, "x":x, "y":y, "dir_x":wall_direction_x_data[y][x].direction_x, "dir_y":wall_direction_y_data[y][x].direction_y})
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


def object_generating(x, y, wcd, dir_x, dir_y, is_placed, *args): #TODO Решить проблему с объектами с wcd == 0
    if wcd == 0:
        air = Air('sprites\sprite_air.png', x * cell_x + 1, y * cell_y + 1, wcd)
        return air
    elif wcd == 1:
        moving = Moving("sprites\moving.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        moving_b.add(moving)
        block_group.add(moving)
        return moving
    elif wcd == 2:
        moveable = Moveable("sprites\moveable.png", x * cell_x + 1, y * cell_y + 1, 0, 0, 1, wcd, is_placed)
        moveable_b.add(moveable)
        block_group.add(moveable)
        return moveable
    elif wcd == 3:
        generating = Generating("sprites\generating.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        generating_b.add(generating)
        block_group.add(generating)
        return generating
    elif wcd == 4:
        rotating = Rotating("sprites\sprite_rotating.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        rotating.start()
        rotating_b.add(rotating)
        block_group.add(rotating)
        return rotating
    elif wcd == 5:
        boosting = Boosting("sprites\sprite_boosting.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        boosting_b.add(boosting)
        block_group.add(boosting)
        return boosting
    elif wcd == 6:
        railed_moveable = Railed_moveable("sprites\sprite_railed_moveable.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        railed_moveable_b.add(railed_moveable)
        block_group.add(railed_moveable)
        return railed_moveable
    elif wcd == 7:
        spike = Spike("sprites\spike.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 5, wcd, is_placed)
        spike_b.add(spike)
        block_group.add(spike)
        return spike
    elif wcd == 8:
        enemy = Enemy("sprites\enemy.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, is_placed)
        enemy_b.add(enemy)
        block_group.add(enemy)
        return enemy
    elif wcd == 9:
        wall = Wall("sprites\wall.png", x * cell_x + 1, y * cell_y + 1, 0, 0, 1, wcd, False)
        wall_b.add(wall)
        block_group.add(wall)
        return wall
    elif wcd == 10:
        wall = Wall("sprites\spiked_wall.png", x * cell_x + 1, y * cell_y + 1, 0, 0, 1, 9, False)
        wall_b.add(wall)
        block_group.add(wall)
        return wall
    elif wcd == -1:
        locateable_cell = Locateable_cell("sprites\locateable_cell.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, False)
        locateable_cell_b.add(locateable_cell)
        return locateable_cell
    elif wcd == -2:
        mirror = Mirror("sprites\mirror.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, -2, False)
        mirror_b.add(mirror)
        block_group.add(mirror)
        return mirror
    elif wcd == -3:
        unexplored = Unexplored("sprites\sprite_unexplored.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, args[0], False, False)
        unexplored_b.add(unexplored)
        block_group.add(unexplored)
        return unexplored
    elif wcd == -4:
        if (args[0] <= 1) and (args[1] <= 2):
            teleporter = Teleporter("sprites\sprites_teleporters\sprite_teleporter_" + str(args[0]) + str(args[1]) + ".png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, False)
            teleporter_b.add(teleporter)
            block_group.add(teleporter)
            return teleporter
    elif wcd == -5:
        deleter = Deleter("sprites\deleter.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, False)
        deleter_b.add(deleter)
        block_group.add(deleter)
        return deleter
    elif wcd == -6:
        wormhole = Wormhole("sprites\wormhole.png", x * cell_x + 1, y * cell_y + 1, dir_x, dir_y, 1, wcd, False)
        wormhole_b.add(wormhole)
        block_group.add(wormhole)
        return wormhole

def animating_moving():
    if not subticking:
        counter = 0
        for i in range(animation_ticks):
            for block in animation_group:
                block.animating(animation_direction[counter])
                counter += 1
        for i in range(len(animation_pushed_block)):
            if animation_pushed_block[i] != None:
                animation_pushed_block[i].update(animation_direction[i], animation_group)

    else:
        for i in range(animation_ticks):
            animation_group.animating()
            drawing()
            display.update()
            time.wait(animation_stop_ticks)

def animating_generating():
    for i in range(animation_ticks):
        animation_group.animating()
        drawing()
        window.blit(fake_image, (self.rect.x + self.direction_x * cell_x, self.rect.y + self.direction_y * cell_y))
        display.update()
        time.wait(animation_stop_ticks)

def drawing():
    global window
    window.blit(background, (0, 0))
    block_group.draw(window)

def start_drawing():
    global window
    window.blit(background, (0, 0))
    locateable_cell_b.draw(window)
    block_group.draw(window)

def wcd_update_all():
    for blick in block_group:
        wall_checking_data[block.cor_y][block.cor_x] = block
    for x in field_x:
        for y in field_y:
            if not wall_checking_data[y][x].rect.collidepoint((x + 1) * cell_x - cell_x // 2, (y + 1) * cell_y - cell_y // 2):
                wall_checking_data[y][x] = object_generating(x, y, 0, 0, 0, False)
