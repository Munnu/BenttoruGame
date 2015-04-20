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
import pygame, sys, time
from PIL import Image

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

sushiPaths = ['images/sushi/sushi1.jpg', 'images/sushi/sushi2.jpg']  # change these into PNGs later
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
            self.image = pygame.transform.flip(self.image, True, False)
            screen.blit(self.image, self.rect)
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
        self.location = location
        self.rect = self.image.get_rect(topleft = self.location)
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


class Timer():
    def __init__(self):
        self.old_position = 0
        self.current_position = 0
        self.old_time = 0
        self.outer_rect_width = 30
        self.outer_rect_dimensions = (50, 10, WIDTH/2, 50) # x, y, width, height
        self.radius = self.outer_rect_dimensions[3]/2
        self.outer_width = 2
        self.timer_height = (self.outer_rect_dimensions[1] + self.outer_rect_dimensions[3])/2 + self.outer_width * 2
        self.inner_width = 0

    def draw_timer(self):
        outer_rectangle = pygame.draw.rect(screen, (11, 100, 247), self.outer_rect_dimensions)
        duration_line = pygame.draw.line(screen, (130, 141, 22),
                        (self.outer_rect_dimensions[0], self.outer_rect_dimensions[1] + self.outer_rect_dimensions[3]/2),
                        (self.outer_rect_dimensions[2] + self.outer_rect_dimensions[0],
                         self.outer_rect_dimensions[1] + self.outer_rect_dimensions[3]/2), 10
                        )

        inner_circle = pygame.draw.circle(screen, (127, 127, 225),
            (self.outer_rect_dimensions[0] + self.radius + self.current_position, self.timer_height),
            self.radius, self.inner_width)

        outer_circle = pygame.draw.circle(screen, (127, 225, 127),
            (self.outer_rect_dimensions[0] + self.radius + self.current_position, self.timer_height),
            self.radius, self.outer_width)

        progress_line = pygame.draw.line(screen, (130, 0, 0),
                    (self.outer_rect_dimensions[0], self.outer_rect_dimensions[1] + self.outer_rect_dimensions[3]/2),
                    (inner_circle[0],
                     self.outer_rect_dimensions[1] + self.outer_rect_dimensions[3]/2), 10)

    def elapse_time(self, max_time):
        current_time = pygame.time.get_ticks()/1000  # convert from milliseconds to seconds
        slider_width = self.outer_rect_dimensions[2] - self.radius
        dx = int(round(slider_width/(max_time/1000.0)))
        if (self.current_position <= slider_width) and (current_time - self.old_time == 1):
            self.old_position = self.current_position
            self.current_position += dx
            self.old_time = current_time
        self.draw_timer()


#--------- Outside function to create new sushi ----------
def sushiCreate(max_image_height, game_timer):
    sushiPath = sushiPaths[random.randrange(0, len(sushiPaths))] # random image
    sushiSpeed = [random.randrange(1, 7), 0] # random X speed
    # future: maybe do a check to see if sushi overlaps (x and y) with another sushi already onscreen
    sushiLocation = [0, random.randrange(game_timer.outer_rect_dimensions[1] + game_timer.outer_rect_dimensions[3],
                                         HEIGHT - (max_image_height*2))] # random Y Location

    newSushi = Sushi(sushiPath, sushiSpeed, sushiLocation)
    print "newSushi sushiLocation", newSushi.rect
    for sushi in sushiGroup:
        print "This is sushiGroup", sushi.rect
        if newSushi.rect.colliderect(sushi):
            print "newSushi %s is on top of sushi %s" % (newSushi.rect, sushi.rect)
            print "let's try to fix that..."
            overlapping_point = newSushi.rect[1]-sushi.rect[1]
            # later: figure out by what height they overlap by, and change it to make them not
            newSushi.location = sushiLocation
    sushiGroup.add(newSushi)


#---------- Game Stuff -------------
def startGame():
    score = 0
    max_time = 1  # maxgame time

    game_timer = Timer()
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
        sushiLocation = [0, random.randrange(game_timer.outer_rect_dimensions[1] + game_timer.outer_rect_dimensions[3],
                                         HEIGHT - (benttoru.imageHeight*2))] # random Y Location
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


        if pygame.time.get_ticks() < max_time:
            eatingBird.charMove()
            benttoru.charMove()

            for sushi in sushiSingle:
                if sushi.isDragged:
                    sushi.setDrag()
            screen.blit(background, (0, 0))
            screen.blit(eatingBird.image, eatingBird.rect)
            screen.blit(benttoru.image, benttoru.rect)
            game_timer.elapse_time(max_time)
            score_text = font.render(str(score), 1, (0, 0,0)) # Displays score
            screen.blit(score_text, (WIDTH/2 + 100, 15))

            for sushi in sushiGroup:
                sushi.draw()
                if sushi.hasCollidedWithWall():
                    sushiGroup.remove(sushi)

                    sushiCreate(benttoru.imageHeight, game_timer)
                elif benttoru.checkCollision(sushi):
                    sushiGroup.remove(sushi)
                    sushiCreate(benttoru.imageHeight, game_timer)
                    score += 1
                elif eatingBird.checkCollision(sushi):
                    sushiGroup.remove(sushi)
                    sushiCreate(benttoru.imageHeight, game_timer)
                    score = 0
                else:
                    sushi.sushiMove()
        elif pygame.time.get_ticks() >= max_time:
            screen.blit(background, (0, 0)) # show a wiped screen,
            # in the future can call a function/method that blits a new bg and has animations or w/e
            gameOverText = font.render("Game Over", 1, (0, 0, 0))
            screen.blit(gameOverText, ((WIDTH/2) - 95, HEIGHT/2))
            if score < 5:  # update this number later
                lose = font.render("You Lose.", 1, (0, 0, 0))
                screen.blit(lose, ((WIDTH/2) - 95, (HEIGHT/2)+30))
            else:
                win = font.render("You Win.", 1, (0, 0, 0))
                screen.blit(win, ((WIDTH/2) - 95, (HEIGHT/2)+30))
            play_again = font.render("Play Again?", 1, (0, 0, 0))
            play_again_rect = play_again.get_rect()
            play_again_rect.left, play_again_rect.top = (WIDTH-play_again_rect[2], HEIGHT-play_again_rect[3])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                        play_again_rect.collidepoint(pygame.mouse.get_pos()):
                    # start game over
                    print "start game over"
            screen.blit(play_again, play_again_rect)
            #screen.blit(play_again, (WIDTH - play_again.get_width(), (HEIGHT - play_again.get_height() * 2)+30))


        pygame.display.flip()
        clock.tick(30) # wait a little before starting again
startGame()