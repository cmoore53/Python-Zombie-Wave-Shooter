import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
ORANGE = (255, 127, 39)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Endless Knight"
BGCOLOR = BROWN
#edit: Added setting to change waves per level
WAVES_PER_LEVEL = 5

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 260
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Weapon settings
BULLET_IMGS = ['bullet.png', 'rifleBullet.png', 'flame.png']

WEAPONLIST = []

WEAPON_IMGS = ['obj_flamethrower.png', 'obj_pistol.png', 'obj_shotgun.png', 'obj_huntingRifle.png','obj_autoRifle.png']

# Mob settings
#Mob images from rileygombart at https://craftpix.net/product/tds-monster-character-sprites/
MOB_IMGS = ['zombie.png', 'tank.png', 'kobold.png', 'spectre.png']
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 50
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 999999

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'splat green.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png',
               'huntingRifle' : 'obj_huntingRifle.png',
               'flamethrower' : 'obj_flamethrower.png',
               'autoRifle' : 'obj_autoRifle.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
#music from https://www.fesliyanstudios.com/royalty-free-music/downloads-c/dark-music/12
BG_MUSIC = 'battle_theme.wav'
# from https://www.fesliyanstudios.com/royalty-free-sound-effects-download/grunting-188
PLAYER_HIT_SOUNDS = ['player_hit1.wav','player_hit2.wav','player_hit3.wav','player_hit4.wav','player_hit5.wav']

PLAYER_DEATH_SOUNDS = ['wilhelm.wav']
# from https://www.fesliyanstudios.com/royalty-free-sound-effects-download/zombie-174
ZOMBIE_MOAN_SOUNDS = ['zombie_noise1.wav','zombie_noise2.wav','zombie_noise3.wav','zombie_noise4.wav','zombie_noise5.wav']
# from https://www.fesliyanstudios.com/royalty-free-sound-effects-download/blood-squirting-77
ZOMBIE_HIT_SOUNDS = ['blood_squirt1.wav','blood_squirt2.wav','blood_squirt3.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'huntingRifle' : ['huntingRifle.wav'],
                 'flamethrower' : ['flamethrower.wav'],
                 'autoRifle' : ['autoRifle.wav']}
EFFECTS_SOUNDS = {'health_up' : 'health_pack.wav',
                  'gun_pickup' : 'gun_pickup.wav',
                  'emptyClip' : 'emptyClip.wav'}
