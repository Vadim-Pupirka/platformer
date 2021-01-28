from pygame import *
import os
import pyganim
import time

PlatformWidth = 32
PlatformHeight = 32
PlatformColor = "#ffffff"
ICON_DIR = os.path.dirname(__file__)

Animation_End_Block = [
    ("%s/Blocks/END1.png" % ICON_DIR),
    ("%s/Blocks/END2.png" % ICON_DIR),
    ("%s/Blocks/END3.png" % ICON_DIR),
    ("%s/Blocks/END4.png" % ICON_DIR),
    ("%s/Blocks/END5.png" % ICON_DIR),
    ("%s/Blocks/END6.png" % ICON_DIR)
]
Animation_SpeedBoost_Block = [
    ("%s/Blocks/Speed_Boost.png" % ICON_DIR),
    ("%s/Blocks/Speed_Boost1.png" % ICON_DIR),
    ("%s/Blocks/Speed_Boost2.png" % ICON_DIR),
    ("%s/Blocks/Speed_Boost3.png" % ICON_DIR)
]
Animation_JumpBoost_Block = [
    ("%s/Blocks/Jump_Boost1.png" % ICON_DIR),
    ("%s/Blocks/Jump_Boost2.png" % ICON_DIR),
    ("%s/Blocks/Jump_Boost3.png" % ICON_DIR),
    ("%s/Blocks/Jump_Boost4.png" % ICON_DIR),
    ("%s/Blocks/Jump_Boost5.png" % ICON_DIR)
]
Animation_Moving_Death_Block = [
    ("%s/Blocks/Moving_Death_Block_1.png" % ICON_DIR),
    ("%s/Blocks/Moving_Death_Block_2.png" % ICON_DIR),
    ("%s/Blocks/Moving_Death_Block_3.png" % ICON_DIR),
    ("%s/Blocks/Moving_Death_Block_4.png" % ICON_DIR),

]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PlatformWidth, PlatformHeight))
        self.image = image.load("%s/Blocks/Block_Rotate_Up.png" % ICON_DIR)
        self.rect = Rect(x, y, PlatformWidth, PlatformHeight)


class DieBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/Blocks/Block_Die.png" % ICON_DIR)


class Moving_Block(Platform):
    def __init__(self, x, y, EndX, Speed, Time):
        global PlatformHeight
        PlatformHeight = 21
        Platform.__init__(self, x, y)
        PlatformHeight = 32
        self.Time = Time
        self.End = EndX
        self.Start = x
        self.Speed = Speed
        if Speed > 0:
            self.image = image.load("%s/Blocks/Moving_Block_Right.png" % ICON_DIR)
        else:
            self.image = image.load("%s/Blocks/Moving_Block_Left.png" % ICON_DIR)
        if x > EndX:
            self.Rotation = "Right"
        else:
            self.Rotation = "Left"
        self.Xvel = Speed
        self.BreakTime = 0
        self.k = False

    def update(self):
        if not self.k:
            self.k = True
        if self.Break(self.Time):
            self.Xvel = self.Speed

            if self.Rotation == "Right":
                if self.rect.x < self.End:
                    self.Xvel = self.Xvel
                    self.image = image.load("%s/Blocks/Moving_Block_Right.png" % ICON_DIR)
                else:
                    self.Xvel = 0
                    self.Rotation = "Left"
                    self.BreakTime = time.time()
                    self.image = image.load("%s/Blocks/Moving_Block_Left.png" % ICON_DIR)
            else:
                if self.rect.x > self.Start:
                    self.Xvel = - self.Xvel
                    self.image = image.load("%s/Blocks/Moving_Block_Left.png" % ICON_DIR)
                else:
                    self.Rotation = "Right"
                    self.Xvel = 0
                    self.BreakTime = time.time()
                    self.image = image.load("%s/Blocks/Moving_Block_Right.png" % ICON_DIR)
        else:
            self.Xvel = 0
        self.rect.x += self.Xvel

    def Break(self, Time):
        if time.time() - self.BreakTime >= Time:
            return True
        return False


class RespawnBlock(Platform):
    def __init__(self, x, y, ):
        Platform.__init__(self, x, y)
        self.active = True
        self.RespawnPointX = x
        self.RespawnPointY = y - 32
        self.image = image.load("%s/Blocks/Respawn_Point.png" % ICON_DIR)

    def Active(self):
        if self.active:
            self.image = image.load("%s/Blocks/Respawn_Point_Activated.png" % ICON_DIR)
            self.active = False


class End_Block(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in Animation_End_Block:
            boltAnim.append((anim, 100))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PlatformColor))
        self.boltAnim.blit(self.image, (0, 0))


class SpeedBoost_Block(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in Animation_SpeedBoost_Block:
            boltAnim.append((anim, 100))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PlatformColor))
        self.boltAnim.blit(self.image, (0, 0))


class JumpBoost_Block(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in Animation_JumpBoost_Block:
            boltAnim.append((anim, 100))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PlatformColor))
        self.boltAnim.blit(self.image, (0, 0))


class Brick_Unknown(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/Blocks/Ground.png" % ICON_DIR)


class Falling_Block(Platform):
    def __init__(self, x, y, EndX, EndY, Move_Speed_OX, Move_Speed_OY,
                 Timeout):  # ВАЖНОЕ УСЛОВИЕ ДЛЯ РАСПОЛОЖЕНИЯ falling, ЭТО ЧТОБЫ (КОНЕЧНАЯ КОРДИНАТА - НАЧАЛЬНАЯ КОРДИНАТА) ДЕЛИЛОСЬ БЕЗ ОСТАТКА НА ЕГО  СКОРОСТЬ (ЭТО ОТНОСИТСЯ КАК И К ОСИ "OX" ТАК И К ОСИ "ОY")
        Platform.__init__(self, x, y)
        self.BreakOut = Timeout
        self.EndX = EndX
        self.EndY = EndY
        self.StartX = x
        self.StartY = y
        self.Moving_Speed_X = Move_Speed_OX
        self.Moving_Speed_Y = Move_Speed_OY
        if x < EndX:
            if y > EndY:
                self.Rotation = 1
            else:
                self.Rotation = 4
        else:
            if y > EndY:
                self.Rotation = 2
            else:
                self.Rotation = 3
        self.Break = False
        boltAnim = []
        for anim in Animation_Moving_Death_Block:
            boltAnim.append((anim, 100))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PlatformColor))
        if self.Break:
            if time.time() - self.BreakTimer > self.BreakOut:
                self.Break_Timer = time.time()
                self.Break = False
                self.rect.x = self.StartX
                self.rect.y = self.StartY
        else:
            self.boltAnim.blit(self.image, (0, 0))
            if self.rect.x != self.EndX and self.rect.y != self.EndY:
                if self.Rotation == 1:
                    self.xvel = self.Moving_Speed_X
                    self.yvel = -self.Moving_Speed_Y
                elif self.Rotation == 2:
                    self.xvel = - self.Moving_Speed_X
                    self.yvel = - self.Moving_Speed_Y
                elif self.Rotation == 3:
                    self.xvel = -self.Moving_Speed_X
                    self.yvel = self.Moving_Speed_Y
                else:
                    self.xvel = self.Moving_Speed_X
                    self.yvel = self.Moving_Speed_Y
                if self.rect.x == self.EndX:
                    self.xvel = 0
                if self.rect.y == self.EndY:
                    self.yvel = 0
                self.rect.x += self.xvel
                self.rect.y += self.yvel
            else:
                self.Break = True
                self.rect.x = -32
                self.rect.y = -32
                self.BreakTimer = time.time()
