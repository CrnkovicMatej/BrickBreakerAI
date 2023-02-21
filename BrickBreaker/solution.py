""" import pygame
import random

from .game import Game
pygame.init()

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
 """