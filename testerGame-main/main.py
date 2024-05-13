import pygame, sys, random

from pygame.locals import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# CONSTANT INTIALIZATION
FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
GRASS     = (124, 252,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
SKYBLUE   = (135, 206, 235)
YELLOW    = (255, 255,   0)
BROWN     = (150,  75,   0)
PURPLE    = (160,  32, 240)
PINK      = (255, 105, 180)
DARKPINK  = (170,  51, 106)
BGCOLOR = SKYBLUE


GROUNDLVL = 50
JUMPHEIGHT = 21
assert JUMPHEIGHT % 1.5 == 0, "Jump height must be a multiple of the fall speed"

BADSIZE = 40
PLAYERSIZE = 30

BADSPEEDLOW = 95
BADSPEEDHIGH = 115

HEARTS = 3

SCORE = 0
 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# IMAGE INITIALIZATION
heartImg = pygame.image.load('testerGame-main\heart.png')
heartImg = pygame.transform.scale(heartImg, (47.25, 37.5))
heartDeadImg = pygame.image.load('testerGame-main\heartDead.png')
heartDeadImg = pygame.transform.scale(heartDeadImg, (47.25, 37.5))

carrotImg = pygame.image.load('testerGame-main\carrot.png')
carrotImg = pygame.transform.scale(carrotImg, (PLAYERSIZE, PLAYERSIZE))

grassImg = pygame.image.load('testerGame-main\grass.jpg')
grassImg = pygame.transform.scale(grassImg, (50, GROUNDLVL))
cloudImg = pygame.image.load('testerGame-main\cloud.png')
cloudImg1 = pygame.transform.scale(cloudImg, (80, 40))
cloudImg2 = pygame.transform.scale(cloudImg, (60, 30))
cloudImg3 = pygame.transform.scale(cloudImg, (100, 50))
cloudImg4 = pygame.transform.scale(cloudImg, (50, 25 ))

cloudSizes = [cloudImg1, cloudImg2, cloudImg3, cloudImg4]

dogImg = pygame.image.load('testerGame-main/foods/hotdog.png')
dogImg = pygame.transform.scale(dogImg, (BADSIZE, BADSIZE))
donutImg = pygame.image.load('testerGame-main/foods/donut.png')
donutImg = pygame.transform.scale(donutImg, (BADSIZE, BADSIZE))
cookieImg = pygame.image.load('testerGame-main/foods\cookie.png')
cookieImg = pygame.transform.scale(cookieImg, (BADSIZE, BADSIZE))
pizzaImg = pygame.image.load('testerGame-main/foods\pizza.png')
pizzaImg = pygame.transform.scale(pizzaImg, (BADSIZE, BADSIZE))
milkImg = pygame.image.load('testerGame-main/foods\milkshake.png')
milkImg = pygame.transform.scale(milkImg, (BADSIZE, BADSIZE))

badFoods = [dogImg, donutImg, cookieImg, pizzaImg, milkImg]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# CLASS INITIALIZATION
class player(pygame.sprite.Sprite):
    def __init__(self, color, backcolor):
        super().__init__()

        self.image = pygame.Surface([PLAYERSIZE, PLAYERSIZE])
        
        self.image.fill(backcolor)
        self.image.set_colorkey(backcolor)
        
        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > WINDOWWIDTH - PLAYERSIZE:
            self.rect.x = WINDOWWIDTH - PLAYERSIZE

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    def moveJump(self, isJump, jumpCount):
        if isJump:
            if jumpCount >= -JUMPHEIGHT:
                neg = 1
                if jumpCount < 0:
                    neg = -1
                ymove = -1 * jumpCount**2 * 0.1 * neg
                
                jumpCount -= 2
                
                self.rect.y += ymove

                return isJump, jumpCount
            else:
                isJump = False
                jumpCount = JUMPHEIGHT
                return isJump, jumpCount
        else:
            return isJump, jumpCount
        
    def testCollide(self, listObj, health, bloodyCount, signage):
        collideTester = pygame.sprite.spritecollideany(self, listObj)
        if collideTester != None:
            listObj.remove(collideTester)
            print("collide")
            if signage:
                bloodyCount = 10
                health -= 1
            else:
                bloodyCount = -10
                health += 1
        return health, bloodyCount
    

class bad(pygame.sprite.Sprite):
    def __init__(self, image, pos, rate):
        super().__init__()

        self.rect = pygame.Rect(pos[0], pos[1], BADSIZE, BADSIZE)
        self.image = image
        self.rate = rate

    def getRate(self):
        return self.rate

    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, HIGHSCORE

    pygame.init()
    HIGHSCORE = 0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    showStartScreen()
    while True:
        SCORE = runGame()
        if SCORE > HIGHSCORE:
            HIGHSCORE = SCORE
        showGameOverScreen(SCORE, HIGHSCORE)

def runGame():
 
    bloodyCount = 0
    levelUpCount = 0
    
    health = HEARTS
    maxHealth = HEARTS
    
    SCORE = 0
    
    BACKCOLOR = BGCOLOR

    isJump = False
    jumpCount = JUMPHEIGHT

    badsList = pygame.sprite.Group()
    numBads = 5
    dropRate = 1
    for i in range(numBads):
        theBad = bad(random.choice(badFoods), buildBad(), random.randint(BADSPEEDLOW, BADSPEEDHIGH))
        badsList.add(theBad)
        print(theBad.getRate())

    speedCounter = -1

    good_sprites_list = pygame.sprite.Group()
    player1 = player(YELLOW, BACKCOLOR)
    player1.rect.x = (WINDOWWIDTH / 2)
    player1.rect.y = (WINDOWHEIGHT - PLAYERSIZE - GROUNDLVL)
    good_sprites_list.add(player1)
    
    heartList = pygame.sprite.Group()
    
    cloudList = []
    for i in range(7):
        cloudList.append([random.randint(-1500, -100), random.randint(-5, int(WINDOWHEIGHT/2)), random.randint(1, 4), random.choice(cloudSizes)])
    

    while (health > 0):
        # tick control
        speedCounter += 1
        SCORE += 1 * (dropRate) * 10
        #generate heart maybe
        if (random.random() <= 0.00075 * (1/health)):
            print("build heart")
            heart = bad(heartImg, buildBad(), 100)
            heartList.add(heart)
        
        # position getters
        x = player1.rect.x
        if (player1.rect.y > (WINDOWHEIGHT - PLAYERSIZE - GROUNDLVL)):
            player1.rect.y = (WINDOWHEIGHT - PLAYERSIZE - GROUNDLVL)
        y = player1.rect.y

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        
        # key check
        key_pressed_is = pygame.key.get_pressed()
        if key_pressed_is[K_LEFT]: 
            player1.moveLeft(8)
        if key_pressed_is[K_RIGHT]: 
            player1.moveRight(8)
        if key_pressed_is[K_UP] and y >= WINDOWHEIGHT - PLAYERSIZE - GROUNDLVL:
            isJump = True
            print("pressed jump")
        if key_pressed_is[K_ESCAPE]:
            terminate()

        
        if (speedCounter % 720 == 0 and speedCounter != 0):
            numBads += 2 * 1
            dropRate += 0.5
            print("level up")
            print(speedCounter)
            levelUpCount = 50
            for i in range(30):
                cloudList.append([random.randint(-1500, -100), random.randint(-5, int(WINDOWHEIGHT/2)), random.randint(1, 4), random.choice(cloudSizes)])
            
        
        if (len(badsList) < numBads):
            for i in range(numBads-len(badsList)):
                badsList.add(bad(random.choice(badFoods), buildBad(), random.randint(BADSPEEDLOW, BADSPEEDHIGH)))
        
        # Makes background
        DISPLAYSURF.fill(BACKCOLOR) 

        if levelUpCount > 0:
            levelUpCount -= 1
            showLevelUp(player1)
        
        dropBads(badsList, dropRate)
        dropBads(heartList, 1)
        isJump, jumpCount = player1.moveJump(isJump, jumpCount)
        health, bloodyCount = player1.testCollide(badsList, health, bloodyCount, True)
        health, bloodyCount = player1.testCollide(heartList, health, bloodyCount, False)
        if health > maxHealth:
            health = maxHealth
        
        if bloodyCount > 0:
            BACKCOLOR = RED
            bloodyCount -= 1
        elif bloodyCount < 0:
            BACKCOLOR = GREEN
            bloodyCount += 1
        else:
            BACKCOLOR = SKYBLUE
           
        
        for i in range(int(WINDOWWIDTH/50)+1):
            DISPLAYSURF.blit(grassImg, ((i*50)-5, WINDOWHEIGHT-GROUNDLVL))
        
        
        
        good_sprites_list.update()
        good_sprites_list.draw(DISPLAYSURF)
        

        
        badsList.update()
        badsList.draw(DISPLAYSURF)
        
        runClouds(cloudList, speedCounter, dropRate)
        
        heartList.update()
        heartList.draw(DISPLAYSURF)

        showScore(SCORE)
        showHealth(health, maxHealth)
        DISPLAYSURF.blit(carrotImg, player1.rect)

        pygame.display.flip()
        #pygame.display.update()
        
        FPSCLOCK.tick(FPS)
    return SCORE
                
def terminate():
    pygame.quit()
    sys.exit()

def buildBad():
    possibleLocations = range(3, WINDOWWIDTH-3, BADSIZE)
    return [random.choice(possibleLocations), random.randint(-150, 0)]

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showHealth(health, maxHealth):
    mover = 70
    for i in range(maxHealth):
        if i < health:
            DISPLAYSURF.blit(heartImg, (WINDOWWIDTH - mover, 10))
        else:
            DISPLAYSURF.blit(heartDeadImg, (WINDOWWIDTH - mover, 10))
        mover += 50

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play', True, BLACK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT - 20)
    pygame.draw.rect(DISPLAYSURF, SKYBLUE, pygame.Rect(pressKeyRect.left-5, pressKeyRect.top-6, pressKeyRect.width+10, pressKeyRect.height+12))
    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(pressKeyRect.left-5, pressKeyRect.top-6, pressKeyRect.width+10, pressKeyRect.height+12), 2, 1)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 75)
    titleSurf1 = titleFont.render('Junk Dropper!', True, WHITE, DARKPINK)
    titleSurf2 = titleFont.render('Junk Dropper!', True, PINK)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 1 # rotate by 3 degrees each frame
        degrees2 += 2 # rotate by 7 degrees each frame

def showGameOverScreen(score, highScore):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    scoreFont = pygame.font.Font('freesansbold.ttf', 40)
    gameSurf = gameOverFont.render('Game', True, BLACK)
    overSurf = gameOverFont.render('Over', True, BLACK)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 20)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    
    scoreSurf = scoreFont.render('Final Score: ' + str(int(score/100)), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (WINDOWWIDTH/2, overRect.bottom + 35)
    
    scoreHSurf = scoreFont.render('High Score: ' + str(int(highScore/100)), True, BLACK)
    scoreHRect = scoreHSurf.get_rect()
    scoreHRect.midtop = (WINDOWWIDTH/2, scoreRect.bottom)

    pygame.draw.rect(DISPLAYSURF, SKYBLUE, pygame.Rect(scoreHRect.left-12, scoreRect.top-12, scoreHRect.width+24, scoreHRect.height + scoreRect.height+16))
    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(scoreHRect.left-12, scoreRect.top-12, scoreHRect.width+24, scoreHRect.height + scoreRect.height+16), 2, 1)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    DISPLAYSURF.blit(scoreHSurf, scoreHRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def showLevelUp(player1):
    levelUpSurf = BASICFONT.render('Level Up!', True, GREEN, DARKGREEN)
    levelUpRect = levelUpSurf.get_rect()
    levelUpRect.midtop = (player1.rect.x + 15, player1.rect.y - 30)
    DISPLAYSURF.blit(levelUpSurf, levelUpRect)
    

def showScore(score):
    scoreSurf = BASICFONT.render('Score: ' + str(int(score/100)), True, BLACK, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 10)
    pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(0, 0, scoreRect.right+10, 40))
    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(0, 0, scoreRect.right+10, 40), 2, 1)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def dropBads(bads, dropRate):
    for i in bads:
        i.rect.y += dropRate * (i.getRate() / 100)
        if i.rect.y > WINDOWHEIGHT - 50 - BADSIZE:
            bads.remove(i)

def runClouds(cloudList, tick, rate):
    for i in cloudList:
        if tick % 2 == 0:
            i[0] += (i[2] * rate)
            if i[0] > WINDOWWIDTH + 150:
                i[0] = random.randint(-1500, -100)
                i[1] = random.randint(-5, int(WINDOWHEIGHT/2))
                i[2] = random.randint(1, 4)
                i[3] = random.choice(cloudSizes)
        DISPLAYSURF.blit(i[3], (i[0], i[1]))



if __name__ == '__main__':
    main()