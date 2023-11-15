import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *
import pers_values as pv

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_ammo(surf, x, y, pct):
    # Draws ammo bar
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, ORANGE, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.map_index = 0
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map_list = ['level1.tmx','level2.tmx','level3.tmx','level4.tmx']
        self.map = TiledMap(path.join(map_folder, self.map_list[self.map_index]))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        for img in BULLET_IMGS:
            self.bullet_images[img] = pg.image.load(path.join(img_folder, img)).convert_alpha()

        self.mob_images = {}
        for img in MOB_IMGS:
            self.mob_images[img] = pg.image.load(path.join(img_folder, img)).convert_alpha()
            #check the mob spawn and set them to their correct sizes
            if img == 'tank.png':
                self.mob_images[img] = pg.transform.scale(self.mob_images[img], (52, 52))
                self.mob_images[img] = pg.transform.rotate(self.mob_images[img], 90)
            if img == 'spectre.png':
                self.mob_images[img] = pg.transform.scale(self.mob_images[img], (40, 40))
                self.mob_images[img] = pg.transform.rotate(self.mob_images[img], 90)
            if img == 'kobold.png':
                self.mob_images[img] = pg.transform.scale(self.mob_images[img], (34, 34))
                self.mob_images[img] = pg.transform.rotate(self.mob_images[img], 90)
            if img == 'zombie.png':
                self.mob_images[img] = pg.transform.scale(self.mob_images[img], (48, 48))

        self.weapon_images = {}
        for img in WEAPON_IMGS:
            self.weapon_images[img] = pg.image.load(path.join(img_folder, img)).convert_alpha()
            self.weapon_images[img] = pg.transform.scale(self.weapon_images[img], (100, 42))
            #pg.transform.scale(self.mob_images[img], (100, 42))

        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        pg.mixer.music.set_volume(.2)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.player_death_sounds = []
        for snd in PLAYER_DEATH_SOUNDS:
            self.player_death_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def next_map(self):
        #increase map index, save health and held weapon to set after map changes, change map and change health and weapon
        self.map_index = (self.map_index + 1) % len(self.map_list)
        pv.temp_health = self.player.health
        pv.temp_weapon = self.player.heldWeapon
        self.load_data()
        while True:
            g.new()
            self.player.health = pv.temp_health
            self.shopping = True
            self.player.heldWeapon = pv.temp_weapon
            WEAPONLIST.remove(self.player.pistol)
            g.run()

    def next_wave(self):
        #save player health for map change, increment currentwave to make the game harder, set difficulty based off currentwave, and then spawn the mobs
        self.temp_health = self.player.health
        pv.currentwave +=1
        pv.difficulty = pv.currentwave*4
        self.spawn_mobs()
        if pv.currentwave%(WAVES_PER_LEVEL+1)>=WAVES_PER_LEVEL:
            self.next_map()
            self.player.health = self.temp_health


    def spawn_mobs(self):
        #find what mobs can be used because of wave and difficulty, and then spawn them at the spawners.
        #mobs lower difficulty counter when __init__ calls, so that the player won't get swarmed by 20 tanks the first time they see them
        for tile_object in self.map.tmxdata.objects:
            self.valid_mobs_list = []
            if pv.difficulty>36 and pv.currentwave >= 14:
                self.valid_mobs_list.append('Tank')
            if pv.difficulty>24 and pv.currentwave >= 9:
                self.valid_mobs_list.append('Spectre')
            if pv.difficulty>8 and pv.currentwave >= 4 and pv.currentwave <= 30:
                self.valid_mobs_list.append('Kobold')
            if pv.difficulty>0 and pv.currentwave <= 20:
                self.valid_mobs_list.append('Mob')
            if tile_object.name == 'spawner':
                if self.valid_mobs_list:
                    self.next_mob = choice(self.valid_mobs_list)
                    if self.next_mob == 'Tank':
                        Tank(self, tile_object.x, tile_object.y)
                    elif self.next_mob == 'Spectre':
                        Spectre(self, tile_object.x, tile_object.y)
                    elif self.next_mob == 'Kobold':
                        Kobold(self, tile_object.x, tile_object.y)
                    elif self.next_mob == 'Mob':
                        Mob(self, tile_object.x, tile_object.y)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun', 'huntingRifle', 'flamethrower']:
                Item(self, obj_center, tile_object.name)
        self.spawn_mobs()
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.shopping = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused and not self.shopping:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # player hits items, no items to hit but the code remains in case of further use
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                #Had a pv.reset_values function, but it didn't work. Had to manually reset the values when the play died
                choice(self.player_death_sounds).play()
                pv.temp_health = PLAYER_HEALTH
                pv.currentwave = 0
                pv.difficulty = 0
                pv.points = 0
                self.show_go_screen()
                self.map_index = 0
                self.load_data()
                while True:
                    g.new()
                    g.run()
        if self.mobs.has(self.mobs)==False:
            self.next_wave()
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONLIST[self.player.heldWeapon].damage * len(hits[hit])
            hit.vel = vec(0, 0)

    def heldWeaponUpdate(self):
        #Ammo Sprite
        weapon_img = 'obj_' + WEAPONLIST[self.player.heldWeapon].ident + '.png'
        #blit(wield_img, self.screen, (0, 60))
        self.screen.blit(self.weapon_images[weapon_img], (0, 55))

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, (Mob, Tank, Kobold, Spectre)):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_ammo(self.screen, 10, 35, WEAPONLIST[self.player.heldWeapon].ammunition / WEAPONLIST[self.player.heldWeapon].magazine_size)
        self.heldWeaponUpdate()
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        #works like pausing the game, but just tells the player how to buy the guns and health.
        if self.shopping:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("A zombie merchant approaches.", self.title_font, 32, RED, WIDTH / 2, HEIGHT / 9, align="center")
            self.draw_text("He stares past you and speaks.", self.title_font, 32, RED, WIDTH / 2, 2*HEIGHT / 9, align="center")
            self.draw_text("Press 1 to buy a shotgun for 20 points.", self.title_font, 32, RED, WIDTH / 2, 3*HEIGHT / 9, align="center")
            self.draw_text("Press 2 to buy a hunting rifle for 25 points.", self.title_font, 32, RED, WIDTH / 2, 4*HEIGHT / 9, align="center")
            self.draw_text("Press 3 to buy a full auto rifle for 40 points.", self.title_font, 32, RED, WIDTH / 2, 5*HEIGHT / 9, align="center")
            self.draw_text("Press 4 to buy a flamethrower for 200 points.", self.title_font, 32, RED, WIDTH / 2, 6*HEIGHT / 9, align="center")
            self.draw_text("Press f to buy a health pack for 10 points.", self.title_font, 32, RED, WIDTH / 2, 7*HEIGHT / 9, align="center")
            self.draw_text("You have "+str(pv.points)+" points. Press X not to buy anything.", self.title_font, 32, RED, WIDTH / 2, 8*HEIGHT / 9, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_z:
                    self.shopping = not self.paused
                if event.key == pg.K_n:
                    self.next_wave()
                if event.key == pg.K_m:
                    self.next_map()
                if event.key == pg.K_k:
                    for mob in self.mobs:
                        mob.health = 0
            if event.type == pg.KEYUP:
                if event.key == pg.K_q:
                    self.player.heldWeapon = (self.player.heldWeapon - 1) % len(WEAPONLIST)
                if event.key == pg.K_e:
                    self.player.heldWeapon = (self.player.heldWeapon + 1) % len(WEAPONLIST)
                if event.key == pg.K_r:
                    self.player.reload()
                #Gun shopping, my favorite pastime. Checks if the player is shopping and what key they're pressing.
                #if the don't have the points, emptyClip plays. if they do, they get the gun and they lose some points
                if self.shopping and event.key == pg.K_1:
                    if pv.points > 20:
                        WEAPONLIST.append(self.player.shotgun)
                        self.effects_sounds['gun_pickup'].play()
                        pv.points -= 20
                        self.shopping = False
                    else:
                        self.effects_sounds['emptyClip'].play()
                if self.shopping and event.key == pg.K_2:
                    if pv.points > 25:
                        WEAPONLIST.append(self.player.huntingRifle)
                        self.effects_sounds['gun_pickup'].play()
                        pv.points -= 25
                        self.shopping = False
                    else:
                        self.effects_sounds['emptyClip'].play()
                if self.shopping and event.key == pg.K_3:
                    if pv.points > 40:
                        WEAPONLIST.append(self.player.autoRifle)
                        self.effects_sounds['gun_pickup'].play()
                        pv.points -= 40
                        self.shopping = False
                    else:
                        self.effects_sounds['emptyClip'].play()
                if self.shopping and event.key == pg.K_4:
                    if pv.points > 200:
                        WEAPONLIST.append(self.player.flamethrower)
                        self.effects_sounds['gun_pickup'].play()
                        pv.points -= 200
                        self.shopping = False
                    else:
                        self.effects_sounds['emptyClip'].play()
                if self.shopping and event.key == pg.K_f:
                    if pv.points > 10:
                        self.player.add_health(HEALTH_PACK_AMOUNT)
                        self.effects_sounds['health_up'].play()
                        pv.points -= 10
                        self.shopping = False
                    else:
                        self.effects_sounds['emptyClip'].play()
                if self.shopping and event.key == pg.K_x:
                    self.shopping = False

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        #Lore, my favorite thing. Thank you HP Lovecraft for those first two lines, very thematic
        self.draw_text("That is not dead which can eternal lie.", self.title_font, 24, RED, WIDTH / 2, HEIGHT / 9, align="center")
        self.draw_text("And with strange aeons even death may die.", self.title_font, 24, RED, WIDTH / 2, 2*HEIGHT / 9, align="center")
        self.draw_text("These words have been proven true.", self.title_font, 24, RED, WIDTH / 2, 3*HEIGHT / 9, align="center")
        self.draw_text("Science has uncovered an ancient crypt filled with death.", self.title_font, 24, RED, WIDTH / 2, 4*HEIGHT / 9, align="center")
        self.draw_text("The Scientists knew not what they worked on and disaster struck.", self.title_font, 24, RED, WIDTH / 2, 5*HEIGHT / 9, align="center")
        self.draw_text("Welcome to the Endless Knight.", self.title_font, 24, RED, WIDTH / 2, 6*HEIGHT / 9, align="center")
        self.draw_text("WASD to move. Q and E to change weapons once you get them. R to reload.", self.title_font, 24, RED, WIDTH / 2, 7*HEIGHT / 9, align="center")
        #SECRET KEYS: Z for shop, M for next map, N for next wave, K to kill everything
        self.draw_text("Survive.", self.title_font, 24, RED, WIDTH / 2, 8*HEIGHT / 9, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Over", self.title_font, 32, RED, WIDTH / 2, HEIGHT / 3, align="center")
        self.draw_text("Press a key to play again", self.title_font, 32, RED, WIDTH / 2, 2*HEIGHT / 3, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
