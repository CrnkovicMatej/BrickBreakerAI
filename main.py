import pygame
import random
import neat
import os

from BrickBreaker import Game
pygame.init()


class BrickBreakerGame:
    def __init__(self):
        self.game = Game()
        self.paddle = self.game.paddle
        self.ball = self.game.ball

    def test_ai(self):
        run = True
        clock = pygame.time.Clock()

        #game = Game()

        score = 0
        hits = 0


        while run:
            clock.tick(game.FPS)
            game.draw(game.WIN, game.paddle, game.ball, hits, game.bricks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            game.handle_paddle_movement(keys, game.paddle)   

            game.ball.move()
            if not game.handle_collision(game.ball, game.paddle):
                lose_text = game.S_FONT.render(f"You Lost! Your score is {hits}", 1, (255, 0, 0))
                game.WIN.blit(lose_text, (game.WIDTH//2 -  lose_text.get_width()/2, game.HEIGHT//2 - lose_text.get_width()/2))
                pygame.display.update()
                pygame.time.delay(1000)
                break

            for brick in game.bricks[:]:
                if(brick.collide(game.ball)):
                    hits +=1
                    if brick.hit == True:
                        game.bricks.remove(brick)
                    break
            
            if hits == 150:
                win_text = game.S_FONT.render(f"You have WON!", 1, (255, 0, 0))
                game.WIN.blit(win_text, (game.WIDTH//2 -  win_text.get_width()/2, game .HEIGHT//2 - win_text.get_width()/2))
                pygame.display.update()
                pygame.time.delay(1000)
                break
        pygame.quit()
        quit()


def eval_genomes(genomes, config):
    pass

def run_neat(config):
    #pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-11')
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))
    winner = pop.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config)