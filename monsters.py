from pygame import *
import pyganim
import os

Monster_Width = 32
Monster_Height = 32
Monster_Color = "#2110FF"
Icon_dir = os.path.dirname(__file__)

Animation_Monster = [("%s/Monster/Monster1.png" % Icon_dir)]


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxWayOX, maxWayOY):
        sprite.Sprite.__init__(self)
        self.image = Surface((Monster_Width, Monster_Height))
        self.image.fill(Color(Monster_Color))
        self.rect = Rect(x, y, Monster_Width, Monster_Height)
        self.image.set_colorkey(Color(Monster_Color))

        self.StartX = x
        self.StartY = y
        self.maxWay = maxWayOX
        self.maxUp = maxWayOY

        self.xvel = left

        self.yvel = up

        boltAnim = []

        for anim in Animation_Monster:
            boltAnim.append((anim, 250))
        self.boltAnim = pyganim.PygAnimation(boltAnim)

        self.boltAnim.play()

    def update(self, platforms):

        self.image.fill(Color(Monster_Color))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.StartX - self.rect.x) > self.maxWay):
            self.xvel = -self.xvel
        if (abs(self.StartY - self.rect.y) > self.maxUp):
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = -self.xvel
                self.yvel = -self.yvel


class Agressive_Monster(sprite.Sprite):
    def __init__(self, x, y, Secure_x, Secure_Y, move_speed_x, move_speed_y):
        sprite.Sprite.__init__(self)
        Animation_Monster_Right = [("%s/Monster/Agressive/Agressive_Right.png" % Icon_dir)]
        self.image = Surface((Monster_Width, Monster_Height))
        self.image.fill(Color(Monster_Color))
        self.rect = Rect(x, y, Monster_Width, Monster_Height)
        self.image.set_colorkey(Color(Monster_Color))
        self.Triggered = False
        self.StartX = x
        self.StartY = y
        self.maxWay = Secure_x
        self.maxUp = Secure_Y

        self.xvel = move_speed_x
        self.yvel = 0
        self.move_speed_y = move_speed_y
        boltAnim = []
        self.move_speed_x = move_speed_x
        for anim in Animation_Monster_Right:
            boltAnim.append((anim, 250))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        Animation_Monster_Left = [("%s/Monster/Agressive/Agressive_Left.png" % Icon_dir)]
        boltAnim = []
        for anim in Animation_Monster_Left:
            boltAnim.append((anim, 250))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        Animation_Monster_Left_Triggered = [("%s/Monster/Agressive/Agressive_Left_Trigger_1.png" % Icon_dir),
                                            ("%s/Monster/Agressive/Agressive_Left_Trigger_2.png" % Icon_dir)]
        boltAnim = []
        for anim in Animation_Monster_Left_Triggered:
            boltAnim.append((anim, 250))
        self.boltAnimLeftTrigger = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeftTrigger.play()

        Animation_Monster_Right_Triggered = [("%s/Monster/Agressive/Agressive_Right_Trigger_1.png" % Icon_dir),
                                             ("%s/Monster/Agressive/Agressive_Right_Trigger_2.png" % Icon_dir)]
        boltAnim = []
        for anim in Animation_Monster_Right_Triggered:
            boltAnim.append((anim, 250))
        self.boltAnimRightTrigger = pyganim.PygAnimation(boltAnim)
        self.boltAnimRightTrigger.play()

        Animation_Monster_Up_Triggered = [("%s/Monster/Agressive/Agressive_Up_Trigger_1.png" % Icon_dir),
                                          ("%s/Monster/Agressive/Agressive_Up_Trigger_2.png" % Icon_dir)]
        boltAnim = []
        for anim in Animation_Monster_Up_Triggered:
            boltAnim.append((anim, 250))
        self.boltAnimUpTrigger = pyganim.PygAnimation(boltAnim)
        self.boltAnimUpTrigger.play()

        Animation_Monster_Down_Triggered = [("%s/Monster/Agressive/Agressive_Down_Trigger_1.png" % Icon_dir),
                                            ("%s/Monster/Agressive/Agressive_Down_Trigger_2.png" % Icon_dir)]
        boltAnim = []
        for anim in Animation_Monster_Down_Triggered:
            boltAnim.append((anim, 250))
        self.boltAnimDownTrigger = pyganim.PygAnimation(boltAnim)
        self.boltAnimDownTrigger.play()

    def update(self, platforms, playerX, playerY):
        self.image.fill(Color(Monster_Color))
        if self.xvel == 0:
            self.xvel = self.move_speed_x  # если нулевая скорость, то её надо дать

        if self.xvel > 0 and not self.Triggered:
            self.boltAnimRight.blit(self.image, (0, 0))  # движение вправо
        elif not self.Triggered:
            self.boltAnimLeft.blit(self.image, (0, 0))  # движение влево

        if playerX >= self.StartX and playerX < self.StartX + self.maxWay and playerY <= self.StartY and playerY >= abs(
                self.StartY - self.maxUp):  # проверка на наличие игрока в защищаемой зоне
            self.Triggered = True
        else:
            self.Triggered = False

        if self.Triggered:
            if playerY == self.rect.y:  # если на одинаковой высоте, то двигаться по оси OY не надо
                self.yvel = 0

            else:

                if playerY > self.rect.y:
                    self.yvel = self.move_speed_y
                else:
                    self.yvel = -self.move_speed_y
            if playerX == self.rect.x:
                self.xvel = 0
            else:

                if playerX > self.rect.x:
                    self.xvel = abs(self.xvel)
                    self.boltAnimRightTrigger.blit(self.image, (0, 0))
                else:
                    self.xvel = -(abs(self.xvel))
                    self.boltAnimLeftTrigger.blit(self.image, (0, 0))
        else:
            if self.rect.y < self.StartY:
                self.yvel = self.move_speed_y
            else:
                self.yvel = 0
        if abs(self.rect.x - playerX) <= 16 and self.Triggered:
            if playerY < self.rect.y:
                self.boltAnimUpTrigger.blit(self.image, (0, 0))
            else:
                self.boltAnimDownTrigger.blit(self.image, (0, 0))
            if abs(self.rect.x - playerX) <= 5:
                self.xvel = 0
        if abs(self.rect.y - playerY) <= 5 and self.Triggered:
            self.yvel = 0
        if (self.rect.x - self.StartX > self.maxWay) and not self.Triggered:
            self.xvel = -self.xvel
        if self.rect.x < self.StartX:
            self.xvel = -self.xvel
        self.rect.y += self.yvel
        self.rect.x += self.xvel
