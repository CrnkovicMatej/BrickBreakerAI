import pygame
import math
import random

from .ball import Ball
from .brick import Brick
from .paddle import Paddle

pygame.init()



class Game:

    WIDTH, HEIGHT = 700, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Brick Braker")

    FPS = 60
    WHITE = (255,255,255)
    BLACK = (0,0,0)

    PADDLE_HEIGHT, PADDLE_WIDTH = 20, 100 
    BALL_RADIUS = 7

    S_FONT = pygame.font.SysFont('comicsans', 50)

    def __init__(self):
        self.paddle = Paddle(self.WIDTH//2 - self.PADDLE_WIDTH//2,self.HEIGHT - 10 - self.PADDLE_HEIGHT, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.ball = Ball(self.paddle.x + self.PADDLE_WIDTH//2, self.paddle.y, self.BALL_RADIUS)
        self.bricks = self.generate_bricks(15, 10)

    def generate_bricks(self, rows, cols):
        gap = 2
        brick_width = (self.WIDTH // cols) - gap
        brick_height = 30

        bricks = []
        for row in range(rows):
            for col in range(cols):
                brick = Brick(col * brick_width + gap*col , row* brick_height + gap*row, brick_width, brick_height, "white")
                bricks.append(brick)
        return bricks

    def draw(self, win, paddle, ball, hits, bricks):

        win.fill(self.BLACK)
        paddle.draw(win)
        ball.draw(win)

        for brick in bricks:
                brick.draw(win)

        hits_text = self.S_FONT.render(f"Score: {hits}", 1, (255, 0, 0))
        win.blit(hits_text, (self.WIDTH//2 -  hits_text.get_width()/2, 15))

        pygame.display.update()

    

    def handle_collision(self, ball, paddle):
        if ball.y + ball.radius >= self.HEIGHT:
            return False
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1
        
        if ball.x <= 0:
            ball.x_vel *=-1
        
        if ball.x + ball.radius >= self.WIDTH:
            ball.x_vel *=-1

        if ball.y_vel > 0:
            if ball.x >= paddle.x and ball.x <= paddle.x + paddle.width  :
                if ball.y + ball.radius >= paddle.y:
                    ball.y_vel *= -1

                    middle_x = paddle.x + paddle.width / 2
                    diff_in_x = middle_x - ball.x
                    redu_fact = (paddle.width / 2) / ball.MAX_VEL
                    x_vel = diff_in_x / redu_fact
                    ball.x_vel = x_vel
        return True

    def handle_paddle_movement(self, keys, paddle):
        if keys[pygame.K_RIGHT] and paddle.x + self.PADDLE_WIDTH+ paddle.VEL <= self.WIDTH:
            paddle.move(right = True)
        elif keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
            paddle.move(right = False)