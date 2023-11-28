import pygame
import random
import math
import keyboard
from collections import deque
import sys
from os import path
from pygame.locals import *
from database import Database
import time
import sqlite3

width, height = 900, 750
fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 750))

black = (0,0,0)
white = (255,255,255)
red  = (200,0,0)
brightred = (255,0,0)
green = (0,200,0)
brightgreen = (0,255,0)
blue = (0,0,200)
brightblue = (0,0,255)
yellow = (200,200,0)
brightyellow = (255,255,0)
purple = (200,0,200)
brightpurple = (255,0,255)
orange = (255,128,0)
BLUE = (0, 0, 255)
RED  = (201,0,0)

img_dir = path.join(path.dirname(__file__),"img")
snd_dir = path.join(path.dirname(__file__),"snd")

#******Setup******
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space War")
icon = pygame.image.load(path.join(img_dir, "icon.png"))
icon.set_colorkey(black)
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

global font_path, font_size, font
font_path = path.join(img_dir, "NanumGothic.ttf")
font_size = 36
font = pygame.font.Font(font_path, font_size)

#******load_graphic********
background = pygame.image.load(path.join(img_dir,"background.jpg")).convert()
background1 = pygame.transform.scale(background,(900,750))
background2 = pygame.transform.scale(background,(1280,900))
infobackground = pygame.image.load(path.join(img_dir,"infobackground.jpg")).convert()
infobackground1 = pygame.transform.scale(infobackground,(900,750))
infobackground2 = pygame.transform.scale(infobackground,(1280,900))
gameoverbackground = pygame.image.load(path.join(img_dir,"gameover.jpg")).convert()
gameoverbackground1 = pygame.transform.scale(gameoverbackground,(900,750))
gameoverbackground2 = pygame.transform.scale(gameoverbackground,(1280,900))
player1img = pygame.image.load(path.join(img_dir,"player1.png")).convert()
player2img = pygame.image.load(path.join(img_dir,"player2.png")).convert()
liveup1img = pygame.transform.scale(player1img,(50,40))
liveup2img = pygame.transform.scale(player2img,(50,40))
meteo_list = ["m1.png","m2.png","m3.png","m4.png","m5.png","m6.png","m7.png"]
mybulletimg = pygame.image.load(path.join(img_dir,"mylaser.png")).convert()
mybulletimg_2 = pygame.image.load(path.join(img_dir,"mylaser2.png")).convert()
mybulletimg_3 = pygame.image.load(path.join(img_dir,"mylaser3.png")).convert()
mybulletimg_4 = pygame.image.load(path.join(img_dir,"mylaser4.png")).convert()
mybulletimg_5 = pygame.image.load(path.join(img_dir,"mylaser5.png")).convert()
mybulletimg_6 = pygame.image.load(path.join(img_dir,"mylaser6.png")).convert()
bulletupimg = pygame.image.load(path.join(img_dir,"bulletup.png")).convert()
ultbulletupimg = pygame.image.load(path.join(img_dir,"ultbulletup.png")).convert()
speedupimg = pygame.image.load(path.join(img_dir,"speedup.png")).convert()
healthupimg = pygame.image.load(path.join(img_dir,"healthup.png")).convert()
enemy1img = pygame.image.load(path.join(img_dir,"enemy1.png")).convert()
enemy2img = pygame.image.load(path.join(img_dir,"enemy2.png")).convert()
roundbulletimg = pygame.image.load(path.join(img_dir,"roundbullet.png")).convert()
boss1img = pygame.image.load(path.join(img_dir,"boss1.png")).convert()
laser1img = pygame.image.load(path.join(img_dir,"laser1.png")).convert()
enemy3img = pygame.image.load(path.join(img_dir,"enemy3.png")).convert()
dartimg = pygame.image.load(path.join(img_dir,"dart.png")).convert()
boss2img = pygame.image.load(path.join(img_dir,"boss2.png")).convert()
boss3img = pygame.image.load(path.join(img_dir,"boss3.png")).convert()
boss4img = pygame.image.load(path.join(img_dir,"boss4.png")).convert()
boss5img = pygame.image.load(path.join(img_dir,"boss5.png")).convert()
ximg = pygame.image.load(path.join(img_dir,"x.png")).convert()
shield1img = pygame.image.load(path.join(img_dir,"shield1.png")).convert()
shield2img = pygame.image.load(path.join(img_dir,"shield2.png")).convert()
shieldupimg = pygame.image.load(path.join(img_dir,"shieldup.png")).convert()
shield_symbolimg = pygame.image.load(path.join(img_dir,"shieldsymbol.png")).convert()
missileimg = pygame.image.load(path.join(img_dir,"missile.png")).convert()
missile_symbolimg = pygame.image.load(path.join(img_dir,"missilesymbol.png")).convert()
missileupimg = pygame.image.load(path.join(img_dir,"missileup.png")).convert()
upimg = pygame.image.load(path.join(img_dir,"up.png")).convert()
upimg = pygame.transform.scale(upimg,(40,40))
downimg = pygame.image.load(path.join(img_dir,"down.png")).convert()
downimg = pygame.transform.scale(downimg,(40,40))
leftimg = pygame.image.load(path.join(img_dir,"left.png")).convert()
leftimg = pygame.transform.scale(leftimg,(40,40))
rightimg = pygame.image.load(path.join(img_dir,"right.png")).convert()
rightimg = pygame.transform.scale(rightimg,(40,40))
spaceimg = pygame.image.load(path.join(img_dir,"space.png")).convert()
spaceimg = pygame.transform.scale(spaceimg,(80,40))

explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['middle'] = []
explosion_anim['small'] = []
explosion_anim['death'] = []
for i in range(9):
    fname = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir,fname)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img,(100,100))
    explosion_anim['large'].append(img_lg)
    img_sm = pygame.transform.scale(img,(50,50))
    explosion_anim['small'].append(img_sm)
    fname = "middleExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir,fname)).convert()
    img.set_colorkey(black)
    img_mi = pygame.transform.scale(img,(150,150))
    explosion_anim['middle'].append(img_mi)

    fname = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir,fname)).convert()
    img.set_colorkey(black)
    explosion_anim['death'].append(img)

#******load_sound********
bulletup_sound = pygame.mixer.Sound(path.join(snd_dir,'bulletup.wav'))
shieldup_sound = pygame.mixer.Sound(path.join(snd_dir,'shieldup.wav'))
healthup_sound = pygame.mixer.Sound(path.join(snd_dir,'healthup.wav'))
liveup_sound = pygame.mixer.Sound(path.join(snd_dir,'liveup.wav'))
missileup_sound = pygame.mixer.Sound(path.join(snd_dir,'missileup.wav'))
speedup_sound = pygame.mixer.Sound(path.join(snd_dir,'speedup.wav'))
explodesm_sound = pygame.mixer.Sound(path.join(snd_dir,'explodesm.wav'))
explodebg_sound = pygame.mixer.Sound(path.join(snd_dir,'explodebg.wav'))
explodedeath_sound = pygame.mixer.Sound(path.join(snd_dir,'explodedeath.wav'))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'shoot.wav'))
shoot_sound2 = pygame.mixer.Sound(path.join(snd_dir,'shoot2.wav'))
missile_sound = pygame.mixer.Sound(path.join(snd_dir,'missile.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir,'shield.wav'))

def quitgame():
    sys.exit()
paused = False
pause_start_time = None  # 퍼즈가 시작된 시간        
def pause():
    global paused, start_time, elapsed_pause_time
    paused = True
    pause_start_time = pygame.time.get_ticks()  # 일시정지 시작 시간 기록
    font = pygame.font.Font(None, 36)
    text = font.render("PAUSED", True, (255, 255, 255))
    text_rect = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, text_rect)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    quitgame()
                elif event.key == pygame.K_p:
                    paused = False

    # 일시정지가 해제되면 경과된 일시정지 시간을 저장
    pause_end_time = pygame.time.get_ticks()
    elapsed_pause_time += pause_end_time - pause_start_time

def newmeteorite():
    m = Meteorite()
    meteorite_sprites.add(m)
    all_sprites.add(m)
    
def bullets1(x,y,radian):
    bullet = Mybullet(x, y, radian)
    bullet_sprites.add(bullet)
    all_sprites.add(bullet)

def bullets2(x,y,radian):
    bullet = bullet2(x, y, radian)
    bullet_sprites_2.add(bullet)
    all_sprites.add(bullet)

def bullets3(x,y,radian):
    bullet = bullet3(x, y, radian)
    bullet_sprites_3.add(bullet)
    all_sprites.add(bullet)

def bullets4(x,y,radian):
    bullet = bullet4(x, y, radian)
    bullet_sprites_4.add(bullet)
    all_sprites.add(bullet)    
    
def bullets5(x,y,radian):
    bullet = bullet5(x, y, radian)
    bullet_sprites_5.add(bullet)
    all_sprites.add(bullet)

def bullets6(x,y,radian):
    bullet = bullet6(x, y, radian)
    bullet_sprites_6.add(bullet)
    all_sprites.add(bullet)

def newbulletup():
    bulletup = Bulletup()
    bulletup_sprites.add(bulletup)
    all_sprites.add(bulletup)
    return bulletup

def newultbulletup():
    ultbulletup = Ultbulletup()
    ultbulletup_sprites.add(ultbulletup)
    all_sprites.add(ultbulletup)
    return ultbulletup

def newspeedup():
    speedup = Speedup()
    speedup_sprites.add(speedup)
    all_sprites.add(speedup)
    return speedup

def newhealthup():
    healthup = Healthup()
    healthup_sprites.add(healthup)
    all_sprites.add(healthup)

def newliveup():
    liveup = Liveup()
    liveup_sprites.add(liveup)
    all_sprites.add(liveup)

def newliveup1():
    liveup2 = Liveup()
    liveup_sprites.add(liveup2)
    all_sprites.add(liveup2)

def newshieldup():
    shieldup = Shieldup()
    shieldup_sprites.add(shieldup)
    all_sprites.add(shieldup)
    return shieldup

def newmissileup():
    missileup = Missileup()
    missileup_sprites.add(missileup)
    all_sprites.add(missileup)

def newenemy1():
    enemy1 = Enemy1()
    enemy1_sprites.add(enemy1)
    all_sprites.add(enemy1)
    return enemy1
def newenemy2():
    enemy2 = Enemy2()
    enemy2_sprites.add(enemy2)
    all_sprites.add(enemy2)
    return enemy2
def newenemy3():
    enemy3 = Enemy3()
    enemy3_sprites.add(enemy3)
    all_sprites.add(enemy3)
    return enemy3

def newboss1():
    boss1 = Boss1()
    boss1_sprites.add(boss1)
    all_sprites.add(boss1)
    return boss1
def newboss2():
    boss2 = Boss2()
    boss2_sprites.add(boss2)
    all_sprites.add(boss2)
    return boss2
def newboss3():
    boss3 = Boss3()
    boss3_sprites.add(boss3)
    all_sprites.add(boss3)
    return boss3
def newboss4():
    boss4 = Boss4()
    boss4_sprites.add(boss4)
    all_sprites.add(boss4)
    return boss4
def newboss5():
    boss5 = Boss5()
    boss5_sprites.add(boss5)
    all_sprites.add(boss5)
    return boss5

def new_roundbullet(x,y,angle):
    roundbullet = Roundbullet(x,y,angle)
    roundbullet_sprites.add(roundbullet)
    all_sprites.add(roundbullet)

def new_laser1(x,y,angle):
    laser1 = Laser1(x,y,angle)
    laser1_sprites.add(laser1)
    all_sprites.add(laser1)

def new_dart(x,y,angle):
    dart = Dart(x,y,angle)
    dart_sprites.add(dart)
    all_sprites.add(dart)

def new_x(x,y,angle):
    x = X(x,y,angle)
    x_sprites.add(x)
    all_sprites.add(x)

def health(ph,x,y):
    if ph <= 0:
        ph = 0
    container = pygame.Rect(x,y,150,20)
    blood = pygame.Rect(x+1,y+1,150*ph/100-2,20-2)
    pygame.draw.rect(screen,white,container,1)
    pygame.draw.rect(screen,red,blood)

def newshield1(center):
    shield = Shield(center)
    shield_sprites.add(shield)
    all_sprites.add(shield)

def newshield2(center):
    shield2 = Shield2(center)
    shield_sprites.add(shield2)
    all_sprites.add(shield2)

def newmissile(centerx,centery):
    missile = Missile(centerx,centery)
    missile_sprites.add(missile)
    all_sprites.add(missile)

def drawscore(score,x,y):
    label("Score: ",x,y,25,purple)
    label(str(score),x+80,y,25,orange)

def drawsec(elapsed_seconds,x,y):
    label("Sec:",x,y,25,red)
    label(str(elapsed_seconds),x+60,y,25,orange)
    
def drawlive1(live,x,y):
    liveimg = pygame.transform.scale(player1img,(42,30))
    liveimg.set_colorkey(black)
    screen.blit(liveimg,(x,y))
    label("X "+str(live),x+65,y+5,30,orange)
    
def drawlive2(live,x,y):
    liveimg1 = pygame.transform.scale(player2img,(42,30))
    liveimg1.set_colorkey(black)
    screen.blit(liveimg1,(x,y))
    label("X "+str(live),x+65,y+5,30,orange)    

def drawshield(num_shield,x,y):
    shield_image = pygame.transform.scale(shield_symbolimg,(50,50))
    shield_image.set_colorkey(black)
    screen.blit(shield_image,(x,y))
    label("X "+str(num_shield),x+65,y+5,30,orange)
    
def drawmissile(num_missile,x,y):
    missile_image = pygame.transform.scale(missile_symbolimg,(30,50))
    missile_image = pygame.transform.rotate(missile_image,45)
    missile_image.set_colorkey(black)
    screen.blit(missile_image,(x,y))
    label("X "+str(num_missile),x+65,y+5,30,orange)

def label(msg,x,y,size,color):
    font = pygame.font.Font(font_path,size)
    text = font.render(msg,True,color)
    screen.blit(text,(x,y))

def Button(msg,x,y,width,height,i_color,a_color,command=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen,a_color,(x,y,width,height))
        if click[0] == 1 and command != None:
            command()
    else:
        pygame.draw.rect(screen,i_color,(x,y,width,height))
    buttontext = pygame.font.Font(font_path,24)
    buttonmsg = buttontext.render(msg,True,black)
    buttonmsgrect = buttonmsg.get_rect()
    buttonmsgrect.center = ((x+width/2),(y+height/2))
    screen.blit(buttonmsg,buttonmsgrect)

#*********Class*********
class Player1(pygame.sprite.Sprite):
    global Player1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1img, (70, 50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2-40
        self.rect.bottom = height - 20
        self.radius = 27
        self.speedx = 0
        self.speedy = 0
        self.lastshoot = pygame.time.get_ticks()
        self.score = 0
        self.ph = 100
        self.live = 3
        self.shootdelay = 400
        self.bulletpower = 1
        self.bulletpower_delay = 20000
        self.bulletpower_time = pygame.time.get_ticks()
        self.bulletpower_now = pygame.time.get_ticks()
        self.speedup_delay = 20000
        self.speedup_time = pygame.time.get_ticks()
        self.shield = 3
        self.missile = 3

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastshoot > self.shootdelay:
            self.lastshoot = now
            shoot_sound.play()
            if self.bulletpower == 1:
                bullets1(self.rect.x+29,self.rect.y,math.pi/2)
            if self.bulletpower == 2:
                bullets2(self.rect.x-5,self.rect.y,math.pi/2)
                bullets2(self.rect.x+70-8,self.rect.y,math.pi/2)
            if self.bulletpower == 3:
                bullets3(self.rect.x+29,self.rect.y,math.pi/2)
                bullets3(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets3(self.rect.x + 70-6, self.rect.y, math.pi / 2)
            if self.bulletpower == 4:
                bullets4(self.rect.x+29,self.rect.y,math.pi/2)
                bullets4(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets4(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                bullets4(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                bullets4(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))
            if self.bulletpower == 5:
                bullets5(self.rect.x+29,self.rect.y,math.pi/2)
                bullets5(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets5(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                bullets5(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                bullets5(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))
                bullets5(self.rect.x-5-20-10,self.rect.y-15,math.pi*1/4)
                bullets5(self.rect.x+70-8+20+10,self.rect.y-15,math.pi*(1-1/4))
            if self.bulletpower == 6:
                bullets6(self.rect.x+29,self.rect.y,math.pi/2)
                bullets6(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets6(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                bullets6(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                bullets6(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))

                bullets6(self.rect.x-5-20-10,self.rect.y-15,math.pi*1/4)
                bullets6(self.rect.x+70-8+20+10,self.rect.y-15,math.pi*(1-1/4))

                bullets6(self.rect.x-5-20-15,self.rect.y-20,math.pi*1/8)
                bullets6(self.rect.x+70-8+20+15,self.rect.y-20,math.pi*(1-1/8))

            bullet_angles = [i * (math.pi / 11) for i in range(12)]
            for angle in bullet_angles:
                if self.bulletpower >= 6:
                    self.bulletpower = 6

    def update(self):
        self.speedx = 0
        self.speedy = 0
        # set for bullet power
        self.bulletpower_now = pygame.time.get_ticks()
        if self.bulletpower_now - self.bulletpower_time > self.bulletpower_delay:
            self.bulletpower_time = pygame.time.get_ticks()
            self.bulletpower -= 1
        if self.bulletpower < 1:
            self.bulletpower = 1
        # set for speedup
        self.speedup_now = pygame.time.get_ticks()
        if self.speedup_now - self.speedup_time > self.speedup_delay:
            self.speedup_time = pygame.time.get_ticks()
            self.shootdelay += 50
        if self.shootdelay < 100:
            self.shootdelay = 100
        if self.shootdelay > 400:
            self.shootdelay = 400
        # player1 ph and live
        if self.ph > 100:
            self.ph = 100
        if self.ph < 1:
            expl = Explosion(self.rect.center, 'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            self.live -= 1
            self.ph = 100
            self.rect.centerx = width / 2
            self.rect.bottom = height - 20
        # player1 key event
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
        if keystate[pygame.K_LEFT]:
            self.speedx = -6
        if keystate[pygame.K_UP]:
            self.speedy = -6
        if keystate[pygame.K_DOWN]:
            self.speedy = 6
        #if keystate[pygame.K_SPACE]:
            #self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player2img, (70, 50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2+40
        self.rect.bottom = height - 20
        self.radius = 27
        self.speedx = 0
        self.speedy = 0
        self.lastshoot = pygame.time.get_ticks()
        self.score = 0
        self.ph = 100
        self.live = 3
        self.shootdelay = 400
        self.bulletpower = 1
        self.bulletpower_delay = 20000
        self.bulletpower_time = pygame.time.get_ticks()
        self.bulletpower_now = pygame.time.get_ticks()
        self.speedup_delay = 20000
        self.speedup_time = pygame.time.get_ticks()
        self.shield = 3
        self.missile = 3

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastshoot > self.shootdelay:
            self.lastshoot = now
            shoot_sound.play()
            if self.bulletpower == 1:
                bullets1(self.rect.x+29,self.rect.y,math.pi/2)
            if self.bulletpower == 2:
                bullets2(self.rect.x-5,self.rect.y,math.pi/2)
                bullets2(self.rect.x+70-8,self.rect.y,math.pi/2)
            if self.bulletpower == 3:
                bullets3(self.rect.x+29,self.rect.y,math.pi/2)
                bullets3(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets3(self.rect.x + 70-6, self.rect.y, math.pi / 2)
            if self.bulletpower == 4:
                bullets4(self.rect.x+29,self.rect.y,math.pi/2)
                bullets4(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets4(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                bullets4(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                bullets4(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))
            if self.bulletpower == 5:
                bullets5(self.rect.x+29,self.rect.y,math.pi/2)
                bullets5(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets5(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                bullets5(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                bullets5(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))
                bullets5(self.rect.x-5-20-10,self.rect.y-15,math.pi*1/4)
                bullets5(self.rect.x+70-8+20+10,self.rect.y-15,math.pi*(1-1/4))
            if self.bulletpower == 6:
                bullets6(self.rect.x+29,self.rect.y,math.pi/2)
                bullets6(self.rect.x-7, self.rect.y, math.pi / 2)
                bullets6(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                bullets6(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                bullets6(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))

                bullets6(self.rect.x-5-20-10,self.rect.y-15,math.pi*1/4)
                bullets6(self.rect.x+70-8+20+10,self.rect.y-15,math.pi*(1-1/4))

                bullets6(self.rect.x-5-20-15,self.rect.y-20,math.pi*1/8)
                bullets6(self.rect.x+70-8+20+15,self.rect.y-20,math.pi*(1-1/8))


            bullet_angles = [i * (math.pi / 11) for i in range(12)]
            for angle in bullet_angles:
                if self.bulletpower >= 6:
                    self.bulletpower = 6

    def update(self):
        self.speedx = 0
        self.speedy = 0
        # set for bullet power
        self.bulletpower_now = pygame.time.get_ticks()
        if self.bulletpower_now - self.bulletpower_time > self.bulletpower_delay:
            self.bulletpower_time = pygame.time.get_ticks()
            self.bulletpower -= 1
        if self.bulletpower < 1:
            self.bulletpower = 1
        # set for speedup
        self.speedup_now = pygame.time.get_ticks()
        if self.speedup_now - self.speedup_time > self.speedup_delay:
            self.speedup_time = pygame.time.get_ticks()
            self.shootdelay += 50
        if self.shootdelay < 100:
            self.shootdelay = 100
        if self.shootdelay > 400:
            self.shootdelay = 400
        # player2 ph and live
        if self.ph > 100:
            self.ph = 100
        if self.ph < 1:
            expl = Explosion(self.rect.center, 'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            self.live -= 1
            self.ph = 100
            self.rect.centerx = width / 2
            self.rect.bottom = height - 20
        # player2 key event
        keystate1 = pygame.key.get_pressed()
        if keystate1[pygame.K_g]:
            self.speedx = 6
        if keystate1[pygame.K_d]:
            self.speedx = -6
        if keystate1[pygame.K_r]:
            self.speedy = -6
        if keystate1[pygame.K_f]:
            self.speedy = 6
        if keystate1[pygame.K_LCTRL]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.meteochoice = random.choice(meteo_list)
        self.meteoriteimg_orig = pygame.image.load(path.join(img_dir, self.meteochoice)).convert()
        self.meteoriteimg_orig.set_colorkey(black)
        self.meteoriteimg = self.meteoriteimg_orig.copy()
        self.image = self.meteoriteimg
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width)
        self.rect.y = -500
        self.radius = int(self.rect.width * 0.85 / 2)
        self.speedx = random.randrange(-10,10)
        self.speedy = random.randrange(3,13)
        self.rot = 0
        self.rotspeed = random.randrange(-15,15)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot+self.rotspeed)%360
            newimage = pygame.transform.rotate(self.meteoriteimg_orig,self.rot)
            old_center = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.right < 0) or (self.rect.left > width) or (self.rect.top > height):
            self.rect.x = random.randrange(0, width)
            self.rect.y = -500
            self.speedx = random.randrange(-10, 10)
            self.speedy = random.randrange(3, 13)

class Mybullet(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -15
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class bullet2(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg_2
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -20
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class bullet3(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg_3
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -20
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class bullet4(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg_4
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -20
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class bullet5(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg_5
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -20
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class bullet6(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg_6
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -20
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,mode):
        pygame.sprite.Sprite.__init__(self)
        self.mode = mode
        self.image = explosion_anim[self.mode][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.update_rate = 90

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.update_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.mode]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.mode][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Bulletup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Ultbulletup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ultbulletupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500 
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Speedup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = speedupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Healthup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = healthupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Liveup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1img,(35,25))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = pygame.transform.scale(enemy1img,(90,70))
        self.image_org.set_colorkey(black)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -random.randrange(300,1300)
        self.radius = int(self.rect.width * 0.85 / 2)
        self.speedy = 3
        self.rotate_time = pygame.time.get_ticks()
        self.angle = 0
        self.shoot_time = pygame.time.get_ticks()
        self.shoot_delay = 700
        self.ph = 70
        self.fullph = 70
        self.drawph = False
        

    def rotate(self,angle):
        now = pygame.time.get_ticks()
        if now - self.rotate_time > 50:
            self.rotate_time = pygame.time.get_ticks()
            newimage = pygame.transform.rotate(self.image_org,angle)
            oldcenter = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = oldcenter

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shoot_delay and self.rect.y > 0:
            self.shoot_time = pygame.time.get_ticks()
            new_roundbullet(self.rect.centerx,self.rect.centery,self.angle)

    def enemy_health(self,ph, fullph, x, y):
        container = pygame.Rect(x, y, 150, 20)
        blood = pygame.Rect(x + 1, y + 1, 150 * ph / fullph - 2, 20 - 2)
        pygame.draw.rect(screen, white, container, 1)
        pygame.draw.rect(screen, purple, blood)

    def update(self):
        global cooperative_mode
        if cooperative_mode:
            dist_to_player1 = math.sqrt((player1.rect.x - self.rect.x) ** 2 + (player1.rect.y - self.rect.y) ** 2)
            dist_to_player2 = math.sqrt((player2.rect.x - self.rect.x) ** 2 + (player2.rect.y - self.rect.y) ** 2)

            # Choose the closest player1
            if dist_to_player1 < dist_to_player2:
                target_player = player1
            else:
                target_player = player2

            try:
                # Calculate angle and rotate towards the target player1
                self.angle = math.degrees(math.atan((target_player.rect.x - self.rect.x) / (target_player.rect.y - self.rect.y)))
            except ZeroDivisionError:
                self.angle = 0

            if target_player.rect.y < self.rect.y:
                self.angle += 180

            self.rotate(self.angle)
            self.shoot()
            self.rect.y += self.speedy
            if self.rect.y > height:
                self.drawph = False
                self.kill()
            if self.ph <= 0:
                self.drawph = False
                expl = Explosion(self.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                self.kill()
        
        else:
            try:
                # Calculate angle and rotate towards the target player1
                self.angle = math.degrees(math.atan((player1.rect.x - self.rect.x) / (player1.rect.y - self.rect.y)))
            except ZeroDivisionError:
                self.angle = 0
            
            if player1.rect.y < self.rect.y:
                self.angle += 180

            self.rotate(self.angle)
            self.shoot()
            self.rect.y += self.speedy
            if self.rect.y > height:
                self.drawph = False
                self.kill()
            if self.ph <= 0:
                self.drawph = False
                expl = Explosion(self.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                self.kill()
                

class Enemy2(Enemy1):
    def __init__(self):
        Enemy1.__init__(self)
        self.image_org = pygame.transform.scale(enemy2img,(90,70))
        self.image_org.set_colorkey(black)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -random.randrange(700,2800)
        self.radius = int(self.rect.width * 0.85 / 2)
        self.shoot_delay = 500
        self.ph = 120
        self.fullph = 120

class Roundbullet(pygame.sprite.Sprite):
    def __init__(self,x,y,degree):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(roundbulletimg,(30,30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 7
        self.speedx = self.speed * math.sin(math.radians(degree))
        self.speedy = self.speed * math.cos(math.radians(degree))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.top > height) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class Boss1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss1img
        self.image.set_colorkey((black))
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = -3500
        self.speedy = 2
        self.speedx = 2
        self.shoot_mode = 1
        self.shootdelay = 700
        self.shoot_time = pygame.time.get_ticks()
        self.shiftmode_delay = 10000
        self.shift_time = pygame.time.get_ticks()
        self.ph = 2000
        self.fullph = 2000
        self.drawph = False

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shootdelay:
            self.shoot_time = now
            if self.shoot_mode == 1:
                new_laser1(self.rect.left+20, self.rect.centery+60, -math.pi/2)
                new_laser1(self.rect.right-20, self.rect.centery+60, -math.pi/2)
            if self.shoot_mode == 2:
                new_roundbullet(self.rect.left+20, self.rect.centery+60, -30)
                new_roundbullet(self.rect.right-20, self.rect.centery+60, 30)
                new_roundbullet(self.rect.centerx,self.rect.bottom,0)
        if now - self.shift_time > self.shiftmode_delay:
            self.shift_time = now
            self.shoot_mode += 1
            if self.shoot_mode > 2:
                self.shoot_mode = 1

    def enemy_health(self,ph, fullph, x, y):
        container = pygame.Rect(x, y, 150, 20)
        blood = pygame.Rect(x + 1, y + 1, 150 * ph / fullph - 2, 20 - 2)
        pygame.draw.rect(screen, white, container, 1)
        pygame.draw.rect(screen, orange, blood)

    def update(self):
        self.rect.centery += self.speedy
        if self.rect.top > 50:
            self.rect.top = 50
            self.rect.centerx += self.speedx
            self.shoot()
            if self.rect.right > width:
                self.speedx = -self.speedx
            if self.rect.left < 0:
                self.speedx = -self.speedx
        if self.ph <= 0:
            self.drawph = False
            expl = Explosion(self.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            self.kill()

class Laser1(Roundbullet):
    def __init__(self,x,y,degree):
        Roundbullet.__init__(self,x,y,degree)
        self.image = laser1img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Enemy3(Enemy1):
    def __init__(self):
        Enemy1.__init__(self)
        self.image_org = pygame.transform.scale(enemy3img,(90,70))
        self.image_org.set_colorkey(black)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -random.randrange(1000,3500)
        self.speedy = 2
        self.radius = int(self.rect.width * 0.85 / 2)
        self.shoot_delay = 350
        self.ph = 150
        self.fullph = 150

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shoot_delay and self.rect.y > 0:
            self.shoot_time = pygame.time.get_ticks()
            new_dart(self.rect.centerx,self.rect.centery,self.angle)

class Dart(Roundbullet):
    def __init__(self,x,y,degree):
        Roundbullet.__init__(self,x,y,degree)
        self.img_orig = dartimg
        self.img_orig.set_colorkey(black)
        self.image = self.img_orig.copy()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.rot = 0
        self.rotspeed = 15
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rotspeed) % 360
            newimage = pygame.transform.rotate(self.img_orig, self.rot)
            old_center = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        if (self.rect.top > height) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

class X(Dart):
    def __init__(self,x,y,degree):
        Dart.__init__(self,x,y,degree)
        self.img_orig = dartimg
        self.img_orig.set_colorkey(black)
        self.image = self.img_orig.copy()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.rot = 0
        self.rotspeed = 20
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = -(self.rot + self.rotspeed) % 360
            newimage = pygame.transform.rotate(self.img_orig, self.rot)
            old_center = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Boss2(Boss1):
    def __init__(self):
        Boss1.__init__(self)
        self.image = boss2img
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = -3500
        self.shootdelay = 600

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shootdelay:
            self.shoot_time = now
            if self.shoot_mode == 1:
                new_laser1(self.rect.centerx+20, self.rect.bottom+20, -math.pi/2)
                new_laser1(self.rect.centerx-20, self.rect.bottom+20, -math.pi/2)
            if self.shoot_mode == 2:
                new_roundbullet(self.rect.left+20, self.rect.centery+60, -30)
                new_roundbullet(self.rect.right-20, self.rect.centery+60, 30)
                new_roundbullet(self.rect.centerx+20,self.rect.bottom,0)
                new_roundbullet(self.rect.centerx-20,self.rect.bottom,0)
            if self.shoot_mode == 3:
                new_dart(self.rect.left+20, self.rect.centery+60, -30)
                new_dart(self.rect.right-20, self.rect.centery+60, 30)
                new_dart(self.rect.centerx,self.rect.bottom,0)

        if now - self.shift_time > self.shiftmode_delay:
            self.shift_time = now
            self.shoot_mode += 1
            if self.shoot_mode > 3:
                self.shoot_mode = 1

class Boss3(Boss1):
    def __init__(self):
        Boss1.__init__(self)
        self.image = boss3img
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = -3500
        self.shootdelay = 550

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shootdelay:
            self.shoot_time = now
            if self.shoot_mode == 1:
                new_laser1(self.rect.centerx+50, self.rect.bottom+20, -math.pi/2)
                new_laser1(self.rect.centerx-50, self.rect.bottom+20, -math.pi/2)
                new_roundbullet(self.rect.centerx+20, self.rect.centery+60, 30)
                new_roundbullet(self.rect.centerx-20, self.rect.centery+60, -30)
            if self.shoot_mode == 2:
                new_dart(self.rect.left+20, self.rect.centery+60, -30)
                new_dart(self.rect.right-20, self.rect.centery+60, 30)
                new_roundbullet(self.rect.centerx+20,self.rect.bottom,0)
                new_roundbullet(self.rect.centerx-20,self.rect.bottom,0)
            if self.shoot_mode == 3:
                new_dart(self.rect.centerx+50,self.rect.bottom,0)
                new_dart(self.rect.centerx-50, self.rect.bottom, 0)
                new_laser1(self.rect.centerx, self.rect.bottom+20, -math.pi/2)
                new_x(self.rect.left+20, self.rect.centery+60, -30)
                new_x(self.rect.left-20, self.rect.centery+60, -30)
        if now - self.shift_time > self.shiftmode_delay:
            self.shift_time = now
            self.shoot_mode += 1
            if self.shoot_mode > 3:
                self.shoot_mode = 1

class Boss4(Boss1):
    def __init__(self):
        Boss1.__init__(self)
        self.image = boss4img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = -3500
        self.shootdelay = 550

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shootdelay:
            self.shoot_time = now
            if self.shoot_mode == 1:
                new_laser1(self.rect.centerx+50, self.rect.bottom+20, -math.pi/2)
                new_laser1(self.rect.centerx-50, self.rect.bottom+20, -math.pi/2)
                new_roundbullet(self.rect.centerx+20, self.rect.centery+60, 30)
                new_roundbullet(self.rect.centerx-20, self.rect.centery+60, -30)
            if self.shoot_mode == 2:
                new_dart(self.rect.left+20, self.rect.centery+60, -30)
                new_dart(self.rect.right-20, self.rect.centery+60, 30)
                new_roundbullet(self.rect.centerx+20,self.rect.bottom,0)
                new_roundbullet(self.rect.centerx-20,self.rect.bottom,0)
            if self.shoot_mode == 3:
                new_dart(self.rect.centerx+50,self.rect.bottom,0)
                new_dart(self.rect.centerx-50, self.rect.bottom, 0)
                new_laser1(self.rect.centerx, self.rect.bottom+20, -math.pi/2)
                new_x(self.rect.left+20, self.rect.centery+60, -30)
                new_x(self.rect.left-20, self.rect.centery+60, -30)
        if now - self.shift_time > self.shiftmode_delay:
            self.shift_time = now
            self.shoot_mode += 1
            if self.shoot_mode > 3:
                self.shoot_mode = 1

class Boss5(Boss1):
    def __init__(self):
        Boss1.__init__(self)
        self.image = boss5img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = -3500
        self.shootdelay = 550

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shootdelay:
            self.shoot_time = now
            #if self.shoot_mode == 1:
            #new_laser1(self.rect.centerx+50, self.rect.bottom+20,  random.uniform(-70, 70))
            #new_laser1(self.rect.centerx-50, self.rect.bottom+20,  random.uniform(-70, 70))
            #if self.shoot_mode == 2:
            #    new_dart(self.rect.left+20, self.rect.centery+60, random.uniform(-70, 70)) 
            #    new_dart(self.rect.right-20, self.rect.centery+60, random.uniform(-70, 70))

            if self.shoot_mode == 1:
                for _ in range(10):
                    position_offset = random.uniform(-70, 70)
                    new_laser1(self.rect.centerx + 60, self.rect.bottom, position_offset)
                    new_laser1(self.rect.centerx - 60, self.rect.bottom, position_offset)
            if self.shoot_mode == 2:
                for _ in range(10):
                    position_offset = random.uniform(-70, 70)
                    new_dart(self.rect.centerx + 60, self.rect.bottom, position_offset)
                    new_dart(self.rect.centerx - 60, self.rect.bottom, position_offset)
            if self.shoot_mode == 3:
                for _ in range(10):
                    position_offset = random.uniform(-70, 70)
                    new_roundbullet(self.rect.centerx + 60, self.rect.bottom, position_offset)
                    new_roundbullet(self.rect.centerx - 60, self.rect.bottom, position_offset)
            if self.shoot_mode == 4:
                for _ in range(10):
                    position_offset = random.uniform(-70, 70)
                    new_x(self.rect.centerx + 60, self.rect.bottom, position_offset)
                    new_x(self.rect.centerx - 60, self.rect.bottom, position_offset)
            if now - self.shift_time > self.shiftmode_delay:
                self.shift_time = now
                self.shoot_mode += 1
            if self.shoot_mode > 4:
                self.shoot_mode = 1

class Shieldup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shieldupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = shield1img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.radius = self.rect.width/2
        self.delay = 7000
        self.shield_time = pygame.time.get_ticks()

    def update(self):
        self.rect.center = player1.rect.center
        now = pygame.time.get_ticks()
        if now - self.shield_time > self.delay:
            self.kill()
            
class Shield2(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = shield2img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.radius = self.rect.width/2
        self.delay = 7000
        self.shield_time = pygame.time.get_ticks()

    def update(self):
        self.rect.center = player2.rect.center
        now = pygame.time.get_ticks()
        if now - self.shield_time > self.delay:
            self.kill()            

class Missileup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missileupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self,centerx,centery):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(missileimg,(40,90))
        self.image.set_colorkey((black))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speedy = +2 # 초기 속도
        self.acceleration = 0.2 # 속도 증가량

    def update(self):
        self.speedy -= self.acceleration  # 속도를 빨라지도록 업데이트        
        self.rect.y += self.speedy

        if self.rect.bottom <= 0:
            self.kill()

cooperative_mode = False

def intro1(): #width, height = 900, 750
    global cooperative_mode  # cooperative_mode를 전역 변수로 사용
    running = True
    music_files = ['game.mp3', 'game2.mp3', 'game3.flac', 'game4.mp3', 'game5.mp3']

    # 음악 파일 경로 설정
    #snd_dir = '경로/음악이/저장된/폴더'  # 실제 경로로 바꿔야 합니다.  

    # 무작위 음악 선택
    random_music = random.choice(music_files)  # music_files 리스트에서 무작위 음악 파일 선택
    pygame.mixer.music.load(path.join(snd_dir, random_music))  # 선택한 음악 파일을 로드
    pygame.mixer.music.play(-1)  # 선택한 음악을 반복 재생-master\sprites.py", line 1010, in intro
    # Create the background which will scroll and loop over a set of different
    # size stars
    introbackground = pygame.Surface((900, 1750))
    introbackground = introbackground.convert()
    introbackground.fill((0,0,0))
    backgroundLoc = 1000
    finalStars = deque()
    for y in range(0, 1000, 30):
        size = random.randint(2, 5)
        x = random.randint(0, 900 - size)
        if y <= 500:
            finalStars.appendleft((x, y + 1000, size))
        pygame.draw.rect(
            introbackground, (255, 255, 0), pygame.Rect(x, y, size, size))
    while finalStars:
        x, y, size = finalStars.pop()
        pygame.draw.rect(
            introbackground, (255, 255, 0), pygame.Rect(x, y, size, size))
    
    speed = 1.5
    while True:
        screen.blit(introbackground, (0, 0), area=pygame.Rect(0, backgroundLoc, 900, 750))
        backgroundLoc -= speed
        if backgroundLoc - speed <= speed:
            backgroundLoc = 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        #screen.blit(introbackground1,(0,0))
        #label("우주 전쟁",width/2-100,100,50,purple)
        label("Welcome to",width/2-90,120,30,green)
        label("SPACE WAR",width/2-170,170,60,red)
        label("팁: 적들을 처치하고 파워 업 하세요!",width/2-230,625,30,purple)
        Button("시작",width/2-50,height/2-50,70,35,green,brightgreen,gameloop1)
        Button("협동",width/2-50,height/2,70,35,green,brightgreen,cooperation1)
        Button("최고점수",width/2-65,height/2+50,100,35,blue,brightblue,highscore)
        Button("게임정보",width/2-65,height/2+100,100,35,blue,brightblue,info1)
        Button("종료",width/2-50,height/2+150,70,35,red,brightred,quitgame)

        clock.tick(15) 
        pygame.display.update()
    

def intro2(): #width, height = 1280, 900
    global cooperative_mode  # cooperative_mode를 전역 변수로 사용
    running = True
    # 음악 파일 목록
    music_files = ['game.mp3', 'game2.mp3', 'game3.flac', 'game4.mp3', 'game5.mp3']

    # 음악 파일 경로 설정
    #snd_dir = '경로/음악이/저장된/폴더'  # 실제 경로로 바꿔야 합니다.  

    # 무작위 음악 선택
    random_music = random.choice(music_files)  # music_files 리스트에서 무작위 음악 파일 선택
    pygame.mixer.music.load(path.join(snd_dir, random_music))
    pygame.mixer.music.play(-1)
    # Create the background which will scroll and loop over a set of different
    # size stars
    introbackground = pygame.Surface((1280,1900))
    introbackground = introbackground.convert()
    backgroundLoc = 1000
    finalStars = deque()
    for y in range(0, 1000, 30):
        size = random.randint(2, 5)
        x = random.randint(0, 1280 - size)
        if y <= 500:
            finalStars.appendleft((x, y + 1000, size))
        pygame.draw.rect(
            introbackground, (255, 255, 0), pygame.Rect(x, y, size, size))
    while finalStars:
        x, y, size = finalStars.pop()
        pygame.draw.rect(
            introbackground, (255, 255, 0), pygame.Rect(x, y, size, size))
    
    speed = 1.5
    while True:
        screen.blit(introbackground, (0, 0), area=pygame.Rect(0, backgroundLoc, 1280, 900))
        backgroundLoc -= speed
        if backgroundLoc - speed <= speed:
            backgroundLoc = 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        #label("우주 전쟁",width/2-100,100,50,purple)
        label("Welcome to",width/2-90,120,30,green)
        label("SPACE WAR",width/2-170,170,60,red)
        label("팁: 적들을 처치하고 파워 업 하세요!",width/2-230,800,30,purple)
        Button("시작",width/2-50,height/2-50,70,35,green,brightgreen,gameloop2)
        Button("협동",width/2-50,height/2,70,35,green,brightgreen,cooperation2)
        Button("최고점수",width/2-65,height/2+50,100,35,blue,brightblue,highscore2)
        Button("게임정보",width/2-65,height/2+100,100,35,blue,brightblue,info2)
        Button("종료",width/2-50,height/2+150,70,35,red,brightred,quitgame)

        clock.tick(15) 
        pygame.display.update()

@staticmethod
def reset_high_scores():
    conn = sqlite3.connect(Database.path)
    c = conn.cursor()
    c.execute("DELETE FROM scores")
    conn.commit()
    conn.close()

def highscore():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        screen.fill((0,0,0))
        font = pygame.font.Font(font_path, 24)
        hiScores = Database.getScores()
        highScoreTexts = [font.render("이름", 1, RED),
                        font.render("점수", 1, RED),
                        font.render("시간", 1, RED)]
        highScorePos = [highScoreTexts[0].get_rect(
                        topleft=screen.get_rect().inflate(-100, -100).topleft),
                        highScoreTexts[1].get_rect(
                        midtop=screen.get_rect().inflate(-100, -100).midtop),
                        highScoreTexts[2].get_rect(
                        topright=screen.get_rect().inflate(-140, -100).topright)]
        for hs in hiScores:
            highScoreTexts.extend([font.render(str(hs[x]), 1, green)
                                for x in range(3)])
            highScorePos.extend([highScoreTexts[x].get_rect(
                topleft=highScorePos[x].bottomleft) for x in range(-3, 0)])
        textOverlays = zip(highScoreTexts, highScorePos)
        for txt, pos in textOverlays:
            screen.blit(txt, pos)

        Button("시작",width/2-310,height/2+250,100,50,green,brightgreen,gameloop1)
        Button("협동",width/2-180, height/2+250, 100, 50, green, brightgreen, cooperation1)
        Button("시작화면",width/2-50,height/2+250,100,50,blue,brightblue,intro1)
        Button("초기화",width/2+80,height/2+250,100,50,red,brightred,reset_high_scores)
        Button("종료",width/2+210,height/2+250,100,50,red,brightred,quitgame)
        pygame.display.flip()

def highscore2():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        screen.fill((0,0,0))
        font = pygame.font.Font(font_path, 24)
        hiScores = Database.getScores()
        highScoreTexts = [font.render("이름", 1, RED),
                        font.render("점수", 1, RED),
                        font.render("시간", 1, RED)]
        highScorePos = [highScoreTexts[0].get_rect(
                        topleft=screen.get_rect().inflate(-100, -100).topleft),
                        highScoreTexts[1].get_rect(
                        midtop=screen.get_rect().inflate(-100, -100).midtop),
                        highScoreTexts[2].get_rect(
                        topright=screen.get_rect().inflate(-140, -100).topright)]
        for hs in hiScores:
            highScoreTexts.extend([font.render(str(hs[x]), 1, green)
                                for x in range(3)])
            highScorePos.extend([highScoreTexts[x].get_rect(
                topleft=highScorePos[x].bottomleft) for x in range(-3, 0)])
        textOverlays = zip(highScoreTexts, highScorePos)
        for txt, pos in textOverlays:
            screen.blit(txt, pos)

        Button("시작",width/2-310,height/2+250,100,50,green,brightgreen,gameloop2)
        Button("협동",width/2-180, height/2+250, 100, 50, green, brightgreen, cooperation2)
        Button("시작화면",width/2-50,height/2+250,100,50,blue,brightblue,intro2)
        Button("초기화",width/2+80,height/2+250,100,50,red,brightred,reset_high_scores)
        Button("종료",width/2+210,height/2+250,100,50,red,brightred,quitgame)
        pygame.display.flip()

def info1(): #width, height = 900, 750
    pygame.mixer.music.load(path.join(snd_dir, 'info.mp3'))
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        screen.blit(infobackground1,(0,0))
        label("게임 정보",width/2-115,70,60,orange)
        label("1P",width/2-200,height/2-195,40,green)
        label("2P",width/2-50,height/2-195,40,green)
        label("공격 :",width/2-360,height/2-120,35,purple)
        label("이동 :",width/2-360,height/2-40,35,purple)
        label("미사일 :",width/2-390,height/2+40,35,purple)
        label("방어막 :",width/2-390,height/2+120,35,purple)
        #1P Keys
        label("M 키",width/2-210,height/2-120,35,purple)
        label("방향키",width/2-225,height/2-40,35,purple)
        label("< 키",width/2-210,height/2+40,35,purple)
        label("> 키",width/2-210,height/2+120,35,purple)
        #2P Keys
        label("Ctrl 키",width/2-65,height/2-120,35,purple)
        label("R,D,F,G 키",width/2-85,height/2-40,35,purple)
        label("Shift 키",width/2-75,height/2+40,35,purple)
        label("Z 키",width/2-60,height/2+120,35,purple)

        screen.blit(bulletupimg,(width/2+150,190))
        label("bullet type up",width/2+200,190,20,brightblue)
        screen.blit(speedupimg,(width/2+150,250))
        label("shooting speed up",width/2+195,250,20,brightblue)
        screen.blit(healthupimg,(width/2+150,310))
        label("health up",width/2+200,310,20,brightblue)
        screen.blit(liveup1img,(width/2+150,370))
        label("live up",width/2+210,375,20,brightblue)
        screen.blit(shieldupimg,(width/2+150,430))
        label("shield up",width/2+200,430,20,brightblue)
        screen.blit(missileupimg,(width/2+150,490))
        label("missile up",width/2+200,490,20,brightblue)

        Button("시작",width/2-245,height/2+250,100,50,green,brightgreen,gameloop1)
        Button("협동",width/2-115, height/2+250, 100, 50, green, brightgreen, cooperation1)
        Button("시작화면",width/2+15,height/2+250,100,50,blue,brightblue,intro1)
        Button("종료",width/2+145,height/2+250,100,50,red,brightred,quitgame)

        clock.tick(15)
        pygame.display.update()

def info2(): #width, height = 1280, 900
    pygame.mixer.music.load(path.join(snd_dir, 'info.mp3'))
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        screen.blit(infobackground2,(0,0))
        label("게임 정보",width/2-130,70,60,orange)

        label("1P",width/2-200,height/2-195,40,green)
        label("2P",width/2-50,height/2-195,40,green)
        label("공격 :",width/2-360,height/2-120,35,purple)
        label("이동 :",width/2-360,height/2-40,35,purple)
        label("미사일 :",width/2-390,height/2+40,35,purple)
        label("방어막 :",width/2-390,height/2+120,35,purple)
        #1P Keys
        label("M 키",width/2-210,height/2-120,35,purple)
        label("방향키",width/2-225,height/2-40,35,purple)
        label("< 키",width/2-210,height/2+40,35,purple)
        label("> 키",width/2-210,height/2+120,35,purple)
        #2P Keys
        label("Ctrl 키",width/2-65,height/2-120,35,purple)
        label("R,D,F,G 키",width/2-75,height/2-40,35,purple)
        label("Shift 키",width/2-75,height/2+40,35,purple)
        label("Z 키",width/2-60,height/2+120,35,purple)

        screen.blit(bulletupimg,(width/2+150,190))
        label("bullet type up",width/2+200,190,20,brightblue)
        screen.blit(speedupimg,(width/2+150,250))
        label("shooting speed up",width/2+195,250,20,brightblue)
        screen.blit(healthupimg,(width/2+150,310))
        label("health up",width/2+200,310,20,brightblue)
        screen.blit(liveup1img,(width/2+150,370))
        label("live up",width/2+210,375,20,brightblue)
        screen.blit(shieldupimg,(width/2+150,430))
        label("shield up",width/2+200,430,20,brightblue)
        screen.blit(missileupimg,(width/2+150,490))
        label("missile up",width/2+200,490,20,brightblue)
        Button("시작",width/2-245,height/2+250,100,50,green,brightgreen,gameloop2)
        Button("협동",width/2-115, height/2+250, 100, 50, green, brightgreen, cooperation2)
        Button("시작화면",width/2+15,height/2+250,100,50,blue,brightblue,intro2)
        Button("종료",width/2+145,height/2+250,100,50,red,brightred,quitgame)

        clock.tick(15)
        pygame.display.update()

class Keyboard(object):
    keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
            pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
            pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
            pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
            pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
            pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
            pygame.K_y: 'Y', pygame.K_z: 'Z', pygame.K_COMMA: ',', pygame.K_PERIOD: '.',
            pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3', pygame.K_4: '4',
            pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8',
            pygame.K_9: '9', pygame.K_0: '0'}

def gameover1():
    pygame.mixer.music.load(path.join(snd_dir, 'loose.mp3'))
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    quitgame()

        screen.blit(gameoverbackground1,(0,0))
        label("게임 오버",width/2-230,height/2-200,100,brightred)
        Button("Re:Solo",150,height/2+40,100,50,green,brightgreen,gameloop1)
        Button("Re:Duo", 150, height/2+100, 100, 50, green, brightgreen, cooperation1)
        Button("시작화면",325,height/2+100,100,50,blue,brightblue,intro1)
        Button("최고점수",475,height/2+100,100,50,blue,brightblue,highscore)
        Button("종료",650,height/2+100,100,50,red,brightred,quitgame)

        clock.tick(15)
        pygame.display.update()

def gameover2(): #width, height = 1280, 900
    pygame.mixer.music.load(path.join(snd_dir, 'loose.mp3'))
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    quitgame()


        screen.blit(gameoverbackground2,(0,0))
        label("게임 오버",width/2-230,height/2-200,100,brightred)
        Button("Re:Solo",200,height/2+40,100,50,green,brightgreen,gameloop2)
        Button("Re:Duo", 200, height/2+100, 100, 50, green, brightgreen, cooperation2)
        Button("시작화면",500,height/2+100,100,50,blue,brightblue,intro2)
        Button("최고점수",800,height/2+100,100,50,blue,brightblue,highscore2)
        Button("종료",1080,height/2+100,100,50,red,brightred,quitgame )

        clock.tick(15)
        pygame.display.update()

def gameloop1():
    start_time = 0
    global cooperative_mode, elapsed_pause_time
    cooperative_mode = False
    screen.blit(background1,(0,0))
    pygame.mixer.init()

    # 음악 파일 목록
    music_files = ['game.mp3', 'game2.mp3', 'game3.flac', 'game4.mp3', 'game5.mp3']

    # 음악 파일 경로 설정
    #snd_dir = '경로/음악이/저장된/폴더'  # 실제 경로로 바꿔야 합니다.

    # 무작위 음악 선택
    random_music = random.choice(music_files)  # music_files 리스트에서 무작위 음악 파일 선택
    pygame.mixer.music.load(path.join(snd_dir, random_music))
    pygame.mixer.music.play(-1)
    # set up
    global all_sprites,meteorite_sprites,bullet_sprites,bullet_sprites_2,bullet_sprites_3,bullet_sprites_4
    global bullet_sprites_5,bullet_sprites_6,bulletup_sprites,ultbulletup_sprites,speedup_sprites
    global healthup_sprites,liveup_sprites,enemy1_sprites,enemy2_sprites,roundbullet_sprites
    global boss1_sprites,laser1_sprites,dart_sprites,enemy3_sprites, boss2_sprites,x_sprites,boss3_sprites
    global boss4_sprites, boss5_sprites,shieldup_sprites,shield_sprites,missileup_sprites,missile_sprites,player1,player2
    all_sprites = pygame.sprite.Group()
    meteorite_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    bullet_sprites_2 = pygame.sprite.Group()
    bullet_sprites_3 = pygame.sprite.Group()
    bullet_sprites_4 = pygame.sprite.Group()
    bullet_sprites_5 = pygame.sprite.Group()
    bullet_sprites_6 = pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()
    ultbulletup_sprites=pygame.sprite.Group()
    speedup_sprites = pygame.sprite.Group()
    healthup_sprites = pygame.sprite.Group()
    liveup_sprites = pygame.sprite.Group()
    enemy1_sprites = pygame.sprite.Group()
    enemy2_sprites = pygame.sprite.Group()
    roundbullet_sprites = pygame.sprite.Group()
    boss1_sprites = pygame.sprite.Group()
    boss4_sprites = pygame.sprite.Group()
    boss5_sprites = pygame.sprite.Group()
    laser1_sprites = pygame.sprite.Group()
    dart_sprites = pygame.sprite.Group()
    enemy3_sprites = pygame.sprite.Group()
    boss2_sprites = pygame.sprite.Group()
    x_sprites = pygame.sprite.Group()
    boss3_sprites = pygame.sprite.Group()
    shieldup_sprites = pygame.sprite.Group()
    shield_sprites = pygame.sprite.Group()
    missileup_sprites = pygame.sprite.Group()
    missile_sprites = pygame.sprite.Group()
    all_drawings = pygame.sprite.Group()
    player1 = Player1()
    all_sprites.add(player1)

    for i in range(4):
        newmeteorite()

    enemy1 = newenemy1()
    enemy1.rect.y = -1000
    enemy2 = newenemy2()
    enemy2.rect.y = -3500
    boss1 = newboss1()
    boss1.rect.y = -5000
    enemy3 = newenemy3()
    enemy3.rect.y = -8000
    count1 = 1

    shieldup = newshieldup()
    shieldup.rect.y = -2000
    bulletup = newbulletup()
    bulletup.rect.y = -700
    speedup = newspeedup()
    speedup.rect.y = -2500
    ultbulletup = newultbulletup()
    ultbulletup.rect.y = - 1900
    shieldup = newshieldup()
    shieldup.rect.y = -4000
    bulletup = newbulletup()
    bulletup.rect.y = -1500
    speedup = newspeedup()
    speedup.rect.y = -3500
    running = True
    start_time = pygame.time.get_ticks()  # 게임 시작 시간 저장
    elapsed_pause_time = 0  # 초기화
    
    score = player1.score
    hiScores = Database.getScores()
    isHiScore = len(hiScores) < Database.numScores or score > hiScores[-1][1]
    name = ''
    nameBuffer = []

    while player1.live >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_PERIOD:
                    if player1.shield > 0:
                        player1.shield -= 1
                        newshield1(player1.rect.center)
                        shield_sound.play()
                if event.key == pygame.K_COMMA:
                    if player1.missile > 0:
                        player1.missile -= 1
                        newmissile(player1.rect.centerx,player1.rect.centery)
                        newmissile(player1.rect.centerx-200,player1.rect.centery)
                        newmissile(player1.rect.centerx+200,player1.rect.centery)
                        missile_sound.play()    
                if event.key == pygame.K_p:
                       pause()
                if event.key == pygame.K_ESCAPE:
                        quitgame()
                if event.key == pygame.K_m:
                    player1.shoot()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time - elapsed_pause_time
        elapsed_seconds = elapsed_time / 1000
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                sys.exit()
        clock.tick(fps)
        
        #******update*****
        all_sprites.update()

        # meteor hit player1
        hits = pygame.sprite.spritecollide(player1,meteorite_sprites,True,pygame.sprite.collide_circle)
        for hit in hits:
            player1.ph -= hit.radius * 1.5
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            newmeteorite()
  
        # mybullet hit meteor
        hits = pygame.sprite.groupcollide(bullet_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()
                
        # missile hit meteor
        hits = pygame.sprite.groupcollide(missile_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        # player1 get bulletup
        hits = pygame.sprite.spritecollide(player1,bulletup_sprites,True)
        for hit in hits:
            player1.bulletpower += 1
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()
            
        # player1 get ultbulletup
        hits = pygame.sprite.spritecollide(player1,ultbulletup_sprites,True)
        for hit in hits:
            player1.score += 200
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()
        # player1 get speedup
        hits = pygame.sprite.spritecollide(player1,speedup_sprites,True)
        for hit in hits:
            player1.shootdelay -= 50
            speedup_sound.play()
        # player1 get health up
        hits = pygame.sprite.spritecollide(player1,healthup_sprites,True)
        for hit in hits:
            player1.ph += random.randrange(10,70)
            healthup_sound.play()
        # player1 get liveup
        hits = pygame.sprite.spritecollide(player1,liveup_sprites,True)
        for hit in hits:
            player1.live += 1
            liveup_sound.play()
        # player1 get shieldup
        hits = pygame.sprite.spritecollide(player1,shieldup_sprites,True)
        for hit in hits:
            player1.shield += 1
            shieldup_sound.play()
        # player1 get missileup
        hits = pygame.sprite.spritecollide(player1,missileup_sprites,True)
        for hit in hits:
            player1.missile += 1
            missileup_sound.play()

        # player1 hit enemy1
        hits = pygame.sprite.spritecollide(player1,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy1.ph
            enemy1.ph = 0  
        # player1 hit enemy2
        hits = pygame.sprite.spritecollide(player1,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy2.ph
            enemy2.ph = 0
        # player1 hit enemy3
        hits = pygame.sprite.spritecollide(player1,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy3.ph
            enemy3.ph = 0    
        # mybullet hit enemy1
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        # mybullet hit enemy2
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        # mybullet hit enemy3
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        # missile hit enemy1
        hits = pygame.sprite.groupcollide(missile_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 700
        # missile hit enemy2
        hits = pygame.sprite.groupcollide(missile_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 700
        # missile hit enemy3
        hits = pygame.sprite.groupcollide(missile_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 700
        # regenerate enemy1
        if enemy1.ph <= 0:
            newbulletup()
            player1.score += 100
            enemy1 = newenemy1()
        if enemy1.rect.top > height:
            enemy1 = newenemy1()
        # regenerate enemy2
        if enemy2.ph <= 0:
            newspeedup()
            player1.score += 100
            enemy2 = newenemy2()
        if enemy2.rect.top > height:
            enemy2 = newenemy2()
        # regenerate enemy3
        if enemy3.ph <= 0:
            newhealthup()
            newmissileup()
            player1.score += 100
            enemy3 = newenemy3()
        if enemy3.rect.top > height:
            enemy3 = newenemy3()

        # roundbullet hit player1
        hits = pygame.sprite.spritecollide(player1,roundbullet_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 10  
        # laser1 hit player1
        hits = pygame.sprite.spritecollide(player1,laser1_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 20
        # dart hit player1
        hits = pygame.sprite.spritecollide(player1,dart_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 30
        # x hit player1
        hits = pygame.sprite.spritecollide(player1,x_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 35 

        # meteorite hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,meteorite_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # roundbullet hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,roundbullet_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # laser1 hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,laser1_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # dart hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,dart_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # x hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,x_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # player1 hit boss1
        hits = pygame.sprite.spritecollide(player1,boss1_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss1.ph
            boss1.ph -= player1.ph
            player1.ph -= hurt
            boss1.drawph = True 
        # player1 hit boss2
        hits = pygame.sprite.spritecollide(player1,boss2_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss2.ph
            boss2.ph -= player1.ph
            player1.ph -= hurt
            boss2.drawph = True  
        # player1 hit boss3
        hits = pygame.sprite.spritecollide(player1,boss3_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss3.ph
            boss3.ph -= player1.ph
            player1.ph -= hurt
            boss3.drawph = True
        # player1 hit boss4
        hits = pygame.sprite.spritecollide(player1,boss4_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss4.ph
            boss4.ph -= player1.ph
            player1.ph -= hurt
            boss4.drawph = True

        # player1 hit boss5
        hits = pygame.sprite.spritecollide(player1,boss5_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss5.ph
            boss5.ph -= player1.ph
            player1.ph -= hurt
            boss5.drawph = True
        # mybullet hit boss1
        hits = pygame.sprite.groupcollide(bullet_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        # mybullet hit boss2
        hits = pygame.sprite.groupcollide(bullet_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        # mybullet hit boss3
        hits = pygame.sprite.groupcollide(bullet_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        # mybullet hit boss4
        hits = pygame.sprite.groupcollide(bullet_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        # mybullet hit boss5
        hits = pygame.sprite.groupcollide(bullet_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10
    
        # missile hit boss1
        hits = pygame.sprite.groupcollide(missile_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 700
        # missile hit boss2
        hits = pygame.sprite.groupcollide(missile_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 700
        # missile hit boss3
        hits = pygame.sprite.groupcollide(missile_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 700
        # missile hit boss4
        hits = pygame.sprite.groupcollide(missile_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 700
        # missile hit boss5
        hits = pygame.sprite.groupcollide(missile_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 700

        try:
            # boss1 die generate boss2
            if boss1.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss2 = newboss2()
                boss2.ph *= count1
                boss2.fullph *= count1
                boss1.drawph = False
                expl = Explosion(boss1.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss1.kill()
                boss1.ph = 1
            # boss2 die generate boss3
            if boss2.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss3 = newboss3()
                boss3.ph *= count1
                boss3.fullph *= count1
                boss2.drawph = False
                expl = Explosion(boss2.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss2.kill()
                boss2.ph = 1
            # boss3 die generate boss4
            if boss3.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss4 = newboss4()
                boss4.ph *= count1
                boss4.fullph *= count1
                boss3.drawph = False
                expl = Explosion(boss3.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss3.kill()
                boss3.ph = 1
            # boss4 die generate boss5
            if boss4.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss5 = newboss5()
                boss5.ph *= count1
                boss5.fullph *= count1
                boss4.drawph = False
                expl = Explosion(boss4.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss4.kill()
                boss4.ph = 1
            # boss5 die 
            if boss5.ph <= 0:
                count1 += 1
                boss5.drawph = False
                expl = Explosion(boss5.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss5.kill()
                boss5.ph = 1
                player1.live = -1
                
        except:
            pass

        #******draw******
        screen.blit(background,(0,0))
        all_sprites.draw(screen)

        drawscore(player1.score,width/2-50,45)
        drawsec(elapsed_seconds,width/2+200,45)
        health(player1.ph,20,50)
        drawlive1(player1.live,40,100)
        drawshield(player1.shield,20,height-120)
        drawmissile(player1.missile,20,height-75)

        # draw enemy1 ph
        try:
            if enemy1.drawph:
                enemy1.enemy_health(enemy1.ph, enemy1.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy2 ph
        try:
            if enemy2.drawph:
                enemy2.enemy_health(enemy2.ph, enemy2.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy3 ph
        try:
            if enemy3.drawph:
                enemy3.enemy_health(enemy3.ph, enemy3.fullph, width/2-75, 85)
        except:
            pass
        # draw boss1 ph
        try:
            if boss1.drawph:
                boss1.enemy_health(boss1.ph, boss1.fullph, width/2-75, 115)
        except:
            pass
        # draw boss2 ph
        try:
            if boss2.drawph:
                boss2.enemy_health(boss2.ph, boss2.fullph, width/2-75, 115)
        except:
            pass
        # draw boss3 ph
        try:
            if boss3.drawph:
                boss3.enemy_health(boss3.ph, boss3.fullph, width/2-75, 115)
        except:
            pass
        # draw boss4 ph
        try:
            if boss4.drawph:
                boss4.enemy_health(boss4.ph, boss4.fullph, width/2-75, 115)
        except:
            pass
        # draw boss5 ph
        try:
            if boss5.drawph:
                boss5.enemy_health(boss5.ph, boss5.fullph, width/2-75, 115)
        except:
            pass

        pygame.display.update()
        pygame.display.flip()
        fpsClock.tick(fps)

    while player1.live < 0:
        clock.tick(fps)

    # Event Handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                or not isHiScore
                and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return False
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and not isHiScore):
                return True
            elif (event.type == pygame.KEYDOWN
                  and event.key in Keyboard.keys.keys()
                  and len(nameBuffer) < 8):
                nameBuffer.append(Keyboard.keys[event.key])
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_BACKSPACE
                  and len(nameBuffer) > 0):
                nameBuffer.pop()
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and len(name) > 0):
                Database.setScore(hiScores, (name, player1.score, elapsed_seconds))
                return gameover1()

        if isHiScore:
            hiScoreText = font.render('HIGH SCORE!', 1, RED)
            hiScorePos = hiScoreText.get_rect(
                midbottom=screen.get_rect().center)
            scoreText = font.render(str(player1.score), 1, green)
            scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
            enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
            enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
            nameText = font.render(name, 1, green)
            namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
            textOverlay = zip([hiScoreText, scoreText,
                               enterNameText, nameText],
                              [hiScorePos, scorePos,
                               enterNamePos, namePos])
        else:
            gameOverText = font.render('GAME OVER', 1, BLUE)
            gameOverPos = gameOverText.get_rect(
                center=screen.get_rect().center)
            scoreText = font.render('SCORE: {}'.format(player1.score), 1, BLUE)
            scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
            textOverlay = zip([gameOverText, scoreText],
                              [gameOverPos, scorePos])

    # Update and draw all sprites
        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        all_drawings.update()
        for txt, pos in textOverlay:
            screen.blit(txt, pos)
        pygame.display.flip()

def gameloop2():
    start_time = 0
    global cooperative_mode, elapsed_pause_time
    cooperative_mode = False
    screen.blit(background2,(0,0))
    # 음악 파일 목록
    music_files = ['game.mp3', 'game2.mp3', 'game3.flac', 'game4.mp3', 'game5.mp3']

    # 음악 파일 경로 설정
    #snd_dir = '경로/음악이/저장된/폴더'  # 실제 경로로 바꿔야 합니다.  

    # 무작위 음악 선택
    random_music = random.choice(music_files)  # music_files 리스트에서 무작위 음악 파일 선택
    pygame.mixer.music.load(path.join(snd_dir, random_music))
    pygame.mixer.music.play(-1)

    # set up
    global all_sprites,meteorite_sprites,bullet_sprites,bullet_sprites_2,bullet_sprites_3,bullet_sprites_4
    global bullet_sprites_5,bullet_sprites_6,bulletup_sprites,ultbulletup_sprites,speedup_sprites
    global healthup_sprites,liveup_sprites,enemy1_sprites,enemy2_sprites,roundbullet_sprites
    global boss1_sprites,laser1_sprites,dart_sprites,enemy3_sprites, boss2_sprites,x_sprites,boss3_sprites
    global boss4_sprites,boss5_sprites,shieldup_sprites,shield_sprites,missileup_sprites,missile_sprites,player1,player2
    all_sprites = pygame.sprite.Group()
    meteorite_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    bullet_sprites_2 = pygame.sprite.Group()
    bullet_sprites_3 = pygame.sprite.Group()
    bullet_sprites_4 = pygame.sprite.Group()
    bullet_sprites_5 = pygame.sprite.Group()
    bullet_sprites_6 = pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()

    ultbulletup_sprites=pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()
    speedup_sprites = pygame.sprite.Group()
    healthup_sprites = pygame.sprite.Group()
    liveup_sprites = pygame.sprite.Group()
    enemy1_sprites = pygame.sprite.Group()
    enemy2_sprites = pygame.sprite.Group()
    roundbullet_sprites = pygame.sprite.Group()
    boss1_sprites = pygame.sprite.Group()
    boss4_sprites = pygame.sprite.Group()
    boss5_sprites = pygame.sprite.Group()
    laser1_sprites = pygame.sprite.Group()
    dart_sprites = pygame.sprite.Group()
    enemy3_sprites = pygame.sprite.Group()
    boss2_sprites = pygame.sprite.Group()
    x_sprites = pygame.sprite.Group()
    boss3_sprites = pygame.sprite.Group()
    shieldup_sprites = pygame.sprite.Group()
    shield_sprites = pygame.sprite.Group()
    missileup_sprites = pygame.sprite.Group()
    missile_sprites = pygame.sprite.Group()
    all_drawings = pygame.sprite.Group()
    player1 = Player1()
    all_sprites.add(player1)
    for i in range(4):
        newmeteorite()

    enemy1 = newenemy1()
    enemy1.rect.y = -1000
    enemy2 = newenemy2()
    enemy2.rect.y = -3500
    boss1 = newboss1()
    boss1.rect.y = -5000
    enemy3 = newenemy3()
    enemy3.rect.y = -8000
    count1 = 1

    shieldup = newshieldup()
    shieldup.rect.y = -2000
    bulletup = newbulletup()
    bulletup.rect.y = -700
    speedup = newspeedup()
    speedup.rect.y = -2500
    ultbulletup = newultbulletup()
    ultbulletup.rect.y = - 1900

    shieldup = newshieldup()
    shieldup.rect.y = -4000
    bulletup = newbulletup()
    bulletup.rect.y = -1500
    speedup = newspeedup()
    speedup.rect.y = -3500
    ultbulletup = newultbulletup()
    ultbulletup.rect.y = - 1800

    running = True
    start_time = pygame.time.get_ticks()  # 게임 시작 시간 저장
    elapsed_pause_time = 0  # 초기화

    score = player1.score
    hiScores = Database.getScores()
    isHiScore = len(hiScores) < Database.numScores or score > hiScores[-1][1]
    name = ''
    nameBuffer = []

    while player1.live >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_PERIOD:
                    if player1.shield > 0:
                        player1.shield -= 1
                        newshield1(player1.rect.center)
                        shield_sound.play()
                if event.key == pygame.K_COMMA:
                    if player1.missile > 0:
                        player1.missile -= 1
                        newmissile(player1.rect.centerx,player1.rect.centery)
                        newmissile(player1.rect.centerx-200,player1.rect.centery)
                        newmissile(player1.rect.centerx+200,player1.rect.centery)
                        missile_sound.play()                
                if event.key == pygame.K_p:
                       pause()
                if event.key == pygame.K_ESCAPE:
                        quitgame()
                if event.key == pygame.K_m:
                    player1.shoot()
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time - elapsed_pause_time
        elapsed_seconds = elapsed_time / 1000
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                sys.exit()
        clock.tick(fps)
        #******update*****
        all_sprites.update()

        # meteor hit player1
        hits = pygame.sprite.spritecollide(player1,meteorite_sprites,True,pygame.sprite.collide_circle)
        for hit in hits:
            player1.ph -= hit.radius * 1.5
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            
        # mybullet hit meteor
        hits = pygame.sprite.groupcollide(bullet_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()

        hits = pygame.sprite.groupcollide(bullet_sprites_2,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()

        hits = pygame.sprite.groupcollide(bullet_sprites_3,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()
            
        hits = pygame.sprite.groupcollide(bullet_sprites_4,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()

        hits = pygame.sprite.groupcollide(bullet_sprites_5,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()

        hits = pygame.sprite.groupcollide(bullet_sprites_6,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            ultbulletup_chance = random.randrange(0,100)
            if ultbulletup_chance > 99:
                newultbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()
                
        # missile hit meteor
        hits = pygame.sprite.groupcollide(missile_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        # player1 get bulletup
        hits = pygame.sprite.spritecollide(player1,bulletup_sprites,True)
        for hit in hits:
            player1.bulletpower += 1
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()
            
        # player1 get ultbulletup
        hits = pygame.sprite.spritecollide(player1,ultbulletup_sprites,True)
        for hit in hits:
            player1.score += 200
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()

        # player1 get speedup
        hits = pygame.sprite.spritecollide(player1,speedup_sprites,True)
        for hit in hits:
            player1.shootdelay -= 50
            speedup_sound.play()
        # player1 get health up
        hits = pygame.sprite.spritecollide(player1,healthup_sprites,True)
        for hit in hits:
            player1.ph += random.randrange(10,70)
            healthup_sound.play()
        # player1 get liveup
        hits = pygame.sprite.spritecollide(player1,liveup_sprites,True)
        for hit in hits:
            player1.live += 1
            liveup_sound.play()
        # player1 get shieldup
        hits = pygame.sprite.spritecollide(player1,shieldup_sprites,True)
        for hit in hits:
            player1.shield += 1
            shieldup_sound.play()
        # player1 get missileup
        hits = pygame.sprite.spritecollide(player1,missileup_sprites,True)
        for hit in hits:
            player1.missile += 1
            missileup_sound.play()

        # player1 hit enemy1
        hits = pygame.sprite.spritecollide(player1,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy1.ph
            enemy1.ph = 0  
        # player1 hit enemy2
        hits = pygame.sprite.spritecollide(player1,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy2.ph
            enemy2.ph = 0
        # player1 hit enemy3
        hits = pygame.sprite.spritecollide(player1,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy3.ph
            enemy3.ph = 0    
       
        # player1 hit enemy1
        hits = pygame.sprite.spritecollide(player1,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy1.ph
            enemy1.ph = 0   
        # player1 hit enemy2
        hits = pygame.sprite.spritecollide(player1,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy2.ph
            enemy2.ph = 0
        # player1 hit enemy3
        hits = pygame.sprite.spritecollide(player1,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy3.ph
            enemy3.ph = 0
        # mybullet hit enemy1
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        # mybullet hit enemy2
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        # mybullet hit enemy3
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        # missile hit enemy1
        hits = pygame.sprite.groupcollide(missile_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 700
        # missile hit enemy2
        hits = pygame.sprite.groupcollide(missile_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 700
        # missile hit enemy3
        hits = pygame.sprite.groupcollide(missile_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 700
        # regenerate enemy1
        if enemy1.ph <= 0:
            newbulletup()
            player1.score += 100
            enemy1 = newenemy1()
        if enemy1.rect.top > height:
            enemy1 = newenemy1()
        # regenerate enemy2
        if enemy2.ph <= 0:
            newspeedup()
            player1.score += 100
            enemy2 = newenemy2()
        if enemy2.rect.top > height:
            enemy2 = newenemy2()
        # regenerate enemy3
        if enemy3.ph <= 0:
            newhealthup()
            newmissileup()
            player1.score += 100
            enemy3 = newenemy3()
        if enemy3.rect.top > height:
            enemy3 = newenemy3()

        # roundbullet hit player1
        hits = pygame.sprite.spritecollide(player1,roundbullet_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 10   
        # laser1 hit player1
        hits = pygame.sprite.spritecollide(player1,laser1_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 20    
        # dart hit player1
        hits = pygame.sprite.spritecollide(player1,dart_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 30
        # x hit player1
        hits = pygame.sprite.spritecollide(player1,x_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 35
            
        # meteorite hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,meteorite_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)            
            
        # roundbullet hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,roundbullet_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # laser1 hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,laser1_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # dart hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,dart_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # x hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,x_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # player1 hit boss1
        hits = pygame.sprite.spritecollide(player1,boss1_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss1.ph
            boss1.ph -= player1.ph
            player1.ph -= hurt
            boss1.drawph = True  
        # player1 hit boss2
        hits = pygame.sprite.spritecollide(player1,boss2_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss2.ph
            boss2.ph -= player1.ph
            player1.ph -= hurt
            boss2.drawph = True   
        # player1 hit boss3
        hits = pygame.sprite.spritecollide(player1,boss3_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss3.ph
            boss3.ph -= player1.ph
            player1.ph -= hurt
            boss3.drawph = True
        # player1 hit boss4
        hits = pygame.sprite.spritecollide(player1,boss4_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss4.ph
            boss4.ph -= player1.ph
            player1.ph -= hurt
            boss4.drawph = True
        # player1 hit boss5
        hits = pygame.sprite.spritecollide(player1,boss5_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss5.ph
            boss5.ph -= player1.ph
            player1.ph -= hurt
            boss5.drawph = True
        # mybullet hit boss1
        hits = pygame.sprite.groupcollide(bullet_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        # mybullet hit boss2
        hits = pygame.sprite.groupcollide(bullet_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        # mybullet hit boss3
        hits = pygame.sprite.groupcollide(bullet_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        # mybullet hit boss4
        hits = pygame.sprite.groupcollide(bullet_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        # mybullet hit boss5
        hits = pygame.sprite.groupcollide(bullet_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        # missile hit boss1
        hits = pygame.sprite.groupcollide(missile_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 700
        # missile hit boss2
        hits = pygame.sprite.groupcollide(missile_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 700
        # missile hit boss3
        hits = pygame.sprite.groupcollide(missile_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 700
        # missile hit boss4
        hits = pygame.sprite.groupcollide(missile_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 700
        # missile hit boss5
        hits = pygame.sprite.groupcollide(missile_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 700

        try:
            # boss1 die generate boss2
            if boss1.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss2 = newboss2()
                boss2.ph *= count1
                boss2.fullph *= count1
                boss1.drawph = False
                expl = Explosion(boss1.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss1.kill()
                boss1.ph = 1
            # boss2 die generate boss3
            if boss2.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss3 = newboss3()
                boss3.ph *= count1
                boss3.fullph *= count1
                boss2.drawph = False
                expl = Explosion(boss2.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss2.kill()
                boss2.ph = 1
            # boss3 die generate boss4
            if boss3.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss4 = newboss4()
                boss4.ph *= count1
                boss4.fullph *= count1
                boss3.drawph = False
                expl = Explosion(boss3.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss3.kill()
                boss3.ph = 1
            # boss4 die generate boss5
            if boss4.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                boss5 = newboss5()
                boss5.ph *= count1
                boss5.fullph *= count1
                boss4.drawph = False
                expl = Explosion(boss4.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss4.kill()
                boss4.ph = 1
            # boss5 die 
            if boss5.ph <= 0:
                count1 += 1
                boss5.drawph = False
                expl = Explosion(boss5.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss5.kill()
                boss5.ph = 1
                player1.live = -1
                
        except:
            pass

        #**draw**
        screen.blit(background,(0,0))
        all_sprites.draw(screen)
        drawscore(player1.score,width/2-200,45)
        drawsec(elapsed_seconds,width/2+50,45)
        health(player1.ph,20,50)
        drawlive1(player1.live,40,100)
        drawshield(player1.shield,20,height-120)
        drawmissile(player1.missile,20,height-75)

        # draw enemy1 ph
        try:
            if enemy1.drawph:
                enemy1.enemy_health(enemy1.ph, enemy1.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy2 ph
        try:
            if enemy2.drawph:
                enemy2.enemy_health(enemy2.ph, enemy2.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy3 ph
        try:
            if enemy3.drawph:
                enemy3.enemy_health(enemy3.ph, enemy3.fullph, width/2-75, 85)
        except:
            pass
        # draw boss1 ph
        try:
            if boss1.drawph:
                boss1.enemy_health(boss1.ph, boss1.fullph, width/2-75, 115)
        except:
            pass
        # draw boss2 ph
        try:
            if boss2.drawph:
                boss2.enemy_health(boss2.ph, boss2.fullph, width/2-75, 115)
        except:
            pass
        # draw boss3 ph
        try:
            if boss3.drawph:
                boss3.enemy_health(boss3.ph, boss3.fullph, width/2-75, 115)
        except: 
            pass
        # draw boss4 ph
        try:
            if boss4.drawph:
                boss4.enemy_health(boss4.ph, boss4.fullph, width/2-75, 115)
        except:
            pass
        # draw boss5 ph
        try:
            if boss5.drawph:
                boss5.enemy_health(boss5.ph, boss5.fullph, width/2-75, 115)
        except:
            pass

        pygame.display.update()
        pygame.display.flip()
        fpsClock.tick(fps)

    while player1.live < 0 or boss5.ph < 0:
        
        clock.tick(fps)

    # Event Handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                or not isHiScore
                and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return False
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and not isHiScore):
                return True
            elif (event.type == pygame.KEYDOWN
                  and event.key in Keyboard.keys.keys()
                  and len(nameBuffer) < 8):
                nameBuffer.append(Keyboard.keys[event.key])
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_BACKSPACE
                  and len(nameBuffer) > 0):
                nameBuffer.pop()
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and len(name) > 0):
                Database.setScore(hiScores, (name, player1.score, elapsed_seconds))
                return gameover2()

        if isHiScore:
            hiScoreText = font.render('HIGH SCORE!', 1, RED)
            hiScorePos = hiScoreText.get_rect(
                midbottom=screen.get_rect().center)
            scoreText = font.render(str(player1.score), 1, green)
            scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
            enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
            enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
            nameText = font.render(name, 1, green)
            namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
            textOverlay = zip([hiScoreText, scoreText,
                               enterNameText, nameText],
                              [hiScorePos, scorePos,
                               enterNamePos, namePos])
        else:
            gameOverText = font.render('GAME OVER', 1, BLUE)
            gameOverPos = gameOverText.get_rect(
                center=screen.get_rect().center)
            scoreText = font.render('SCORE: {}'.format(player1.score), 1, BLUE)
            scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
            textOverlay = zip([gameOverText, scoreText],
                              [gameOverPos, scorePos])

    # Update and draw all sprites
        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        all_drawings.update()
        for txt, pos in textOverlay:
            screen.blit(txt, pos)
        pygame.display.flip()
        
def cooperation1():
    start_time = 0
    global cooperative_mode, elapsed_pause_time
    cooperative_mode = True
    pygame.mixer.music.load(path.join(snd_dir, 'game.mp3'))
    pygame.mixer.music.play(-1)
    # set up
    global all_sprites,meteorite_sprites,bullet_sprites,bullet_sprites_2,bullet_sprites_3,bullet_sprites_4
    global bullet_sprites_5,bullet_sprites_6,bulletup_sprites,ultbulletup_sprites,speedup_sprites
    global healthup_sprites,liveup_sprites,enemy1_sprites,enemy2_sprites,roundbullet_sprites
    global boss1_sprites,laser1_sprites,dart_sprites,enemy3_sprites, boss2_sprites,x_sprites,boss3_sprites
    global boss4_sprites,boss5_sprites,shieldup_sprites,shield_sprites,missileup_sprites,missile_sprites,player1,player2
    all_sprites = pygame.sprite.Group()
    meteorite_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    bullet_sprites_2 = pygame.sprite.Group()
    bullet_sprites_3 = pygame.sprite.Group()
    bullet_sprites_4 = pygame.sprite.Group()
    bullet_sprites_5 = pygame.sprite.Group()
    bullet_sprites_6 = pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()

    ultbulletup_sprites=pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()
    speedup_sprites = pygame.sprite.Group()
    healthup_sprites = pygame.sprite.Group()
    liveup_sprites = pygame.sprite.Group()
    enemy1_sprites = pygame.sprite.Group()
    enemy2_sprites = pygame.sprite.Group()
    roundbullet_sprites = pygame.sprite.Group()
    boss1_sprites = pygame.sprite.Group()
    boss4_sprites = pygame.sprite.Group()
    boss5_sprites = pygame.sprite.Group()
    laser1_sprites = pygame.sprite.Group()
    dart_sprites = pygame.sprite.Group()
    enemy3_sprites = pygame.sprite.Group()
    boss2_sprites = pygame.sprite.Group()
    x_sprites = pygame.sprite.Group()
    boss3_sprites = pygame.sprite.Group()
    shieldup_sprites = pygame.sprite.Group()
    shield_sprites = pygame.sprite.Group()
    missileup_sprites = pygame.sprite.Group()
    missile_sprites = pygame.sprite.Group()
    all_drawings = pygame.sprite.Group()
    player1 = Player1()
    all_sprites.add(player1)
    player2 = Player2()
    all_sprites.add(player2)
    for i in range(4):
        newmeteorite()

    enemy1 = newenemy1()
    enemy1.rect.y = -1000
    enemy2 = newenemy2()
    enemy2.rect.y = -3500
    boss1 = newboss1()
    boss1.rect.y = -5000
    enemy3 = newenemy3()
    enemy3.rect.y = -8000
    count1 = 1

    shieldup = newshieldup()
    shieldup.rect.y = -2000
    bulletup = newbulletup()
    bulletup.rect.y = -700
    speedup = newspeedup()
    speedup.rect.y = -2500
    shieldup = newshieldup()
    shieldup.rect.y = -4000
    bulletup = newbulletup()
    bulletup.rect.y = -1500
    speedup = newspeedup()
    speedup.rect.y = -3500
    ultbulletup = newultbulletup()
    ultbulletup.rect.y = - 1800
    bulletup = newultbulletup()
    ultbulletup.rect.y = - 1900

    running = True
    start_time = pygame.time.get_ticks()  # 게임 시작 시간 저장
    elapsed_pause_time = 0  # 초기화

    score = player1.score
    hiScores = Database.getScores()
    isHiScore = len(hiScores) < Database.numScores or score > hiScores[-1][1]
    name = ''
    nameBuffer = []

    while player1.live >= 0 and player2.live >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_PERIOD:
                    if player1.shield > 0:
                        player1.shield -= 1
                        newshield1(player1.rect.center)
                        shield_sound.play()
                if event.key == pygame.K_COMMA:
                    if player1.missile > 0:
                        player1.missile -= 1
                        newmissile(player1.rect.centerx,player1.rect.centery)
                        newmissile(player1.rect.centerx-200,player1.rect.centery)
                        newmissile(player1.rect.centerx+200,player1.rect.centery)
                        missile_sound.play()
                if event.key == pygame.K_z:
                    if player2.shield > 0:
                        player2.shield -= 1
                        newshield2(player2.rect.center)
                        shield_sound.play()
                if event.key == pygame.K_LSHIFT:
                    if player2.missile > 0:
                        player2.missile -= 1
                        newmissile(player1.rect.centerx,player1.rect.centery)
                        newmissile(player1.rect.centerx-200,player1.rect.centery)
                        newmissile(player1.rect.centerx+200,player1.rect.centery)
                        missile_sound.play()
                if event.key == pygame.K_p:
                       pause()
                if event.key == pygame.K_ESCAPE:
                        quitgame()
                if event.key == pygame.K_m:
                    player1.shoot() 
                if event.key == pygame.K_LCTRL:
                    player2.shoot()
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time - elapsed_pause_time
        elapsed_seconds = elapsed_time / 1000
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                sys.exit()
        clock.tick(fps)
        #******update*****
        all_sprites.update()

        # meteor hit player1
        hits = pygame.sprite.spritecollide(player1,meteorite_sprites,True,pygame.sprite.collide_circle)
        for hit in hits:
            player1.ph -= hit.radius * 1.5
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            
        # meteor hit player2
        hits1 = pygame.sprite.spritecollide(player2,meteorite_sprites,True,pygame.sprite.collide_circle)
        for hit in hits1:
            player2.ph -= hit.radius * 1.5
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            newmeteorite()    
  
        # mybullet hit meteor
        hits = pygame.sprite.groupcollide(bullet_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()
                
        # missile hit meteor
        hits = pygame.sprite.groupcollide(missile_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        # player1 get ultbulletup
        hits = pygame.sprite.spritecollide(player1,ultbulletup_sprites,True)
        for hit in hits:
            player1.score += 200
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()

        # player2 get ultbulletup
        hits1 = pygame.sprite.spritecollide(player2,ultbulletup_sprites,True)
        for hit in hits1:
            player1.score += 200
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()

        # player1 get bulletup
        hits = pygame.sprite.spritecollide(player1,bulletup_sprites,True)
        for hit in hits:
            player1.bulletpower += 1
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()
        # player2 get bulletup
        hits1 = pygame.sprite.spritecollide(player2,bulletup_sprites,True)
        for hit in hits1:
            player2.bulletpower += 1
            bulletup_sound.play()
            player2.bulletpower_time = pygame.time.get_ticks()
        # player1 get speedup
        hits = pygame.sprite.spritecollide(player1,speedup_sprites,True)
        for hit in hits:
            player1.shootdelay -= 50
            speedup_sound.play()
        # player2 get speedup
        hits1 = pygame.sprite.spritecollide(player2,speedup_sprites,True)
        for hit in hits1:
            player2.shootdelay -= 50
            speedup_sound.play()
        # player1 get health up
        hits = pygame.sprite.spritecollide(player1,healthup_sprites,True)
        for hit in hits:
            player1.ph += random.randrange(10,70)
            healthup_sound.play()
        # player2 get health up
        hits1 = pygame.sprite.spritecollide(player2,healthup_sprites,True)
        for hit in hits1:
            player2.ph += random.randrange(10,70)
            healthup_sound.play()
        # player1 get liveup
        hits = pygame.sprite.spritecollide(player1,liveup_sprites,True)
        for hit in hits:
            player1.live += 1
            liveup_sound.play()
        # player2 get liveup
        hits1 = pygame.sprite.spritecollide(player2,liveup_sprites,True)
        for hit in hits1:
            player2.live += 1
            liveup_sound.play()
        # player1 get shieldup
        hits = pygame.sprite.spritecollide(player1,shieldup_sprites,True)
        for hit in hits:
            player1.shield += 1
            shieldup_sound.play()
        # player2 get shieldup
        hits1 = pygame.sprite.spritecollide(player2,shieldup_sprites,True)
        for hit in hits1:
            player2.shield += 1
            shieldup_sound.play()
        # player1 get missileup
        hits = pygame.sprite.spritecollide(player1,missileup_sprites,True)
        for hit in hits:
            player1.missile += 1
            missileup_sound.play()
        # player2 get missileup
        hits1 = pygame.sprite.spritecollide(player2,missileup_sprites,True)
        for hit in hits1:
            player2.missile += 1
            missileup_sound.play()

        # player1 hit enemy1
        hits = pygame.sprite.spritecollide(player1,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy1.ph
            enemy1.ph = 0
        # player2 hit enemy1
        hits1 = pygame.sprite.spritecollide(player2,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player2.ph -= enemy1.ph
            enemy1.ph = 0    
        # player1 hit enemy2
        hits = pygame.sprite.spritecollide(player1,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy2.ph
            enemy2.ph = 0
        # player2 hit enemy2
        hits1 = pygame.sprite.spritecollide(player2,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player2.ph -= enemy2.ph
            enemy2.ph = 0
        # player1 hit enemy3
        hits = pygame.sprite.spritecollide(player1,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy3.ph
            enemy3.ph = 0 
        # player2 hit enemy3
        hits1 = pygame.sprite.spritecollide(player2,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player2.ph -= enemy3.ph
            enemy3.ph = 0    
        # mybullet hit enemy1
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        # mybullet hit enemy2
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        # mybullet hit enemy3
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        # missile hit enemy1
        hits = pygame.sprite.groupcollide(missile_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 700
        # missile hit enemy2
        hits = pygame.sprite.groupcollide(missile_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 700
        # missile hit enemy3
        hits = pygame.sprite.groupcollide(missile_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 700
        # regenerate enemy1
        if enemy1.ph <= 0:
            newbulletup()
            player1.score += 100
            enemy1 = newenemy1()
        if enemy1.rect.top > height:
            enemy1 = newenemy1()
        # regenerate enemy2
        if enemy2.ph <= 0:
            newspeedup()
            player1.score += 100
            enemy2 = newenemy2()
        if enemy2.rect.top > height:
            enemy2 = newenemy2()
        # regenerate enemy3
        if enemy3.ph <= 0:
            newhealthup()
            newmissileup()
            player1.score += 100
            enemy3 = newenemy3()
        if enemy3.rect.top > height:
            enemy3 = newenemy3()

        # roundbullet hit player1
        hits = pygame.sprite.spritecollide(player1,roundbullet_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 10
        # roundbullet hit player2
        hits1 = pygame.sprite.spritecollide(player2,roundbullet_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 10    
        # laser1 hit player1
        hits = pygame.sprite.spritecollide(player1,laser1_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 20
        # laser1 hit player2
        hits1 = pygame.sprite.spritecollide(player2,laser1_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 20    
        # dart hit player1
        hits = pygame.sprite.spritecollide(player1,dart_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 30
        # dart hit player2
        hits1 = pygame.sprite.spritecollide(player1,dart_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 30    
        # x hit player1
        hits = pygame.sprite.spritecollide(player1,x_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 35
        # x hit player2
        hits1 = pygame.sprite.spritecollide(player2,x_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 35    

        # meteorite hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,meteorite_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # roundbullet hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,roundbullet_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # laser1 hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,laser1_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # dart hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,dart_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # x hit shield
        hits = pygame.sprite.groupcollide(shield_sprites,x_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # player1 hit boss1
        hits = pygame.sprite.spritecollide(player1,boss1_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss1.ph
            boss1.ph -= player1.ph
            player1.ph -= hurt
            boss1.drawph = True
        # player2 hit boss1
        hits1 = pygame.sprite.spritecollide(player2,boss1_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss1.ph
            boss1.ph -= player2.ph
            player2.ph -= hurt
            boss1.drawph = True    
        # player1 hit boss2
        hits = pygame.sprite.spritecollide(player1,boss2_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss2.ph
            boss2.ph -= player1.ph
            player1.ph -= hurt
            boss2.drawph = True
        # player2 hit boss2
        hits1 = pygame.sprite.spritecollide(player2,boss2_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss2.ph
            boss2.ph -= player2.ph
            player2.ph -= hurt
            boss2.drawph = True    
        # player1 hit boss3
        hits = pygame.sprite.spritecollide(player1,boss3_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss3.ph
            boss3.ph -= player1.ph
            player1.ph -= hurt
            boss3.drawph = True
        # player2 hit boss3
        hits1 = pygame.sprite.spritecollide(player2,boss3_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss3.ph
            boss3.ph -= player2.ph
            player2.ph -= hurt
            boss3.drawph = True
        # player1 hit boss4
        hits = pygame.sprite.spritecollide(player1,boss4_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss4.ph
            boss4.ph -= player1.ph
            player1.ph -= hurt
            boss4.drawph = True
        # player2 hit boss4
        hits1 = pygame.sprite.spritecollide(player2,boss4_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss4.ph
            boss4.ph -= player2.ph
            player2.ph -= hurt
            boss4.drawph = True
        # player1 hit boss5
        hits = pygame.sprite.spritecollide(player1,boss5_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss5.ph
            boss5.ph -= player1.ph
            player1.ph -= hurt
            boss5.drawph = True
        # player2 hit boss5
        hits1 = pygame.sprite.spritecollide(player2,boss5_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss5.ph
            boss5.ph -= player2.ph
            player2.ph -= hurt
            boss5.drawph = True    
        # mybullet hit boss1
        hits = pygame.sprite.groupcollide(bullet_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        # mybullet hit boss2
        hits = pygame.sprite.groupcollide(bullet_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        # mybullet hit boss3
        hits = pygame.sprite.groupcollide(bullet_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        # mybullet hit boss4
        hits = pygame.sprite.groupcollide(bullet_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10
        # mybullet hit boss5
        hits = pygame.sprite.groupcollide(bullet_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        # missile hit boss1
        hits = pygame.sprite.groupcollide(missile_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 700
        # missile hit boss2
        hits = pygame.sprite.groupcollide(missile_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 700
        # missile hit boss3
        hits = pygame.sprite.groupcollide(missile_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 700
        # missile hit boss4
        hits = pygame.sprite.groupcollide(missile_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 700
        # missile hit boss5
        hits = pygame.sprite.groupcollide(missile_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 700

        try:
            # boss1 die generate boss2
            if boss1.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss2 = newboss2()
                boss2.ph *= count1
                boss2.fullph *= count1
                boss1.drawph = False
                expl = Explosion(boss1.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss1.kill()
                boss1.ph = 1
            # boss2 die generate boss3
            if boss2.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss3 = newboss3()
                boss3.ph *= count1
                boss3.fullph *= count1
                boss2.drawph = False
                expl = Explosion(boss2.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss2.kill()
                boss2.ph = 1
            # boss3 die generate boss4
            if boss3.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss4 = newboss4()
                boss4.ph *= count1
                boss4.fullph *= count1
                boss3.drawph = False
                expl = Explosion(boss3.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss3.kill()
                boss3.ph = 1
            # boss4 die generate boss5
            if boss4.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss5 = newboss5()
                boss5.ph *= count1
                boss5.fullph *= count1
                boss4.drawph = False
                expl = Explosion(boss4.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss4.kill()
                boss4.ph = 1
            # boss5 die
            if boss5.ph <= 0:
                count1 += 1
                boss5.drawph = False
                expl = Explosion(boss5.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss5.kill()
                boss5.ph = 1
                player1.live = -1
                player2.live = -1
                
        except:
            pass

        #******draw******
        screen.blit(background,(0,0))
        all_sprites.draw(screen)

        drawscore(player1.score,width/2-135,45)
        drawsec(elapsed_seconds,width/2+40,45)
        
        health(player1.ph,20,50)
        drawlive1(player1.live,40,100)
        drawshield(player1.shield,20,height-120)
        drawmissile(player1.missile,20,height-75)

        health(player2.ph,730,50)
        drawlive2(player2.live,755,100)
        drawshield(player2.shield,770,height-120)
        drawmissile(player2.missile,770,height-75)
        
        # draw enemy1 ph
        try:
            if enemy1.drawph:
                enemy1.enemy_health(enemy1.ph, enemy1.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy2 ph
        try:
            if enemy2.drawph:
                enemy2.enemy_health(enemy2.ph, enemy2.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy3 ph
        try:
            if enemy3.drawph:
                enemy3.enemy_health(enemy3.ph, enemy3.fullph, width/2-75, 85)
        except:
            pass
        # draw boss1 ph
        try:
            if boss1.drawph:
                boss1.enemy_health(boss1.ph, boss1.fullph, width/2-75, 115)
        except:
            pass
        # draw boss2 ph
        try:
            if boss2.drawph:
                boss2.enemy_health(boss2.ph, boss2.fullph, width/2-75, 115)
        except:
            pass
        # draw boss3 ph
        try:
            if boss3.drawph:
                boss3.enemy_health(boss3.ph, boss3.fullph, width/2-75, 115)
        except:
            pass
        # draw boss4 ph
        try:
            if boss4.drawph:
                boss4.enemy_health(boss4.ph, boss4.fullph, width/2-75, 115)
        except:
            pass
        # draw boss5 ph
            try:
                if boss5.drawph:
                    boss5.enemy_health(boss5.ph, boss5.fullph, width/2-75, 115)
            except:
                pass

        pygame.display.update()
        pygame.display.flip()
        fpsClock.tick(fps)

    while player1.live < 0 or player2.live < 0:
        
        clock.tick(fps)

    # Event Handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                or not isHiScore
                and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return False
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and not isHiScore):
                return True
            elif (event.type == pygame.KEYDOWN
                  and event.key in Keyboard.keys.keys()
                  and len(nameBuffer) < 8):
                nameBuffer.append(Keyboard.keys[event.key])
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_BACKSPACE
                  and len(nameBuffer) > 0):
                nameBuffer.pop()
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and len(name) > 0):
                Database.setScore(hiScores, (name, player1.score, elapsed_seconds))
                return gameover1()

        if isHiScore:
            hiScoreText = font.render('HIGH SCORE!', 1, RED)
            hiScorePos = hiScoreText.get_rect(
                midbottom=screen.get_rect().center)
            scoreText = font.render(str(player1.score), 1, green)
            scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
            enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
            enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
            nameText = font.render(name, 1, green)
            namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
            textOverlay = zip([hiScoreText, scoreText,
                               enterNameText, nameText],
                              [hiScorePos, scorePos,
                               enterNamePos, namePos])
        else:
            gameOverText = font.render('GAME OVER', 1, BLUE)
            gameOverPos = gameOverText.get_rect(
                center=screen.get_rect().center)
            scoreText = font.render('SCORE: {}'.format(player1.score), 1, BLUE)
            scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
            textOverlay = zip([gameOverText, scoreText],
                              [gameOverPos, scorePos])

    # Update and draw all sprites
        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        all_drawings.update()
        for txt, pos in textOverlay:
            screen.blit(txt, pos)
        pygame.display.flip()

def cooperation2():
    start_time = 0
    global cooperative_mode, elapsed_pause_time
    cooperative_mode = True
    pygame.mixer.music.load(path.join(snd_dir, 'game.mp3'))
    pygame.mixer.music.play(-1)
    # set up
    global all_sprites,meteorite_sprites,bullet_sprites,bullet_sprites_2,bullet_sprites_3,bullet_sprites_4
    global bullet_sprites_5,bullet_sprites_6,bulletup_sprites,ultbulletup_sprites,speedup_sprites
    global healthup_sprites,liveup_sprites,enemy1_sprites,enemy2_sprites,roundbullet_sprites
    global boss1_sprites,laser1_sprites,dart_sprites,enemy3_sprites, boss2_sprites,x_sprites,boss3_sprites
    global boss4_sprites,boss5_sprites,shieldup_sprites,shield_sprites,missileup_sprites,missile_sprites,player1,player2
    all_sprites = pygame.sprite.Group()
    meteorite_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    bullet_sprites_2 = pygame.sprite.Group()
    bullet_sprites_3 = pygame.sprite.Group()
    bullet_sprites_4 = pygame.sprite.Group()
    bullet_sprites_5 = pygame.sprite.Group()
    bullet_sprites_6 = pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()

    ultbulletup_sprites=pygame.sprite.Group()
    bulletup_sprites = pygame.sprite.Group()
    speedup_sprites = pygame.sprite.Group()
    healthup_sprites = pygame.sprite.Group()
    liveup_sprites = pygame.sprite.Group()
    enemy1_sprites = pygame.sprite.Group()
    enemy2_sprites = pygame.sprite.Group()
    roundbullet_sprites = pygame.sprite.Group()
    boss1_sprites = pygame.sprite.Group()
    boss4_sprites = pygame.sprite.Group()
    boss5_sprites = pygame.sprite.Group()
    laser1_sprites = pygame.sprite.Group()
    dart_sprites = pygame.sprite.Group()
    enemy3_sprites = pygame.sprite.Group()
    boss2_sprites = pygame.sprite.Group()
    x_sprites = pygame.sprite.Group()
    boss3_sprites = pygame.sprite.Group()
    shieldup_sprites = pygame.sprite.Group()
    shield_sprites = pygame.sprite.Group()
    missileup_sprites = pygame.sprite.Group()
    missile_sprites = pygame.sprite.Group()
    all_drawings = pygame.sprite.Group()
    player1 = Player1()
    all_sprites.add(player1)
    player2 = Player2()
    all_sprites.add(player2)
    for i in range(4):
        newmeteorite()

    enemy1 = newenemy1()
    enemy1.rect.y = -1000
    enemy2 = newenemy2()
    enemy2.rect.y = -3500
    boss1 = newboss1()
    boss1.rect.y = -5000
    enemy3 = newenemy3()
    enemy3.rect.y = -8000
    count1 = 1

    shieldup = newshieldup()
    shieldup.rect.y = -2000
    bulletup = newbulletup()
    bulletup.rect.y = -700
    speedup = newspeedup()
    speedup.rect.y = -2500
    shieldup = newshieldup()
    shieldup.rect.y = -4000
    bulletup = newbulletup()
    bulletup.rect.y = -1500
    speedup = newspeedup()
    speedup.rect.y = -3500
    ultbulletup = newultbulletup()
    ultbulletup.rect.y = - 1800
    bulletup = newultbulletup()
    ultbulletup.rect.y = - 1900

    running = True
    start_time = pygame.time.get_ticks()  # 게임 시작 시간 저장
    elapsed_pause_time = 0  # 초기화

    score = player1.score
    hiScores = Database.getScores()
    isHiScore = len(hiScores) < Database.numScores or score > hiScores[-1][1]
    name = ''
    nameBuffer = []

    while player1.live >= 0 and player2.live >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_PERIOD:
                    if player1.shield > 0:
                        player1.shield -= 1
                        newshield1(player1.rect.center)
                        shield_sound.play()
                if event.key == pygame.K_COMMA:
                    if player1.missile > 0:
                        player1.missile -= 1
                        newmissile(player1.rect.centerx,player1.rect.centery)
                        newmissile(player1.rect.centerx-200,player1.rect.centery)
                        newmissile(player1.rect.centerx+200,player1.rect.centery)
                        missile_sound.play()
                if event.key == pygame.K_z:
                    if player2.shield > 0:
                        player2.shield -= 1
                        newshield2(player2.rect.center)
                        shield_sound.play()
                if event.key == pygame.K_LSHIFT:
                    if player2.missile > 0:
                        player2.missile -= 1
                        newmissile(player1.rect.centerx,player1.rect.centery)
                        newmissile(player1.rect.centerx-200,player1.rect.centery)
                        newmissile(player1.rect.centerx+200,player1.rect.centery)
                        missile_sound.play()
                if event.key == pygame.K_p:
                       pause()
                if event.key == pygame.K_ESCAPE:
                        quitgame()
                if event.key == pygame.K_m:
                    player1.shoot() 
                if event.key == pygame.K_LCTRL:
                    player2.shoot()
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time - elapsed_pause_time
        elapsed_seconds = elapsed_time / 1000
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                sys.exit()
        clock.tick(fps)
        #******update*****
        all_sprites.update()

        # meteor hit player1
        hits = pygame.sprite.spritecollide(player1,meteorite_sprites,True,pygame.sprite.collide_circle)
        for hit in hits:
            player1.ph -= hit.radius * 1.5
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            
        # meteor hit player2
        hits1 = pygame.sprite.spritecollide(player2,meteorite_sprites,True,pygame.sprite.collide_circle)
        for hit in hits1:
            player2.ph -= hit.radius * 1.5
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            newmeteorite()    
  
        # mybullet hit meteor
        hits = pygame.sprite.groupcollide(bullet_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10
            bulletup_chance = random.randrange(0,100)
            if bulletup_chance > 95:
                newbulletup()
            speedup_chance = random.randrange(0,100)
            if speedup_chance > 95:
                newspeedup()
            healthup_chance = random.randrange(0,100)
            if healthup_chance > 95:
                newhealthup()
            liveup_chance = random.randrange(0,100)
            if liveup_chance > 99:
                newliveup()
            shieldup_chance = random.randrange(0,100)
            if shieldup_chance > 95:
                newshieldup()
            missileup_chance = random.randrange(0,100)
            if missileup_chance > 90:
                newmissileup()
                
        # missile hit meteor
        hits = pygame.sprite.groupcollide(missile_sprites,meteorite_sprites,True,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            newmeteorite()
            player1.score += 10

        # player1 get ultbulletup
        hits = pygame.sprite.spritecollide(player1,ultbulletup_sprites,True)
        for hit in hits:
            player1.score += 200
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()

        # player2 get ultbulletup
        hits1 = pygame.sprite.spritecollide(player2,ultbulletup_sprites,True)
        for hit in hits1:
            player1.score += 200
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()
            
        # player1 get bulletup
        hits = pygame.sprite.spritecollide(player1,bulletup_sprites,True)
        for hit in hits:
            player1.bulletpower += 1
            bulletup_sound.play()
            player1.bulletpower_time = pygame.time.get_ticks()
        # player2 get bulletup
        hits1 = pygame.sprite.spritecollide(player2,bulletup_sprites,True)
        for hit in hits1:
            player2.bulletpower += 1
            bulletup_sound.play()
            player2.bulletpower_time = pygame.time.get_ticks()
        # player1 get speedup
        hits = pygame.sprite.spritecollide(player1,speedup_sprites,True)
        for hit in hits:
            player1.shootdelay -= 50
            speedup_sound.play()
        # player2 get speedup
        hits1 = pygame.sprite.spritecollide(player2,speedup_sprites,True)
        for hit in hits1:
            player2.shootdelay -= 50
            speedup_sound.play()
        # player1 get health up
        hits = pygame.sprite.spritecollide(player1,healthup_sprites,True)
        for hit in hits:
            player1.ph += random.randrange(10,70)
            healthup_sound.play()
        # player2 get health up
        hits1 = pygame.sprite.spritecollide(player2,healthup_sprites,True)
        for hit in hits1:
            player2.ph += random.randrange(10,70)
            healthup_sound.play()
        # player1 get liveup
        hits = pygame.sprite.spritecollide(player1,liveup_sprites,True)
        for hit in hits:
            player1.live += 1
            liveup_sound.play()
        # player2 get liveup
        hits1 = pygame.sprite.spritecollide(player2,liveup_sprites,True)
        for hit in hits1:
            player2.live += 1
            liveup_sound.play()
        # player1 get shieldup
        hits = pygame.sprite.spritecollide(player1,shieldup_sprites,True)
        for hit in hits:
            player1.shield += 1
            shieldup_sound.play()
        # player2 get shieldup
        hits1 = pygame.sprite.spritecollide(player2,shieldup_sprites,True)
        for hit in hits1:
            player2.shield += 1
            shieldup_sound.play()
        # player1 get missileup
        hits = pygame.sprite.spritecollide(player1,missileup_sprites,True)
        for hit in hits:
            player1.missile += 1
            missileup_sound.play()
        # player2 get missileup
        hits1 = pygame.sprite.spritecollide(player2,missileup_sprites,True)
        for hit in hits1:
            player2.missile += 1
            missileup_sound.play()

        # player1 hit enemy1
        hits = pygame.sprite.spritecollide(player1,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy1.ph
            enemy1.ph = 0
        # player2 hit enemy1
        hits1 = pygame.sprite.spritecollide(player2,enemy1_sprites,False,pygame.sprite.collide_circle)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player2.ph -= enemy1.ph
            enemy1.ph = 0    
        # player1 hit enemy2
        hits = pygame.sprite.spritecollide(player1,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy2.ph
            enemy2.ph = 0
        # player2 hit enemy2
        hits1 = pygame.sprite.spritecollide(player2,enemy2_sprites,False,pygame.sprite.collide_circle)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player2.ph -= enemy2.ph
            enemy2.ph = 0
        # player1 hit enemy3
        hits = pygame.sprite.spritecollide(player1,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player1.ph -= enemy3.ph
            enemy3.ph = 0 
        # player2 hit enemy3
        hits1 = pygame.sprite.spritecollide(player2,enemy3_sprites,False,pygame.sprite.collide_circle)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            player2.ph -= enemy3.ph
            enemy3.ph = 0
        # mybullet hit enemy1
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 10
        # mybullet hit enemy2
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 10
        # mybullet hit enemy3
        hits = pygame.sprite.groupcollide(bullet_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_2,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_3,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_4,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_5,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        hits = pygame.sprite.groupcollide(bullet_sprites_6,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 10
        # missile hit enemy1
        hits = pygame.sprite.groupcollide(missile_sprites,enemy1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy1.drawph = True
            enemy1.ph -= 700
        # missile hit enemy2
        hits = pygame.sprite.groupcollide(missile_sprites,enemy2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy2.drawph = True
            enemy2.ph -= 700
        # missile hit enemy3
        hits = pygame.sprite.groupcollide(missile_sprites,enemy3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            enemy3.drawph = True
            enemy3.ph -= 700
        # regenerate enemy1
        if enemy1.ph <= 0:
            newbulletup()
            player1.score += 100
            enemy1 = newenemy1()
        if enemy1.rect.top > height:
            enemy1 = newenemy1()
        # regenerate enemy2
        if enemy2.ph <= 0:
            newspeedup()
            player1.score += 100
            enemy2 = newenemy2()
        if enemy2.rect.top > height:
            enemy2 = newenemy2()
        # regenerate enemy3
        if enemy3.ph <= 0:
            newhealthup()
            newmissileup()
            player1.score += 100
            enemy3 = newenemy2()
        if enemy3.rect.top > height:
            enemy3 = newenemy3()

        # roundbullet hit player1
        hits = pygame.sprite.spritecollide(player1,roundbullet_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 10
        # roundbullet hit player2
        hits1 = pygame.sprite.spritecollide(player2,roundbullet_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 10    
        # laser1 hit player1
        hits = pygame.sprite.spritecollide(player1,laser1_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 20
        # laser1 hit player2
        hits1 = pygame.sprite.spritecollide(player2,laser1_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 20    
        # dart hit player1
        hits = pygame.sprite.spritecollide(player1,dart_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 30
        # dart hit player1
        hits1 = pygame.sprite.spritecollide(player2,dart_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 30    
        # x hit player1
        hits = pygame.sprite.spritecollide(player1,x_sprites,True)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player1.ph -= 35
        # x hit player2
        hits1 = pygame.sprite.spritecollide(player2,x_sprites,True)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            player2.ph -= 35    

        # meteorite hit shield1
        hits = pygame.sprite.groupcollide(shield_sprites,meteorite_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # roundbullet hit shield1
        hits = pygame.sprite.groupcollide(shield_sprites,roundbullet_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # laser1 hit shield1
        hits = pygame.sprite.groupcollide(shield_sprites,laser1_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion((hit.rect.centerx,hit.rect.centery-50),'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # dart hit shield1
        hits = pygame.sprite.groupcollide(shield_sprites,dart_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
        # x hit shield1
        hits = pygame.sprite.groupcollide(shield_sprites,x_sprites,False,True,pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)

        # player1 hit boss1
        hits = pygame.sprite.spritecollide(player1,boss1_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss1.ph
            boss1.ph -= player1.ph
            player1.ph -= hurt
            boss1.drawph = True
        # player2 hit boss1
        hits1 = pygame.sprite.spritecollide(player2,boss1_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss1.ph
            boss1.ph -= player2.ph
            player2.ph -= hurt
            boss1.drawph = True    
        # player1 hit boss2
        hits = pygame.sprite.spritecollide(player1,boss2_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss2.ph
            boss2.ph -= player1.ph
            player1.ph -= hurt
            boss2.drawph = True
        # player2 hit boss2
        hits1 = pygame.sprite.spritecollide(player2,boss2_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss2.ph
            boss2.ph -= player2.ph
            player2.ph -= hurt
            boss2.drawph = True    
        # player1 hit boss3
        hits = pygame.sprite.spritecollide(player1,boss3_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss3.ph
            boss3.ph -= player1.ph
            player1.ph -= hurt
            boss3.drawph = True
        # player2 hit boss3
        hits1 = pygame.sprite.spritecollide(player2,boss3_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss3.ph
            boss3.ph -= player2.ph
            player2.ph -= hurt
            boss3.drawph = True
        # player1 hit boss4
        hits = pygame.sprite.spritecollide(player1,boss4_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss4.ph
            boss4.ph -= player1.ph
            player1.ph -= hurt
            boss4.drawph = True
        # player2 hit boss4
        hits1 = pygame.sprite.spritecollide(player2,boss4_sprites,False)
        for hit in hits1:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss4.ph
            boss4.ph -= player2.ph
            player2.ph -= hurt
            boss4.drawph = True
        # player1 hit boss5
        hits = pygame.sprite.spritecollide(player1,boss5_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss5.ph
            boss5.ph -= player1.ph
            player1.ph -= hurt
            boss5.drawph = True
        # player1 hit boss5
        hits1 = pygame.sprite.spritecollide(player2,boss5_sprites,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'large')
            explodebg_sound.play()
            all_sprites.add(expl)
            hurt = boss5.ph
            boss5.ph -= player2.ph
            player2.ph -= hurt
            boss5.drawph = True
        # mybullet hit boss1
        hits = pygame.sprite.groupcollide(bullet_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 10

        # mybullet hit boss2
        hits = pygame.sprite.groupcollide(bullet_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 10

        # mybullet hit boss3
        hits = pygame.sprite.groupcollide(bullet_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 10

        # mybullet hit boss4
        hits = pygame.sprite.groupcollide(bullet_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 10

        # mybullet hit boss5
        hits = pygame.sprite.groupcollide(bullet_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_2,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_3,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_4,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_5,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10

        hits = pygame.sprite.groupcollide(bullet_sprites_6,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'small')
            explodesm_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 10
        # missile hit boss1
        hits = pygame.sprite.groupcollide(missile_sprites,boss1_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss1.drawph = True
            boss1.ph -= 700
        # missile hit boss2
        hits = pygame.sprite.groupcollide(missile_sprites,boss2_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss2.drawph = True
            boss2.ph -= 700
        # missile hit boss3
        hits = pygame.sprite.groupcollide(missile_sprites,boss3_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss3.drawph = True
            boss3.ph -= 700
        # missile hit boss4
        hits = pygame.sprite.groupcollide(missile_sprites,boss4_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss4.drawph = True
            boss4.ph -= 700
        # missile hit boss5
        hits = pygame.sprite.groupcollide(missile_sprites,boss5_sprites,True,False)
        for hit in hits:
            expl = Explosion(hit.rect.center,'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            boss5.drawph = True
            boss5.ph -= 700

        try:
            # boss1 die generate boss2
            if boss1.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss2 = newboss2()
                boss2.ph *= count1
                boss2.fullph *= count1
                boss1.drawph = False
                expl = Explosion(boss1.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss1.kill()
                boss1.ph = 1
            # boss2 die generate boss3
            if boss2.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss3 = newboss3()
                boss3.ph *= count1
                boss3.fullph *= count1
                boss2.drawph = False
                expl = Explosion(boss2.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss2.kill()
                boss2.ph = 1
            # boss3 die generate boss4
            if boss3.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss4 = newboss4()
                boss4.ph *= count1
                boss4.fullph *= count1
                boss3.drawph = False
                expl = Explosion(boss3.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss3.kill()
                boss3.ph = 1
            # boss4 die generate boss5
            if boss4.ph <= 0:
                count1 += 1
                newbulletup()
                newspeedup()
                newliveup()
                newliveup()
                boss5 = newboss5()
                boss5.ph *= count1
                boss5.fullph *= count1
                boss4.drawph = False
                expl = Explosion(boss4.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss4.kill()
                boss4.ph = 1
            # boss5 die
            if boss5.ph <= 0:
                count1 += 1
                boss5.drawph = False
                expl = Explosion(boss5.rect.center,'death')
                explodedeath_sound.play()
                all_sprites.add(expl)
                boss5.kill()
                boss5.ph = 1
                player1.live = -1
                player2.live = -1
        except:
            pass

        #******draw******
        screen.blit(background,(0,0))
        all_sprites.draw(screen)

        drawscore(player1.score,width/2-200,45)
        drawsec(elapsed_seconds,width/2+50,45)
        
        health(player1.ph,20,50)
        drawlive1(player1.live,40,100)
        drawshield(player1.shield,20,height-120)
        drawmissile(player1.missile,20,height-75)

        health(player2.ph,1110,50)
        drawlive2(player2.live,1135,100)
        drawshield(player2.shield,1150,height-120)
        drawmissile(player2.missile,1150,height-75)
        
        # draw enemy1 ph
        try:
            if enemy1.drawph:
                enemy1.enemy_health(enemy1.ph, enemy1.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy2 ph
        try:
            if enemy2.drawph:
                enemy2.enemy_health(enemy2.ph, enemy2.fullph, width/2-75, 85)
        except:
            pass
        # draw enemy3 ph
        try:
            if enemy3.drawph:
                enemy3.enemy_health(enemy3.ph, enemy3.fullph, width/2-75, 85)
        except:
            pass
        # draw boss1 ph
        try:
            if boss1.drawph:
                boss1.enemy_health(boss1.ph, boss1.fullph, width/2-75, 115)
        except:
            pass
        # draw boss2 ph
        try:
            if boss2.drawph:
                boss2.enemy_health(boss2.ph, boss2.fullph, width/2-75, 115)
        except:
            pass
        # draw boss3 ph
        try:
            if boss3.drawph:
                boss3.enemy_health(boss3.ph, boss3.fullph, width/2-75, 115)
        except:
            pass
        # draw boss4 ph
        try:
            if boss4.drawph:
                boss4.enemy_health(boss4.ph, boss4.fullph, width/2-75, 115)
        except:
            pass
        # draw boss5 ph
        try:
            if boss5.drawph:
                boss5.enemy_health(boss5.ph, boss5.fullph, width/2-75, 115)
        except:
            pass

        pygame.display.update()
        pygame.display.flip()
        fpsClock.tick(fps)

    while player1.live < 0 or player2.live < 0:
        
        clock.tick(fps)

    # Event Handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                or not isHiScore
                and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return False
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and not isHiScore):
                return True
            elif (event.type == pygame.KEYDOWN
                  and event.key in Keyboard.keys.keys()
                  and len(nameBuffer) < 8):
                nameBuffer.append(Keyboard.keys[event.key])
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_BACKSPACE
                  and len(nameBuffer) > 0):
                nameBuffer.pop()
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and len(name) > 0):
                Database.setScore(hiScores, (name, player1.score, elapsed_seconds))
                return gameover2()

        if isHiScore:
            hiScoreText = font.render('HIGH SCORE!', 1, RED)
            hiScorePos = hiScoreText.get_rect(
                midbottom=screen.get_rect().center)
            scoreText = font.render(str(player1.score), 1, green)
            scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
            enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
            enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
            nameText = font.render(name, 1, green)
            namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
            textOverlay = zip([hiScoreText, scoreText,
                               enterNameText, nameText],
                              [hiScorePos, scorePos,
                               enterNamePos, namePos])
        else:
            gameOverText = font.render('GAME OVER', 1, BLUE)
            gameOverPos = gameOverText.get_rect(
                center=screen.get_rect().center)
            scoreText = font.render('SCORE: {}'.format(player1.score), 1, BLUE)
            scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
            textOverlay = zip([gameOverText, scoreText],
                              [gameOverPos, scorePos])

    # Update and draw all sprites
        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        all_drawings.update()
        for txt, pos in textOverlay:
            screen.blit(txt, pos)
        pygame.display.flip()

running = True
def change_screen_size(width, height):
    global screen
    pygame.display.set_mode((width, height))
    running = pygame.display.set_mode((width, height))

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

label("Change screen size",width/2-270,140,60,white)
label("K_1 : 900 x 750",width/2-220,285,60,purple)
label("K_2 : 1280 x 900",width/2-220,420,60,green)
press_key('0')
while running:
        for event in pygame.event.get():        
            if event.type == KEYUP:
                if event.key == K_1:
                    change_screen_size(900, 750)
                    width, height = 900, 750
                    screen = pygame.display.set_mode((900, 750))
                    intro1()
                elif event.key == K_2:
                    change_screen_size(1280, 900)
                    width, height = 1280, 900
                    screen = pygame.display.set_mode((1280, 900))
                    intro2()

                pygame.display.update()
                pygame.display.flip()

intro1()
quitgame()
