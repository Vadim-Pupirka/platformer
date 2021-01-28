from pygame import *
import pyganim
import blocks
import time
import monsters
import os

width = 32
height = 32
color = "#ff1337"
Gravity = 0.2
Animation_Delay = 2
Move_Boost = 2
Jump_Boost = 2.2
Animation_Boost_delay = 1
Speed_Boost = 3

ICON_DIR = os.path.dirname(__file__)
Animation_Right = [("%s/Player/player_move_right.png" % ICON_DIR)]

Animation_Left = [("%s/Player/player_move_left.png" % ICON_DIR)]

Animation_Jump_Left = [("%s/Player/player_move_left.png" % ICON_DIR, 1)]
Animation_Jump_Right = [("%s/Player/player_move_right.png" % ICON_DIR, 1)]
Animation_Stay = [("%s/Player/player_stand.png" % ICON_DIR, 1)]

Animation_Jump = [("%s/Player/player_jump.png" % ICON_DIR, 1)]


class Player(sprite.Sprite):
    def __init__(self, x, y, SpeedX, SpeedY):
        global Move_Speed, Jump_Power
        sprite.Sprite.__init__(self)
        self.FPS = 65
        self.winner = False
        self.inertia = 0.25
        Move_Speed = SpeedX
        Jump_Power = SpeedY
        self.current_time_Speed_Boost = 0
        self.current_time_TP = 0
        self.current_time_Jump_Boost = 0
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.Respawn_startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.Respawn_startY = y
        self.Speed_boost = False
        self.yvel = 0  # скорость вертикального перемещения
        self.onFloor = False  # На земле ли я?
        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, width, height)  # прямоугольный объект
        self.image.set_colorkey(Color(color))
        boltAnim = []
        boltAnimBoost = []
        for anim in Animation_Right:
            boltAnimBoost.append((anim, Animation_Boost_delay))
            boltAnim.append((anim, Animation_Delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightBoost = pyganim.PygAnimation(boltAnimBoost)
        self.boltAnimRightBoost.play()
        self.Jump_Boost = False
        #        Анимация движения влево
        boltAnim = []
        boltAnimBoost = []
        for anim in Animation_Left:
            boltAnimBoost.append((anim, Animation_Boost_delay))
            boltAnim.append((anim, Animation_Delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimLefttBoost = pyganim.PygAnimation(boltAnimBoost)
        self.boltAnimLefttBoost.play()

        self.boltAnimStay = pyganim.PygAnimation(Animation_Stay)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(Animation_Jump_Left)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(Animation_Jump_Right)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(Animation_Jump)
        self.boltAnimJump.play()
        self.activeRespawnBlockTime = 0
        self.winner = False
        self.winnerTime = 0
        self.On_Moving_Block = False

    def update(self, left, right, up, micro, Level_Width, platforms, Moving_Block_Speed):
        if up:
            if self.onFloor:
                self.yvel = -Jump_Power
                if self.Jump_Boost:
                    self.yvel -= Jump_Boost
                self.image.fill(Color(color))
                self.boltAnimJump.blit(self.image, (0, 0))
        if left:
            self.xvel = -Move_Speed
            self.image.fill(Color(color))
            if not up:
                self.boltAnimLeft.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            if self.Speed_boost:
                self.xvel -= Speed_Boost
                self.Efect_Speed_Boost(5)
                self.boltAnimLefttBoost.blit(self.image, (0, 0))
            if micro and time.time() - self.current_time_TP >= 7:
                if self.rect.x != 32:
                    self.current_time_TP = time.time()
                self.xvel -= 192
                self.ZAPAS = self.rect.x - 192
                if 32 > self.ZAPAS:
                    while self.ZAPAS < 32:
                        self.xvel += 32
                        self.ZAPAS += 32
        if right:
            self.xvel = Move_Speed
            self.image.fill(Color(color))
            if not up and self.Speed_boost:
                self.boltAnimRightBoost.blit(self.image, (0, 0))
            if not up:
                self.boltAnimRight.blit(self.image, (0, 0))
            if self.Speed_boost:
                self.xvel += Speed_Boost
            if micro and time.time() - self.current_time_TP >= 7:
                if self.rect.x != Level_Width - 96:
                    self.current_time_TP = time.time()
                self.xvel += 192
                self.ZAPAS = self.rect.x + 192
                if Level_Width - 96 < self.ZAPAS:
                    while self.ZAPAS > Level_Width - 96:
                        self.xvel -= 32
                        self.ZAPAS -= 32
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
        if not (left or right):
            if abs(self.xvel) - 1 < 0:
                self.xvel = 0
            if self.xvel > 0:
                self.xvel -= self.inertia
            elif self.xvel < 0:
                self.xvel += self.inertia
            if not up:
                self.image.fill(Color(color))
                self.boltAnimStay.blit(self.image, (0, 0))

            if self.On_Moving_Block:
                self.xvel = self.Moving_Block_xvel
        if not self.onFloor:
            self.yvel += Gravity
        self.onFloor = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.winner = False
        self.collide(self.xvel, 0, platforms)
        self.Efect_Speed_Boost(5)
        self.Efect_Jump_Boost(5)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, blocks.Moving_Block):
                    self.Moving_Block_xvel = p.Xvel
                    self.On_Moving_Block = True
                else:
                    self.On_Moving_Block = False
                if isinstance(p, blocks.SpeedBoost_Block):
                    self.Speed_boost = True
                    self.current_time_Speed_Boost = time.time()
                if isinstance(p, blocks.JumpBoost_Block):
                    self.Jump_Boost = True
                    self.current_time_Jump_Boost = time.time()
                if isinstance(p, blocks.RespawnBlock):
                    if self.rect.x > self.Respawn_startX + 32:
                        self.Respawn_startX = p.RespawnPointX
                        self.Respawn_startY = p.RespawnPointY
                    p.Active()
                if isinstance(p, blocks.DieBlock) \
                        or isinstance(p, monsters.Monster) \
                        or isinstance(p, blocks.Brick_Unknown) \
                        or isinstance(p, monsters.Agressive_Monster) \
                        or isinstance(p, blocks.Falling_Block):
                    self.die()
                elif isinstance(p, blocks.End_Block):
                    if time.time() - self.winnerTime > 10:
                        self.winner = True
                        self.winnerTime = time.time()

                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onFloor = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

    def die(self):
        time.sleep(0.5)
        self.teleporting(self.Respawn_startX, self.Respawn_startY)
        self.Efect_Speed_Boost(0)
        self.current_time_TP = time.time() - 7
        self.Efect_Jump_Boost(0)
        self.yvel = 0
        self.xvel = 0

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def Efect_Speed_Boost(self, Time):
        if time.time() - self.current_time_Speed_Boost >= Time:
            self.Speed_boost = False

    def Efect_Jump_Boost(self, Time):
        if time.time() - self.current_time_Jump_Boost >= Time:
            self.Jump_Boost = False
