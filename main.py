import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerFiring = "single"
isFiring = False

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = []
bulletX = []
bulletY = []
bulletX_change = []
bulletY_change = []
bullet_state = []
num_of_bullets = 10


# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

for i in range(num_of_bullets):
    bulletImg.append(pygame.image.load('bullet.png'))
    bulletX.append(0)
    bulletY.append(480)
    bullet_state.append("ready")
bulletX_change = 0
bulletY_change = 20
bulletX_offset = 20
bulletY_offset = 10

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Firing Type

firingX = 575
firingY = 10

firing_font = pygame.font.Font('freesansbold.ttf', 24)

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_firing(x, y, firing_type):
    firing = firing_font.render("Blasters: " + str(firing_type), True, (255, 255, 255))
    screen.blit(firing, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y, i):
    bullet_state[i] = "fire"
    screen.blit(bulletImg[i], (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LALT:
                if playerFiring == "single":
                    playerFiring = "semi"
                    break
                if playerFiring == "semi":
                    playerFiring = "dual"
                    break
                if playerFiring == "dual":
                    playerFiring = "auto"
                    break
                if playerFiring == "auto":
                    playerFiring = "single"
                    break
            if event.key == pygame.K_SPACE:
                # Get the current x coordinate of the spaceship
                isFiring = True
                if playerFiring == "single":
                    for i in range(1):
                        if bullet_state[i] == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bulletX[i] = playerX
                            fire_bullet(bulletX[i], bulletY[i], i)
                            break
                elif playerFiring == "semi":
                    for i in range(num_of_bullets):
                        if bullet_state[i] == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bulletX[i] = playerX
                            fire_bullet(bulletX[i], bulletY[i], i)
                            break
                elif playerFiring == "dual":
                    for i in range(0, num_of_bullets, 2):
                        if bullet_state[i] == "ready" and bullet_state[i + 1] == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bulletX[i] = playerX - bulletX_offset
                            bulletX[i + 1] = playerX + bulletX_offset
                            bulletY[i] = playerY
                            bulletY[i + 1] = playerY
                            fire_bullet(bulletX[i], bulletY[i], i)
                            fire_bullet(bulletX[i + 1], bulletY[i + 1], i + 1)
                            break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                isFiring = False

    if playerFiring == "auto" and isFiring is True:
        for i in range(num_of_bullets):
            if bullet_state[i] == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bulletX[i] = playerX
                bulletY[i] = playerY - (24*i)
                fire_bullet(bulletX[i], bulletY[i], i)
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision

        for j in range(num_of_bullets):
            collision = isCollision(enemyX[i], enemyY[i], bulletX[j], bulletY[j])
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY[j] = 480
                bullet_state[j] = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    for i in range(num_of_bullets):

        if bulletY[i] <= 0:
            bulletY[i] = 480
            bullet_state[i] = "ready"

        if bullet_state[i] == "fire":
            fire_bullet(bulletX[i], bulletY[i], i)
            bulletY[i] -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_firing(firingX, firingY, playerFiring)
    pygame.display.update()
