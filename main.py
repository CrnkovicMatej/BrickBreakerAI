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
    

gen = 0
def eval_genomes(genomes, config):
    global gen
    gen += 1
    nets = []
    ge = []
    

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    for index in range(len(nets)):
        game = BrickBreakerGame()
        paddle = game.game.paddle
        running = True
        penalty = 0  # time penalty for fitness function
        start_ticks = pygame.time.get_ticks()  # to prevent infinite loop
        paddle_bonus = 0
        boxIndex = 0
        clock = pygame.time.Clock()
        while running:
            clock.tick(1000)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()  
                    break
            game_info = game.game.loop()
            penalty += 0.0001  # time penalty of 1 point per 100 seconds
            inputList = [game.ball.x_vel, game.ball.y_vel, abs(paddle.x -game.ball.x), abs(paddle.y - game.ball.y)]
            output = nets[index].activate(tuple(inputList))
            if output[0] > 0.5 and paddle.x - paddle.VEL >= 0:
                game.paddle.move(right=False)
            if output[1] > 0.5 and  paddle.x + game.game.PADDLE_WIDTH + paddle.VEL <= game.game.WIDTH:
                game.paddle.move(right=True)
            score = game_info.score
            ge[index].fitness = score + game_info.hits - penalty 
            if game_info.dead_ball:
                ge[index].fitness -= abs(game.ball.x - paddle.x)/50
                if score == 1:
                    ge[index].fitness -= 5
                running = False

            gen_label = game.game.S_FONT.render("Gen: " + str(gen) + " Species: " + str(index+1), 1, (255, 0, 0))
            game.game.WIN.blit(gen_label, (game.game.WIDTH - gen_label.get_width() - 10, 2))
            pygame.display.update()
            local_dir = os.path.dirname(__file__)
            if score >= 49 and game_info.dead_ball:  # saves models that score 49 or beat the game
                perfect_path = os.path.join(local_dir, "perfect.pickle")
                with open(perfect_path, 'wb') as f:
                    pickle.dump(nets[index], f)
                break
            elif score - penalty >= 46 and game_info.dead_ball:  # saves models that scored 47 or more
                best_path = os.path.join(local_dir, "best.pickle")
                with open(best_path, 'wb') as f:
                    pickle.dump(nets[index], f)
                break
            elif score - penalty >= 40 and ge[index].fitness > 44 and game_info.dead_ball:  # saves models with a score over ~42
                good_path = os.path.join(local_dir, "good.pickle")
                with open(good_path, 'wb') as f:
                    pickle.dump(nets[index], f)
                break

            if (pygame.time.get_ticks() - start_ticks)/1000 > 500:
                ge[index].fitness -= 8
                running = False
                game_info.dead_ball = True
                print("Infinite loop occurred")
                break
        if running == False:
            continue


def run_neat(config):
    """
    This is a standard configuration to start training the model from the beginning.
    If you want to continue from some checkpoint uncomment the line below 
    and comment the line pop = neat.Population(config)"""
    #pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))
    winner = pop.run(eval_genomes, 100)
    local_dir = os.path.dirname(__file__)
    winner_path = os.path.join(local_dir, "winner.pkl")
    with open(winner_path, 'wb') as f:
        pickle.dump(winner, f)

def test_best_network(config):
    local_dir = os.path.dirname(__file__)
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
    run_neat(config)
    #test_best_network(config)
