from blocks import *
import pygame
from Player import *
from monsters import *

Win_Width = 800
Win_Height = 600
Display = (Win_Width, Win_Height)
BackGround_color = "#000000"
PlatformWidth = 32
PlatformHeight = 32
PlatformColor = "#ffffff"
ICON_DIR = os.path.dirname(__file__)
Player_SpeedX = 0
Player_SpeedY = 0


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + Win_Width / 2, -t + Win_Height / 2

    l = min(0, l)
    l = max(-(camera.width - Win_Width), l)
    t = max(-(camera.height - Win_Height), t)
    t = min(0, t)

    return Rect(l, t, w, h)


Moving_Block_Speed = 0


def loadLevel(Level):
    global Respawn_playerX, Respawn_playerY, levelwidth, Win_Width, Win_Height, Player_SpeedX, Player_SpeedY, Moving_Block_Speed
    levelFile = 0
    if Level == 1:
        levelFile = open('%s/levels/1' % ICON_DIR)
    elif Level == 2:
        levelFile = open('%s/levels/2' % ICON_DIR)
    elif Level == 3:
        levelFile = open('%s/levels/3' % ICON_DIR)
    elif Level == 4:
        levelFile = open('%s/levels/4' % ICON_DIR)
    elif Level == 5:
        levelFile = open("%s/levels/5" % ICON_DIR)
    line = " "
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"
                    levelwidth = len(line) * 32 - 32
        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда player
                    Respawn_playerX = int(commands[1])  # то записываем координаты героя
                    Respawn_playerY = int(commands[2])
                    Player_SpeedX = int(commands[3])
                    Player_SpeedY = int(commands[4])
                if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                if commands[0] == "agressive":  # если первая команда agressive, то создаем агресивного монстра
                    mn = Agressive_Monster(int(commands[1]), int(commands[2]), int(commands[5]), int(commands[6]),
                                           int(commands[3]), int(commands[4]))
                    entities.add(mn)
                    platforms.append(mn)
                    Agressive.add(mn)
                if commands[0] == "display":
                    Win_Width = int(commands[1])
                    Win_Height = int(commands[2])
                    print(Win_Width)
                    print(Win_Height)
                if commands[0] == "falling":
                    fl = Falling_Block(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                       int(commands[5]), int(commands[6]), int(commands[7]))
                    entities.add(fl)
                    platforms.append(fl)
                    Falling.add(fl)
                if commands[0] == "moving":
                    if Moving_Block_Speed:
                        mv = Moving_Block(int(commands[1]), int(commands[2]), int(commands[3]),
                                          int(commands[4]), int(commands[5]))
                        Moving_Block_Speed = int(commands[4])
                    else:
                        mv = Moving_Block(int(commands[1]), int(commands[2]), int(commands[3]),
                                          int(commands[4]), int(commands[5]))
                    entities.add(mv)
                    platforms.append(mv)
                    Moving.add(mv)


def intro():
    in_intro = True
    pygame.init()
    while in_intro:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                quitgame()
        menuDisplay = pygame.display.set_mode(Display)
        menuDisplay.fill((255, 255, 255))
        button_functions(menuDisplay, 0, 0, 800, 100, (255, 255, 0), (255, 255, 0), main)

        button_functions(menuDisplay, 0, 500, 800, 100, (0, 0, 155), (0, 0, 200), main)
        pygame.display.update()


def button_functions(Display, x, y, width, height, Acctive_color, Inacctive_color, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for i in pygame.event.get():
        if i.type == QUIT:
            raise SystemExit("QUIT")
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(Display, Acctive_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(Display, Inacctive_color, (x, y, width, height))


def quitgame():
    pygame.quit()
    quit()


def TEXT(text, window):
    textWindow = window.render(text, True, (0, 0, 0))
    return textWindow, textWindow.get_rect()


def main():
    global CurrentLevel, entities, level, animated_Entities, monsters, Agressive, Falling, Moving, platforms
    pygame.init()
    loadLevel(CurrentLevel)
    hero = Player(Respawn_playerX, Respawn_playerY, Player_SpeedX, Player_SpeedY)
    left, right = False, False
    up = False
    entities.add(hero)
    Display = ((Win_Width, Win_Height))
    screen = pygame.display.set_mode(Display)
    BG = Surface((Win_Width, Win_Height))
    Time_Stop = False
    micro_tp = False
    timer = pygame.time.Clock()
    x = y = 0
    BG.fill((Color(BackGround_color)))
    RespawnBlockList = []
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = DieBlock(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                Win = End_Block(x, y)
                entities.add(Win)
                platforms.append(Win)
                animated_Entities.add(Win)
            if col == "S":
                Sp = SpeedBoost_Block(x, y)
                entities.add(Sp)
                platforms.append(Sp)
                animated_Entities.add(Sp)
            if col == "J":
                Ju = JumpBoost_Block(x, y)
                entities.add(Ju)
                platforms.append(Ju)
                animated_Entities.add(Ju)
            if col == "N":
                Un = Brick_Unknown(x, y)
                entities.add(Un)
                platforms.append(Un)
            if col == "R":
                Res = RespawnBlock(x, y)
                entities.add(Res)
                platforms.append(Res)
                RespawnBlockList.append(Res)
            x += PlatformWidth
        y += PlatformHeight
        x = 0
    total_level_width = len(level[0]) * PlatformWidth  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PlatformHeight  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    while True:
        for i in pygame.event.get():
            if i.type == QUIT:
                raise SystemExit("QUIT")
            if i.type == KEYDOWN and (i.key == K_LEFT or i.key == K_a):
                left = True

            if i.type == KEYDOWN and (i.key == K_RIGHT or i.key == K_d):
                right = True

            if i.type == KEYUP and (i.key == K_RIGHT or i.key == K_d):
                right = False
            if i.type == KEYUP and (i.key == K_LEFT or i.key == K_a):
                left = False

            if i.type == KEYDOWN and (i.key == K_UP or i.key == K_w or i.key == K_SPACE):
                up = True
            if i.type == KEYDOWN and i.key == K_LCTRL and not Time_Stop:
                Time_Stop = True
            elif i.type == KEYDOWN and i.key == K_LCTRL and Time_Stop:
                Time_Stop = False
            if i.type == KEYUP and (i.key == K_UP or i.key == K_w or i.key == K_SPACE):
                up = False
            if i.type == KEYDOWN and i.key == K_LALT:
                micro_tp = True
            if i.type == KEYUP and i.key == K_LALT:
                micro_tp = False
        screen.blit(BG, (0, 0))

        camera.update(hero)
        monsters.update(platforms)
        animated_Entities.update()
        Moving.update()
        Agressive.update(platforms, hero.rect.x, hero.rect.y)
        hero.update(left, right, up, micro_tp, levelwidth, platforms, Moving_Block_Speed)
        Falling.update()
        if hero.winner:
            CurrentLevel += 1
            level = []
            entities = pygame.sprite.Group()
            animated_Entities = pygame.sprite.Group()
            monsters = pygame.sprite.Group()
            Agressive = pygame.sprite.Group()
            Falling = pygame.sprite.Group()
            Moving = pygame.sprite.Group()
            platforms = []
            main()
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
        timer.tick(hero.FPS)


level = []
entities = pygame.sprite.Group()
animated_Entities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
Agressive = pygame.sprite.Group()
Falling = pygame.sprite.Group()
Moving = pygame.sprite.Group()
platforms = []
CurrentLevel = 2
if __name__ == "__main__":
    intro()
