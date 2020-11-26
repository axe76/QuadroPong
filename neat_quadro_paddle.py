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

    def draw(self,win):
        win.blit(self.paddle_img,(self.x,self.y))

class Ball:
    def __init__(self,x,y):
        self.velocity = [random.choice([-1,1]),random.choice([-2,2])]
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.done = False
        self.ball_img = pygame.transform.scale(pygame.image.load(os.path.join("images","ball.png")),(12,12))

    def update(self):
        #Termination
        if self.x > 800 or self.x < 0 or self.y > 800 or self.y < 0:
            self.done = True
            # pygame.quit()
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self,win):
        win.blit(self.ball_img,(self.x,self.y))

    def collide(self,paddle):
        if paddle.id == 0: # Left paddle
            if self.x < paddle.x+30 and self.y + 15 > paddle.y and self.y < paddle.y+140:
                self.x = paddle.x + 30
                self.velocity[0] = -self.velocity[0]
                paddle.score += 1
                paddle.hit = True
            elif self.x <= paddle.x+30 and (self.y + 15 < paddle.y or self.y > paddle.y+140):
                paddle.hit = False

        if paddle.id == 1: # Right Paddle
            if self.x > paddle.x - 15 and self.y + 15 > paddle.y and self.y < paddle.y+140:
                self.x = paddle.x - 15
                self.velocity[0] = -self.velocity[0]
                paddle.score += 1
                paddle.hit = True
            elif self.x >= paddle.x - 15 and (self.y + 15 < paddle.y or self.y > paddle.y+140):
                paddle.hit = False
        
        if paddle.id == 2: # Up paddle
            if self.y < paddle.y+30 and self.x + 15 > paddle.x and self.x < paddle.x+140:
                self.y = paddle.y + 30
                self.velocity[1] = -self.velocity[1]
                paddle.score += 1
                paddle.hit = True
            elif self.y <= paddle.y+30 and (self.x + 15 < paddle.x or self.x > paddle.x+140):
                paddle.hit = False

        if paddle.id == 3: # Down Paddle
            if self.y > paddle.y - 15 and self.x + 15 > paddle.x and self.x < paddle.x+140:
                self.y = paddle.y - 15
                self.velocity[1] = -self.velocity[1]
                paddle.score += 1
                paddle.hit = True
            elif self.y >= paddle.y - 15 and (self.x + 15 < paddle.x or self.x > paddle.x+140):
                paddle.hit = False

        return paddle.hit
        
def draw_win(win,paddles,ball):
    win.fill((50,50,50))
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)
    pygame.display.update()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,500)

def main(genomes,config):
    pygame.init()

    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("QuadroPong")

    nets = []
    ge = []
    paddles = []
    ball = Ball(400,400)

    for x,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        if (x-1)%4 == 0:
            paddles.append(Paddle(0,200,0))
        elif (x-1)%4 == 1:
            paddles.append(Paddle(770,200,1))
        elif (x-1)%4 == 2:
            paddles.append(Paddle(200,0,2))
        elif (x-1)%4 == 3:
            paddles.append(Paddle(200,770,3))
        g.fitness = 0
        ge.append(g)

    clk = pygame.time.Clock()
    speed = 150

    while not ball.done:
        clk.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ball.done = True
                pygame.quit()
                break

        if len(paddles)==0:
            ball.done = True

        for x,paddle in enumerate(paddles):
            ge[x].fitness += 0.1
            
            output = nets[x].activate((abs(paddle.y-ball.y),abs(paddle.x-ball.x)))

            if output[0]<0.5:
                paddle.move_paddle(0)
            else:
                paddle.move_paddle(1)

        for x,paddle in enumerate(paddles):
            if ball.collide(paddle):
                ge[x].fitness += 5
            
            if not paddle.hit:
                ge[x].fitness -= 1
                paddles.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        ball.update()
        draw_win(win,paddles,ball)

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)