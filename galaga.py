import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.left = 75
        self.rect.bottom = 550
    def moveLeft(self):
        self.rect.move_ip(-8, 0)
        if self.rect.left < 0:
            self.rect.left = 0
    def moveRight(self):
        self.rect.move_ip(8, 0)
        if self.rect.right > 800:
            self.rect.right = 800

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((30, 10))
        self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect()

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface((3, 10))
        self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect()
        self.speed = -15
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top < 0:
            self.kill()

def lvl1():
    for x in range(3):
        enemy = Enemy()
        enemy.rect.x = 40*x + 20
        enemy.rect.y = 25
        all_sprites.add(enemy)
        enemies.add(enemy)



pygame.init()
pygame.font.init()

clock = pygame.time.Clock()



screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Galaga')
screen.fill((255, 255, 255))

player = Player()
pygame.display.flip()

enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
font = pygame.font.SysFont('Comic Sans MS', 30)
lvltext = font.render('level: 1', True, (0, 0, 0))
screen.blit(lvltext,(750,450))

scoretext = font.render('score: 0', True, (0, 0, 0))
screen.blit(scoretext,(0,0))

pygame.display.flip()
running = True
wonRound = True
projectiletimer = 0
score = 0
lvl = 0
while running:
    if wonRound == True:
        lvl1()
        lvl += 1
        wonRound = False
    if projectiletimer > 2:
        projectiletimer = 0
    elif projectiletimer > 0:
        projectiletimer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT:
                player.moveLeft()
            if event.key == K_RIGHT:
                player.moveRight()
            if event.key == K_UP and projectiletimer == 0:
                projectile = Projectile()
                projectile.rect.x = player.rect.left + (player.rect.right - player.rect.left)/2
                projectile.rect.y = player.rect.y - 10
                all_sprites.add(projectile)
                projectiles.add(projectile)
                projectiletimer = 1
    # Check if projectile hits enemy
    for pro in projectiles:
        pro.update()
        enemiesHit = pygame.sprite.spritecollide(pro, enemies, True)
        if len(enemiesHit) > 0:
            pro.kill()
            score += 1
        if len(enemies.sprites()) == 0:
            wonRound = True
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    lvltext = font.render('level: ' + str(lvl), True, (0, 0, 0))
    scoretext = font.render('score: ' + str(score), True, (0, 0, 0))


    screen.blit(lvltext,(20,0))
    screen.blit(scoretext,(700,0))
    pygame.display.flip()
    screen.fill((255, 255, 255))
    clock.tick(30)
pygame.quit()
