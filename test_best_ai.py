import pygame
from BrickBreaker import Game
import pickle
import neat
import os

pygame.init()
class BrickBreakerGame:
    def __init__(self):
        self.game = Game()
        self.paddle = self.game.paddle
        self.ball = self.game.ball
        self.bricks = self.game.bricks

    def test_ai(self, net):
        run = True
        clock = pygame.time.Clock()
        while run:
            game_info = self.game.loop()
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            inputList = [self.game.ball.x_vel, self.game.ball.y_vel, abs(self.paddle.x -self.game.ball.x), abs(self.paddle.y - self.game.ball.y)]
            output = net.activate(tuple(inputList))
            if output[0] > 0.5 and self.paddle.x - self.paddle.VEL >= 0:
                self.game.paddle.move(right=False)
            if output[1] > 0.5 and  self.paddle.x + self.game.PADDLE_WIDTH + self.paddle.VEL <= self.game.WIDTH:
                self.game.paddle.move(right=True)

            pygame.display.update()

        pygame.quit()

def test_best_network(config):
    local_dir = os.path.dirname(__file__)
    #if you wish to test some other pickle this is the place to specify it
    winner_path = os.path.join(local_dir, "winner.pkl")
    with open(winner_path, "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    brick_breaker = BrickBreakerGame()
    brick_breaker.test_ai(winner_net)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    test_best_network(config)