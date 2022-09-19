from pygame import *
from constants import *
from GameSprite import *
from functions import *

class Unobtainable(GameSprite):
    pass
class Player(GameSprite):
    pass
class Locateable_cell(GameSprite):
    pass


class Wormhole(Unobtainable):
    pass
class Deleter(Unobtainable):
    pass
class Teleporter(Unobtainable):
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
    def update(self, direction, group):
        collided = sprite.collideany(self, group)
        if collided:
            collided.kill()


class Moving(GameSprite):
    def update(self):
        x = self.rect.x + cell_x * self.direction_x
        y = self.rect.y + cell_y * self.direction_y
        global direction, animation_group
        if (x <= win_width - cell_x) and (x >= cell_x) and (y <= win_height - cell_y * (1 + 3)) and (y >= cell_y):
            pushed, pushed_block, prepushed_block = self.wcd_checking(1, 1)
            if (pushed != 9) and (pushed != 6 and not prepushed_block.wcd == -2):
                if pushed == 0:
                    pushed_block.kill()
                if subticking:
                    animating_moving()
                    direction = self.direction_x, self.direction_y
                    pushed_block.update(direction)
                wcd_update_all()
                    #wall_checking_data[self.rect.y // cell_y][self.rect.x // cell_x] = 1


                    
class Generating(Player):
    def update(self): 
        x = self.rect.x + cell_x * self.direction_x
        y = self.rect.y + cell_y * self.direction_y
        global direction, animation_group
        if (x <= win_width - cell_x * self.direction_x * 2) and (x >= cell_x * self.direction_x * 2) and (y <= win_height - cell_y * self.direction_y * (1 + 3)) and (y >= cell_y * self.direction_y * 2):
            copied = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x].wcd
            if ((copied > 0) and (copied < 7)) or (copied <= -5):
                pushed, pushed_block, prepushed_block = self.wcd_checking(0, 1)
                if (pushed != 9) and (pushed != 6):
                    copied_block = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x]
                    if pushed == 0:
                        pushed_block.kill()
                    dir_x, dir_y = copied_block.direction_x, copied_block.direction_y
                    generated = object_generating(self.rect.x // cell_x + self.direction_x, self.rect.y // cell_y + self.direction_y, copied, dir_x, dir_y, False)
                    if subticking:
                        animating_generating()
                        direction = self.direction_x, self.direction_y
                        pushed_block.update(direction)
                    wcd_update_all()



class Rotating(Player):
    def update(self): 
        x = self.rect.x // cell_x
        y = self.rect.y // cell_y
        if (wall_checking_data[y][x + 1].wcd != 0) and (wall_checking_data[y][x + 1].wcd != 9):
            wall_checking_data[y][x + 1].rotated()
        if (wall_checking_data[y + 1][x].wcd != 0) and (wall_checking_data[y + 1][x].wcd != 9):
            wall_checking_data[y + 1][x].rotated()
        if (wall_checking_data[y][x - 1].wcd != 0) and (wall_checking_data[y][x - 1].wcd != 9):
            wall_checking_data[y][x - 1].rotated()
        if (wall_checking_data[y - 1][x].wcd != 0) and (wall_checking_data[y - 1][x].wcd != 9):
            wall_checking_data[y - 1][x].rotated()


#!TODO
class Boosting(Player):
    def update(self):
        x = self.rect.x
        y = self.rect.y
        if (x <= win_width - self.direction_x * cell_x * 2) and (x >= self.direction_x * cell_x * 2) and (y <= win_height - self.direction_y * cell_y * (2 + 3)) and (y >= self.direction_y * cell_y * 2):
            boosted = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x]
            pushed = wall_checking_data[self.rect.y // cell_y + self.direction_y * 2][self.rect.x // cell_x + self.direction_x * 2]
            s = 2
            if ((boosted > 0) and (boosted < 7)) or (boosted == -5):
                pushed, pushed_object, prepushed_block
                if (pushed != 9) and (pushed != 6):
                    wcd = wall_checking_data[self.rect.y // cell_y + self.direction_y][self.rect.x // cell_x + self.direction_x]
                    wcd_boosted = wall_checking_data[self.rect.y // cell_y - self.direction_y][self.rect.x // cell_x - self.direction_x]
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