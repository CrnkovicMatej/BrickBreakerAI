import pygame

WHITE = (255,255,255)
class Paddle:
    COLOUR = WHITE
    VEL = 10
    def __init__(self, x ,y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x , self.y, self.width, self.height))

    def move(self, right = True ):
        if right:
            self.x += self.VEL
        else:
            self.x -= self.VEL