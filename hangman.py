import pygame
from pygame.sprite import Sprite, Group

import string

import sys

import random

# colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (100, 100, 255)
red = (255, 50, 50)
green = (0, 255, 0)

limbs = [pygame.image.load('blank.png'),
         pygame.transform.scale(pygame.image.load('stickman_body (1).png'), (200, 200)), # [2] (image)
         pygame.transform.scale(pygame.image.load('stickman_body (1) (1).png'), (200, 200)), # [2] (image)
         pygame.transform.scale(pygame.image.load('stickman_body (1) (2).png'), (200, 200)), # [2] (image)
         pygame.transform.scale(pygame.image.load('stickman_body (1) (3).png'), (200, 200)), # [2] (image)
         pygame.transform.scale(pygame.image.load('stickman_body (1) (4).png'), (200, 200)), # [2] (image)
         pygame.transform.scale(pygame.image.load('stickman_body (1) (5).png'), (200, 200))] # [2] (image)
lg = []
guessed_wrong = 0


class Button(Sprite):
    """make the button that will be used on the screen for hangman"""

    def __init__(self, screen, msg=None):
        super().__init__()
        # initialize variables
        self.msg = msg
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        # create font and rect
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, 50, 50)

        self.msg_image = self.font.render(msg, True, black, red)
        self.msg_image_rect = self.msg_image.get_rect()

    def show(self):
        # make the button visible
        self.screen.fill(red, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


buttons = Group()

pygame.init()
screen = pygame.display.set_mode((1000, 600))
screen_rect = screen.get_rect()
pygame.display.set_caption('HANGMAN')
letter_font = pygame.font.SysFont(None, 60)


def get_word():
    with open('words.txt', 'r') as f_obj:
        words = f_obj.readlines()
        w = random.choice(words).rstrip()
        return w

word = get_word()

def get_spaced_word(word, lg=None):
    if lg is None:
        lg = []
    w = ''
    for l in range(len(word)):
        w += '_ '
        for g in lg:
            if word[l].upper() == g.upper():
                w = w[:-2]
                w += g + ' '
    return w



def make_buttons(screen):
    button = Button(screen)
    space_x = button.screen_rect.width - 1.4 * button.rect.width
    num_buttons_x = int(space_x / (button.rect.width * 1.4))
    num_rows = round(26 / num_buttons_x)
    for row_num in range(num_rows):
        for button_num in range(num_buttons_x):
            if len(buttons) <= 25:
                button_letter = string.ascii_letters.lower()[len(buttons)]
                button = Button(screen, button_letter)
                button.rect.x = (button.rect.width + 1.5 * button.rect.width * button_num) - 25
                button.rect.y = (row_num * button.rect.height * 1.5) + 25
                button.msg_image_rect.center = button.rect.center
                buttons.add(button)


make_buttons(screen)

def end(win=True):
    global lg
    global guessed_wrong
    global word
    again = True # [1] (this line)
    if not win:
        screen.fill(red)
        font = letter_font.render('You lose... Try again', 1, black)
        screen.blit(font, (300, 300))
        wordfont = letter_font.render(f'your word was {word}', 1, black)
        screen.blit(wordfont, (300, 400))
    else:
        screen.fill(green)
        font = letter_font.render('YOU WIN', 1, black)
        screen.blit(font, (300, 300))
        wordfont = letter_font.render(f'your word was {word}', 1, black)
        screen.blit(wordfont, (300, 400))
    pygame.display.flip()

    while again:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    again = False
                    buttons.empty()
                    make_buttons(screen)

                    word = get_word()
                    lg = []
                    guessed_wrong = 0


def update():
    screen.fill(blue)
    for i in buttons.sprites():
        i.show()
    label = letter_font.render(get_spaced_word(word, lg), 2, black)
    screen.blit(label, (screen_rect.width / 2 - label.get_width() / 2, 500))
    screen.blit(limbs[guessed_wrong], (500, 200))
    # vertical line
    pygame.draw.line(screen, black, (400, 500), (400, 200), 10)
    # horizontal line
    pygame.draw.line(screen, black, (400, 200), (600, 200), 10)
    # refresh screen
    pygame.display.flip()


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for b in buttons:
                collide = b.rect.collidepoint(mouse_x, mouse_y)
                if collide:
                    lg.append(b.msg)
                    if b.msg in list(word):
                        pass
                    else:
                        guessed_wrong += 1
                    buttons.remove(b)
                    if guessed_wrong >= 6:
                        end(win=False)
                    if get_spaced_word(word, lg).count('_') == 0:
                        end(win=True)
    update()
