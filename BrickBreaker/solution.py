""" import pygame
import random

from .game import Game

pygame.init()

WIDTH, HEIGHT = 700, 800

def main():
    run = True
    clock = pygame.time.Clock()

    paddle = Paddle(WIDTH//2 - Game.PADDLE_WIDTH//2,HEIGHT - 10 - Game.PADDLE_HEIGHT, Game.PADDLE_WIDTH, Game.PADDLE_HEIGHT)
    
    ball = Ball(paddle.x + Game.PADDLE_WIDTH//2, paddle.y, Game.BALL_RADIUS)

    score = 0
    hits = 0
    bricks = Game.generate_bricks(15, 10)

    while run:
        clock.tick(Game.FPS)
        Game.draw(Game.WIN, paddle, ball, hits, bricks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        Game.handle_paddle_movement(keys, paddle)   

        ball.move()
        if not Game.handle_collision(ball, paddle):
            lose_text = Game.S_FONT.render(f"You Lost! Your score is {hits}", 1, (255, 0, 0))
            Game.WIN.blit(lose_text, (WIDTH//2 -  lose_text.get_width()/2, HEIGHT//2 - lose_text.get_width()/2))
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
            win_text = Game.S_FONT.render(f"You have WON!", 1, (255, 0, 0))
            Game.WIN.blit(win_text, (WIDTH//2 -  win_text.get_width()/2, HEIGHT//2 - win_text.get_width()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break
    pygame.quit()
    quit()


if __name__ == '__main__':
    main() """
