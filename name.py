import pygame
import random
import math
from pygame import mixer

# Pygame initialisation
pygame.init()

# For Windows display
win = pygame.display.set_mode((800, 500))

# Background
bg = pygame.image.load('IMG/Plan B/file.jpg')
mixer.music.load('music/background music.wav')
mixer.music.play(-1)

# For title and logo
pygame.display.set_caption("Ninja Wars: The Journey Awaits")
icon = pygame.image.load('IMG/Plan B/ninja (1).png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('IMG/Plan B/ninja (1).png')
playerX = 400
playerY = 350
px_change = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
ex_change = []
ey_change = []
enemy_num = 5

for i in range(enemy_num):
    enemy_img.append(pygame.image.load('IMG/Plan B/samurai (1).png'))
    enemyX.append(random.randint(0, 775))
    enemyY.append(random.randint(50, 150))
    ex_change.append(0.1)
    ey_change.append(35)

# Projectile
pro_img = pygame.image.load('IMG/Plan B/star (1).png')
proX = 0
proY = 350
prox_change = 0
proy_change = 1
pro_state = "ready"

# SCOREBOARD
score = 0
font = pygame.font.Font('font/osake.ttf', 32)
scoreX = 10
scoreY = 10

# GAME OVER
over_font = pygame.font.Font('font/osake.ttf', 64)

# Functions
def player(x, y):
    win.blit(player_img, (x, y))

def enemy(x, y, i):
    win.blit(enemy_img[i], (x, y))

def projectile(x, y):
    global pro_state
    pro_state = "fire"
    win.blit(pro_img, (x + 16, y + 10))

def collision(proX, proY, enemyX, enemyY):
    dist = math.sqrt(math.pow(enemyX - proX, 2) + math.pow(enemyY - proY, 2))
    return dist < 27

def is_game_over(playerX, playerY, enemyX, enemyY):
    dist = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
    return dist < 27

def scoreboard(x, y):
    score_display = font.render("Score: " + str(score), True, (0, 0, 0))
    win.blit(score_display, (x, y))

def gameover():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    win.blit(over_text, (200, 250))  # Adjusted position for better centering

# Main game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement controls
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    px_change = -0.3
                if event.key == pygame.K_RIGHT:
                    px_change = 0.3
                if event.key == pygame.K_SPACE:
                    if pro_state == "ready":
                        proX = playerX
                        projectile(proX, proY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                px_change = 0

    if not game_over:
        # Filling the background
        win.fill((255, 255, 255))
        win.blit(bg, (0, 0))

        # Movement of the player
        playerX += px_change
        if playerX <= 0:
            playerX = 0
        if playerX >= 775:
            playerX = 775

        # Movement of the enemy
        for i in range(enemy_num):
            enemyX[i] += ex_change[i]
            if enemyX[i] <= 0:
                enemyY[i] += ey_change[i]
                ex_change[i] = 0.1
            if enemyX[i] >= 775:
                enemyY[i] += ey_change[i]
                ex_change[i] = -0.1

            # Check for game over (collision with player)
            if is_game_over(playerX, playerY, enemyX[i], enemyY[i]):
                for j in range(enemy_num):
                    enemyY[j] = 2000  # Move enemies off-screen
                gameover()
                game_over = True
                break

            # Collision with projectile
            collide = collision(proX, proY, enemyX[i], enemyY[i])
            if collide:
                col_sound = mixer.Sound('music/sound effect ugh.wav')
                col_sound.play()
                proY = 350
                pro_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 775)
                enemyY[i] = random.randint(50, 150)

            # Drawing the enemy
            enemy(enemyX[i], enemyY[i], i)

        # Movement of the projectile
        if pro_state == "fire":
            projectile(proX, proY)
            proY -= proy_change
        if proY <= 0:
            proY = playerY
            pro_state = "ready"

        # Drawing the player
        player(playerX, playerY)

        # Displaying the scoreboard
        scoreboard(scoreX, scoreY)

    pygame.display.update()
