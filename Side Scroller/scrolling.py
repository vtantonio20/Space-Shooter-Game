import pygame
import sys
pygame.init()



BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
YELLOW   = ( 255, 235,   0)
BLUE     = (   0,   0, 255)

class Player():
    def __init__(self, screen, xpos, ypos, xsize, ysize, bulletList):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.xsize = xsize
        self.ysize = ysize
        self.speed = 6
        self.bullets = bulletList
        self.lastShot = pygame.time.get_ticks()
        self.coolDownTime = 300
        self.playerRect = pygame.draw.rect(self.screen, WHITE , (self.xpos ,self.ypos, self.xsize, self.ysize), 2)

    def show_player(self):
        self.playerRect = pygame.draw.rect(self.screen, WHITE , (self.xpos ,self.ypos, self.xsize, self.ysize), 2)

    def get_player_rect(self):
        return self.playerRect

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

    def player_shoot(self):
        key = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and len(bullets) < 5 and now - self.lastShot >= self.coolDownTime:
            self.lastShot = now
            self.bullets.append(Projectile(self.screen, GREEN, self.xpos + self.xsize, self.ypos + round(self.ysize/2)))

    def bound_pos(self, check_type):
        if self.ypos <= 10  and check_type == 0:
            return False
        if self.xpos <= 5 and check_type == 1:
            return False
        if self.ypos >= Y_SCREEN_SIZE - self.ysize -5 and check_type ==2:
            return False
        if self.xpos >= X_SCREEN_SIZE / 2 - self.xsize -5 and check_type ==3:
            return False
        return True

class Projectile():
    def __init__(self, screen, color, xpos, ypos):
        self.screen = screen
        self.color = color
        self.xpos = xpos
        self.ypos = ypos

    def move_bullet(self, vel ,xdir):
        self.xpos += vel *xdir
    def show_bullet(self):
        self.bulletRect = pygame.draw.rect(self.screen, self.color, (self.xpos, self.ypos, 15, 5))

    def get_bullet_rect(self):
        return self.bulletRect


        #bullets.append(Projectile)

class Enemy():
    def __init__(self, screen,xpos, ypos, size, dir):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.moveSpeed = 2
        self.size = size
        self.ydir = dir
        self.enemyRect = pygame.draw.rect(self.screen, RED, (self.xpos, self.ypos, size, size), 5)

    def show_enemy(self):
        self.enemyRect = pygame.draw.rect(self.screen, RED, (self.xpos, self.ypos, self.size, self.size), 5)

    def get_enemy_rect(self):
        return self.enemyRect

    def check_enemy_collisions(self,enemies):
        if self.enemyRect.colliderect(enemies):
            self.set_enemy_direction()
            self.ypos += 2*self.ydir

    def check_bullet_collisons(self, bullets):
        if self.enemyRect.colliderect(bullets):
            return True
        else:
            return False

    def move_enemy(self):
        if self.ydir > 0:
            speed = self.moveSpeed *self.ydir - 1
        else:
            speed = self.moveSpeed * self.ydir + 1
        self.ypos += speed
        #self.xpos += speed
    def get_enemy_pos(self):
        return self.ypos

    def set_enemy_direction(self):
        if self.ydir == 1:
            self.ydir = -1
        else:
            self.ydir = 1

    def enemy_shoot(self, time, coolDownTime, enemyBullets):
        if time % coolDownTime == 0:
            enemyBullets.append(Projectile(self.screen, YELLOW, self.xpos - int(self.size /2), self.ypos + int(self.size /2)))
            print("enemy shoot")
class BackGround():
    def __init__(self, screen, image):
        self.image = pygame.image.load(image)

#-------------------------------------------------------------------------------------


X_SCREEN_SIZE= 800
Y_SCREEN_SIZE =450
screen = pygame.display.set_mode((X_SCREEN_SIZE, Y_SCREEN_SIZE))
bg = BackGround(screen, r'assets\space_bg.jpg')

xBgScroll = 0


clock = pygame.time.Clock()

bullets = []
user = Player(screen,50, 210, 40, 25 , bullets)

enemies = []
enemyBullets = []


def events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            sys.exit()

def redraw_game():
    user.show_player()
    user.move_player()
    user.player_shoot()
    for bullet in bullets:
        bullet.show_bullet()
    for enemy in enemies:
        enemy.show_enemy()
    for enemyBulls in enemyBullets:
        enemyBulls.show_bullet()
    pygame.display.update()


time = 0
def spawn_wave(numOfEnemies, wave):
    if time % 100 == 0:
        if 1 < len(enemies) <=  numOfEnemies and check_spawn_pos(enemies):
            if len(enemies) % 2 ==0:
                enemies.append(Enemy(screen, 500, 212, 25, 1))
            else:
                enemies.append(Enemy(screen, 500, 212, 25, -1))
        elif len(enemies) <= 1:
            if len(enemies) % 2 ==0:
                enemies.append(Enemy(screen, 500, 212, 25, 1))
            else:
                enemies.append(Enemy(screen, 500, 212, 25, -1))
        else:
            print('cant spawn')


def check_spawn_pos(enemyList):
    for e, ex in enumerate(enemyList):
        if int(ex.get_enemy_pos()) > 182 and int(ex.get_enemy_pos()) < 242:
            return False
            break

    return True
def kill_enemies(enemy ,enemyList, bulletList):
    for bull in bulletList:
        if enemy.check_bullet_collisons(bull.get_bullet_rect()):
            enemies.pop(enemyList.index(enemy))
            break

while True:
    events(user)
    rel_x = xBgScroll % bg.image.get_rect().width
    screen.blit(bg.image,(rel_x - bg.image.get_rect().width,0))

    if rel_x < 800:
        screen.blit(bg.image,(rel_x, 0))
    xBgScroll-= 1

    spawn_wave(25, 1)
    redraw_game()

    for bullet in bullets:
        if bullet.xpos < X_SCREEN_SIZE and bullet.xpos > 0:
            bullet.move_bullet(15, 1)
        else:
            bullets.pop(bullets.index(bullet))
    for bullet in enemyBullets:
        if bullet.xpos < X_SCREEN_SIZE and bullet.xpos > 0:
            bullet.move_bullet(15, -1)
        else:
            enemyBullets.pop(enemyBullets.index(bullet))

    for e in enemies:
        if e.get_enemy_pos() < 0:
            e.set_enemy_direction()
        if e.get_enemy_pos() > (Y_SCREEN_SIZE - 25):
            e.set_enemy_direction()

        checkEnemies = enemies.copy()
        checkEnemies.pop(enemies.index(e))

        kill_enemies(e, enemies, bullets)

        for ce in checkEnemies:
            if e.check_enemy_collisions(ce.get_enemy_rect()):
                e.set_enemy_direction()
        e.move_enemy()
        e.enemy_shoot(time, 50, enemyBullets)


    pygame.display.update()
    time+=1
    clock.tick(60)
