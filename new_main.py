from GameSprite import *
from constants import *
from functions import *
from block_classes import *
from time import time as timer
import os
import json

def game_loop():
    while run:
        #waiting_parameter = 0
        window.blit(background, (0, 0))
        cells.draw(window)
        clock.tick(FPS) 
        start_drawing()
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
            boosting_b.update()

            #generating update and animation
            animation_group.empty()
            animation_direction = []
            generators = len(generating_b.sprites())
            print(generators)
            j = 1
            for i in generating_b.sprites():
                if j <= generators:
                    i.update()
                    j += 1
                    #!print("animation_group", animation_group)
                else:
                    break
                

            #moving update and animation
            animation_group = []
            animation_direction = []
            for i in moving_b.sprites():
                i.update()

            #rotating update and animation
            boosting_b.update()
            every_move = False
            drawing()

            #for block in deleter_b:
            #    block.start()


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
                if (wcd != 0) and (wcd != -1):
                    explored = object_seeking(x // cell_x, y // cell_y, wcd, "seeking")
                    object_generating(x // cell_x, y // cell_y, -3, explored.direction_x, explored.direction_x, False, wcd)
        elif (keys[K_c]) and not work_time and not game_started and development_mode:
            x, y = mouse.get_pos()
            if y < (field_y * cell_y):
                wcd = wall_checking_data[y // cell_y][x // cell_x]
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                object_generating(x // cell_x, y // cell_y, -4, 1, 1, False, len(teleporter_b) // 2 + 1, len(teleporter_b) % 2 + 1)
        elif (keys[K_v]) and not work_time and not game_started and development_mode:
            x, y = mouse.get_pos()
            if y < (field_y * cell_y):
                wcd = wall_checking_data[y // cell_y][x // cell_x]
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                object_generating(x // cell_x, y // cell_y, -5, 1, 1, False)
        elif (keys[K_b]) and not work_time and not game_started and development_mode:
            x, y = mouse.get_pos()
            if y < (field_y * cell_y):
                wcd = wall_checking_data[y // cell_y][x // cell_x]
                if (wcd == 0) or (wcd == -1):
                    pass
                else:
                    object_seeking(x // cell_x, y // cell_y, wcd, "seeking", None).kill()
                    wall_checking_data[y // cell_y][x // cell_x] = 0
                object_generating(x // cell_x, y // cell_y, -6, 1, 1, False)
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
                    for i in range(16):
                        try:
                            deleted = object_seeking(x // cell_x, y // cell_y, i - 6, "seeking", None)
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
                    Scene_saver

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

Scene_loader('level_1.json')
game_loop()