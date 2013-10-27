#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Munnu
#
# Created:     10/11/2013
# Copyright:   (c) Munnu 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random
import pygame, sys

pygame.init()
clock = pygame.time.Clock() # fps clock
font = pygame.font.Font(None, 50)

screenSize = WIDTH, HEIGHT = [800, 600]
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption('Benttoru Food Game')

bgpath = "images/cloudBG.jpg"
background = pygame.Surface(screen.get_size())

bgColorRGB = [153, 204, 255]
background.fill(bgColorRGB)
background = pygame.image.load(bgpath)

sushiPaths = ['images/sushi/sushi1.jpg', 'images/sushi/sushi2.jpg']
sushiGroup = pygame.sprite.Group()
sushiSingle = pygame.sprite.GroupSingle() # for storing a single sprite in a group

clock = pygame.time.Clock()
minY = 50

class Benttoru(pygame.sprite.Sprite):
    def __init__(self, path, speed):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.image.load(path) # load sprite from path/file loc.
        self.rect = self.image.get_rect() # get bounds of image
        self.imageHeight = self.image.get_height()
        self.speed = speed

    # sets location of the image, gets the start location of object
    # sets the start location as the image's left and top location
    def setLocation(self, location):
        self.rect.left, self.rect.top = location

    def charMove(self):
        if ( (self.rect.left < 0) or (self.rect.right >= WIDTH) ):
            self.speed[0] = -self.speed[0]
##            pygame.transform.flip(self.image, True, False)
        self.rect = self.rect.move(self.speed)

    def checkCollision(self, sushi):
        if pygame.sprite.collide_rect(self, sushi):
            return True

class EatingBird(pygame.sprite.Sprite):
    def __init__(self, path, speed):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.image.load(path) # load sprite from path/file loc.
        self.rect = self.image.get_rect() # get bounds of image
        self.imageWidth = self.image.get_width()
        self.speed = speed

    # sets location of the image, gets the start location of object
    # sets the start location as the image's left and top location
    def setLocation(self, location):
        self.rect.left, self.rect.top = location

    def charMove(self):
        if ( (self.rect.top < minY) or (self.rect.bottom >= HEIGHT - self.image.get_height()) ):
            self.speed[1] = -self.speed[1]
        self.rect = self.rect.move(self.speed)

    def checkCollision(self, sushi):
        if pygame.sprite.collide_rect(self, sushi):
            return True

# get the array of sushi. The array of sushi contains a bunch of paths
class Sushi(pygame.sprite.Sprite):
    def __init__(self, path, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = location)
        self.speed = speed
        self.isDragged = False

    # move sushi pieces from one side of the screen to the other
    def sushiMove(self):
        # get speed of sushis
        newImageLocation = self.rect.move(self.speed)
        self.rect = newImageLocation

    def hasCollidedWithWall(self):
        if (self.rect.right >= WIDTH) or (self.rect.bottom >= HEIGHT):
            return True
        return False

    def getMouseDistance(self, mx, my):
        dx, dy = (mx - self.rect.centerx), (my - self.rect.centery)
        return ((dx) ** 2 +(dy) ** 2) ** 0.5

    def mouseOnImage(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        screen.blit(self.image, self.rect)

    def setDrag(self):
        self.rect.topleft = pygame.mouse.get_pos() # set top left loc as mouse pos

#--------- Outside function to create new sushi ----------
def sushiCreate():
    sushiPath = sushiPaths[random.randrange(0, len(sushiPaths))] # random image
    sushiSpeed = [random.randrange(1, 7), 0] # random X speed
    sushiLocation = [0, random.randrange(minY, HEIGHT - 75)] # random Y Location

    newSushi = Sushi(sushiPath, sushiSpeed, sushiLocation)
    sushiGroup.add(newSushi)

#---------- Game Stuff -------------
def startGame():
    score = 0

    # dogPath = ['images/benttoru1.jpg', 'benttoru2.jpg']
    # I do a for loop in the class to
    dogPath = 'images/benttoru.jpg'
    benttoru = Benttoru(dogPath, [3,0])
    benttoru.setLocation([0, HEIGHT - benttoru.imageHeight])

    birdPath = 'images/benttoru.jpg'
    eatingBird = EatingBird(birdPath, [0,5])
    eatingBird.setLocation([WIDTH - eatingBird.imageWidth, minY])

    # eventual list of 3 holding onscreen sushi in the class(?)
    sushiPaths = ['images/sushi/sushi1.jpg', 'images/sushi/sushi2.jpg']
    for i in range(3):
        sushiPath = sushiPaths[random.randrange(0, len(sushiPaths))] # random image
        sushiSpeed = [random.randrange(1, 7), 0] # random X speed
        sushiLocation = [0, random.randrange(minY, HEIGHT - benttoru.imageHeight)] # random Y Location
        sushi = Sushi(sushiPath, sushiSpeed, sushiLocation)
        sushiGroup.add(sushi)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sushiPiece in sushiGroup:
                    if sushiPiece.mouseOnImage():
                        sushiSingle.add(sushiPiece)
                        sushiPiece.isDragged = True
                        #pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                for sushiPiece in sushiGroup:
                    sushiPiece.isDragged = False
        eatingBird.charMove()
        benttoru.charMove()

        for sushi in sushiSingle:
            if sushi.isDragged:
                sushi.setDrag()
        screen.blit(background, (0, 0))
        screen.blit(eatingBird.image, eatingBird.rect)
        screen.blit(benttoru.image, benttoru.rect)
        score_text = font.render(str(score), 1, (0, 0,0)) # Displays score
        screen.blit(score_text, (WIDTH - 50, 10))

        for sushi in sushiGroup:
            sushi.draw()
            if sushi.hasCollidedWithWall():
                sushiGroup.remove(sushi)

                sushiCreate()
            elif benttoru.checkCollision(sushi):
                sushiGroup.remove(sushi)
                sushiCreate()
                score += 1
            elif eatingBird.checkCollision(sushi):
                sushiGroup.remove(sushi)
                sushiCreate()
                score = 0
            else:
                sushi.sushiMove()
        if pygame.time.get_ticks() >= 30000:
            gameOverText = font.render("Game Over", 1, (0, 0, 0))
            screen.blit(gameOverText, ((WIDTH/2) - 95, HEIGHT/2))
            if score < 5:
                lose = font.render("You Lose.", 1, (0, 0, 0))
                screen.blit(lose, ((WIDTH/2) - 95, (HEIGHT/2)+30))
            else:
                win = font.render("You Win.", 1, (0, 0, 0))
                screen.blit(win, ((WIDTH/2) - 95, (HEIGHT/2)+30))


        pygame.display.flip()
        clock.tick(30) # wait a little before starting again
startGame()