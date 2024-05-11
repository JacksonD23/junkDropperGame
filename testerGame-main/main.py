import pygame, sys, random


from pygame.locals import *
#from pygame.sprite import _Group
#from pygame.sprite import _Group

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
BGCOLOR = SKYBLUE

LEFT = 'left'
RIGHT = 'right'
UP = 'up'

GROUNDLVL = 50
JUMPHEIGHT = 21
assert JUMPHEIGHT % 1.5 == 0, "Jump height must be a multiple of the fall speed"

BADSIZE = 40
PLAYERSIZE = 20

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# IMAGE INITIALIZATION
heartImg = pygame.image.load('testerGame-main\heart.png')
heartImg = pygame.transform.scale(heartImg, (47.25, 37.5))

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
    def __init__(self, color):
        super().__init__()

        self.image = pygame.Surface([PLAYERSIZE, PLAYERSIZE])
        #self.image.fill(BGCOLOR)
        #self.image.set_colorkey(PURPLE)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, PLAYERSIZE, PLAYERSIZE))

        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

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
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    #showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():

    health = 3

    isJump = False
    jumpCount = JUMPHEIGHT

    badsList = pygame.sprite.Group()
    numBads = 5
    dropRate = 1
    for i in range(numBads):
        theBad = bad(random.choice(badFoods), buildBad(), random.randint(85, 115))
        #badsList.append(buildBad())
        badsList.add(theBad)
        print(theBad.getRate())

    speedCounter = -1

    good_sprites_list = pygame.sprite.Group()
    player1 = player(YELLOW)
    player1.rect.x = (WINDOWWIDTH / 2)
    player1.rect.y = (WINDOWHEIGHT - 20 - GROUNDLVL)
    good_sprites_list.add(player1)


    while (health > 0):
        # tick control
        speedCounter += 1
        
        #position getters
        x = player1.rect.x
        if (player1.rect.y > (WINDOWHEIGHT - 20 - GROUNDLVL)):
            player1.rect.y = (WINDOWHEIGHT - 20 - GROUNDLVL)
        y = player1.rect.y

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        
        key_pressed_is = pygame.key.get_pressed()
        if key_pressed_is[K_LEFT] and x >= 8 + 0: 
            player1.moveLeft(8)
        if key_pressed_is[K_RIGHT] and x <= WINDOWWIDTH - 8 - 14: 
            player1.moveRight(8)
        if key_pressed_is[K_UP] and y >= WINDOWHEIGHT - 20 - GROUNDLVL:
            isJump = True
            print("pressed jump")
        if key_pressed_is[K_ESCAPE]:
            terminate()

        
        DISPLAYSURF.fill(BGCOLOR)
        groundRect = pygame.Rect(-5, WINDOWHEIGHT-50, WINDOWWIDTH+10, 50)
        pygame.draw.rect(DISPLAYSURF, BROWN, groundRect)
        grassRect = pygame.Rect(-5, WINDOWHEIGHT-50, WINDOWWIDTH+10, 15)
        pygame.draw.rect(DISPLAYSURF, GRASS, grassRect)

        dropBads(badsList, dropRate)
        
        #badsList, health = checkBads(x, y, badsList, health)
        
        isJump, jumpCount = player1.moveJump(isJump, jumpCount)
        
        drawHealth(health)
        
        
        if (speedCounter % 360 == 0):
            numBads += 2
            dropRate += 0.5
            print("level up")
            print(speedCounter)
        
        if (len(badsList) < numBads):
            for i in range(numBads-len(badsList)):
                badsList.add(bad(random.choice(badFoods), buildBad(), random.randint(85, 115)))
        
        good_sprites_list.update()
        good_sprites_list.draw(DISPLAYSURF)

        badsList.update()
        badsList.draw(DISPLAYSURF)

        pygame.display.flip()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
                

def terminate():
    pygame.quit()
    sys.exit()

def buildBad():
    possibleLocations = range(0+BADSIZE, WINDOWWIDTH-BADSIZE, BADSIZE)
    return [random.choice(possibleLocations), random.randint(-180, 0)]

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def drawHealth(health):
    mover = 70
    for i in range(health):
        DISPLAYSURF.blit(heartImg, (WINDOWWIDTH - mover, 10))
        mover += 60

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, BLACK)
    overSurf = gameOverFont.render('Over', True, BLACK)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return
    

def dropBads(bads, dropRate):
    removeBads = []
    for i in bads:
        i.rect.y += dropRate
        if i.rect.y > WINDOWHEIGHT - 50 - BADSIZE:
            removeBads.append(i)
            continue
        #badRect = pygame.Rect(bads[i][0], bads[i][1], BADSIZE, BADSIZE)
        #pygame.draw.rect(DISPLAYSURF, RED, badRect)
        
        #pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(bads[i][0], bads[i][1], BADSIZE, BADSIZE))
        #DISPLAYSURF.blit(bads[i][2], (bads[i][0], bads[i][1]))

    for i in removeBads:
        bads.remove(i)

def checkBads(x, y, bads, health):
    removeList = []
    xrange = range(int(x)-10, int(x)+10)
    yrange = range(int(y)-10, int(y)+10)
    xTrue = False
    yTrue = False

    for i in range(len(bads)):
        for j in range(len(xrange) - 1):
            if (bads[i][0]+(BADSIZE/2) > xrange[j] and (bads[i][0]+(BADSIZE/2) < xrange[j+1])):
                xTrue = True
                print("xtrue")
        for j in range(len(yrange) - 1):
            if (bads[i][1]-(BADSIZE/2) < yrange[j] and bads[i][1]-(BADSIZE/2) > yrange[j+1]):
                yTrue = True
                print("ytrue")
        if (xTrue and yTrue):
            print("found bad")
            removeList.append(bads[i])
    for i in range(len(removeList)):
        pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(removeList[i][0], removeList[i][1], BADSIZE, BADSIZE))
        health -= 1
        bads.remove(removeList[i])
    return bads, health


def checkJump(isJump, jumpCount):
    if isJump:
        if jumpCount >= -JUMPHEIGHT:
            neg = 1
            if jumpCount < 0:
                neg = -1
            ymove = -1 * jumpCount**2 * 0.1 * neg
            
            jumpCount -= 1.5
            
            return isJump, ymove, jumpCount
        else:
            isJump = False
            jumpCount = JUMPHEIGHT
            return isJump, 0, jumpCount
    else:
        return isJump, 0, jumpCount


if __name__ == '__main__':
    main()