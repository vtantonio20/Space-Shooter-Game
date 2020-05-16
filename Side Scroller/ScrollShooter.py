import pygame
import sys
import math
import random
pygame.init()

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
YELLOW   = ( 255, 235,   0)
BLUE     = (   0,   0, 255)

class Player():
    PLAYER_SHOOT_SOUND = pygame.mixer.Sound(r'assets\laser2.wav')
    PLAYER_HIT_SOUND = pygame.mixer.Sound(r'assets\hit.wav')
    PLAYER_HIT_SOUND.set_volume(.25)
    def __init__(self, screen, xpos, ypos, bulletList , health=150):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.bullets = bulletList

        self.speed = 5

        self.lastShot = pygame.time.get_ticks()
        self.coolDownTime = 300

        self.playerImage = pygame.image.load(r'assets\play.png')
        self.playerImage = pygame.transform.rotate(self.playerImage, 270)
        self.playerImage = pygame.transform.scale(self.playerImage, (50,50))

        self.xsize = self.playerImage.get_width()
        self.ysize = self.playerImage.get_height()
        self.health = health

        self.playerRect = self.playerImage.get_rect(center = (X_SCREEN_SIZE -self.xpos, Y_SCREEN_SIZE- self.ypos))

    def show_player(self):
        self.screen.blit(self.playerImage, (self.xpos, self.ypos))

    def move_player(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.bound_pos(0):
            self.ypos -= self.speed
        if key[pygame.K_a] and self.bound_pos(1):
            self.xpos -= self.speed
        if key[pygame.K_s] and self.bound_pos(2):
            self.ypos += self.speed
        if key[pygame.K_d] and self.bound_pos(3):
            self.xpos += self.speed
        self.playerRect = self.playerImage.get_rect(center = (X_SCREEN_SIZE -self.xpos, Y_SCREEN_SIZE- self.ypos))

    def player_shoot(self, bulletList):
        key = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and len(bulletList) < 5 and now - self.lastShot >= self.coolDownTime:
            self.PLAYER_SHOOT_SOUND.play()
            self.lastShot = now
            self.bullets.append(Projectile(self.screen, GREEN, self.xpos + self.xsize, self.ypos + round(self.ysize/2 -3) , 15 ))

    def bound_pos(self, check_type):
        if self.ypos <= 0  and check_type == 0:
            return False
        if self.xpos <= 5 and check_type == 1:
            return False
        if self.ypos >= Y_SCREEN_SIZE - self.ysize  and check_type ==2:
            return False
        if self.xpos >= X_SCREEN_SIZE/2 - self.xsize -5 and check_type ==3:
            return False
        return True

    def do_damage(self, damage = 0):
        self.health -= damage
        self.PLAYER_HIT_SOUND.play()

    def set_health(self, health=150):
        self.health = health

class Projectile():
    LASER_IMAGE = pygame.image.load(r'assets\bullet2.png')
    LASER_IMAGE = pygame.transform.scale2x(LASER_IMAGE)
    LASER_IMAGE2 = pygame.image.load(r'assets\bullet.png')
    LASER_IMAGE2 = pygame.transform.scale2x(LASER_IMAGE2)

    def __init__(self, screen, color, xpos, ypos, xsize, bullType = 'p'):
        self.screen = screen
        self.color = color
        self.xpos = xpos
        self.ypos = ypos
        self.xsize = xsize
        self.bullType = bullType

        if self.bullType == 'p':
            self.bulletImage = self.LASER_IMAGE
            self.bulletImage = pygame.transform.rotate(self.LASER_IMAGE, 270)
        elif self.bullType == 'e':
            self.bulletImage = self.LASER_IMAGE2
            self.bulletImage = pygame.transform.rotate(self.LASER_IMAGE2, 90)

        self.bulletRect = self.bulletImage.get_rect()

    def move_bullet(self, vel ,xdir):
        self.xpos += vel *xdir

    def show_bullet(self):
        self.bulletRect = self.screen.blit(self.bulletImage, (self.xpos, self.ypos))

class Enemy():
    ENEMY_IMAGE =  pygame.image.load(r'assets\enemy.png')
    def __init__(self, screen,xpos, ypos, dir):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.ydir = dir

        self.enemyImage =  pygame.image.load(r'assets\enemy.png')
        self.enemyImage = pygame.transform.rotate(self.enemyImage, 90)
        self.enemyImage = pygame.transform.scale(self.enemyImage, (40,40))
        self.shieldImage = pygame.image.load(r'assets\sheild.png')
        self.shieldImage = pygame.transform.scale(self.shieldImage, (60, 60))
        self.enemyRect = self.enemyImage.get_rect(center =(0,0))

        self.isSheilded = True

        self.state = 'spawn'

        self.waiting = False

    def show_enemy(self):
        if self.isSheilded:
            self.enemyRect = self.screen.blit(self.shieldImage, (self.xpos -10, self.ypos -10))
            self.screen.blit(self.enemyImage, (self.xpos, self.ypos))
            self.state = 'spawn'
        else:
            self.state = 'battle'
            self.enemyRect = self.screen.blit(self.enemyImage, (self.xpos, self.ypos))

    def spawn_path(self, oEnemies, battlePos, sparks=[], wave=1):
        #this will be the waiting positionx
        checked = False
        if len(oEnemies) > 0:
            xwait = int(max(oe.xpos for oe in oEnemies ) +60)
        else:
            xwait = battlePos

        if self.state == 'spawn':
            #gets into waiting spot
            if self.xpos >= xwait and not self.waiting or len(oEnemies) == 0:
                self.move_xenemy(wave)
            elif self.xpos > battlePos:
                for oe in oEnemies:
                    if oe.ypos == self.ypos and oe.state != 'battle' and oe.xpos <= 560:
                        self.waiting = True
                        checked = True
                        break
                    if oe.state == 'battle' and (oe.ypos +50 > self.ypos and oe.ypos -50 < self.ypos) and self.xpos <= 560:
                        self.waiting = True
                        checked = True
                        break
                    else:
                        self.waiting = False
                if len(sparks) > 0 and not checked:
                    for sp in sparks:
                        if sp.ypos + 50 > self.ypos and sp.ypos -50 < self.ypos:
                            self.waiting = True
                            break
                        else:
                            self.waiting = False
                if not self.waiting:
                    self.move_xenemy(wave)
            elif self.xpos == battlePos:
                self.state = 'battle'

    def move_xenemy(self, wave =1):
        multiplier = math.ceil(wave/2) if wave < 9 else  5
        self.xpos -= 1*math.ceil(wave/2)

    def move_yenemy(self, wave =1):
        multiplier = math.ceil(wave/2) if wave < 4 else  2
        self.ypos += 1 * self.ydir * multiplier

    def enemy_shoot(self, time, coolDownTime, enemyBullets):
        if time % coolDownTime == 0 and not self.isSheilded and random.randint(0,4) > 1:
            enemyBullets.append(Projectile(self.screen, YELLOW, self.xpos - int(self.enemyImage.get_width()/2), self.ypos + int(self.enemyImage.get_width()/2), 30, 'e') )

class Sparks():
    def __init__(self, xpos, ypos, timer , type='e'):
        self.xpos = xpos + 15
        self.ypos = ypos + 15

        self.timer = timer
        self.awakeTimer = pygame.time.get_ticks()
        self.type = type

        if self.type == 'e':
            self.SPARK_IMAGE = pygame.image.load(r'assets\spark.png')
        else:
            self.SPARK_IMAGE = pygame.image.load(r'assets\spark2.png')

        self.sparkEnemyImage = self.SPARK_IMAGE

    def show_sparks(self):
        now = pygame.time.get_ticks() - self.awakeTimer
        if self.sparkEnemyImage.get_width() <= 40:
            self.sparkEnemyImage = pygame.transform.scale(self.SPARK_IMAGE, ( int(now/7.5), int(now/7.5)))
            self.xpos -= int(math.sqrt(now)/10)
            self.ypos -= int(math.sqrt(now)/10)

        if now < self.timer:
            screen.blit(self.sparkEnemyImage, (self.xpos, self.ypos))
            return True
        else:
            return False

class BackGround():
    def __init__(self, screen, image):
        self.image = pygame.image.load(image)

class PowerUp():
    HEALTH_IMAGE = pygame.image.load(r'assets\health.png')
    def __init__(self, screen, ypos, type='health'):
        self.screen = screen
        self.type = type
        self.xpos = X_SCREEN_SIZE
        self.ypos = random.randint(50, Y_SCREEN_SIZE-50)

        self.powerUpImage = self.HEALTH_IMAGE
        self.powerUpRect = self.powerUpImage.get_rect()

    def show_power_up(self):
        screen.blit(self.powerUpImage, ( self.xpos,self.ypos ))
    def move_power_up(self, wave):
        if wave <= 6:
            self.xpos -=1*wave
        else:
            self.xpos -= 6

        self.powerUpRect = self.powerUpImage.get_rect(center = (X_SCREEN_SIZE -self.xpos, Y_SCREEN_SIZE- self.ypos))
#-------------------------------------------------------------------------------------

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            sys.exit()

def hurt_player(player, damage, wave):
    player.do_damage(damage)

def redraw_text(health, clock, wave):
    screenText = fpsFont.render(str(int(clock.get_fps())), 100, YELLOW)
    screen.blit(screenText, (25, 25))
    screenText = waveFont.render('Wave: ' + str(wave), 100, RED)
    screen.blit(screenText, (X_SCREEN_SIZE- 125, 15))
    screenText = healthFont.render('Health: ' + str(health), 100, GREEN)
    screen.blit(screenText, (25, Y_SCREEN_SIZE-25))

def redraw_game(player, pbullets, enemyList, ebullets, sparks,clock, wave, powerups):
    redraw_text(player.health,clock,wave)
    for po in powerups:
        po.move_power_up(wave)
        po.show_power_up()
        if po.xpos <0:
            powerups.pop(powerups.index(po))
        elif po.powerUpRect.colliderect(player.playerRect):
            player.set_health()
            powerups.pop(powerups.index(po))

    player.show_player()
    player.move_player()
    player.player_shoot(pbullets)

    for pbullet in pbullets:
        pbullet.show_bullet()
    for enemy in enemyList:
        enemy.show_enemy()
    for ebullet in ebullets:
        ebullet.show_bullet()
    for spark in sparks:
        if spark.show_sparks():
            pass
        else:
            sparks.pop(sparks.index(spark))


    pygame.display.update()

def move_p_bullets(pbullets):
    for pbullet in pbullets:
        if pbullet.xpos < X_SCREEN_SIZE and pbullet.xpos > 0:
            pbullet.move_bullet(15, 1)
        else:
            pbullets.pop(pbullets.index(pbullet))

def continue_spawing_wave(numOfEnemies, enemyList, spawn, time):
    direction = 1 if len(enemyList) % 2 == 0 else  -1

    currSpawn = spawn
    if len(enemyList) ==0:
        enemyList.append(Enemy(screen, 750, spawn, direction))
        return True
    if len(enemyList) < numOfEnemies and currSpawn < Y_SCREEN_SIZE and check_queue_full(enemyList, currSpawn):
        enemyList.append(Enemy(screen, 750, currSpawn, direction))
        return True
    else:
        currSpawn +=100
        if len(enemyList) < numOfEnemies and currSpawn < Y_SCREEN_SIZE and check_queue_full(enemyList, currSpawn):
            enemyList.append(Enemy(screen, 750, currSpawn, direction))
            return True
        else:
            currSpawn +=100
            if len(enemyList) < numOfEnemies and currSpawn < Y_SCREEN_SIZE and check_queue_full(enemyList, currSpawn):
                enemyList.append(Enemy(screen, 750, currSpawn, direction))
                return True
            else:
                currSpawn +=100
                if len(enemyList) < numOfEnemies and currSpawn < Y_SCREEN_SIZE and check_queue_full(enemyList, currSpawn):
                    enemyList.append(Enemy(screen, 750, currSpawn, direction))
                    return True
    return False

def check_queue_full(enemyList, yspawn):
    for e in enemyList:
        if e.ypos == yspawn and e.xpos > 690:
            return False
    return True

def move_e_bullets(player, enemyBullets, enemyBulletDamage, wave):
    for ebullet in enemyBullets:
        if player.xpos <= ebullet.xpos <= player.xpos +50  and ebullet.ypos <=player.ypos + 40 and ebullet.ypos >= player.ypos:
            hurt_player(player, enemyBulletDamage, wave)
            enemyBullets.pop(enemyBullets.index(ebullet))
            break
        elif X_SCREEN_SIZE > ebullet.xpos > 0:
            ebullet.move_bullet(15, -1)
        else:
            enemyBullets.pop(enemyBullets.index(ebullet))

def kill_enemies(enemy ,enemyList, bulletList, sparks):
    for bull in bulletList:
        if enemy.enemyRect.colliderect(bull.bulletRect):
            xpos = enemy.xpos
            ypos = enemy.ypos
            if not enemy.isSheilded:
                sparks.append(Sparks(xpos,ypos, 750))

            bulletList.pop(bulletList.index(bull))
            return True
    return False

def e_move(e, oEnemies, battlePos, sparks, wave):
        if e.xpos > battlePos:
            e.spawn_path(oEnemies, battlePos, sparks, wave)
        else:
            e.isSheilded = False
            wait = False
            for oe in oEnemies:
                if oe.waiting == True:
                        wait = True
                        break
            e.move_yenemy(wave)

def draw_end_game(player,wave, clock, enemyList, sparks):
    redraw_text(player.health,clock, wave)
    for sp in sparks:
        sp.show_sparks()
    for enemy in enemyList:
        enemy.show_enemy()

def spawn_power_up(powerups, numOfEnemies,wave):
    #25 % chance
    if random.randint(0,4*numOfEnemies) <= 1*wave and len(powerups) <= 2:
        powerups.append(PowerUp(screen, random.randint(50, Y_SCREEN_SIZE-50)))
        return True
    return False

#---------------------------------------------------------------------------------
X_SCREEN_SIZE= 800
Y_SCREEN_SIZE =450
screen = pygame.display.set_mode((X_SCREEN_SIZE, Y_SCREEN_SIZE))
music = pygame.mixer.music.load(r'assets\music.wav')
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(-1)
bg = BackGround(screen, r'assets\space_bg.jpg')
FPS = 60
fpsFont = pygame.font.SysFont(None, 50)
waveFont = pygame.font.SysFont(None, 40)
healthFont = pygame.font.SysFont(None, 30)
gameOverFont = pygame.font.SysFont(None, 50)

def main():
    xBgScroll = 0
    clock = pygame.time.Clock()
    bullets = []
    user = Player(screen,50, 210, bullets)
    enemies = []
    enemyBullets = []
    sparks = []
    powerups = []
    time = 0
    battlePos = 500
    spawn = 50
    numOfEnemies = 4
    enemiesAddedPerWave =4
    enemyBulletDamage = 25
    epreviouslySpawned = 0
    wave = 1
    running = True
    spawnedPowerUps = 0
    while running:
        events()
        #Background scroll must be in while loop
        rel_x = xBgScroll % bg.image.get_rect().width
        screen.blit(bg.image,(rel_x - bg.image.get_rect().width,0))
        if rel_x < 800:
            screen.blit(bg.image,(rel_x, 0))
        xBgScroll-= 1* math.ceil(wave/2)

        #this if elif will limit amount of enemies in a wave
        if numOfEnemies > epreviouslySpawned:
            if continue_spawing_wave(numOfEnemies, enemies, spawn, time):
                epreviouslySpawned+=1
        elif numOfEnemies == epreviouslySpawned and len(enemies) == 0:
            numOfEnemies+=enemiesAddedPerWave
            epreviouslySpawned = 0
            wave +=1
            spawnedPowerUps = 0
            user.set_health()

        redraw_game(user, bullets, enemies,enemyBullets,sparks, clock, wave, powerups)
        move_p_bullets(bullets)
        move_e_bullets(user, enemyBullets, enemyBulletDamage, wave)

        #time %10 to avoid clipping
        for e in enemies:
            if e.ypos <= 0:
                e.ydir *= -1
            elif e.ypos >= (Y_SCREEN_SIZE - 40):
                e.ydir *= -1

            checkEnemies = enemies.copy()
            checkEnemies.pop(enemies.index(e))

            if kill_enemies(e, enemies, bullets, sparks) and not e.isSheilded:
                enemies.pop(enemies.index(e))
                if spawn_power_up(powerups, numOfEnemies, wave) and spawnedPowerUps <= 5:
                    spawnedPowerUps +=1

            #this for loop will check if the enemies collide and if they do it will change their directiosn
            for ce in checkEnemies:
                if e.enemyRect.colliderect(ce.enemyRect):
                    e.ydir *= -1
            if len(sparks) > 0:
                for sp in sparks:
                    if e.ypos == sp.ypos + 20 or e.ypos + 20 == sp.ypos:
                        e.ydir *= -1

            e_move(e, checkEnemies, battlePos, sparks, wave)
            e.enemy_shoot(time, 50, enemyBullets)

        time+=1
        clock.tick(FPS)

        #GAME OVER
        if user.health <= 0:
            sparks.append(Sparks(user.xpos + 25, user.ypos +25, 1000, 'p'))
            running = False
#----------------------------------------END OF GAME
    xBgScroll = 0
    while True:
        rel_x = xBgScroll % bg.image.get_rect().width
        screen.blit(bg.image,(rel_x - bg.image.get_rect().width,0))
        if rel_x < 800:
            screen.blit(bg.image,(rel_x, 0))
        xBgScroll-= 1*wave
        draw_end_game(user, wave, clock, enemies, sparks)
        screenText = gameOverFont.render('Game Over!', 100, WHITE)
        screen.blit(screenText, (300, int(Y_SCREEN_SIZE/3)))
        screenText = gameOverFont.render('Press r to restart.', 100, WHITE)
        screen.blit(screenText, (250, int(Y_SCREEN_SIZE/3) + screenText.get_height() + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()

                
main()
