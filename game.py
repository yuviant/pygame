import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (1200, 700)
screen = pygame.display.set_mode(screen_size)
FPS = 50
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')
tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


class Enemy(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def check(self, pos_hero):
        if pos_hero == self.pos:
            return battle()


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    global hero, max_x, max_y, enemies, level_map
    fon = pygame.transform.scale(load_image('8w2.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 500 < x < 700:
                    if 250 < y < 320:
                        text()
                        level_map = load_level("map1.txt")
                        hero, max_x, max_y, enemies = generate_level(level_map)
                        game()
                    elif 350 < y < 420:
                        game_load()
        pygame.display.flip()
        clock.tick(FPS)


def text():
    screen.fill(pygame.Color("black"))
    intro_text = ['Предыстория, жил-был камень. Жил он спокойно, никого не трогал, как вдруг,',
                  'откуда невозьмись появляется странный человек, который оживляет камень.',
                  'После этого, камень начинает путешествовать,',
                  'но вскоре он устал от бесконечных приключений и захотел покоя.',
                  'Для этого он начинает поиски того самого человека...']
    font = pygame.font.Font(None, 30)
    text_coord = 600

    while text_coord > -350:
        screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = 200
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord -= 351
        pygame.display.flip()
        clock.tick(FPS)


def menu():
    fon = pygame.transform.scale(load_image('menu.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < 190:
                    if 300 > y > 270:
                        return True
                    elif 350 < y < 400:
                        save()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def battle():
    fon = pygame.transform.scale(load_image('bat1.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    hp1 = 60
    hp2 = 60

    while True:
        if hp1 <= 0:
            return False
        elif hp2 <= 0:
            return True
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 700 > y > 550:
                    if x < 400:
                        hp2 -= 10
                        hp1 -= 5
                    elif x > 800:
                        return False
        pygame.draw.rect(screen, (0, 0, 0), (168, 215, 120, 20), 1)
        pygame.draw.rect(screen, (0, 0, 0), (904, 168, 120, 20), 1)
        pygame.draw.rect(screen, (255, 0, 0), (169, 216, -2 + hp1 * 2, 18))
        pygame.draw.rect(screen, (255, 0, 0), (905, 169, -2 + hp2 * 2, 18))
        pygame.display.flip()
        clock.tick(FPS)


def game_load():
    global hero, max_x, max_y, enemies, level_map
    level_map = load_level("save.txt")
    hero, max_x, max_y, enemies = generate_level(level_map)
    game()


def save():
    s_map = level_map
    h_pos = hero.pos
    s_map[h_pos[1]][h_pos[0]] = '@'
    for i in enemies:
        pos = i.pos
        s_map[pos[1]][pos[0]] = 'x'
    with open('data/save.txt', mode='w') as f_out:
        f = ''
        for i in s_map:
            f += ''.join(i) + '\n'
        f_out.write(f)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    new_enemies = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.' or level[y][x] == '=' or level[y][x] == '!':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                new_enemies.append(Enemy(x, y))
                level[y][x] = "."
    return new_player, x, y, new_enemies


def move(hero, movement):
    x, y = hero.pos

    if movement == "up":
        if y > 0 and level_map[y - 1][x] != "#":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] != "#":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] != "#":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] != "#":
            hero.move(x + 1, y)


def end_list():
    fon = pygame.transform.scale(load_image('end.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def game():
    global level_map, hero, max_x, max_y, running, sprite_group, hero_group, enemies
    print(*level_map, sep='\n')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(hero, "up")
                elif event.key == pygame.K_DOWN:
                    move(hero, "down")
                elif event.key == pygame.K_LEFT:
                    move(hero, "left")
                elif event.key == pygame.K_RIGHT:
                    move(hero, "right")
                if level_map[hero.pos[1]][hero.pos[0]] == '=':
                    sprite_group = SpriteGroup()
                    hero_group = SpriteGroup()
                    level_map = load_level("map2.txt")
                    hero, max_x, max_y, enemies = generate_level(level_map)
                elif level_map[hero.pos[1]][hero.pos[0]] == '!':
                    end_list()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu():
                    start_screen()
            for enemy in enemies:
                if enemy.check(hero.pos):
                    enemy.kill()
                    del enemies[enemies.index(enemy)]

        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


start_screen()
pygame.quit()
