
import pygame
import sys
import random
import sqlite3

pygame.init() # инициализация окна игры
size = width, height = 700, 700
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
pygame.display.set_caption('HARDERTALE')


is_fight = False # объявление флагов
is_bosses_menu = False
is_menu = True
is_start_menu = True
is_controls_menu = False
is_credits_menu = False
is_fight_menu = False
is_stats_menu = False
up = False
down = False
left = False
right = False
fps = 60
frame_counter = 0

hp = 100 # здоровье боссов и игрока
dummy_hp = 1000
papirus_hp = 2500

attack_cooldown = None # объявление переменных для игрового процесса
num_cooldown = None
hp_cooldawn = None
k = None
wall_animation_counter = None
attack_num = None
cant_click = None
after_fight_menu_offset = None
death_offset = None
win_offset = None
walls_limit = None
attack_list = []
mouse_tap_pos = None

db = sqlite3.connect('attemps_db.db') # создание и подключение к бд
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS attemps (
    id INTEGER PRIMARY KEY,
    dummy INTEGER DEFAULT 0,
    papyrus INTEGER DEFAULT 0
)
''')
cursor.execute('''CREATE TABLE IF NOT EXISTS result (
    id INTEGER PRIMARY KEY,
    dummy_result INTEGER DEFAULT NULL,
    papyrus_result INTEGER DEFAULT NULL
)
''')
cursor.execute('INSERT INTO attemps (id, dummy, papyrus) VALUES (1, 0, 0) ON CONFLICT(id) DO NOTHING')
cursor.execute('INSERT INTO result (id, dummy_result, papyrus_result) VALUES (1, NULL, NULL) ON CONFLICT(id) DO NOTHING')
db.commit()

clock = pygame.time.Clock() #создание групп спрайтов
heart = pygame.sprite.Group()
all_wals = pygame.sprite.Group()
horizontal_barriers = pygame.sprite.Group()
vertical_barriers = pygame.sprite.Group()
boss_interface = pygame.sprite.Group()
start_interface = pygame.sprite.Group()
control_menu = pygame.sprite.Group()
credits_menu = pygame.sprite.Group()
fight_menu = pygame.sprite.Group()
fight_menu_messages = pygame.sprite.Group()

dummy_attack = pygame.sprite.Group()
vertical_attack = pygame.sprite.Group()
horizontal_attack = pygame.sprite.Group()
static_attack = pygame.sprite.Group()
dynamic_attack = pygame.sprite.Group()

right_wall = pygame.sprite.Group()
left_wall = pygame.sprite.Group()

dummy = pygame.image.load('IMAGES/Dummy.webp') # спрайты боссов
papyrus = pygame.image.load('IMAGES/lox_prosto.jpg')
coming_soon = pygame.image.load('IMAGES/coming_soon.png')

dummy = pygame.transform.scale(dummy, (140, 200))
papyrus = pygame.transform.scale(papyrus, (140, 200))
coming_soon = pygame.transform.scale(coming_soon, (512, 512))

pages = [dummy, papyrus, coming_soon]

class StartMenu(pygame.sprite.Sprite): # класс стартового меню
    def __init__(self, group, is_start_menu, is_bosses_menu, is_controls_menu, is_credits_menu, is_stats_menu):

        self.f_start_menu = is_start_menu
        self.f_bosses_menu = is_bosses_menu
        self.f_controls_menu = is_controls_menu
        self.f_credits_menu = is_credits_menu
        self.f_stats_menu = is_stats_menu

        super().__init__(group)

        self.start_image = pygame.image.load('IMAGES/start.jpg')
        self.controls_image = pygame.image.load('IMAGES/controls.jpg')
        self.credits_image = pygame.image.load('IMAGES/credits.jpg')
        self.exit_image = pygame.image.load('IMAGES/exit.jpg')
        self.hardertale_image = pygame.image.load('IMAGES/hardertale.png')
        self.stats_image = pygame.image.load('IMAGES/stats.png')

        self.hardertale = pygame.transform.scale(self.hardertale_image, (600, 80))

        self.image = self.start_image
        self.rect = self.image.get_rect()
        self.rect.center = (350, 210)

        self.controls_rect = self.controls_image.get_rect(center=(350, 310))
        self.credits_rect = self.credits_image.get_rect(center=(350, 510))
        self.exit_rect = self.exit_image.get_rect(center=(350, 610))
        self.hardertale_rect = self.hardertale.get_rect(center=(350, 80))
        self.stats_image_rect = self.stats_image.get_rect(center=(350, 410))

    def draw(self, surface): # отрисовка спрайтов
        surface.blit(self.image, self.rect)
        surface.blit(self.controls_image, self.controls_rect)
        surface.blit(self.credits_image, self.credits_rect)
        surface.blit(self.exit_image, self.exit_rect)
        surface.blit(self.hardertale, self.hardertale_rect)
        surface.blit(self.stats_image, self.stats_image_rect)

    def update(self, tap_pos): # обновление стартового меню
        if tap_pos:
            if self.rect.collidepoint(tap_pos):
                self.f_bosses_menu = True
                self.f_start_menu = False
                bosses_menu.f_bosses_menu = True

            elif self.controls_rect.collidepoint(tap_pos):
                self.f_controls_menu = True
                self.f_start_menu = False
                controls_menu.f_control_menu = True
                controls_menu.f_start_menu = False

            elif self.credits_rect.collidepoint(tap_pos):
                self.f_credits_menu = True
                self.f_start_menu = False
                credits_menu.f_credits_menu = True
                credits_menu.f_start_menu = False

            elif self.exit_rect.collidepoint(tap_pos):
                sys.exit()

            elif self.stats_image_rect.collidepoint(tap_pos):
                self.f_start_menu = False
                self.f_stats_menu = True
                stats_menu.f_start_menu = False
                stats_menu.f_stats_menu = True


class StatsMenu(): # класс меню статистики
    def __init__(self, is_start_menu, is_stats_menu):
        self.f_start_menu = is_start_menu
        self.f_stats_menu = is_stats_menu

        self.papyrus_stats = pygame.image.load('IMAGES/papyrus_stats.png')
        self.dummy_stats = pygame.image.load('IMAGES/dummy_stats.png')
        self.atts_now = pygame.image.load('IMAGES/atts_now.png')
        self.best_res = pygame.image.load('IMAGES/best_res.png')

        self.image = self.papyrus_stats
        self.rect = self.image.get_rect()
        self.rect.center = (232 + 234 + 234 / 2 + 25, 170 / 2)

        self.dummy_stats_rect = self.dummy_stats.get_rect(center=(232 + 4 / 2 - 25, 170 / 2))
        self.atts_now_rect = self.atts_now.get_rect(center=(630 / 2 + 50 - 15, 190 + 234 / 2))
        self.best_res_rect = self.best_res.get_rect(center=(630 / 2 + 50 - 15, 240 + 234 + 234 / 2))

        self.papyrus_stats = pygame.transform.scale(self.papyrus_stats, (200, 50))
        self.dummy_stats = pygame.transform.scale(self.dummy_stats, (234, 50))
        self.atts_now = pygame.transform.scale(self.atts_now, (37, 230))
        self.best_res = pygame.transform.scale(self.best_res, (37, 230))

    def draw(self, surface): # отрисовка меню статистики
        surface.blit(self.papyrus_stats, self.rect)
        surface.blit(self.dummy_stats, self.dummy_stats_rect)
        surface.blit(self.atts_now, self.atts_now_rect)
        surface.blit(self.best_res, self.best_res_rect)

    def exit(self): # выход из меню статистики
        self.f_start_menu = True
        self.f_stats_menu = False
        start_menu.f_start_menu = True
        start_menu.f_stats_menu = False


class ControlsMenu(pygame.sprite.Sprite): #класс меню управления
    def __init__(self, group, is_control_menu, is_start_menu):
        self.f_control_menu = is_control_menu
        self.f_start_menu = is_start_menu

        super().__init__(group)

        self.image = pygame.image.load("IMAGES/controls_menu.png")

        self.rect = self.image.get_rect()
        self.rect.center = (350, 350)

    def draw(self, surface): # отрисовка меню управления
        surface.blit(self.image, self.rect)

    def exit(self): # выход и меню управления
        self.f_start_menu = True
        self.f_control_menu = False
        start_menu.f_start_menu = True
        start_menu.f_controls_menu = False


class CreditsMenu(pygame.sprite.Sprite): # класс credits меню
    def __init__(self, group, is_credits_menu, is_start_menu):
        self.f_credits_menu = is_credits_menu
        self.f_start_menu = is_start_menu

        super().__init__(group)

        self.image = pygame.image.load("IMAGES/credits_menu.jpg")

        self.rect = self.image.get_rect()
        self.rect.center = (350, 350)

    def draw(self, surface): # отрисовка credits меню
        surface.blit(self.image, self.rect)

    def exit(self): # выход из credits меню
        self.f_start_menu = True
        self.f_credits_menu = False
        start_menu.f_start_menu = True
        start_menu.f_credits_menu = False


class BossesMenu(pygame.sprite.Sprite): # класс меню с боссами
    def __init__(self, group, is_fight, is_bosses_menu, is_start_menu):

        self.f_fight = is_fight
        self.f_bosses_menu = is_bosses_menu
        self.f_start_menu = is_start_menu
        super().__init__(group)

        self.start_image = pygame.image.load('IMAGES/start.jpg')
        self.right_arrow_image = pygame.image.load('IMAGES/r_arrow.png')
        self.left_arrow_image = pygame.image.load('IMAGES/l_arrow.png')

        self.start = self.start_image
        self.right_arrow = pygame.transform.scale(self.right_arrow_image, (150, 150))
        self.left_arrow = pygame.transform.scale(self.left_arrow_image, (150, 150))

        self.image = self.start
        self.rect = self.image.get_rect()
        self.rect.center = (350, 500)

        self.start_rect = self.start.get_rect(center=(350, 500))
        self.right_arrow_rect = self.right_arrow.get_rect(center=(650, 350))
        self.left_arrow_rect = self.left_arrow.get_rect(center=(60, 350))

    def draw(self, surface): # отрисовка меню с боссами
        if Pages.pages_counter != 2:
            surface.blit(self.right_arrow, self.right_arrow_rect)
            surface.blit(self.start, self.start_rect)
        if Pages.pages_counter != 0:
            surface.blit(self.left_arrow, self.left_arrow_rect)

    def update(self, tap_pos): # обновление меню с боссами
        keys = pygame.key.get_pressed()
        if keys:
            if keys[pygame.K_z] or keys[pygame.K_l]:
                if Pages.pages_counter == 0:
                    DummyMusic()
                else:
                    pass
                if Pages.pages_counter == 1:
                    PapyrusMusic()
                else:
                    pass
                self.f_fight = True
                self.f_bosses_menu = False
                player.f_fight = True
                start_menu.f_bosses_menu = False
                player.hp = 100
                if Pages.pages_counter == 0:
                    player.dummy_hp = 1000
                else:
                    player.papirus_hp = 2500

        if tap_pos:
            if self.rect.collidepoint(tap_pos) and Pages.pages_counter != 2:
                if Pages.pages_counter == 0:
                    DummyMusic()
                else:
                    pass
                if Pages.pages_counter == 1:
                    PapyrusMusic()
                else:
                    pass
                self.f_fight = True
                self.f_bosses_menu = False
                player.f_fight = True
                start_menu.f_bosses_menu = False
                player.hp = 100
                if Pages.pages_counter == 0:
                    player.dummy_hp = 1000
                else:
                    player.papirus_hp = 2500

            if self.right_arrow_rect.collidepoint(tap_pos):
                Pages.plus_page(self)

            if self.left_arrow_rect.collidepoint(tap_pos):
                Pages.minus_page(self)

    def exit(self): # выход из меню боссов
        self.f_bosses_menu = False
        self.f_start_menu = True
        start_menu.f_bosses_menu = False
        start_menu.f_start_menu = True
        Pages.pages_counter = 0


class Pages(): # класс страниц
    def __init__(self, pages):
        self.pages = pages
        Pages.pages_counter = 0

    def minus_page(self): # переключение страницы
        if Pages.pages_counter > 0:
            Pages.pages_counter -= 1

    def plus_page(self): # переключение страницы
        if Pages.pages_counter < 2:
            Pages.pages_counter += 1

    def draw(self, surface): # отрисовка спрайтов страниц
        current_page = self.pages[self.pages_counter]
        width, height = current_page.get_size()
        center_x, center_y = 350, 350
        surface.blit(current_page, (center_x - width // 2, center_y - height // 2))

    def counter(self): # возвращает кол-во страниц
        return Pages.pages_counter

    def draw_fight(self, surface, page): # отрисовка спрайтов боссов в бою
        current_page = self.pages[page]
        width, height = current_page.get_size()
        center_x, center_y = 350, 150
        surface.blit(current_page, (center_x - width // 2, center_y - height // 2))

    def draw_fight_menu(self, surface, page): # отрисовка спрайтов боссов в меню боя
        current_page = self.pages[page]
        width, height = current_page.get_size()
        center_x, center_y = 350, 150
        surface.blit(current_page, (center_x - width // 2, center_y - height // 2))


class Player(pygame.sprite.Sprite): # класс игрока
    def __init__(self, group, is_fight, is_bosses_menu, is_fight_menu):
        self.hp = 100

        self.dummy_hp = 1000
        self.papirus_hp = 2500

        super().__init__(group)
        self.f_fight_menu = is_fight_menu
        self.f_fight = is_fight
        self.f_bosses_menu = is_bosses_menu

        self.frame_counter = 0
        self.fps = 60

        self.up_dash = False
        self.down_dash = False
        self.left_dash = False
        self.right_dash = False
        self.dash = False
        self.can_make_dash = False
        self.is_dash = False

        self.horizontal_barriers_list = None
        self.vertical_barriers_list = None

        self.image = pygame.image.load('IMAGES/soul.png')

        self.copy_image = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.dash_speed = 20
        self.last_dash_time = 0
        self.dash_cooldown = 500

        self.rect.x = 335
        self.rect.y = 435

    def update(self, up, down, left, right): # обновление игрока
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_z] and (current_time - self.last_dash_time >= self.dash_cooldown):
            self.dash = True
            self.last_dash_time = current_time

        elif keys[pygame.K_l] and (current_time - self.last_dash_time >= self.dash_cooldown):
            self.dash = True
            self.last_dash_time = current_time

        if not(self.horizontal_barriers_list):
            self.horizontal_barriers_list = horizontal_barriers.sprites()
            self.up_barrier = self.horizontal_barriers_list[0]
            self.down_barrier = self.horizontal_barriers_list[1]

        if not(self.vertical_barriers_list):
            self.vertical_barriers_list = vertical_barriers.sprites()
            self.left_barrier = self.vertical_barriers_list[0]
            self.right_barrier = self.vertical_barriers_list[1]

        if pygame.sprite.collide_mask(self, self.up_barrier): # проверка на то что игрок двигается вверх и не сталкивается с барьером
            self.up = False
        if self.up:
            self.rect.y -= 5

        if pygame.sprite.collide_mask(self, self.down_barrier): # проверка на то что игрок двигается вниз и не сталкивается с барьером
            self.down = False
        if self.down:
            self.rect.y += 5

        if pygame.sprite.collide_mask(self, self.left_barrier): # проверка на то что игрок двигается влево и не сталкивается с барьером
            self.left = False
        if self.left:
            self.rect.x -= 5

        if pygame.sprite.collide_mask(self, self.right_barrier): # проверка на то что игрок двигается вправо  и не сталкивается с барьером
            self.right = False
        if self.right:
            self.rect.x += 5

        if self.dash:
            self.is_dash = True
            self.not_make_dash = True
            self.dash = False

        if self.is_dash:
            self.dash_animation()

        if self.rect.x < 200: # проверка на то что игрок не вышел за поля
            self.rect.x = 200

        if self.rect.x > 470:
            self.rect.x = 470

        if self.rect.y < 250:
            self.rect.y = 250

        if self.rect.y > 520:
            self.rect.y = 520

    def dash_animation(self): # анимация рывка

        self.frame_counter += 1
        self.first_frame_dash = pygame.image.load('IMAGES/first_hide.png')
        self.second_frame_dash = pygame.image.load('IMAGES/second_hide.png')
        self.third_frame_dash = pygame.image.load('IMAGES/third_hide.png')
        self.fourth_frame_dash = pygame.image.load('IMAGES/first_unhide.png')
        self.fifth_frame_dash = pygame.image.load('IMAGES/second_unhide.png')
        self.sixth_frame_dash = pygame.image.load('IMAGES/third_unhide.png')

        if self.frame_counter == 1:
            self.image = self.third_frame_dash

        if self.frame_counter == 2:
            self.image = self.second_frame_dash

        if self.frame_counter == 4:
            self.image = self.first_frame_dash
            self.can_make_dash = True
            if self.not_make_dash and self.can_make_dash:
                if self.up:
                    self.rect.y -= 100
                    self.up = False
                if self.down:
                    self.rect.y += 100
                    self.down = False
                if self.left:
                    self.rect.x -= 100
                    self.left = False
                if self.right:
                    self.rect.x += 100
                    self.right = False
            self.not_make_dash = False
            self.can_make_dash = False

        if self.frame_counter == 6:
            self.image = self.first_frame_dash

        if self.frame_counter == 8:
            self.image = self.fifth_frame_dash

        if self.frame_counter == 10:
            self.image = self.sixth_frame_dash

        if self.frame_counter == 12:
            self.image = self.copy_image
            self.frame_counter = 0
            self.is_dash = False
            self.up_dash = False
            self.down_dash = False
            self.left_dash = False
            self.right_dash = False

    def is_dummy_damage(self): # проверка на урон от урон от первого босса
        if pygame.sprite.spritecollideany(self, dummy_attack):
            self.hp -= 1

    def is_papirus_damage(self): # проверка на урон от урон от второго босса
        if pygame.sprite.spritecollideany(self, vertical_attack):
            self.hp -= 1

        if pygame.sprite.spritecollideany(self, horizontal_attack):
            self.hp -= 1

        if pygame.sprite.spritecollideany(self, static_attack):
            if self.up or self.down or self.right or self.left:
                self.hp -= 1

        if pygame.sprite.spritecollideany(self, dynamic_attack):
            if self.up or self.down or self.right or self.left:
                pass
            else:
                self.hp -= 1

    def exit(self): # выход из боя
        self.f_fight = False
        self.f_bosses_menu = True
        bosses_menu.f_fight = False
        bosses_menu.f_bosses_menu = True
        start_menu.f_bosses_menu = True
        start_menu.f_start_menu = False

    def player_cords(self): # возвращение координат игрока
        return (self.rect.x, self.rect.y)

    def player_remove(self): # перемещение игрока на стартовую позицию
        self.rect.x = 335
        self.rect.y = 435


class Walls(pygame.sprite.Sprite): # класс барьеров
    def __init__(self, x1, y1, x2, y2):
        color = (255, 255, 255)
        thickness = 2
        super().__init__(all_wals)
        if x1 == x2: # проверка на тип барьера
            self.add(vertical_barriers)
            height = y2 - y1
            self.image = pygame.Surface([thickness, height])
            self.image.fill((0, 0, 0))
            pygame.draw.line(self.image, color, (0, 0), (0, height), thickness)
            self.rect = pygame.Rect(x1, y1, thickness, height)
        elif y1 == y2:
            self.add(horizontal_barriers)
            width = x2 - x1
            self.image = pygame.Surface([width, thickness])
            self.image.fill((0, 0, 0))
            pygame.draw.line(self.image, color, (0, 0), (width, 0), thickness)
            self.rect = pygame.Rect(x1, y1, width, thickness)


class FightMenu(pygame.sprite.Sprite): # меню боя
    def __init__(self, group, is_fight, is_fight_menu):

        self.after_fight_menu_offset = None
        self.fight_or_heal = None
        self.attack_cooldawn = None

        self.f_fight = is_fight
        self.f_fight_menu = is_fight_menu
        self.damage = None
        self.hp_offset = None

        super().__init__(group)

        self.fight_button = pygame.image.load('IMAGES/fight.png')
        self.act_button = pygame.image.load('IMAGES/act.png')
        self.heal_button = pygame.image.load('IMAGES/heal.png')
        self.mercy_button = pygame.image.load('IMAGES/mercy.png')

        self.fight_button = pygame.transform.scale(self.fight_button, (140, 70))
        self.act_button = pygame.transform.scale(self.act_button, (140, 70))
        self.heal_button = pygame.transform.scale(self.heal_button, (140, 70))
        self.mercy_button = pygame.transform.scale(self.mercy_button, (140, 70))

        self.image = self.fight_button
        self.rect = self.image.get_rect()
        self.rect.center = (100, 650)

        self.fight_button_rect = self.fight_button.get_rect(center=(125, 650))
        self.act_button_rect = self.act_button.get_rect(center=(275, 650))
        self.heal_button_rect = self.heal_button.get_rect(center=(425, 650))
        self.mercy_button_rect = self.mercy_button.get_rect(center=(575, 650))

    def update(self, tap_pos): # обновление меню боя
        keys = pygame.key.get_pressed()
        if keys:
            if keys[pygame.K_z] or keys[pygame.K_l]:
                self.fight_or_heal = True

            if keys[pygame.K_k] or keys[pygame.K_x]:
                self.fight_or_heal = False

        if tap_pos:
            if self.fight_button_rect.collidepoint(tap_pos):
                self.fight_or_heal = True

            if self.act_button_rect.collidepoint(tap_pos):
                pass

            if self.heal_button_rect.collidepoint(tap_pos):
                self.fight_or_heal = False

            if self.mercy_button_rect.collidepoint(tap_pos):
                pass

    def draw(self, surface): # отрисовка кнопок боя
        surface.blit(self.fight_button, self.fight_button_rect)
        surface.blit(self.act_button, self.act_button_rect)
        surface.blit(self.heal_button, self.heal_button_rect)
        surface.blit(self.mercy_button, self.mercy_button_rect)

    def fight(self): # бой
        player.f_fight = True
        player.f_fight_menu = False
        self.f_fight = True
        self.f_fight_menu = False
        self.attack_cooldawn = 30

        if Pages.pages_counter == 0:
            self.damage = random.randint(80, 120)
            player.dummy_hp -= self.damage
            self.hp_offset = 60

        if Pages.pages_counter == 1:
            self.damage = random.randint(200, 250)
            player.papirus_hp -= self.damage
            self.hp_offset = 60

    def heal(self): # лечение игрока
        self.fight_or_heal = None
        if player.hp + 50 > 100:
            player.hp = 100
        else:
            player.hp += 50
        player.f_fight = True
        player.f_fight_menu = False
        self.f_fight = True
        self.f_fight_menu = False


class DummyAttack(pygame.sprite.Sprite): # класса первого босса
    def __init__(self, group):
        self.frame_counter = 0
        self.true_frame_counter = 0
        super().__init__(group)

        self.first_attack_image = pygame.image.load('IMAGES/dummy_second_attack.png')
        self.second_attack_image = pygame.image.load('IMAGES/dummy_first_attack.png')
        self.third_attack_image = pygame.image.load('IMAGES/dummy_third_attack.png')

        self.first_attack_image = pygame.transform.scale(self.first_attack_image, (25, 25))
        self.second_attack_image = pygame.transform.scale(self.second_attack_image, (25, 25))
        self.third_attack_image = pygame.transform.scale(self.third_attack_image, (25, 25))

        self.image = self.first_attack_image
        self.rect = self.image.get_rect()

        num = random.randint(1, 4)

        if num == 1: # выбор положения аттаки
            self.rect.x = random.randint(0, 700)
            self.rect.y = 0

        if num == 2:
            self.rect.x = width
            self.rect.y = random.randint(0, 700)

        if num == 3:
            self.rect.x = random.randint(0, 700)
            self.rect.y = height

        if num == 4:
            self.rect.x = 0
            self.rect.y = random.randint(0, 700)

    def update(self, pos_player_x, pos_player_y): # обновление атак босса
        self.frame_counter += 1
        self.true_frame_counter += 1

        if self.frame_counter == 5:
            self.image = self.second_attack_image

        if self.frame_counter == 10:
            self.image = self.third_attack_image

        if self.frame_counter == 15:
            self.frame_counter = 0
            self.image = self.first_attack_image

        if self.rect.x > pos_player_x:
            self.rect.x -= 2
        if self.rect.x < pos_player_x:
            self.rect.x += 2
        if self.rect.y > pos_player_y:
            self.rect.y -= 2
        if self.rect.y < pos_player_y:
            self.rect.y += 2

        if self.true_frame_counter == 240:
            self.rect.x = 99999
            self.rect.x = 99999


class VerticalBoneAttack(pygame.sprite.Sprite): # вертикальные атаки второго босса
    def __init__(self, group, x):
        self.x = x

        super().__init__(group)

        self.vertical_bone_attack = pygame.image.load('IMAGES/vertical_bone.png')
        self.vertical_bone_attack = pygame.transform.scale(self.vertical_bone_attack, (30, 100))

        self.image = self.vertical_bone_attack
        self.rect = self.image.get_rect()

        self.rect.x = self.x + 10
        self.rect.y = 700

    def update(self): # перемещение атаки
        self.rect.y -= 20


class HorizontalBoneAttack(pygame.sprite.Sprite): # вертикальные атаки второго босса
    def __init__(self, group, y):
        self.y = y

        super().__init__(group)

        self.horizontal_bone_attack = pygame.image.load('IMAGES/horizontal_bone.png')
        self.horizontal_bone_attack = pygame.transform.scale(self.horizontal_bone_attack, (100, 30))

        self.image = self.horizontal_bone_attack
        self.rect = self.image.get_rect()

        self.rect.x = 700
        self.rect.y = self.y

    def update(self):# перемещение атаки
        self.rect.x -= 20


class StaticBoneAttack(pygame.sprite.Sprite): # статичные атаки второго босса
    def __init__(self, group):
        super().__init__(group)

        self.static_bone_attack = pygame.image.load('IMAGES/static_bone.png')
        self.static_bone_attack = pygame.transform.scale(self.static_bone_attack, (15, 300))

        self.image = self.static_bone_attack
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 250

    def update(self):# перемещение атаки
        self.rect.x += 10


class DynamicBoneAttack(pygame.sprite.Sprite): # динамичные атаки второго босса
    def __init__(self, group):
        super().__init__(group)

        self.dynamic_bone_attack = pygame.image.load('IMAGES/dynamic_bone.png')
        self.dynamic_bone_attack = pygame.transform.scale(self.dynamic_bone_attack, (300, 15))

        self.image = self.dynamic_bone_attack
        self.rect = self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 0

    def update(self):# перемещение атаки
        self.rect.y += 10


class VerticalBoneAttackSpam(pygame.sprite.Sprite): # вертикальные атаки второго босса
    def __init__(self, group, x):
        self.x = x

        super().__init__(group)

        self.vertical_bone_attack = pygame.image.load('IMAGES/vertical_bone.png')

        self.image = self.vertical_bone_attack
        self.rect = self.image.get_rect()

        self.rect.x = self.x + 10
        self.rect.y = 700

    def update(self):# перемещение атаки
        self.rect.y -= 20


class HorizontalBoneAttackSpam(pygame.sprite.Sprite): # горизонтальные атаки второго босса
    def __init__(self, group, y):
        self.y = y

        super().__init__(group)

        self.horizontal_bone_attack = pygame.image.load('IMAGES/horizontal_bone.png')

        self.image = self.horizontal_bone_attack
        self.rect = self.image.get_rect()

        self.rect.x = 700
        self.rect.y = self.y

    def update(self):# перемещение атаки
        self.rect.x -= 20


class FightMenuMessages(pygame.sprite.Group): # класса сообщений в меню боя
    def __init__(self, group):

        super().__init__(group)
        self.rare_screen_first = pygame.image.load('IMAGES/Bolkich.PNG')
        self.rare_screen_second = pygame.image.load('IMAGES/bolkich2.PNG')
        self.rare_screen_third = pygame.image.load('IMAGES/upd_page_plz.PNG')
        self.rare_screen_fourth = pygame.image.load('IMAGES/bbbbbbb.PNG')
        self.rare_screen_fifth = pygame.image.load('IMAGES/wth.PNG')

        self.def_screen = pygame.image.load('IMAGES/press_any_button.PNG')

        num = random.randint(0, 99) # выбор сообщения

        if num == 0:
            self.image = self.rare_screen_first
            self.image = pygame.transform.scale(self.image, (350, 60))

        elif num == 20:
            self.image = self.rare_screen_second
            self.image = pygame.transform.scale(self.image, (350, 60))

        elif num == 40:
            self.image = self.rare_screen_third
            self.image = pygame.transform.scale(self.image, (350, 60))

        elif num == 60:
            self.image = self.rare_screen_fourth
            self.image = pygame.transform.scale(self.image, (350, 60))

        elif num == 80:
            self.image = self.rare_screen_fifth
            self.image = pygame.transform.scale(self.image, (350, 60))

        else:
            self.image = self.def_screen

            self.image = pygame.transform.scale(self.image, (300, 60))

        self.rect = self.image.get_rect()

        self.rect.x = 60
        self.rect.y = 375

    def draw(self, surface): # отрисовка сообщения в меню боя
        surface.blit(self.image, self.rect)


class DummyMusic(): # музыка первого босса
    def __init__(self):
        pygame.mixer.music.load('MUSIC/Undertale OST： 036 - Dummy!.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def dummy_music_stop(self): # остановка музыки первого босса
        pygame.mixer.music.stop()


class PapyrusMusic(): # музыка второго босса
    def __init__(self):
        pygame.mixer.music.load('MUSIC/Disbelief Papyrus phase 1 theme - Interstellar Retribution.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def papyrus_music_stop(self): # остановка музыки второго босса
        pygame.mixer.music.stop()


fight_menu = FightMenu(fight_menu, is_fight, is_fight_menu) # создание экземпляров классов меню
start_menu = StartMenu(start_interface, is_start_menu, is_bosses_menu, is_controls_menu, is_credits_menu, is_stats_menu)
bosses_menu = BossesMenu(boss_interface, is_fight, is_bosses_menu, is_start_menu)
controls_menu = ControlsMenu(control_menu, is_controls_menu, is_start_menu)
credits_menu = CreditsMenu(credits_menu, is_credits_menu, is_start_menu)
stats_menu = StatsMenu(is_stats_menu, is_stats_menu)

page = Pages(pages)
player = Player(heart, is_fight, is_bosses_menu, is_fight_menu)

Walls(200, 250, width - 200, 250) # создание барьеров
Walls(200, height - 150, width - 200, height - 150)
Walls(200, 250, 200, height - 150)
Walls(width - 200, 250, width - 200, height - 150)

attack_cooldown = 60 # объявление переменных для игрового процесса
num_cooldown = 0
attack_num = 0
walls_limit = 30
wall_animation_counter = 0

while True: # основной цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # проверка на выход
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: # считывание нажатия
            mouse_tap_pos = event.pos

        if event.type == pygame.KEYDOWN: # считывание нажатых клавиш
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                up = True

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                down = True

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = True

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = True

            if event.key == pygame.K_ESCAPE and is_stats_menu: # выход из меню статистики
                stats_menu.exit()
                mouse_tap_pos = None

            if event.key == pygame.K_ESCAPE and is_controls_menu: # выход из меню управления
                controls_menu.exit()
                mouse_tap_pos = None

            if event.key == pygame.K_ESCAPE and is_credits_menu: # выход из меню credits
                credits_menu.exit()
                mouse_tap_pos = None

            if event.key == pygame.K_ESCAPE and is_bosses_menu: # выход из меню боссов
                bosses_menu.exit()
                mouse_tap_pos = None

            if event.key == pygame.K_ESCAPE and is_fight: # выход из боя
                if Pages.pages_counter == 0:
                    cursor.execute('UPDATE attemps SET dummy = dummy + 1')
                    DummyMusic.dummy_music_stop(self=True)
                    db.commit()

                if Pages.pages_counter == 1:
                    cursor.execute('UPDATE attemps SET papyrus = papyrus + 1')
                    PapyrusMusic.papyrus_music_stop(self=True)
                    db.commit()

                frame_counter = 0
                player.exit()
                dummy_attack = pygame.sprite.Group()
                vertical_attack = pygame.sprite.Group()
                horizontal_attack = pygame.sprite.Group()
                static_attack = pygame.sprite.Group()
                dynamic_attack = pygame.sprite.Group()
                fight_menu.hp_offset = 0
                attack_cooldown = 60
                num_cooldown = 0
                player.player_remove()
                mouse_tap_pos = None
                death_offset = 90

        if event.type == pygame.KEYUP: # считывание отжатых клавиш
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                up = False

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                down = False

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = False

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = False

    font_size = 35
    font = pygame.font.Font(None, font_size)

    screen.fill((0, 0, 0))
    pages = Pages.pages_counter

    if is_stats_menu: # обновление флагов статистики
        is_stats_menu = stats_menu.f_stats_menu
        is_start_menu = stats_menu.f_start_menu

    if is_fight_menu: # обновление флагов меню боя
        is_fight = fight_menu.f_fight
        is_fight_menu = fight_menu.f_fight_menu

    if is_fight: # обновление флагов боя
        is_fight = player.f_fight
        is_bosses_menu = player.f_bosses_menu
        is_fight_menu = player.f_fight_menu

    if is_bosses_menu: # обновление флагов меню боссов
        is_fight = bosses_menu.f_fight
        is_bosses_menu = bosses_menu.f_bosses_menu
        is_start_menu = bosses_menu.f_start_menu

    if is_start_menu: # обновление флагов стартового меню
        is_bosses_menu = start_menu.f_bosses_menu
        is_start_menu = start_menu.f_start_menu
        is_controls_menu = start_menu.f_controls_menu
        is_credits_menu = start_menu.f_credits_menu
        is_stats_menu = start_menu.f_stats_menu

    if is_controls_menu: # обновление флагов управления
        is_controls_menu = controls_menu.f_control_menu
        is_start_menu = controls_menu.f_start_menu

    if is_credits_menu: # обновление флагов credits
        is_credits_menu = credits_menu.f_credits_menu
        is_start_menu = credits_menu.f_start_menu

    if is_fight: # инициализация игрового процесса
        fight_menu.draw(screen)
        pygame.mouse.set_visible(False)
        hp = player.hp
        cords = player.player_cords()
        frame_counter += 1
        page.draw_fight(screen, pages)
        heart.update(up, down, left, right)
        heart.draw(screen)
        all_wals.draw(screen)

        font_size = 50
        font = pygame.font.Font(None, font_size)

        text = font.render(f'hp: {hp}', True, (0, 255, 0))
        text_rect = text.get_rect(center=(350, height - 120))

        font_size = 35
        font = pygame.font.Font(None, font_size)

        screen.blit(text, text_rect)

        if hp <= 0: # проверка на здоровье
            if Pages.pages_counter == 0:
                cursor.execute('UPDATE attemps SET dummy = dummy + 1')
                DummyMusic.dummy_music_stop(self=True)
                db.commit()
            if Pages.pages_counter == 1:
                cursor.execute('UPDATE attemps SET papyrus = papyrus + 1')
                PapyrusMusic.papyrus_music_stop(self=True)
                db.commit()
            frame_counter = 0
            dummy_attack = pygame.sprite.Group()
            vertical_attack = pygame.sprite.Group()
            horizontal_attack = pygame.sprite.Group()
            static_attack = pygame.sprite.Group()
            dynamic_attack = pygame.sprite.Group()
            player.exit()
            attack_cooldown = None
            player.player_remove()
            death_offset = 90

        if pages == 0: # проверка выбранного босса
            cursor.execute('''UPDATE attemps
                                            SET dummy = 1
                                            WHERE dummy = 0''')
            if attack_cooldown: # проверка на задержку атаки
                attack_cooldown -= 1

                if attack_cooldown == 0: # проверка на готовность атаки
                    attack_cooldown = 30
                    DummyAttack(dummy_attack)
                    dummy_attack.draw(screen)
                    player.is_dummy_damage()
                else:
                    dummy_attack.draw(screen)
                    player.is_dummy_damage()
                    dummy_attack.update(cords[0], cords[1])

            else:
                attack_cooldown = 1

            text = font.render(f'hp: {player.dummy_hp}', True, (0, 255, 0)) # вывод здоровья игрока
            text_rect = text.get_rect(center=(455, 235))
            screen.blit(text, text_rect)

            dummy_hp = player.dummy_hp
            if dummy_hp <= 0: # проверка здоровья босса
                win_offset = 90
                cursor.execute('''UPDATE result
                                    SET dummy_result = CASE
                                                            WHEN dummy_result IS NULL OR (SELECT dummy FROM attemps WHERE attemps.id = result.id) < dummy_result
                                                            THEN (SELECT dummy FROM attemps WHERE attemps.id = result.id)
                                                            ELSE dummy_result
                                                        END''')
                cursor.execute('''UPDATE attemps
                                                    SET dummy = 0''')
                db.commit()
                DummyMusic.dummy_music_stop(self=True)
                player.exit()
                dummy_hp = 1000
                player.dummy_hp = 1000
                fight_menu.hp_offset = 0

        if pages == 1: # проверка выбранного босса
            cursor.execute('''UPDATE attemps
                                            SET papyrus = 1
                                            WHERE papyrus = 0''')
            if attack_cooldown: # проверка на задержку атаки
                attack_cooldown -= 1
                if attack_cooldown == 0: # проверка на готовность атаки
                    if num_cooldown:
                        num_cooldown -= 1

                    if num_cooldown == 0: # проверка на готовность выбора атаки
                        attack_cooldown = 60
                        if attack_num == 0:
                            attack_num = 1

                        elif attack_num == 1:
                            attack_num = 2

                        elif attack_num == 2:
                            attack_num = 3

                        elif attack_num == 3:
                            attack_num = 0

                        if attack_num == 0:
                            num_cooldown = 0

                        if attack_num == 1:
                            num_cooldown = 5

                        if attack_num == 2:
                            num_cooldown = 5

                        if attack_num == 3:
                            num_cooldown = 2

                    if attack_num == 0: # первая атака
                        if num_cooldown:
                            attack_cooldown = 30

                        VerticalBoneAttack(vertical_attack, cords[0])
                        vertical_attack.draw(screen)
                        vertical_attack.update()

                        HorizontalBoneAttack(horizontal_attack, cords[1])
                        horizontal_attack.draw(screen)
                        horizontal_attack.update()

                    if attack_num == 1: # вторая атака
                        if num_cooldown:
                            attack_cooldown = 5

                        VerticalBoneAttackSpam(vertical_attack, cords[0])
                        vertical_attack.draw(screen)
                        vertical_attack.update()

                        HorizontalBoneAttackSpam(horizontal_attack, cords[1])
                        horizontal_attack.draw(screen)
                        horizontal_attack.update()

                    if attack_num == 2: # третья атака
                        if num_cooldown:
                            attack_cooldown = 25

                        if num_cooldown % 2 == 0:
                            StaticBoneAttack(static_attack)
                            static_attack.draw(screen)
                            static_attack.update()
                        else:
                            DynamicBoneAttack(dynamic_attack)
                            dynamic_attack.draw(screen)
                            dynamic_attack.update()

                    if attack_num == 3: # четвертая атака
                        attack_cooldown = 30
                        if num_cooldown % 2 == 0:
                            for i in range(4):
                                HorizontalBoneAttack(horizontal_attack, (i * 75) + 250)

                        else:
                            for i in range(4):
                                HorizontalBoneAttack(horizontal_attack, (i * 75) + 280)
                else:
                    vertical_attack.draw(screen)
                    vertical_attack.update()
                    horizontal_attack.draw(screen)
                    horizontal_attack.update()
                    static_attack.draw(screen)
                    static_attack.update()
                    dynamic_attack.draw(screen)
                    dynamic_attack.update()

                    player.is_papirus_damage()
            else:
                attack_cooldown = 1

            text = font.render(f'hp: {player.papirus_hp}', True, (0, 255, 0)) # вывод здоровья второго босса
            text_rect = text.get_rect(center=(455, 235))
            screen.blit(text, text_rect)
            papirus_hp = player.papirus_hp

            if papirus_hp <= 0: # проверка на здоровья второго босса
                win_offset = 90
                cursor.execute('''UPDATE result
                                                                    SET papyrus_result = CASE
                                                                                            WHEN papyrus_result IS NULL OR (SELECT papyrus FROM attemps WHERE attemps.id = result.id) < papyrus_result
                                                                                            THEN (SELECT papyrus FROM attemps WHERE attemps.id = result.id)
                                                                                            ELSE dummy_result
                                                                                        END''')
                cursor.execute('''UPDATE attemps
                                                    SET papyrus = 0''')
                db.commit()
                PapyrusMusic.papyrus_music_stop(self=True)
                player.exit()

                papirus_hp = 2500
                fight_menu.hp_offset = 0

                vertical_attack = pygame.sprite.Group()
                horizontal_attack = pygame.sprite.Group()
                static_attack = pygame.sprite.Group()
                dynamic_attack = pygame.sprite.Group()

                papirus_hp = player.papirus_hp

        if fight_menu.hp_offset:
            text = font.render(f'- {fight_menu.damage}', True, (255, 0, 0))
            text_rect = text.get_rect(center=(455, 200))
            screen.blit(text, text_rect)
            fight_menu.hp_offset -= 1

    if pages == 0: #
        k = 8
    if pages == 1:
        k = 12

    if frame_counter == 60 * k: # проверка на окончание атаки
        pygame.mouse.set_visible(True)

        walls_limit = 30
        cant_click = 30
        player.player_remove()
        frame_counter = 0

        is_fight = False
        is_fight_menu = True
        player.f_fight = False
        player.f_fight_menu = True
        fight_menu.f_fight = False
        fight_menu.f_fight_menu = True

        attack_cooldown = 60
        num_cooldown = 0
        attack_num == 0
        dummy_attack = pygame.sprite.Group()
        vertical_attack = pygame.sprite.Group()
        horizontal_attack = pygame.sprite.Group()
        static_attack = pygame.sprite.Group()
        dynamic_attack = pygame.sprite.Group()

        fight_menu.fight_or_heal = None
        after_fight_menu_offset = None

        message = FightMenuMessages(fight_menu_messages)

    if is_fight_menu: # проверка на меню битвы

        text = font.render(f'L/Z', True, (255, 0, 0))
        text_rect = text.get_rect(center=(125, 600))
        screen.blit(text, text_rect)

        text = font.render(f'K/X', True, (0, 255, 0))
        text_rect = text.get_rect(center=(425, 600))
        screen.blit(text, text_rect)

        if (fight_menu.fight_or_heal == True or fight_menu.fight_or_heal == False) and after_fight_menu_offset == None:
            after_fight_menu_offset = 30

        if fight_menu.fight_or_heal == True and after_fight_menu_offset == 0:
            fight_menu.fight()
            wall_animation_counter = 0

        if fight_menu.fight_or_heal == False and after_fight_menu_offset == 0:
            fight_menu.heal()
            wall_animation_counter = 0

        if after_fight_menu_offset:
            after_fight_menu_offset -= 1
            pygame.draw.line(screen, (255, 255, 255),
                             (200 - wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (500 + wall_animation_counter * 5, 250 + wall_animation_counter * 4), 3)

            pygame.draw.line(screen, (255, 255, 255), (200 - wall_animation_counter * 5, height - 150),
                             (500 + wall_animation_counter * 5, height - 150), 3)

            pygame.draw.line(screen, (255, 255, 255),
                             (200 - wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (200 - wall_animation_counter * 5, 550), 3)

            pygame.draw.line(screen, (255, 255, 255),
                             (500 + wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (500 + wall_animation_counter * 5, 550), 3)
            wall_animation_counter -= 1

        if walls_limit:
            walls_limit -= 1
            pygame.draw.line(screen, (255, 255, 255), (200 - wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (500 + wall_animation_counter * 5, 250 + wall_animation_counter * 4) , 3)

            pygame.draw.line(screen, (255, 255, 255), (200 - wall_animation_counter * 5, height - 150),
                             (500 + wall_animation_counter * 5, height - 150), 3)

            pygame.draw.line(screen, (255, 255, 255), (200 - wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (200 - wall_animation_counter * 5, 550), 3)

            pygame.draw.line(screen, (255, 255, 255), (500 + wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (500 + wall_animation_counter * 5, 550), 3)

            wall_animation_counter += 1
        else:
            pygame.draw.line(screen, (255, 255, 255),
                             (200 - wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (500 + wall_animation_counter * 5, 250 + wall_animation_counter * 4), 3)

            pygame.draw.line(screen, (255, 255, 255), (200 - wall_animation_counter * 5, height - 150),
                             (500 + wall_animation_counter * 5, height - 150), 3)

            pygame.draw.line(screen, (255, 255, 255),
                             (200 - wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (200 - wall_animation_counter * 5, 550), 3)

            pygame.draw.line(screen, (255, 255, 255),
                             (500 + wall_animation_counter * 5, 250 + wall_animation_counter * 4),
                             (500 + wall_animation_counter * 5, 550), 3)

        if walls_limit == 0 and after_fight_menu_offset == None:
            message.draw(screen)

        page.draw_fight_menu(screen, pages)
        fight_menu.draw(screen)
        if cant_click:
            cant_click -= 1
        else:
            fight_menu.update(mouse_tap_pos)
            mouse_tap_pos = None
        text = font.render(f'hp: {hp}', True, (0, 255, 0))
        text_rect = text.get_rect(center=(50, 20))
        screen.blit(text, text_rect)
        attack_cooldown = fight_menu.attack_cooldawn

    elif is_menu:
        if is_start_menu:
            start_interface.update(mouse_tap_pos)
            start_interface.draw(screen)
            start_menu.draw(screen)
            mouse_tap_pos = None

        if is_bosses_menu: # проверка на меню боссов
            if death_offset:
                death_offset -= 1

                font_size = 50
                font = pygame.font.Font(None, font_size)
                text = font.render(f'You Lose...', True, (255, 0, 0))
                text_rect = text.get_rect(center=(350, 175))
                screen.blit(text, text_rect)
                font_size = 35
                font = pygame.font.Font(None, font_size)

            if win_offset:
                win_offset -= 1

                font_size = 50
                font = pygame.font.Font(None, font_size)
                text = font.render(f'You Win!!!', True, (0, 255, 0))
                text_rect = text.get_rect(center=(350, 175))
                screen.blit(text, text_rect)
                font_size = 35
                font = pygame.font.Font(None, font_size)

            if not(win_offset) and not(death_offset):
                boss_interface.update(mouse_tap_pos)

            pygame.mouse.set_visible(True)
            boss_interface.draw(screen)
            bosses_menu.draw(screen)
            page.draw(screen)
            mouse_tap_pos = None
            pygame.draw.line(screen, (255, 255, 255), (0, 50), (width, 50), 3)
            pygame.draw.line(screen, (255, 255, 255), (0, height - 50), (width, height - 50), 3)

        if is_controls_menu: # проверка на меню управления
            control_menu.draw(screen)

        if is_credits_menu: # проверка на credits
            credits_menu.draw(screen)

        if is_stats_menu:# проверка на меню статистики
            stats_menu.draw(screen)
            cursor.execute('SELECT dummy FROM attemps')
            row = cursor.fetchall()
            if row:
                dummy_attemps = row[0]

            cursor.execute('SELECT papyrus FROM attemps')
            row = cursor.fetchall()
            if row:
                papyrus_attemps = row[0]

            cursor.execute('SELECT dummy_result FROM result')
            roww = cursor.fetchall()
            if roww:
                dummy_result = roww[0]

            cursor.execute('SELECT papyrus_result FROM result')
            roww = cursor.fetchall()
            if roww:
                papyrus_result = roww[0]
            font_size = 80
            font = pygame.font.Font(None, font_size)

            text1 = font.render(f'{dummy_attemps[0]}', True, (255, 255, 255))
            text1_rect = text1.get_rect(center=(160, height - 420))

            text2 = font.render(f'{papyrus_attemps[0]}', True, (255, 255, 255))
            text2_rect = text2.get_rect(center=(550, height - 420))

            text3 = font.render(f'{dummy_result[0]}', True, (255, 255, 255))
            text3_rect = text3.get_rect(center=(160, height - 120))

            text4 = font.render(f'{papyrus_result[0]}', True, (255, 255, 255))
            text4_rect = text4.get_rect(center=(550, height - 120))

            pygame.draw.line(screen, (255, 255, 255), (320, 125), (320, 700), 3)
            pygame.draw.line(screen, (255, 255, 255), (380, 125), (380, 700), 3)
            pygame.draw.line(screen, (255, 255, 255), (350, 0), (350, 125), 3)
            pygame.draw.line(screen, (255, 255, 255), (0, 125), (700, 125), 3)
            pygame.draw.line(screen, (255, 255, 255), (0, 420), (700, 420), 3)

            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)
            screen.blit(text4, text4_rect)

    pygame.display.flip() # обновление изображения
    clock.tick(fps)