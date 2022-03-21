import pygame
import random
import math
from pygame import mixer


# intialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# backgrounf
banckground = pygame.image.load("background.png")

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("Russia.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies = 10
for i in range (num_of_enemies):

    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(40, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"  # cant see the bullet on screen     # fire = bullet is currently moving

#score
score_Value= 0
font = pygame.font.Font("freesansbold.ttf",36)

textX = 10
textY = 10

#Game Over TExt
Over_font = pygame.font.Font("freesansbold.ttf",66)

def show_score(x,y):
    score = font.render("score :"+ str(score_Value), True, (255,100,230))
    screen.blit(score,(x, y))

def game_over_text ():
    over_text = Over_font.render("GAME OVER", True, (255,100,230))
    screen.blit(over_text, (200, 250))


def Player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 16))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


# Game loop
running = True
while True:
    screen.fill((230, 230, 230))
    # background image
    screen.blit(banckground, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check the key strokes
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = - 3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current x co ordiante of the spaceship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # check for boundary of spaceship

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(num_of_enemies):

        #gameover
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_Value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(40, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    Player(playerX, playerY)

    show_score(textX,textY)
    pygame.display.update()
