import math
import random
import pygame
from pygame import mixer
from sys import exit

# Intialize the pygame
pygame.init()

WINDOWHEIGHT = 600
WINDOWWIDTH = 800
GREENYELLOW = (106, 238, 40)
DARKGREY = (34, 34, 34)
GREENYELLOW = (106, 238, 40)
ORANGE = (255, 102, 0)
YELLOW = (255, 255, 102)

# create the screen
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Background
background = pygame.image.load('background.png')


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Surrendered
surrendered_font = pygame.font.Font('freesansbold.ttf', 54)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def surrendered_text():
    surrender_text = surrendered_font.render("YOU'VE BEEN CAPTURED!", True, (255, 255, 255))
    screen.blit(surrender_text, (50, 250))

# Home Menu
def draw_text(surface, text, size, x, y, color):
    #draw text to screen
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surface.blit(text_surface, text_rect)

def menu():

    mixer.music.load("background.wav")
    mixer.music.play(-1)
    # display main menu
    while True:
        title = pygame.image.load("space-invaders.png")
        background_rect = background.get_rect()

        screen.blit(background, background_rect)
        screen.blit(title, (175, 20))
        pygame.draw.rect(screen, GREENYELLOW, (240, 250, 320, 35))
        pygame.draw.rect(screen, YELLOW, (200, 300, 400, 35))
        pygame.draw.rect(screen, YELLOW, (265, 350, 270, 35))
        draw_text(screen, "PRESS [ENTER] TO BEGIN", 30, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 50, DARKGREY)
        draw_text(screen, "PRESS [M/N] TO MUTE/UNMUTE", 30, WINDOWWIDTH / 2, (WINDOWHEIGHT / 2), DARKGREY)
        draw_text(screen, "PRESS [ESC] TO QUIT", 30, WINDOWWIDTH / 2, (WINDOWHEIGHT / 2) + 50, DARKGREY)

        # game instructions
        pygame.draw.rect(screen, ORANGE, (190, 430, 420, 35))
        pygame.draw.rect(screen, ORANGE, (190, 480, 420, 35))
        pygame.draw.rect(screen, ORANGE, (190, 530, 420, 35))
        draw_text(screen, "MOVE: LEFT/RIGHT ARROW KEYS", 30, 400, 430, DARKGREY)
        draw_text(screen, "SHOOT: SPACE BAR", 30, 400, 480, DARKGREY)
        draw_text(screen, "FIRING MODE: LEFT ALT", 30, 400, 530, DARKGREY)

        pygame.display.update()
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                play_game()
            elif event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_n:
                pygame.mixer.music.unpause()
            if event.key == pygame.K_m:
                pygame.mixer.music.pause()
        elif event.type == pygame.QUIT:
            exit()

# Pause Screen

def paused():
    # display paused screen

    title = pygame.image.load("space-invaders.png")
    background_rect = background.get_rect()

    screen.blit(background, background_rect)
    screen.blit(title, (175, 20))
    pygame.draw.rect(screen, GREENYELLOW, (200, 250, 400, 35))
    pygame.draw.rect(screen, YELLOW, (200, 300, 400, 35))
    pygame.draw.rect(screen, ORANGE, (200, 350, 400, 35))
    draw_text(screen, "PRESS [ESCAPE] TO UNPAUSE", 30, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 50, DARKGREY)
    draw_text(screen, "PRESS [M/N] TO MUTE/UNMUTE", 30, WINDOWWIDTH / 2, (WINDOWHEIGHT / 2), DARKGREY)
    draw_text(screen, "PRESS [S] TO SURRENDER", 30, WINDOWWIDTH / 2, (WINDOWHEIGHT / 2) + 50, DARKGREY)

    pygame.display.update()

    loop = True

    while loop:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
            elif event.key == pygame.K_s:
                screen.blit(background, background_rect)
                surrendered_text()
                pygame.display.update()
                pygame.time.delay(3000)
                menu()
            if event.key == pygame.K_n:
                pygame.mixer.music.unpause()
            if event.key == pygame.K_m:
                pygame.mixer.music.pause()
            break
        elif event.type == pygame.QUIT:
            exit()


def play_game():

    # Sound

    is_muted = False

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
    num_fired = 1

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

    # Accuracy

    accuracy_font = pygame.font.Font('freesansbold.ttf', 32)
    accuracyX = 10
    accuracyY = 5

    # Score

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    scoreX = 10
    scoreY = 40

    # Firing Type

    firingX = 575
    firingY = 10

    firing_font = pygame.font.Font('freesansbold.ttf', 24)

    def show_accuracy(x, y):
        accuracy = font.render("Accuracy: " + "{:.2%}".format(score_value / num_fired), True, (255, 255, 255))
        screen.blit(accuracy, (x, y))

    def show_score(x, y):
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def show_firing(x, y, firing_type):
        firing = firing_font.render("Blasters: " + str(firing_type), True, (255, 255, 255))
        screen.blit(firing, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y, i):
        bullet_state[i] = "fire"
        screen.blit(bulletImg[i], (x + 16, y + 10))

    def toggle_audio(is_muted):
        if is_muted is False:
            is_muted = True
        else:
            is_muted = False

    def play_bullet_sound():
        if is_muted is True:
            pass
        else:
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.play()

    def play_explosion_sound():
        if is_muted is True:
            pass
        else:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    running = True
    while running:

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_ESCAPE:
                    paused()
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
                                play_bullet_sound()
                                bulletX[i] = playerX
                                bullet_state[i] = "fire"
                                # fire_bullet(bulletX[i], bulletY[i], i)
                            break
                    elif playerFiring == "semi":
                        for i in range(num_of_bullets):
                            if bullet_state[i] == "ready":
                                play_bullet_sound()
                                bulletX[i] = playerX
                                bullet_state[i] = "fire"
                                # fire_bullet(bulletX[i], bulletY[i], i)
                                break
                    elif playerFiring == "dual":
                        for i in range(0, num_of_bullets, 2):
                            if bullet_state[i] == "ready" and bullet_state[i + 1] == "ready":
                                play_bullet_sound()
                                bulletX[i] = playerX - bulletX_offset
                                bulletX[i + 1] = playerX + bulletX_offset
                                bullet_state[i] = "fire"
                                bullet_state[i + 1] = "fire"
                                # bulletY[i] = playerY
                                # bulletY[i + 1] = playerY
                                # fire_bullet(bulletX[i], bulletY[i], i)
                                # fire_bullet(bulletX[i + 1], bulletY[i + 1], i + 1)
                                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_SPACE:
                    isFiring = False

        if playerFiring == "auto" and isFiring is True:
            for i in range(int(num_of_bullets / 2)):
                if bullet_state[i] == "ready":
                    play_bullet_sound()
                    bulletX[i] = playerX
                    bulletY[i] = playerY - (48 * i)
                    bullet_state[i] = "fire"
                    # fire_bullet(bulletX[i], bulletY[i], i)

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 420:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                running = False
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
                    play_explosion_sound()
                    # bulletY[j] = 480
                    # bullet_state[j] = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        for i in range(num_of_bullets):

            if bulletY[i] < -3:
                print(str(num_fired))
                num_fired += 1
                bulletY[i] = 480
                bullet_state[i] = "ready"

            if bullet_state[i] == "fire":
                fire_bullet(bulletX[i], bulletY[i], i)
                bulletY[i] -= bulletY_change

        player(playerX, playerY)
        show_accuracy(accuracyX, accuracyY)
        show_score(scoreX, scoreY)
        show_firing(firingX, firingY, playerFiring)
        pygame.display.update()
    pygame.display.update()
    pygame.time.delay(3000)
    return 0


#Testing Area
#paused()

#Main Menu
menu()

# Game Loop
#play_game()