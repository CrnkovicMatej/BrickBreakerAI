import pygame
import random
pygame.init()

WIDTH, HEIGHT = 700, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Brick Braker")

FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_HEIGHT, PADDLE_WIDTH = 20, 100 
BALL_RADIUS = 7

S_FONT = pygame.font.SysFont('comicsans', 50)

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

class Brick:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.hit = False

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x , self.y, self.width, self.height))

    def collide(self, ball):
        #from above 
        if 0 < self.y - ball.y <= ball.radius and self.x - ball.radius/2 <= ball.x <= self.x + self.width + ball.radius/2: 
            self.hit = True
            ball.y_vel *= -1
            return True
        #from below
        elif 0 < ball.y - self.y - self.height <= ball.radius and self.x - ball.radius/2 <= ball.x <= self.x + self.width + ball.radius/2: 
            self.hit = True
            ball.y_vel *= -1
            return True
        #from left
        elif 0 < self.x - ball.x <= ball.radius and self.y - ball.radius <= ball.y <= self.y + self.height + ball.radius:
            self.hit = True
            ball.x_vel *= -1
            return True
        #from right
        elif 0 < ball.x - self.x - self.width <= ball.radius and self.y - ball.radius <= ball.y <= self.y + self.height + ball.radius:
            self.hit = True
            ball.x_vel *= -1
            return True
        """ elif(ball.y <= self.y + self.height and ball.y >= self.y and ball.x >= self.x and ball.x <= self.x + self.width):
            self.hit = True
            ball.y_vel *= -1
            return True
        
        elif(ball.x + ball.radius > self.x and ball.y <= self.y + self.height and ball.y + ball.radius <= self.y):
            self.hit = True
            ball.x_vel *= -1
            return True

        elif(ball.x <= self.x + self.width and ball.x >= self.x + ball.radius  and ball.y <= self.y + self.height and ball.y + ball.radius <= self.y):
            self.hit = True
            ball.x_vel *= -1
            return True """
        return False

def draw(win, paddle, ball, hits, bricks):

    win.fill(BLACK)
    paddle.draw(win)
    ball.draw(win)

    for brick in bricks:
            brick.draw(win)

    hits_text = S_FONT.render(f"Score: {hits}", 1, (255, 0, 0))
    win.blit(hits_text, (WIDTH//2 -  hits_text.get_width()/2, 15))

    pygame.display.update()

def generate_bricks(rows, cols):
    gap = 2
    brick_width = (WIDTH // cols) - gap
    brick_height = 30

    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = Brick(col * brick_width + gap*col , row* brick_height + gap*row, brick_width, brick_height, "white")
            bricks.append(brick)
    return bricks

def handle_collision(ball, paddle):
    if ball.y + ball.radius >= HEIGHT:
        return False
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x <= 0:
        ball.x_vel *=-1
    
    if ball.x + ball.radius >= WIDTH:
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

def handle_paddle_movement(keys, paddle):
    if keys[pygame.K_RIGHT] and paddle.x + PADDLE_WIDTH+ paddle.VEL <= WIDTH:
        paddle.move(right = True)
    elif keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
        paddle.move(right = False)

def main():
    run = True
    clock = pygame.time.Clock()

    paddle = Paddle(WIDTH//2 - PADDLE_WIDTH//2,HEIGHT - 10 - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    ball = Ball(paddle.x + PADDLE_WIDTH//2, paddle.y, BALL_RADIUS)

    score = 0
    hits = 0
    bricks = generate_bricks(15, 10)

    while run:
        clock.tick(FPS)
        draw(WIN, paddle, ball, hits, bricks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, paddle)   

        ball.move()
        if not handle_collision(ball, paddle):
            lose_text = S_FONT.render(f"You Lost! Your score is {hits}", 1, (255, 0, 0))
            WIN.blit(lose_text, (WIDTH//2 -  lose_text.get_width()/2, HEIGHT//2 - lose_text.get_width()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break

        for brick in bricks[:]:
            if(brick.collide(ball)):
                hits +=1
                if brick.hit == True:
                    bricks.remove(brick)
                break
        
        if hits == 150:
            win_text = S_FONT.render(f"You have WON!", 1, (255, 0, 0))
            WIN.blit(win_text, (WIDTH//2 -  win_text.get_width()/2, HEIGHT//2 - win_text.get_width()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
