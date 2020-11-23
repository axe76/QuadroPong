import pygame
import os
from random import randint
import neat
import numpy as np
import pickle
import math

class Paddle:
    def __init__(self,x,y,pad_id):
        self.x = x
        self.y = y
        self.id = pad_id
        self.dx = 10
        self.dy = 10
        self.score = 0
        self.terminate = False
        if self.id == 0 or self.id == 1:
            self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle_LR.png")))
        if self.id == 2 or self.id == 3:
            self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle_UD.png")))

    def step(self,ball,action):
        self.move_paddle(action)
        self.collide(ball)
        observation = (self.x, self.y, ball.x, ball.y, abs(self.x-ball.x), abs(self.y-ball.y))
        reward = self.score
        return observation, reward, ball.done

    def collide(self,ball):
        if self.id == 0: # Left paddle
            if ball.x < self.x+30 and ball.y > self.y and ball.y < self.y+140:
                ball.velocity[0] = -ball.velocity[0]
                self.score += 1
        
        if self.id == 1: # Right Paddle
            if ball.x > self.x and ball.y > self.y and ball.y < self.y+140:
                ball.velocity[0] = -ball.velocity[0]
                self.score += 1
    
        if self.id == 2: # Up Paddle
            if ball.y < self.y+30 and ball.x > self.x and ball.x < self.x+140:
                ball.velocity[1] = -ball.velocity[1]
                self.score += 1
            
        if self.id == 3: # Down Paddle
            if ball.y > self.y and ball.x > self.x and ball.x < self.x+140:
                ball.velocity[1] = -ball.velocity[1]
                self.score += 1

        #Termination
        if ball.x > 800 or ball.x < 0 or ball.y > 800 or ball.y < 0:
            ball.done = True
            pygame.quit()

        ball.x += ball.velocity[0]
        ball.y += ball.velocity[1]


    def move_paddle(self,action):
        if self.id == 0 or self.id == 1:
            if action == 0 and self.y >= 0:
                self.y -= self.dy
            if action == 1 and self.y <= 660:
                self.y += self.dy
        if self.id == 2 or self.id == 3:
            if action == 0 and self.x >= 0:
                self.x -= self.dx
            if action == 1 and self.x <= 660:
                self.x += self.dx
    
    def get_observation(self,ball):
        return (self.x, self.y, ball.x, ball.y, abs(self.x-ball.x), abs(self.y-ball.y))


    def draw(self,win):
        win.blit(self.paddle_img,(self.x,self.y))

class Ball:
    def __init__(self,x,y):
        self.velocity = [randint(1,2),randint(-2,2)]
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.done = False
        self.ball_img = pygame.transform.scale(pygame.image.load(os.path.join("images","ball.png")),(12,12))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self,win):
        win.blit(self.ball_img,(self.x,self.y))

    def reset(self):
        # try reseting the paddle position
        self.x = 400
        self.y = 400
        self.velocity = [randint(1,2),randint(-2,2)]
        
        return 
    
def draw_win(win,paddles,ball):
    win.fill((50,50,50))
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)
    pygame.display.update()

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, n=5000) # n is no. of generations

def main(genomes,config):
    pygame.init()

    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("QuadroPong")

    ball = Ball(400,400)
    paddles = [Paddle(0,200,0),Paddle(770,200,1),Paddle(200,0,2),Paddle(200,770,3)]
    t = 0
    while not ball.done:
        pygame.time.delay(20)    
        for genome_id_,genome in genomes:
            genome_id = (genome_id_ - 1)%4
            genome.fitness = 0.0
            net = neat.nn.FeedForwardNetwork.create(genome,config)
            
            observation = paddles[genome_id].get_observation(ball)
            flat_observation = np.array(observation)
            action = net.activate(flat_observation)
            step = action.index(max(action))
            observation, reward, done = paddles[genome_id].step(ball,step)
            
            if done:
                print("{} <-- Episode _________ {} timesteps __________ reward {} ".format(genome_id,t + 1, reward))
                break
            genome.fitness = reward
            print("Genome : {}  Fitness : {}".format(genome_id,genome.fitness))
            
            draw_win(win,paddles,ball)
        t += 1
        

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'config-feedforward.txt')
    run(config_path)