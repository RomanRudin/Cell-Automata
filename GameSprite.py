from pygame import *
from constants import *

class GameSprite(sprite.Sprite):
    def __init__ (self, block_image, block_x, block_y, direction_x, direction_y, health, wcd, is_placed, *args):
        super().__init__()
        self.health = health
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.wcd = wcd
        self.is_placed = is_placed
        #self.image_main = transform.scale(image.load(block_image), (cell_x - 2, cell_y - 2))
        self.image = transform.scale(image.load(block_image), (cell_x - 2, cell_y - 2))
        if len(args) > 0:
            self.found = args[0]
        self.rotated(0, False)
        self.block_image = image.load(block_image)
        self.rect = self.image.get_rect()
        self.rect[0] += block_x
        self.rect[1] += block_y
    
    #method blits objects 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    #I dpn't really know now if I'll need this method, that came from previous version of the game
    # def moved(self, direction):#! Dunno if it will be used
    #     if abs(direction) == 1:
    #         self.rect.x += cell_x * direction
    #     if abs(direction) == 2:
    #         self.rect.y += cell_y * (direction / 2)
    #     colliding(self, direction,)
    #sraer method updates wcd
    def start(self):
        wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x] = self
    #methods transforms images for rotated blocks
    def rotated(self, direct, is_rotating):
        if self.wcd > 0 and self.wcd != 4:
            if is_rotating:
                if self.direction_x == 1:
                    self.direction_x = 0
                    self.direction_y = direct * (-1)
                elif self.direction_x == -1:
                    self.direction_x = 0
                    self.direction_y = direct
                elif self.direction_y == 1:
                    self.direction_y = 0
                    self.direction_x = direct
                elif self.direction_y == -1:
                    self.direction_y = 0
                    self.direction_x = direct * (-1)
            if self.direction_x == 1:
                self.image = self.image_main
            elif self.direction_x == -1:
                self.image = transform.rotate(self.image_main, 180)
            elif self.direction_y == 1:
                self.image = transform.rotate(self.image_main, -90)
            elif self.direction_y == -1:
                self.image = transform.rotate(self.image_main, 90)

        elif self.wcd == 4:
            if is_rotating:
                self.direction_x *= -1
            if self.direction_x == 1:
                self.direction_x = -1
                self.image = transform.flip(self.image_main, True, False)
            elif self.direction_x == -1:
                self.direction_x = 1
                self.image = self.image_main
        
        elif self.wcd == -2:
            if is_rotating:
                if self.direction_x == -1:
                    if self.direction_y == -1:
                        if direct == 1:
                            self.direction_y = 1
                        else:
                            self.direction_x = 1
                    else:
                        if direct == 1:
                            self.direction_x = 1
                        else:
                            self.direction_y = -1
                else:
                    if self.direction_y == -1:
                        if direct == 1:
                            self.direction_x = -1
                        else:
                            self.direction_y = 1
                    else:
                        if direct == 1:
                            self.direction_y = -1
                        else:
                            self.direction_x = -1
            if (self.direction_x == 1) and (self.direction_y == 1):
                self.image = self.image_main
            elif (self.direction_x == 1) and (self.direction_y == -1):
                self.image = transform.rotate(self.image_main, 90)
            elif (self.direction_x == -1) and (self.direction_y == -1):
                self.image = transform.rotate(self.image_main, 180)
            elif (self.direction_x == -1) and (self.direction_y == 1):
                self.image = transform.rotate(self.image_main, -90)
    #method will be asked in animating part of drawing for the whole animation_group group
    def animating(self, direction):
        self.rect.x += cell_x // animation_ticks * direction[0]
        self.rect.y += cell_y // animation_ticks * direction[1]
    #method checks, if updated blocks (such as generators, movers and boosters) can be updated
    def wcd_checking(self, self_adding, s):
        while True:
            pushed_block = wall_checking_data[self.rect.y // cell_y + s * self.direction_y][self.rect.x // cell_x + s * self.direction_x]
            pushed = pushed_block.wcd
            if (pushed == 0) or (pushed >= 8) or (pushed == -1) or (pushed <= -4):
                break
            elif pushed == 6:
                if (self.direction_x != abs(pushed_block.direction_x)) and (self.direction_y != abs(pushed_block.direction_y)):
                    break
            elif pushed == -2:
                if (self.direction_x == pushed_block.direction_x * -1) or (self.direction_y == pushed_block.direction_y * -1):
                    break
            elif pushed == 7:
                if ((self.direction_x == pushed_block.direction_x) and (self.direction_x != 0)) or ((self.direction_y == pushed_block.direction_y) and (self.direction_y != 0)):
                    wall_check = wall_checking_data[self.rect.y // cell_y + self.direction_y * (s + 1)][self.rect.x // cell_x + self.direction_x * (s + 1)]
                    if wall_check.wcd == 9:
                        wall_check.kill()
                        pushed_block.kill()
                        object_generating(self.rect.x // cell_x + self.direction_x * (s + 1), self.rect.y // cell_y + self.direction_y * (s + 1), 10, 0, 0, False)
                        s -= 1
                    #s += 1 #! Dunno if it will be used
                    break
                else:
                    break
            s += 1
        animation_group.empty()
        for i in range(s - 1 + self_adding):
            animation_group.add(wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x])
            animation_direction.append((self.direction_x, self.direction_y))
            animation_pushed_block.append(None)
        animation_pushed_block[-1] = pushed
        if s > 1 - self_adding:
            prepushed_block = wall_checking_data[self.rect.y // cell_y + (s - 1) * self.direction_y][self.rect.x // cell_x + (s - 1) * self.direction_x]
            if prepushed_block.wcd == -2 or prepushed_block.wcd == 7:
                animation_special_update.add(prepushed_block)
        else:
            prepushed_block = None
        return pushed, pushed_block, prepushed_block


class StableGameSprite(sprite.Sprite):
    def __init__(self, available_image, x, y):
        super().__init__()
        self.image = transform.scale(image.load(available_image), (cell_x - 2, cell_y - 2))
        self.block_image = image.load(available_image)
        self.rect = self.image.get_rect()
        self.rect[0] += x
        self.rect[1] += y


class NedoButton(sprite.Sprite):
    def __init__(self, available_image, x, y, index):
        super().__init__()
        self.image = transform.scale(image.load(available_image), (cell_x - 2, cell_y - 2))
        self.block_image = image.load(available_image)
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
        self.block_image = image.load(cell_image)
        self.rect = self.image.get_rect()
        self.rect[0] += x
        self.rect[1] += y
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Air(sprite.Sprite):
    def __init__(self, block_image, block_x, block_y):
        super().__init__()
        self.image = transform.scale(image.load(block_image), (cell_x - 2, cell_y - 2))
        self.rect = self.image.get_rect()
        self.rect[0] += block_x
        self.rect[1] += block_y
        self.wcd = 0
