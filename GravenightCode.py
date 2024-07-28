# Siodhachan Morehead
# Gravenight

# IMPORTANT!!! - Inputs for Testing
# '\' - skips the current round (works during a night)
# 'g' - gives health (works during a night)
# 'm' - gives money (works in the menu)
# 'q' - quits game (works in the menu)

import pygame
import random
import math

# Initialize pygame
pygame.init()
DISPLAY = (1000, 700)
screen = pygame.display.set_mode(DISPLAY)

# Constants
#-------------------------------------------------------
# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 120, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARKRED = (125, 0, 0)
DARKGRAY = (25, 25, 25)
GARLICGREEN = (0, 50, 0)
GRAY = (127, 127, 127)
LIGHTGRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
UIFONTSMALLEST = pygame.font.SysFont("ebrimo", 20)
UIFONTSMALLERERER = pygame.font.SysFont("ebrimo", 30)
UIFONTSMALLERER = pygame.font.SysFont("ebrimo", 40)
UIFONTSMALLER = pygame.font.SysFont("ebrimo", 60)
UIFONTSMALL = pygame.font.SysFont("ebrimo", 80)
UIFONTMEDIUM = pygame.font.SysFont("ebrimo", 100)
UIFONTLARGE = pygame.font.SysFont("ebrimo", 120)
UIFONTLARGEALT = pygame.font.SysFont("cambria", 120)

# Sounds
whipSound = pygame.mixer.Sound("whipAttack.mp3")
bowSound = pygame.mixer.Sound("shootBow.mp3")
garlicSound = pygame.mixer.Sound("garlicAttack.mp3")
buySound = pygame.mixer.Sound("buyWeapon.mp3")
upgradeSound = pygame.mixer.Sound("upgradeWeapon.mp3")
menuSound = pygame.mixer.Sound("buttonClick.mp3")
deathSound = pygame.mixer.Sound("playerDied.mp3")
loseSound = pygame.mixer.Sound("playerLost.mp3")
hitEnemySound = pygame.mixer.Sound("hitEnemy.mp3")
winSound = pygame.mixer.Sound("playerWin.mp3")
gameMusic = pygame.mixer.Sound("backgroundMusic.mp3")
gameMusic.set_volume(0.7)
winSound.set_volume(0.5)

# Images
gameBackground = pygame.image.load("backgroundImage.PNG")

# Player and weapon variables
playerHEALTH = 100
whipDAMAGE = 20 # insta kill zombie at lvl. 3 - increments of 15
bowDAMAGE = 30 # insta kill skele at lvl 3 - increments of 20
garlicDAMAGE = 60 # insta kill ghost at lvl 3 - increments of 30

# Enemy variables
zombieHEALTH = 60
zombieDAMAGE = 20

skeletonHEALTH = 90
skeletonDAMAGE = 40

ghostHEALTH = 150
ghostDAMAGE = 60

vampHEALTH = 250
vampDAMAGE = 75

dragonHEALTH = 1000
dragonDAMAGE = 100

nightTIME = 120 # seconds

# Functions
#------------------------------------------
def Distance(x1, x2, y1, y2): # Distance between two points
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def circleCollision(x1, y1, r1, x2, y2, r2): # Collision between two circles
    radiusSum = r1 + r2
    centreDistance = Distance(x1, x2, y1, y2)
    
    if radiusSum > centreDistance:
        return True

def rectCollision(weapon, enemy): # Collision between two rectangles
    if weapon.colliderect(enemy):
        return True
    
    return False

def drawBackground(): # Draws a dark green square for the background
    screen.blit(gameBackground, (0, 0, 1000, 700))
    
def drawPlayer(x, y): # Draws the player as a black circle with radius 15
    pygame.draw.circle(screen, BLACK, (x, y), 15)
    
def drawEnemies(enemyType, enemyAmount, enemyPos): # Draws enemies
    if enemyType == "Zombie":
        for n in range(enemyAmount[0]):
            pygame.draw.circle(screen, DARKGREEN, (enemyPos), 15)
            
    if enemyType == "Skeleton":
        for n in range(len(enemyAmount)):
            pygame.draw.circle(screen, LIGHTGRAY, (enemyPos), 14)
            
    if enemyType == "Ghost":
        for n in range(len(enemyAmount)):
            pygame.draw.circle(screen, WHITE, (enemyPos), 14)
            
    if enemyType == "Vampire":
        for n in range(len(enemyAmount)):
            pygame.draw.circle(screen, BLUE, (enemyPos), 16)
            
    if enemyType == "Dragon":
        for n in range(len(enemyAmount)):
            pygame.draw.circle(screen, RED, (enemyPos), 20)

def drawProjectiles(projectileType, projectileAmount, projectilePos): # Draws all projectiles
    if projectileType == "Arrow":
        for n in range(projectileAmount[0]):
            pygame.draw.circle(screen, BLACK, (projectilePos), 5)

def spawnEnemies(night, time): # Spawns enemies, takes nightState and time in seconds
    # Higher night = greater chance of spawning a zombie every 2 seconds
    # Zombies:
    # N1: 38% - N2: 46% - N3: 54% - N4 - 62% - N5 - 70% N6: 78%
    # Skeletons:
    # N2: 50% - N3: 55% - N4: 60% - N5 - 65% - N6 - 70%
    # Ghosts:
    # N3 - 50% - N4: 54% - N5: 58% - N6: 62%
    # Vampires:
    # N4 - 70% - N5 - 78% - N6: 86%
    # Dragons:
    # N5: 60% - N6: 80%
    
    global enemyAmount
    global enemyType
    global enemyPos
    global enemyHealth
    global enemyRadius
    global speedList
    global playerX

    # Increases difficulty of night as the time goes on by increasing number of enemies spawned at once
    if time >= 50 and time < 100:
        doubleEnemy = 2
    elif time >= 100:
        doubleEnemy = 3
    else:
        doubleEnemy = 1

    if night == 6:
        doubleEnemy += 1

    randomNumber = random.randint(1, 100)

    if time % 1 == 0: # Spawns zombies
        if randomNumber <= (night*8 + 30):
            for x in range(doubleEnemy):
                enemyType.append('Zombie')
                enemyAmount[0] += 1
                enemyPos.append((random.choice((random.randint(-20, int(playerX-20)), random.randint(int(playerX)+20, 1020))), random.randint(0, 700)))
                enemyHealth.append(zombieHEALTH)
                enemyRadius.append(15)
                zombieSpeed = round(random.uniform(0, 2), 3)
                speedList.append(zombieSpeed)
        
    if time % 2 == 0: # Spawns skeletons
        if night > 1:
            if randomNumber <= (night*5 + 40):
                for x in range(doubleEnemy):
                    enemyType.append('Skeleton')
                    enemyAmount[1] += 1
                    enemyPos.append((random.choice((random.randint(-40, int(playerX-40)), random.randint(int(playerX)+40, 1040))), random.randint(0, 700)))
                    enemyHealth.append(skeletonHEALTH)
                    enemyRadius.append(14)
                    skeletonSpeed = round(random.uniform(2, 2.5), 3)
                    speedList.append(skeletonSpeed)
                
    if time % 4 == 0: # Spawns ghosts 
        if night > 2:
            if randomNumber <= (night*4 + 38):
                for x in range(doubleEnemy):
                    enemyType.append('Ghost')
                    enemyAmount[2] += 1
                    enemyPos.append((random.choice((random.randint(-60, int(playerX-60)), random.randint(int(playerX)+60, 1060))), random.randint(0, 700)))
                    enemyHealth.append(ghostHEALTH)
                    enemyRadius.append(14)
                    ghostSpeed = round(random.uniform(1, 3), 3)
                    speedList.append(ghostSpeed)
    
    if time % 8 == 0: # Spawns vampires
        if night > 3:
            if randomNumber <= (night * 8 + 58):
                for x in range(doubleEnemy):
                    enemyType.append('Vampire')
                    enemyAmount[3] += 1
                    enemyPos.append((random.choice((random.randint(-80, int(playerX-80)), random.randint(int(playerX)+80, 1080))), random.randint(0, 700)))
                    enemyHealth.append(vampHEALTH)
                    enemyRadius.append(16)
                    vampireSpeed = round(random.uniform(3, 3.5), 3)
                    speedList.append(vampireSpeed)
    
    if time % 15 == 0: # Spawns dragons
        if night > 4:
            if randomNumber <= (night * 20 - 40):
                for x in range(doubleEnemy):
                    enemyType.append('Dragon')
                    enemyAmount[4] += 1
                    enemyPos.append((random.choice((random.randint(-100, int(playerX-100)), random.randint(int(playerX)+100, 1100))), random.randint(0, 700)))
                    enemyHealth.append(dragonHEALTH)
                    enemyRadius.append(20)
                    dragonSpeed = round(random.uniform(3.5, 4), 3)
                    speedList.append(dragonSpeed)   

def enemyMovement(): # Moves the enemies - very basic but works
    global enemyPos
    global playerY
    global playerX
    global enemyType
    global speedList
    
    for i in range(len(enemyPos)): # Works by simply changing the enemies position if they are not at the player's position 
        if enemyPos[i][0] < playerX:
            enemyPos[i] = (((enemyPos[i])[0] + speedList[i]), ((enemyPos[i])[1]))
        if (enemyPos[i])[0] > playerX:
            enemyPos[i] = (((enemyPos[i])[0] - speedList[i]), ((enemyPos[i])[1]))
                
        if (enemyPos[i])[1] < playerY:
            enemyPos[i] = (((enemyPos[i])[0]), ((enemyPos[i])[1] + speedList[i]))
        if (enemyPos[i])[1] > playerY:
            enemyPos[i] = (((enemyPos[i])[0]), ((enemyPos[i])[1] - speedList[i]))   
            
def projectileMovement(): # Moves all projectiles
    global projectilePos
    global projectileType

    for i in range(len(projectilePos)):      
        if projectileType[i] == 'Arrow':
            if attackSide[i] == 'right': # Used to make arrows go the correct direction
                projectilePos[i] = (((projectilePos[i])[0] + 8), ((projectilePos[i])[1]))
            else:
                projectilePos[i] = (((projectilePos[i])[0] - 8), ((projectilePos[i])[1]))

def playerRegen():  # Rengerates player health, playerLevel increases amount healed
    global playerHealth
    global playerRegenTime

    if playerHealth < (100 + 20*playerLevel):
            playerRegenTime += 1
            if playerRegenTime == 30:
                playerHealth += 2 + (0.2 * playerLevel)
                playerRegenTime = 0
            if playerHealth > (100 + 20*playerLevel):
                playerHealth = (100 + 20*playerLevel)  

def enemyCooldownCheck(): # Checks enemy attack cooldown
    global enemyCooldown
    global enemyCooldownTime
    if enemyCooldown == True:
            enemyCooldownTime += 1
            if enemyCooldownTime == 30:
                enemyCooldown = False
                enemyCooldownTime = 0 

def weaponCooldownCheck(currentWeapon): # Checks weapon attack cooldown, cooldown decreases with weapon level
    global weaponCooldown
    global cooldownTime
    if weaponCooldown:
            cooldownTime += 1
            if currentWeapon == 'Whip':       
                if cooldownTime == 60 - 5 * whipLevel:
                    weaponCooldown = False
                    cooldownTime = 0
            elif currentWeapon == 'Bow':
                if cooldownTime == 60 - 7 * bowLevel:
                    weaponCooldown = False  
                    cooldownTime = 0
            else:
                if cooldownTime == 40 - 3 * garlicLevel:
                    weaponCooldown = False
                    cooldownTime = 0

def playerUI(seconds): # Draws the player UI
    
    global currentWeapon
    global playerX
    global playerY
    global playerDamaged
    global damagedFrames
    global damageFrames
    global collisionPos
    global weaponHitPos
    global attackFrames
    global nightState
    global enemyKilled
    global playerMoney
    global playerHealth

    xRemovedSum = 0
    # 400, 200
    # 395, 210
    pygame.draw.rect(screen, BLACK, (495 - ((100)*(1 + playerLevel*0.2))/2, 595, (100)*(1 + playerLevel*0.2) + 10, 60))
    pygame.draw.rect(screen, RED, (500 - ((100)*(1 + playerLevel*0.2))/2, 600, (100)*(1 + playerLevel*0.2), 50))
    pygame.draw.rect(screen, GREEN, (500 - ((100)*(1 + playerLevel*0.2))/2, 600, playerHealth, 50))

    # pygame.draw.line(screen, BLACK, (500, 0), (500, 700))
    TimeText = UIFONTLARGE.render("%3s"%(int(seconds)), 1, WHITE)
    screen.blit(TimeText, (433, 50, 200, 200))

    MoneyText = UIFONTSMALLER.render("$%-4s"%(playerMoney), 1, YELLOW)
    screen.blit(MoneyText, (40, 27, 200, 200))
    
    KillsText = UIFONTSMALLERER.render("%3s"%(enemyKilled), 1, DARKRED)
    screen.blit(KillsText, (850, 30, 200, 200))   

    if len(collisionPos) > 0:
        DamageText = UIFONTSMALLERER.render(playerDamaged, 1, RED)	
        screen.blit(DamageText, (playerX-15, playerY - 40, 200, 200))
        damagedFrames += 1
        if damagedFrames == 25:
            damagedFrames = 0
            collisionPos.pop(0)

    for x in range(len(weaponHitPos)):
        x -= xRemovedSum
        if currentWeapon == 'Whip':
            weaponDamage = whipDAMAGE + 15*whipLevel
        elif currentWeapon == 'Bow':
            weaponDamage = bowDAMAGE + 20*bowLevel
        else:
            weaponDamage = garlicDAMAGE + 30*garlicLevel
            
        attackText = UIFONTSMALLERERER.render(str(weaponDamage), 1, RED)
        screen.blit(attackText, (weaponHitPos[x][0]-10, weaponHitPos[x][1]-30, 200, 200))
        attackFrames += 1
        if attackFrames == 20:
            attackFrames = 0
            weaponHitPos.pop(x)
            xRemovedSum += 1
            
# Clock
IGT = pygame.time.Clock()

# Game states/booleans
game = True
nightState = 1
night = False
menu = True
newGame = True

# Player and weapon variables

currentWeapon = 'Whip'
whipLevel = 0
haveBow = False
bowLevel = 0
haveGarlic = False
garlicLevel = 0

playerMoney = 0
playerLevel = 0

gameMusic.play()
pygame.mixer.pause()

while game:
    # Lists
    #----------------------------------------------------------
    projectilePos = []
    projectileType = []
    # 0: Arrows - 1: N/A - 2: N/A
    projectileAmount = [0, 0, 0]

    # 0: Zombie - 1: Skeleton - 2: Ghost - 3: Vampire - 4: Dragon
    enemyAmount = [0, 0, 0, 0, 0]
    enemyPos = []
    enemyHealth = []
    enemyType = []
    enemyRadius = []
    speedList = []

    collisionPos = []
    weaponHitPos = []
    attackSide = []
    projectileRemoved = []

    # Booleans
    #-----------------------------------------------------------
    enemyCooldown = False
    weaponCooldown = False
    projectileCooldown = False

    attack = False
    drawWeapon = False
    roundWon = False
    playMusic = True

    # Integers and floats
    #-----------------------------------------------------------
    damagedFrames = 0
    damageFrames = 0
    enemyCooldownTime = 0
    enemyKilled = 0
    previousSecond = 0
    cooldownTime = 0
    previousSecond = 0
    enemyCooldownTime = 0
    weaponFrames = 0
    attackFrames = 0
    framesSum = 0
    seconds = 0

    # Menu state 
    if newGame:
        menuState = 1
    else:
        menuState = 2
    
    # Player variables
    playerHealth = 0
    playerHealth += playerHEALTH + playerLevel * 20
    playerSPEED = (4 + 0.1*playerLevel)
    playerDamaged = ''
    playerX = 500
    playerY = 350
    playerRegenTime = 0 
    
    while night:
        if playMusic:
            pygame.mixer.unpause()
            playMusic = False
        drawBackground() # Draws the background every frame
        if drawWeapon: # If drawing a weapon
            if currentWeapon == 'Whip': # If weapon is whip
                if rightSideAttack:
                    pygame.draw.rect(screen, ORANGE, (playerX + 15, playerY - 4, 45, 8))
                else:
                    pygame.draw.rect(screen, ORANGE, (playerX - 60, playerY - 4, 45, 8))
                    
            elif currentWeapon == 'Bow': # If weapon is bow
                if rightSideAttack:
                    pygame.draw.rect(screen, WHITE, (playerX + 15, playerY-10, 10, 20))
                else:
                    pygame.draw.rect(screen, WHITE, (playerX - 25, playerY-10, 10, 20))
    
            else: # If weapon is garlic
                pygame.draw.circle(screen, GARLICGREEN, (playerX, playerY), 45 + 15*garlicLevel)
                
            weaponFrames += 1
            if weaponFrames == 10:
                weaponFrames = 0
                drawWeapon = False

        # Every second, spawnEnemies()
        if int(seconds) != int(previousSecond):
            spawnEnemies(nightState, int(seconds))
            
        # Player regen
        playerRegen()  
        
        # Enemy cooldown
        enemyCooldownCheck()
                
        # Weapon cooldown
        weaponCooldownCheck(currentWeapon)
        
        # Enemy movement
        enemyMovement() 

        # Draws all spawned enemies
        for x in range(len(enemyType)):
            drawEnemies(enemyType[x], enemyAmount, enemyPos[x])     
                    
        # Projectile movement
        projectileMovement()

        # Draws all projectiles in the list
        for x in range(len(projectileType)):
            drawProjectiles(projectileType[x], projectileAmount, projectilePos[x])           
        
        # Draw player function
        drawPlayer(playerX, playerY)
        
        # Check for player input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse1Pressed = True
                    mousePressedPos = event.pos
                    
                    rightSideAttack = False
                    leftSideAttack = False                    
                    
                    # Gives right/left side attack depending on mouse position
                    if mousePressedPos[0] >= playerX:
                        rightSideAttack = True
                    elif mousePressedPos[0] < playerX:
                        leftSideAttack = True
            else:
                mouse1Pressed = False
                    
        # Player movement
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            playerY -= playerSPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            playerY += playerSPEED
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            playerX -= playerSPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            playerX += playerSPEED       
        
        # Enemy collision
        
        for i in range(len(enemyPos)):
            if enemyType[i] == 'Zombie': # Zombie collision
                zombieHit = circleCollision(playerX, playerY, 15, enemyPos[i][0], enemyPos[i][1], 15)
                if zombieHit and not enemyCooldown:
                    hitEnemySound.play()
                    collisionPos.append((enemyPos[i][0], enemyPos[i][1]))
                    playerHealth -= zombieDAMAGE
                    enemyCooldown = True
                    zombieHit = False
                    playerDamaged = str(zombieDAMAGE)
                    
            elif enemyType[i] == 'Skeleton': # Skeleton collision
                skeletonHit = circleCollision(playerX, playerY, 15, enemyPos[i][0], enemyPos[i][1], 14)
                if skeletonHit and not enemyCooldown:
                    hitEnemySound.play()
                    collisionPos.append((enemyPos[i][0], enemyPos[i][1]))
                    playerHealth -= skeletonDAMAGE
                    enemyCooldown = True
                    skeletonHit = False
                    playerDamaged = str(skeletonDAMAGE)
            
            elif enemyType[i] == 'Ghost': # Ghost collision
                ghostHit = circleCollision(playerX, playerY, 15, enemyPos[i][0], enemyPos[i][1], 14)
                if ghostHit and not enemyCooldown:
                    hitEnemySound.play()
                    collisionPos.append((enemyPos[i][0], enemyPos[i][1]))
                    playerHealth -= ghostDAMAGE
                    enemyCooldown = True
                    ghostHit = False
                    playerDamaged = str(ghostDAMAGE)
            
            elif enemyType[i] == 'Vampire': # Vampire collision
                vampHit = circleCollision(playerX, playerY, 15, enemyPos[i][0], enemyPos[i][1], 16)
                if vampHit and not enemyCooldown:
                    hitEnemySound.play()
                    collisionPos.append((enemyPos[i][0], enemyPos[i][1]))
                    playerHealth -= vampDAMAGE
                    enemyCooldown = True
                    vampHit = False
                    playerDamaged = str(vampDAMAGE)
            
            else: # Dragon collision
                dragonHit = circleCollision(playerX, playerY, 15, enemyPos[i][0], enemyPos[i][1], 20)
                if dragonHit and not enemyCooldown:
                    hitEnemySound.play()
                    collisionPos.append((enemyPos[i][0], enemyPos[i][1]))
                    playerHealth -= dragonDAMAGE
                    enemyCooldown = True
                    dragonHit = False
                    playerDamaged = str(dragonDAMAGE)            
                
        # Weapon collision 
        
        if mouse1Pressed == True and not weaponCooldown:
            if currentWeapon == 'Whip': # Whip collision
                if rightSideAttack:
                    whipRect = pygame.Rect(playerX + 15, playerY-4, 45, 8)
                else:
                    whipRect = pygame.Rect(playerX - 60, playerY-4, 45, 8) 

                whipSound.play()
                attack = True
                drawWeapon = True
                if attack and not weaponCooldown:
                    for i in range(len(enemyPos)):
                        enemyAttacked = rectCollision(whipRect, (enemyPos[i][0]-enemyRadius[i], enemyPos[i][1]-enemyRadius[i], enemyRadius[i]*2, enemyRadius[i]*2))
                        if enemyAttacked:
                            weaponHitPos.append((enemyPos[i][0], enemyPos[i][1]))
                            enemyHealth[i] -= whipDAMAGE + 15 * whipLevel      
                            hitEnemySound.play()
                            if rightSideAttack:
                                enemyPos[i] = (enemyPos[i][0] + 20, enemyPos[i][1])
                            else:
                                enemyPos[i] = (enemyPos[i][0] - 20, enemyPos[i][1])  
                            
                
            elif currentWeapon == 'Bow': # Bow attack action and projectile creator
                attack = True
                drawWeapon = True
                bowSound.play()
                if attack and not weaponCooldown:
                    if rightSideAttack:
                        attackSide.append('right')
                        projectilePos.append((playerX+15, playerY))
                    else:
                        attackSide.append('left')  
                        projectilePos.append((playerX-15, playerY))
                    projectileType.append('Arrow')
                    projectileAmount[0] += 1
                    projectileRemoved.append(False)
                    
            else: # Garlic collision
                attack = True
                drawWeapon = True
                garlicSound.play()
                if attack and not weaponCooldown:
                    for i in range(len(enemyPos)):
                        enemyAttacked = circleCollision(playerX, playerY, 45 + 15*garlicLevel, enemyPos[i][0], enemyPos[i][1], enemyRadius[i])
                        if enemyAttacked:
                            hitEnemySound.play()
                            weaponHitPos.append((enemyPos[i][0], enemyPos[i][1]))
                            enemyHealth[i] -= garlicDAMAGE + 30 * garlicLevel
                            if enemyPos[i][0] > playerX:
                                enemyPos[i] = (enemyPos[i][0] + 30, enemyPos[i][1])
                            else:
                                enemyPos[i] = (enemyPos[i][0] - 30, enemyPos[i][1])
                                
            weaponCooldown = True
            mouse1Pressed = False

        # Arrow collision which can use different projectiles if needed
        for i in range(len(enemyPos)):
            for x in range(len(projectilePos)):
                if projectileType[x] == 'Arrow':
                    enemyAttacked = circleCollision(projectilePos[x][0], projectilePos[x][1], 5, enemyPos[i][0], enemyPos[i][1], enemyRadius[i])
                if enemyAttacked:
                    hitEnemySound.play()
                    weaponHitPos.append((enemyPos[i][0], enemyPos[i][1]))
                    enemyHealth[i] -= (bowDAMAGE + 20*bowLevel)
                    projectileRemoved[x] = True
                    
                    if rightSideAttack:
                        enemyPos[i] = (enemyPos[i][0] + 15, enemyPos[i][1])
                    else:
                        enemyPos[i] = (enemyPos[i][0] - 15, enemyPos[i][1])
        
        # Removes enemies if their health is zero
        enemyRemoved = 0
        for m in range(len(enemyHealth)):
            # Length of list changes when enemy is removed
            m -= enemyRemoved
            
            # Increases enemy speed to their max if they get hit (kind of like aggro)
            if enemyType[m] == 'Zombie':
                if enemyHealth[m] < zombieHEALTH:
                    speedList[m] = 2
            elif enemyType[m] == 'Skeleton':
                if enemyHealth[m] < skeletonHEALTH:
                    speedList[m] = 2.5
            elif enemyType[m] == 'Ghost':
                if enemyHealth[m] < ghostHEALTH:
                    speedList[m] = 3
            elif enemyType[m] == 'Vampire':
                if enemyHealth[m] < vampHEALTH:
                    speedList[m] = 3.5
            else:
                if enemyHealth[m] < dragonHEALTH:
                    speedList[m] = 4

            if enemyHealth[m] <= 0:
                enemyPos.pop(m)
                enemyHealth.pop(m)
                
                # Gives player money
                if enemyType[m] == 'Zombie':
                    playerMoney += 1 * nightState
                    enemyAmount[0] -= 1
                elif enemyType[m] == 'Skeleton':
                    playerMoney += 2 * nightState
                    enemyAmount[1] -= 1
                elif enemyType[m] == 'Ghost':
                    playerMoney += 4 * nightState
                    enemyAmount[2] -= 1
                elif enemyType[m] == 'Vampire':
                    playerMoney += 12 * nightState
                    enemyAmount[3] -= 1
                else:
                    playerMoney += 40 * nightState
                    enemyAmount[4] -= 1
                    
                enemyType.pop(m)
                enemyRadius.pop(m) 
                speedList.pop(m)  
                enemyRemoved += 1
                enemyKilled += 1

        # Removes projectiles if they are outside of the map
        projectileDeleted = 0
        for p in range(len(projectileType)):
            p -= projectileDeleted
            # weird error here sometimes - fixed! switched .remove() for .pop()
            if projectilePos[p][0] < 0 or projectilePos[p][0] > 1000 or projectilePos[p][1] > 700 or projectilePos[p][1] < 0 or projectileRemoved[p] == True:
                projectilePos.pop(p)
                projectileType.pop(p)
                attackSide.pop(p)
                projectileRemoved.pop(p)
                projectileAmount[0] -= 1
                projectileDeleted += 1

        # Map boundaries
        if playerX < 15:
            playerX = 15
        if playerX > 985:
            playerX = 985
        if playerY < 15:
            playerY = 15
        if playerY > 685:
            playerY = 685
        
        # Runs the playerUI() function
        playerUI(seconds)
        
        # If the player's health is less than zero, game over
        if playerHealth <= 0:
            night = False
            roundWon = False
            menu = True
            pygame.mixer.pause()
            deathSound.play()
            loseSound.play()
        
        # If the player has survived 120 seconds, they won the round
        if seconds > nightTIME:
            night = False
            roundWon = True
            menu = True
            playerMoney += (nightState)**2 * 50
            nightState += 1
            pygame.mixer.pause()
            winSound.play()
        
        # Test key that gives health
        if keys[pygame.K_g]:
            playerHealth += 100       
        
        # Test key that skips the night
        if keys[pygame.K_BACKSLASH]:
            night = False
            roundWon = True
            menu = True
            playerMoney += (nightState)**2 * 50
            nightState += 1
            if nightState == 7:
                menuState = 0
            pygame.mixer.pause()
            winSound.play()

        if gameMusic.get_num_channels() == 0:
            playMusic = True
            gameMusic.play()
    
        pygame.display.flip()
        IGT.tick(60)
        previousSecond = seconds
        # Acts as a clock which gives seconds
        seconds += 1/60
    
    while menu: # While in the menu between nights
        # Background
        pygame.draw.rect(screen, BLACK, (0, 0, 1000, 700))
        
        for event in pygame.event.get(): # For every player input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse1Pressed = True
                    mousePressedPos = event.pos
            else:
                mouse1Pressed = False   
        
        keys = pygame.key.get_pressed()

        # Test key that gives money
        if keys[pygame.K_m]:
            playerMoney += 100
        
        # Test key that quits the game
        if keys[pygame.K_q]:
            pygame.quit()
        
        if menuState == 2: # Default menu after each night
            if newGame: # If playing for the first time
                MenuText1 = UIFONTLARGE.render("Welcome...", 1, WHITE)
                MenuText2 = UIFONTSMALLER.render("Moving on to Night %1s..."%nightState, 1, RED)
                tcontButton = UIFONTSMALL.render("Continue", 1, WHITE)
            else:
                if roundWon: # If player won
                    MenuText1 = UIFONTLARGE.render("Well done!", 1, WHITE)
                    MenuText2 = UIFONTSMALLER.render("Moving on to Night %1s..."%nightState, 1, RED)
                    tcontButton = UIFONTSMALL.render("Continue", 1, WHITE)

                else: # If player lost
                    MenuText1 = UIFONTLARGE.render("Too bad...", 1, WHITE)
                    MenuText2 = UIFONTSMALLER.render("You lasted %s seconds..."%int(seconds), 1, RED)
                    tcontButton = UIFONTSMALL.render("Try again", 1, WHITE)
                
            MenuText3 = UIFONTSMALLERER.render("$%-4s"%playerMoney, 1, YELLOW)
            buyButton = UIFONTSMALL.render("Buy", 1, WHITE)
            backButton = UIFONTSMALL.render("Back", 1, WHITE)
            
            screen.blit(MenuText1, (302, 30, 200, 200))      
            screen.blit(MenuText2, (297, 120, 200, 200))   
            screen.blit(MenuText3, (25, 25, 200, 200))
        
            # Continue/try again, buy, and back buttons
            for y in range(250, 551, 150):
                pygame.draw.rect(screen, WHITE, (300, y, 400, 100))
                pygame.draw.rect(screen, BLACK, (305, y+5, 390, 90))
            
            screen.blit(tcontButton, (375, 272, 200, 200))
            screen.blit(buyButton, (445, 422, 200, 200))
            screen.blit(backButton, (433, 572, 200, 200)) 
            
            if mouse1Pressed: # Button collision checking
                for x in range(300, 700):
                    for y in range(250, 351):
                        if mousePressedPos == (x, y):
                            menuSound.play()
                            menu = False
                            night = True
                    for y in range(400, 500):
                        if mousePressedPos == (x, y):
                            menuState += 1
                            menuSound.play()
                    for y in range(550, 650):
                        if mousePressedPos == (x, y):
                            menuState -= 1           
                            menuSound.play()            
                
        if menuState == 3: # Buy and upgrade menu
            MenuText3 = UIFONTSMALLERER.render("$%-4s"%playerMoney, 1, YELLOW)
            screen.blit(MenuText3, (25, 25, 200, 200))
            
            pygame.draw.rect(screen, WHITE, (370, 550, 260, 100))
            pygame.draw.rect(screen, BLACK, (375, 555, 250, 90))    
            backButton = UIFONTSMALL.render("Back", 1, WHITE)
            screen.blit(backButton, (433, 572, 200, 200)) 
            
            # Whip 
            if whipLevel == 5:
                upgradeWhipPlus = UIFONTSMALL.render("+", 1, YELLOW)
                whipLevelText = UIFONTSMALLER.render("Lvl. Max", 1, YELLOW)
            else:
                whipLevelText = UIFONTSMALLER.render("Lvl. %s"%whipLevel, 1, WHITE)
                if playerMoney >= ((whipLevel + 1)**2 * 20):
                    upgradeWhipPlus = UIFONTSMALL.render("+", 1, GREEN)
                else:
                    upgradeWhipPlus = UIFONTSMALL.render("+", 1, RED)
                
            
            pygame.draw.rect(screen, WHITE, (190, 125, 120, 120))
            pygame.draw.rect(screen, BLACK, (195, 130, 110, 110)) 
            pygame.draw.rect(screen, ORANGE, (245, 140, 20, 70))            
            
            whipText = UIFONTSMALLER.render("WHIP", 1, WHITE)
            screen.blit(whipText, (195, 82, 200, 200))   
            screen.blit(upgradeWhipPlus, (325, 122, 200, 200)) 
            screen.blit(whipLevelText, (325, 195, 200, 200))
            
            # Bow - 200 spacing
            if not haveBow:
                if playerMoney >= 500:
                    buyBowText = UIFONTSMALL.render("BUY", 1, GREEN)
                    upgradeBowPlus = UIFONTSMALL.render("+", 1, RED)
                else:
                    buyBowText = UIFONTSMALL.render("BUY", 1, RED)
                    upgradeBowPlus = UIFONTSMALL.render("+", 1, RED)
                
                screen.blit(buyBowText, (50, 360, 200, 200))
            else:
                if bowLevel == 5:
                    upgradeBowPlus = UIFONTSMALL.render("+", 1, YELLOW)
                    bowLevelText = UIFONTSMALLER.render("Lvl. Max", 1, YELLOW)
                else:
                    bowLevelText = UIFONTSMALLER.render("Lvl. %s"%bowLevel, 1, WHITE)
                    if playerMoney >= (bowLevel + 1)**2 * 40:
                        upgradeBowPlus = UIFONTSMALL.render("+", 1, GREEN)
                    else:
                        upgradeBowPlus = UIFONTSMALL.render("+", 1, RED)
                
                screen.blit(bowLevelText, (325, 395, 200, 200))    
            
            bowText = UIFONTSMALLER.render("BOW", 1, WHITE)
            
            pygame.draw.rect(screen, WHITE, (190, 325, 120, 120))
            pygame.draw.rect(screen, BLACK, (195, 330, 110, 110)) 
            pygame.draw.rect(screen, WHITE, (245, 340, 20, 70))       
            
            screen.blit(bowText, (200, 282, 295, 200))   
            screen.blit(upgradeBowPlus, (325, 322, 200, 200)) 
            
            # Garlic
            if not haveGarlic:
                if playerMoney >= 1500:
                    buyGarlicText = UIFONTSMALL.render("BUY", 1, GREEN)
                    upgradeGarlicPlus = UIFONTSMALL.render("+", 1, RED)
                else:
                    buyGarlicText = UIFONTSMALL.render("BUY", 1, RED)
                    upgradeGarlicPlus = UIFONTSMALL.render("+", 1, RED)
                
                screen.blit(buyGarlicText, (550, 160, 200, 200))
            else:
                if garlicLevel == 5:
                    upgradeGarlicPlus = UIFONTSMALL.render("+", 1, YELLOW)
                    garlicLevelText = UIFONTSMALLER.render("Lvl. Max", 1, YELLOW)
                else:
                    garlicLevelText = UIFONTSMALLER.render("Lvl. %s"%garlicLevel, 1, WHITE)
                    if playerMoney >= (garlicLevel + 1)**2 * 80:
                        upgradeGarlicPlus = UIFONTSMALL.render("+", 1, GREEN)
                    else:
                        upgradeGarlicPlus = UIFONTSMALL.render("+", 1, RED)
                
                screen.blit(garlicLevelText, (825, 195, 200, 200))    
            
            garlicText = UIFONTSMALLER.render("GARLIC", 1, WHITE)
            
            pygame.draw.rect(screen, WHITE, (690, 125, 120, 120))
            pygame.draw.rect(screen, BLACK, (695, 130, 110, 110)) 
            pygame.draw.circle(screen, WHITE, (750, 185), 25)

            screen.blit(garlicText, (670, 82, 295, 200))   
            screen.blit(upgradeGarlicPlus, (825, 122, 200, 200))             

            # Player level (affects health, regen amount)
            if playerLevel == 10:
                upgradeLevelPlus = UIFONTSMALL.render("+", 1, YELLOW)
                playerLevelText = UIFONTSMALLER.render("Lvl. Max", 1, YELLOW)
            else:
                playerLevelText = UIFONTSMALLER.render("Lvl. %s"%playerLevel, 1, WHITE)
                if playerMoney >= ((playerLevel + 1)**2 * 20):
                    upgradeLevelPlus = UIFONTSMALL.render("+", 1, GREEN)
                else:
                    upgradeLevelPlus = UIFONTSMALL.render("+", 1, RED)
                
            
            pygame.draw.rect(screen, WHITE, (690, 325, 120, 120))
            pygame.draw.rect(screen, BLACK, (695, 330, 110, 110)) 
            pygame.draw.circle(screen, RED, (737, 380), 15)
            pygame.draw.circle(screen, RED, (763, 380), 15)   
            pygame.draw.polygon(screen, RED, ((725, 388), (774, 388), (750, 412),))          
            
            pLevelText = UIFONTSMALLER.render("PLAYER LEVEL", 1, WHITE)
            screen.blit(pLevelText, (600, 282, 200, 200))   
            screen.blit(upgradeLevelPlus, (825, 322, 200, 200)) 
            screen.blit(playerLevelText, (825, 395, 200, 200))
            
            if mouse1Pressed:
                    for x in range(325, 360):
                        if whipLevel < 5:
                            for y in range(122, 170):
                                if mousePressedPos == (x, y):
                                    if playerMoney >= (whipLevel + 1)**2 * 20:
                                        playerMoney -= (whipLevel + 1)**2 * 20   
                                        whipLevel += 1
                                        whipDAMAGE += 5
                                        upgradeSound.play()
                        if haveBow:
                            for y in range(322, 370):
                                if mousePressedPos == (x, y):
                                    if playerMoney >= (bowLevel + 1)**2 * 40 and bowLevel < 5:
                                        playerMoney -= (bowLevel + 1)**2 * 40 
                                        bowLevel += 1          
                                        bowDAMAGE += 7     
                                        upgradeSound.play                                  
                
                    if not haveBow:
                        for x in range(50, 165):
                            for y in range(360, 410):
                                if mousePressedPos == (x, y):
                                    if playerMoney >= 500:
                                        playerMoney -= 500
                                        haveBow = True
                                        currentWeapon = 'Bow'
                                        buySound.play()
                    
                    for x in range(825, 860):
                        if playerLevel < 10:
                            for y in range(322, 370):
                                if mousePressedPos == (x, y):
                                    if playerMoney >= (playerLevel + 1)**2 * 20:
                                        playerMoney -= (playerLevel + 1)**2 * 20   
                                        playerLevel += 1
                                        upgradeSound.play()
                        if haveGarlic:
                            for y in range(122, 170):
                                if mousePressedPos == (x, y):
                                    if playerMoney >= (garlicLevel + 1)**2 * 80 and garlicLevel < 5:
                                        playerMoney -= (garlicLevel + 1)**2 * 80
                                        garlicLevel += 1
                                        upgradeSound.play()
                    
                    if not haveGarlic:
                        for x in range(550, 665):
                            for y in range(160, 208):
                                if mousePressedPos == (x, y):
                                    if playerMoney >= 1500:
                                        playerMoney -= 1500
                                        haveGarlic = True
                                        currentWeapon = 'Garlic'
                                        buySound.play()

                    for x in range(370, 530):
                        for y in range(550, 650):
                            if mousePressedPos == (x, y):
                                menuState -= 1
                                menuSound.play()
            
        if menuState == 1:
            MenuText1 = UIFONTLARGEALT.render("Gravenight", 1, WHITE)
            screen.blit(MenuText1, (215, 30, 200, 200))  

            for y in range(250, 451, 200):
                pygame.draw.rect(screen, WHITE, (300, y, 400, 100))
                pygame.draw.rect(screen, BLACK, (305, y+5, 390, 90)) 
            
            playButton = UIFONTSMALL.render("Play", 1, WHITE)
            quitButton = UIFONTSMALL.render("Quit", 1, WHITE)

            screen.blit(playButton, (440, 272, 200, 200))
            screen.blit(quitButton, (440, 472, 200, 200))
            if mouse1Pressed:
                for x in range(300, 700):
                            for y in range(250, 350):
                                if mousePressedPos == (x, y):
                                    menuState += 1
                                    menuSound.play()
                            for y in range(450, 550):
                                if mousePressedPos == (x, y):
                                    menuSound.play()
                                    pygame.quit()
        
        if menuState == 0:
            MenuText1 = UIFONTLARGEALT.render("You win!", 1, WHITE)
            screen.blit(MenuText1, (283, 30, 200, 200))  

            playButton = UIFONTSMALL.render("Play again", 1, WHITE)
            quitButton = UIFONTSMALL.render("Quit", 1, WHITE)

            for y in range(250, 451, 200):
                pygame.draw.rect(screen, WHITE, (300, y, 400, 100))
                pygame.draw.rect(screen, BLACK, (305, y+5, 390, 90)) 

            screen.blit(playButton, (370, 272, 200, 200))
            screen.blit(quitButton, (440, 472, 200, 200))

            if mouse1Pressed:
                for x in range(300, 700):
                            for y in range(250, 350):
                                if mousePressedPos == (x, y):
                                    menuState += 1
                                    nightState = 1
                                    menuSound.play()
                                    haveBow = False
                                    haveGarlic = False
                                    whipLevel = 0
                                    bowLevel = 0
                                    garlicLevel = 0
                                    playerLevel = 0
                                    playerMoney = 0
                                    newGame = True
                        
                            for y in range(450, 550):
                                if mousePressedPos == (x, y):
                                    menuSound.play()
                                    pygame.quit()

        pygame.display.flip()
        mouse1Pressed = False
        IGT.tick(60) 

    newGame = False       