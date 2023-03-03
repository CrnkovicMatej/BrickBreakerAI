import pygame
from BrickBreaker import Game

pygame.init()

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    while run:
        game_info = game.loop()
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        if game_info.dead_ball == True:
            run = False
            break
    pygame.time.delay(5000)
    pygame.quit()
    quit()    


if __name__ == '__main__':
    main() 