import pygame
import random
import math
from pygame import mixer


pygame.init()

# SCREEN
s = pygame.display.set_mode((800, 600))
b = pygame.image.load('D:/Tools/space.jpg')

mixer.music.load('D:/Tools/background.wav')
mixer.music.play(-1)

#NAME & ICON
pygame.display.set_caption('naGame')
i = pygame.image.load('D:/Tools/spainv.jpg')
pygame.display.set_icon(i)

# PLAYER
p = pygame.image.load('D:/Tools/spaceship.png')
px = 370
py = 480
pxc = 0

# ENEMY
e = []
ex = []
ey = []
exc = []
eyc = []
n = 6

for i in range(n):
    e.append(pygame.image.load('D:/Tools/enemy.png'))
    ex.append(random.randint(0, 736))
    ey.append(random.randint(50, 200))
    exc.append(1.1)
    eyc.append(40)

# BULLET
f = pygame.image.load('D:/Tools/bullet.png')
fx = 0
fy = 480
fyc = 5
fs = 'ready'

# TEXT
scoval = 0
ft = pygame.font.SysFont("Times New Roman", 32)
tx = 10
ty = 10

go = pygame.font.SysFont("Cooper Black", 64)

agn = pygame.font.SysFont("Cooper Black", 32)

ln = pygame.font.SysFont("Arial", 32)


def score(x, y):
    sco = ft.render("Socre : " + str(scoval), True, (255, 255, 255))
    s.blit(sco, (x, y))


def player(x, y):
    s.blit(p, (x, y))


def enemy(x, y, i):
    s.blit(e[i], (x, y))


def bg():
    s.blit(b, (0, 0))


def fir(x, y):
    global fs
    fs = 'fire'
    s.blit(f, (x+16, y-10))


def collision(a1, a2, a3, a4):
    D = math.sqrt((math.pow(a1-a3, 2)) + (math.pow(a2-a4, 2)))
    if D < 36:
        return True


def gameover():
    global tx
    global ty
    g = go.render("GAME OVER", True, (50, 200, 50))
    s.blit(g, (200, 150))
    tx = 345
    ty = 250


def again():
    a = ft.render("Press 'ENTER' to play again", True, (255, 0, 0))
    s.blit(a, (220, 320))


def line():
    l1 = ln.render("------------------------------------------------------------------------------------------------------------------------------", True, (255, 165, 0))
    l2 = ln.render("------------------------------------------------------------------------------------------------------------------------------", True, (255, 0, 0))
    s.blit(l1, (0, 450))
    s.blit(l2, (0, 460))


# Game Loop
r = True
while r:

    # RGB
    s.fill((0, 0, 0))
    bg()
    line()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pxc += -1
            if event.key == pygame.K_d:
                pxc += 1
            if event.key == pygame.K_SPACE:
                if fs == 'ready':
                    bsound = mixer.Sound('D:/Tools/laser.wav')
                    bsound.play()
                    fx = px
                    fir(fx, fy)
            if event.key == pygame.K_RETURN:
                for i in range(n):
                    ex[i] = random.randint(0, 736)
                    ey[i] = random.randint(50, 200)
                    scoval = 0
                    tx = 10
                    ty = 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or pygame.K_d:
                pxc = 0

    px += pxc

    # BOUNDRIES
    if px <= 0:
        px = 0
    elif px >= 736:
        px = 736

    # ENEMY MOVEMENT
    for i in range(n):
        ex[i] += exc[i]
        if ex[i] <= 0:
            exc[i] *= -1
            ey[i] += eyc[i]
        elif ex[i] >= 736:
            exc[i] *= -1
            ey[i] += eyc[i]

        c = collision(ex[i], ey[i], fx, fy)
        if c:
            exsound = mixer.Sound('D:/Tools/explosion.wav')
            exsound.play()
            fy = 480
            fs = 'ready'
            scoval += 1
            ex[i] = random.randint(0, 736)
            ey[i] = random.randint(50, 200)

        enemy(ex[i], ey[i], i)

        if ey[i] >= 420:
            for j in range(n):
                gameover()
                again()
                ey[j] = 2000

    # BULLET MOVEMENT
    if fy <= 0:
        fy = 480
        fs = 'ready'

    if fs == 'fire':
        fir(fx, fy)
        fy -= fyc

    player(px, py)
    score(tx, ty)
    
    pygame.display.update()
