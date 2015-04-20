#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Munnu
#
# Created:     04/17/2015
# Copyright:   (c) Munnu 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random
import pygame, sys, time
from PIL import Image

CAPTION = "Benttoru Food Game"
SCREEN_SIZE = WIDTH, HEIGHT = [800, 600]
BACKGROUND_COLOR = [153, 204, 255]
BG_IMAGE_PATH = "images/cloudBG.jpg"
FONT_SIZE = 50
ORIGIN = (0, 0)
MAX_Y = 50  # limit for the items to be drawn in
MAX_TIME = 10000  # in milliseconds
MAX_SUSHI_WIN_AMOUNT = 1
GAME_SCORE_WIN_FOR_LEVELS = {1: {'sushi_win_amount': 1}, 2: {'sushi_win_amount': 1}, 3: {'sushi_win_amount': 1}}   # adjust amount later
MAX_GAME_LEVELS = len(GAME_SCORE_WIN_FOR_LEVELS)


class Timer():
    def __init__(self):
        self.old_position = 0
        self.current_position = 0
        self.old_time = 0
        #self.outer_rect_width = 30
        self.outer_rect_dimensions = {'x_pos': 50, 'y_pos': 10, 'width': WIDTH/2, 'height': 50}  # x, y, width, height
        self.outer_rect_dimensions_tuple = (self.outer_rect_dimensions['x_pos'], self.outer_rect_dimensions['y_pos'],
                                            self.outer_rect_dimensions['width'], self.outer_rect_dimensions['height'])
        self.radius = self.outer_rect_dimensions['height']/2
        self.outer_width = 2
        self.timer_height = (self.outer_rect_dimensions['y_pos'] + self.outer_rect_dimensions['height'])/2 + self.outer_width * 2
        self.inner_width = 0

    def draw_timer(self):
        outer_rectangle = pygame.draw.rect(screen, (11, 100, 247), self.outer_rect_dimensions_tuple)
        duration_line = pygame.draw.line(screen, (130, 141, 22),
                                         (self.outer_rect_dimensions['x_pos'],
                                         self.outer_rect_dimensions['y_pos'] + self.outer_rect_dimensions['height']/2),
                                         (self.outer_rect_dimensions['width'] + self.outer_rect_dimensions['x_pos'],
                                          self.outer_rect_dimensions['y_pos'] + self.outer_rect_dimensions['height']/2), 10)

        inner_circle = pygame.draw.circle(screen, (127, 127, 225),
            (self.outer_rect_dimensions['x_pos'] + self.radius + self.current_position, self.timer_height),
            self.radius, self.inner_width)

        outer_circle = pygame.draw.circle(screen, (127, 225, 127),
            (self.outer_rect_dimensions['x_pos'] + self.radius + self.current_position, self.timer_height),
            self.radius, self.outer_width)

        progress_line = pygame.draw.line(screen, (130, 0, 0),
                                         (self.outer_rect_dimensions['x_pos'], self.outer_rect_dimensions['y_pos'] +
                                          self.outer_rect_dimensions['height']/2),
                                         (inner_circle[0], self.outer_rect_dimensions['y_pos'] +
                                          self.outer_rect_dimensions['height']/2), 10)

    def elapse_time(self, max_time):
        current_time = pygame.time.get_ticks()/1000  # convert from milliseconds to seconds
        slider_width = self.outer_rect_dimensions['width'] - self.radius
        dx = int(round(slider_width/(max_time/1000.0)))
        #print "ct", current_time, "ot", self.old_time
        if (self.current_position <= slider_width) and (current_time - self.old_time >= 1):
            self.old_position = self.current_position
            self.current_position += dx
            self.old_time = current_time
        self.draw_timer()


class Score():
    def __init__(self, font):
        self.score = 0
        self.score_font_color = (0, 0, 0)
        self.antialias = 1
        self.score_text = font.render(str(self.score), self.antialias, self.score_font_color)  # Displays score
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.left, self.score_text_rect.top = (WIDTH-self.score_text_rect[2],
                                                               HEIGHT-self.score_text_rect[3])

    def update(self, new_score, font):
        self.score = new_score
        self.score_text = font.render(str(self.score), self.antialias, self.score_font_color)  # Displays score

    def draw(self, timer):
        score_start_position = (timer.outer_rect_dimensions['x_pos'] + timer.outer_rect_dimensions['width'] + 50,
                                timer.outer_rect_dimensions['y_pos'] + self.score_text_rect[2]/2)
        screen.blit(self.score_text, score_start_position)

    def get_score(self):
        return self.score


class CurrentLevelText():
    def __init__(self, font, current_level, timer):
        self.current_level = current_level
        self.current_level_font_color = (0, 0, 0)
        self.antialias = 1
        self.current_level_text = font.render(str("Level " + str(self.current_level)), self.antialias, self.current_level_font_color)
        self.current_level_text_rect = self.current_level_text.get_rect()
        self.current_level_text_rect.left, self.current_level_text_rect.top = (
            WIDTH - self.current_level_text.get_width() - 10, self.current_level_text.get_height()/2)

    def draw(self):
        screen.blit(self.current_level_text, self.current_level_text_rect)

    def get_current_level(self):
        return self.current_level


class Benttoru(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.dog_path = 'images/benttoru.jpg'
        self.image = pygame.image.load(self.dog_path)  # load sprite from path/file loc.
        self.rect = self.image.get_rect()  # get bounds of image
        self.imageHeight = self.image.get_height()
        self.speed = [3, 0]
        self.start_coords = [0, HEIGHT - self.imageHeight]
        self.start_location = self.rect.left, self.rect.top = self.start_coords

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        """ get Benttoru to move """
        if (self.rect.left < 0) or (self.rect.right >= WIDTH):
            self.speed[0] = -self.speed[0]
            self.image = pygame.transform.flip(self.image, True, False)
            screen.blit(self.image, self.rect)
        self.rect = self.rect.move(self.speed)


class EatingBird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.bird_path = 'images/benttoru.jpg'  # for now, change later
        self.image = pygame.image.load(self.bird_path)  # load sprite from path/file loc.
        self.rect = self.image.get_rect()  # get bounds of image
        self.imageWidth = self.image.get_width()
        self.speed = [0, 5]
        self.start_coords = [WIDTH - self.imageWidth, MAX_Y]
        self.start_location = self.rect.left, self.rect.top = self.start_coords

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        """ get eating bird to move """
        if (self.rect.top < MAX_Y) or (self.rect.bottom >= HEIGHT - self.image.get_height()):
            self.speed[1] = -self.speed[1]
        self.rect = self.rect.move(self.speed)

    def check_collision(self, sushi):
        """
        checks to see if EatingBird and sushi meet
        :param sushi: The items to collect of sprite object type
        :return: True
        """
        if pygame.sprite.collide_rect(self, sushi):
            return True


class Sushi(pygame.sprite.Sprite):
    """ creates a single sushi """
    def __init__(self, timer, benttoru):
        pygame.sprite.Sprite.__init__(self)
        self.sushi_paths = ['images/sushi/sushi1.jpg', 'images/sushi/sushi2.jpg']
        self.image = pygame.image.load(self.sushi_paths[random.randrange(0, len(self.sushi_paths))])
        self.start_coords = [0, random.randrange(timer.outer_rect_dimensions['y_pos'] + timer.outer_rect_dimensions['height'],
                                                 HEIGHT - (benttoru.imageHeight*2))]  # random start coordinates in Y
        self.rect = self.image.get_rect()
        self.start_location = self.rect.left, self.rect.top = self.start_coords
        self.rect = self.image.get_rect(topleft=self.start_location)  # force set the start_location
        self.speed = [random.randrange(1, 7), 0]  # random X speed
        self.is_dragged = False

    def update(self):
        """
        move sushi pieces from one side of the screen to the other
        """
        self.rect = self.rect.move(self.speed)  # set the new image location by speed of sushi

    def get_event(self, event, sushi_single):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_on_image = self.rect.collidepoint(pygame.mouse.get_pos())
            if mouse_on_image:
                sushi_single.add(self)
                self.is_dragged = True
                print "this is sushi_single", sushi_single
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragged = False

        if self.is_dragged:
            for sushi in sushi_single:
                sushi.rect.topleft = pygame.mouse.get_pos()  # set top left loc as mouse pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def new_sushi_create(self, sushi_group, timer, benttoru):
        new_sushi = Sushi(timer, benttoru)  # recreate a new sushi in old sushi's place
        for sushi in sushi_group:
            while new_sushi.rect.colliderect(sushi):
                new_sushi = Sushi(timer, benttoru)  # while the new sushi happens to be on top of an old one
        sushi_group.add(new_sushi)

    def check_collision(self, sushi_group, benttoru, eating_bird, timer, score, font):
        """
        checks to see if Benttoru and sushi meet
        :param sushi_group: Sprite group that holds all the sushi
        :param benttoru: The dog/main character
        :param eating_bird: the very hungry bird who likes sushi
        :param timer: the timer at the top of the game screen.
                            Used as height cutoff for sushi
        :param score: self explanatory, game score.
        """
        if (self.rect.right >= WIDTH) or (self.rect.bottom >= HEIGHT):
            sushi_group.remove(self)  # remove sushi from sprite group
            self.new_sushi_create(sushi_group, timer, benttoru)
        elif pygame.sprite.collide_rect(self, benttoru):
            sushi_group.remove(self)
            self.new_sushi_create(sushi_group, timer, benttoru)
            new_score = score.score + 1
            score.update(new_score, font)
        elif pygame.sprite.collide_rect(self, eating_bird):
            sushi_group.remove(self)
            self.new_sushi_create(sushi_group, timer, benttoru)
            new_score = 0
            score.update(new_score, font)
        else:
            self.update()


class Control(object):
    """ holds base game stuff, is the controller/middle-person """
    def __init__(self, current_level):
        """
        initialize the important parts of the game
        """
        self.current_level = current_level
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()  # if needed
        self.background = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()  # fps clock
        self.fps = 30.0
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.keys = pygame.key.get_pressed()
        self.start_time = 0
        self.done = False
        # -------------------
        self.game_over = EndGameScreen()
        self.timer = Timer()
        self.score = Score(self.font)
        self.current_level_text = CurrentLevelText(self.font, self.current_level, self.timer)
        # -------------------
        self.benttoru = Benttoru()
        self.eating_bird = EatingBird()
        self.sushi_group = pygame.sprite.Group()
        self.sushi_single = pygame.sprite.GroupSingle()  # for storing a single sprite in a group
        print self.sushi_single.__dict__
        for i in range(3):  # generate 3 sushi on screen
            self.sushi = Sushi(self.timer, self.benttoru)
            self.sushi_group.add(self.sushi)
        print self.sushi_group

    def event_loop(self):
        """ events for this game (clicking actions, etc) """
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
                sys.exit()
            for sushi_piece in self.sushi_group:
                sushi_piece.get_event(event, self.sushi_single)

    def update(self):
        """ updates Timer, Benttoru, Bird, and Sushi """
        self.timer.elapse_time(MAX_TIME)
        self.benttoru.update()
        self.eating_bird.update()
        for sushi_piece in self.sushi_group:
            sushi_piece.check_collision(self.sushi_group, self.benttoru, self.eating_bird, self.timer, self.score,
                                        self.font)
            sushi_piece.update()

    def draw(self):
        """ draw base elements of game """
        self.background.fill(BACKGROUND_COLOR)
        self.background = pygame.image.load(BG_IMAGE_PATH)
        self.screen.blit(self.background, ORIGIN)
        self.timer.draw_timer()
        self.score.draw(self.timer)
        self.current_level_text.draw()
        self.benttoru.draw(self.screen)
        self.eating_bird.draw(self.screen)
        for sushi_piece in self.sushi_group:
            sushi_piece.draw(self.screen)

    def main_loop(self):
        """ main game loop that calls all the other methods/classes """
        self.start_time = pygame.time.get_ticks()
        while not self.done and pygame.time.get_ticks() - self.start_time < MAX_TIME:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)  # wait a little while before starting again
        return self.score.get_score()  # this is the game status


class GameOverText():
    def __init__(self):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.font_color = {'base_color': (0, 0, 0), 'win_color': (0, 0, 0),
                           'lose_color': (0, 0, 0), 'misc_color': (0, 0, 0)}
        self.game_over_text = self.font.render("Game Over", 1, self.font_color['base_color'])
        self.lose = self.font.render("You Lose.", 1, self.font_color['lose_color'])
        self.win = self.font.render("You Win.", 1, self.font_color['win_color'])
        self.play_again = self.font.render("Play Again?", 1, self.font_color['misc_color'])
        self.play_again_rect = self.play_again.get_rect()
        self.play_again_rect.left, self.play_again_rect.top = (WIDTH-self.play_again_rect[2],
                                                               HEIGHT-self.play_again_rect[3])

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                self.play_again_rect.collidepoint(pygame.mouse.get_pos()):
            # start game over
            print "start game over"
            return True
        return False

    def draw(self, score):
        screen.blit(self.game_over_text, ((WIDTH/2) - 95, HEIGHT/2))
        if score < MAX_SUSHI_WIN_AMOUNT:  # update this number to a higher number later
            screen.blit(self.lose, ((WIDTH/2) - 95, (HEIGHT/2)+30))
        else:
            screen.blit(self.win, ((WIDTH/2) - 95, (HEIGHT/2)+30))
        screen.blit(self.play_again, self.play_again_rect)


class EndGameScreen():
    """ End Game Screen """
    def __init__(self):
        """ initialize the important parts of the ending screen """
        self.keys = pygame.key.get_pressed()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()  # if needed
        self.background = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()  # fps clock
        self.fps = 30.0
        self.done = False
        self.play_again_bool = False
        # -----------
        self.game_over_text = GameOverText()

    def draw(self, score):
        self.background.fill(BACKGROUND_COLOR)
        self.background = pygame.image.load(BG_IMAGE_PATH)
        self.screen.blit(self.background, ORIGIN)  # show a wiped screen
        # in the future can call a function/method that blits a new bg and has animations or w/e
        self.game_over_text.draw(score)

    def event_loop(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            return self.game_over_text.get_event(event)

    def game_over_main_loop(self, score):
        """ main game loop that calls all the other methods/classes """
        while not self.done and self.play_again_bool is not True:
            self.play_again_bool = self.event_loop()
            self.draw(score)  # draw win/lose based on score user received
            pygame.display.flip()
            self.clock.tick(self.fps)  # wait a little while before starting again
        return self.play_again_bool

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    continue_gameplay = True
    current_level = 0
    game_status = None
    while continue_gameplay:
        if current_level == 0:
            print "this will be the instruction page area"
            current_level += 1  # bump up to level 1
        else:
            if current_level <= len(GAME_SCORE_WIN_FOR_LEVELS):
                if (game_status is None) or (game_status >= GAME_SCORE_WIN_FOR_LEVELS[current_level]['sushi_win_amount']):
                        # onwards to next level
                        start_game = Control(current_level)
                        game_status = start_game.main_loop()  # gets the user score
                        current_level += 1
                else:
                    game_over = EndGameScreen()
                    continue_gameplay = game_over.game_over_main_loop(game_status)  # true/false continue game
                    current_level = 1  # reset everything
                    game_status = None
            else:
                game_over = EndGameScreen()
                continue_gameplay = game_over.game_over_main_loop(game_status)  # true/false continue game
                current_level = 1  # reset everything
                game_status = None

    pygame.quit()
    sys.exit()