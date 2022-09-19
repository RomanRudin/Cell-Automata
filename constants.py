#from pygame import sprite as sprite
#from pygame import display as display
from pygame import *
import os

available_blocks = 7
subticking = 0
animation_ticks = 50
animation_stop_ticks = 5
animation_direction = []
animation_pushed_block = []
subticking_title = ""
animation_ticks_title = ""
animation_stop_ticks_title = ""
cell_x = 50
cell_y = 50
direction = 0
generated = 0
numeric_crutch = 0
field_x = 5
field_y = 3
wall_checking_data = []
level_checking_data = []
level_data = {}
level = 1
available = []


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

marker_x, marker_y = 0, 0
level_name = ''


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
teleporter_b = sprite.Group()
deleter_b = sprite.Group()
wormhole_b = sprite.Group()
buttons = sprite.Group()
cells = sprite.Group()

block_group = sprite.Group()

animation_group = sprite.Group()
animation_direction = []

win_width, win_height = 600, 400
window = display.set_mode((win_width, win_height), RESIZABLE)
display.toggle_fullscreen()
display.set_caption('game.exe')
background = transform.scale(image.load("sprites\level_background.png"), (win_width, win_height))
buttons = sprite.Group()

files = len(os.listdir(path="levels"))

clock = time.Clock() 