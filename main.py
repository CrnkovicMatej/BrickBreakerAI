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
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            inputList = [self.paddle.x, self.paddle.y, self.game.ball.x, self.game.ball.y, self.game.ball.x_vel, self.game.ball.y_vel]
            inputList.append(game_info.score)
            inputList.append(game_info.hits)
            output = net.activate(tuple(inputList))
            if output[0] > 0.5 and self.paddle.x - self.paddle.VEL >= 0:
                self.game.paddle.move(right=False)
            if output[1] > 0.5 and  self.paddle.x + self.game.PADDLE_WIDTH + self.paddle.VEL <= self.game.WIDTH:
                self.game.paddle.move(right=True)

            pygame.display.update()

        pygame.quit()
    
    """def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            game_info = self.game.loop()
            
            pygame.display.update()
            output1 = net.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            output2 = net2.activate(
                (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)


            game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break


    def calculate_fitness(self, genome1, game_info):
        genome1.fitness += game_info.score
        genome1.fitness += game_info.hits"""

gen = 129
def eval_genomes(genomes, config):
    """for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        game = BrickBreakerGame()
        game.train_ai(genome, config)"""
    #pygame.init()
    global gen
    gen += 1
    nets = []
    #agents = []
    ge = []
    

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        #agents.append(game.paddle)
        ge.append(genome)

    for index in range(len(nets)):
        game = BrickBreakerGame()
        paddle = game.game.paddle
        #paddle = agents[index]
        running = True
        penalty = 0  # time penalty for fitness function
        start_ticks = pygame.time.get_ticks()  # to prevent infinite loop, break after 200 seconds
        paddle_bonus = 0
        boxIndex = 0
        clock = pygame.time.Clock()
        while running:
            clock.tick(1000)  # sets highest fps possible for fastest training
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()  
                    break
            game_info = game.game.loop()
            #pygame.display.update() 
            penalty += 0.0001  # time penalty of 1 point per 100 seconds
            # input for NEAT will be the following + 1 or 0 for each brick that's unbroken/broken in order.
            inputList = [paddle.x, paddle.y, game.ball.x, game.ball.y, game.ball.x_vel, game.ball.y_vel]
            #brokenList = [0] * boxIndex
            #for box in game.bricks[0:]:
            #    brokenList[box.index] = 1
            #inputList.extend(brokenList)
            inputList.append(game_info.score)
            inputList.append(game_info.hits)
            output = nets[index].activate(tuple(inputList))
            if output[0] > 0.5 and paddle.x - paddle.VEL >= 0:
                game.paddle.move(right=False)
            if output[1] > 0.5 and  paddle.x + game.game.PADDLE_WIDTH + paddle.VEL <= game.game.WIDTH:
                game.paddle.move(right=True)
            score = game_info.score
            #if score < 5 and paddle.y == game.ball.y + game.ball.radius and paddle.x - game.ball.radius/2 <= game.ball.x <= paddle.x + paddle.width + game.ball.radius/2:
            #    paddle_bonus += 0.8
            ge[index].fitness = score + game_info.hits - penalty #+ paddle_bonus
            if game_info.dead_ball:
                ge[index].fitness -= abs(game.ball.x - paddle.x)/50
                if score == 1:
                    ge[index].fitness -= 5
                running = False
            #pygame.display.update()
            #score_label = game.game.S_FONT.render("Score: " + str(score), 1, (255, 0, 0))
            #game.game.WIN.blit(score_label, (10, 10))
            gen_label = game.game.S_FONT.render("Gen: " + str(gen) + " Species: " + str(index+1), 1, (255, 0, 0))
            game.game.WIN.blit(gen_label, (game.game.WIDTH - gen_label.get_width() - 10, 2))
            pygame.display.update()
            if score >= 49 and game_info.dead_ball:  # saves models that score 49 or beat the game
                pickle.dump(nets[index], open("perfect.pickle", "wb"))
                break
            elif score - penalty >= 46 and game_info.dead_ball:  # saves models that scored 47 or more
                pickle.dump(nets[index], open("best.pickle", "wb"))
                break
            elif score - penalty >= 40 and ge[index].fitness > 44 and game_info.dead_ball:  # saves models with a score over ~42
                pickle.dump(nets[index], open("good.pickle", "wb"))
                break

            if (pygame.time.get_ticks() - start_ticks)/1000 > 20:
                ge[index].fitness -= 8
                running = False
                game_info.dead_ball = True
                print("Infinite loop occurred")
                break
        if running == False:
            continue


def run_neat(config):
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-129')
    #pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))
    winner = pop.run(eval_genomes, 300)
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)

def test_best_network(config):
    with open("best.pickle", "rb") as f:
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

"""import pygame
import random
import neat
import os
import pickle
import time
import numpy as np

from BrickBreaker import Game
pygame.init()


class BrickBreakerGame:
    def __init__(self):
        self.game = Game()
        self.paddle = self.game.paddle
        self.ball = self.game.ball

    def train_ai(self, genome, config):

        run = True
        start_time = time.time()

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            game_info = self.game.loop()

            self.move_ai_paddle(net)
            pygame.display.update()

            duration = time.time() - start_time
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.calculate_fitness(game_info, duration)
                break

        return False


        max_hits = 50
     def test_ai(self):
        run = True
        clock = pygame.time.Clock()

        game = Game()

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

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = Game()
    fitness = 0
    done = False
    while not done:
        state = game.observe()
        output = net.activate(state)
        action = np.argmax(output)
        reward, done = game.play(action)
        fitness += reward

    return fitness

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config) 

def run_neat(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    #pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-11')
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))
    winner = pop.run(eval_genomes)
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)"""