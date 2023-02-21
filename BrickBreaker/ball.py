import pygame
import random

WHITE = (255,255,255)
class Ball:
    MAX_VEL = -5
    COLOUR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius    
        #self.x_vel = 4
        self.x_vel = random.randint(-6, 6)
        self.y_vel = self.MAX_VEL

    def draw(self, win):
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x 
        self.y = self.original_y 
        #self.x_vel = 4
        self.x_vel = random.randint(-6, 6)
        self.y_vel = self.MAX_VEL