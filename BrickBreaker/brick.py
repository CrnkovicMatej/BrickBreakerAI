import pygame



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