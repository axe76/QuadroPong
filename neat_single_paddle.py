import pygame
import os
import random
import neat
import numpy as np
import pickle
import math

class Paddle:
    def __init__(self,x,y,pad_id):
        self.x = x
        self.y = y
        self.id = pad_id
        self.dx = 5
        self.dy = 5
        self.score = 0
        self.hit = True
        self.terminate = False
        if self.id == 0 or self.id == 1:
            self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle_LR.png")))
        if self.id == 2 or self.id == 3:
            self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle_UD.png")))

    def move_paddle(self,action):
        if self.id == 0:
            if action == 0:
                self.y -= self.dy
            if action == 1:
                self.y += self.dy
       
    def draw(self,win):
        win.blit(self.paddle_img,(self.x,self.y))

class Ball:
    def __init__(self,x,y):
        self.velocity = [random.choice([-2,-1,1,2]),random.choice([-2,-1,1,2])]
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

def collide(ball,paddle):
    if paddle.id == 0: # Left paddle
        if ball.x < paddle.x+30 and ball.y > paddle.y and ball.y < paddle.y+140:
            ball.velocity[0] = -ball.velocity[0]
            paddle.score += 1
            
        if ball.x > 785:
            ball.velocity[0] = -ball.velocity[0] 
        if ball.y > 785 or ball.y < 0:
            ball.velocity[1] = -ball.velocity[1]    
    
        ball.x += ball.velocity[0]
        ball.y += ball.velocity[1]


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
    winner = p.run(main, n=10000) # n is no. of generations

def main(genomes,config):
    pygame.init()

    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("QuadroPong")

    run = True

    ball = Ball(400,400)
    paddles = []
    nets = []
    ge = []
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        paddles.append(Paddle(0,200,0))
        genome.fitness = 0
        ge.append(genome)

    while not ball.done:
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ball.done = True
                pygame.quit()
                break
        
        if len(paddles) <= 0:
            ball.done = True
            break
        
        for x,paddle in enumerate(paddles):
    
            ge[x].fitness += 0.1
            
            output = nets[x].activate((paddle.y,abs(paddle.y-ball.y),abs(paddle.x-ball.x)))

            if output[0]>0.5:
                paddle.move_paddle(0)
            else:
                paddle.move_paddle(1)

        for x,paddle in enumerate(paddles):
            collide(ball,paddle)
            #Termination
            if ball.x <= paddle.x + 30 and (ball.y < paddle.y or ball.y > paddle.y+140):
                ball.done = True
                paddle.hit = False
                # pygame.quit()
            if not paddle.hit:
                ge[x].fitness -= 1
                paddles.pop(x)
                nets.pop(x)
                ge.pop(x)
            elif paddle.hit and ball.x <= paddle.x + 30:
                ge[x].fitness += 1
        
        for x,paddle in enumerate(paddles):    
            if paddle.y>=800 or paddle.y+140<0:
                paddles.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_win(win,paddles,ball)


if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'config-feedforward.txt')
    run(config_path)
