import pygame
import os
from random import randint

class Paddle:
    def __init__(self,x,y,pad_id):
        self.x = x
        self.y = y
        self.id = pad_id
        self.dx = 5
        self.dy = 5
        self.score = 0
        self.terminate = False
        if self.id == 0 or self.id == 1:
            self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle_LR.png")))
        if self.id == 2 or self.id == 3:
            self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle_UD.png")))


    def move_paddle(self):
        if self.id == 0 or self.id == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.y >= 0:
                self.y -= self.dy
            if keys[pygame.K_DOWN] and self.y <= 660:
                self.y += self.dy
        if self.id == 2 or self.id == 3:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.x >= 0:
                self.x -= self.dx
            if keys[pygame.K_RIGHT] and self.x <= 660:
                self.x += self.dx

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

    def collide(self,paddle):
        if paddle.id == 0: # Left paddle
            if self.x < paddle.x+30 and self.y > paddle.y and self.y < paddle.y+140:
                self.velocity[0] = -self.velocity[0]
                paddle.score += 1
            # if self.x>=790:
            #     self.velocity[0] = -self.velocity[0]
            # if self.y>790:
            #     self.velocity[1] = -self.velocity[1]
            # if self.y<0:
            #     self.velocity[1] = -self.velocity[1]
        if paddle.id == 1: # Right Paddle
            if self.x > paddle.x and self.y > paddle.y and self.y < paddle.y+140:
                self.velocity[0] = -self.velocity[0]
                paddle.score += 1
    
        if paddle.id == 2: # Up Paddle
            if self.y < paddle.y+30 and self.x > paddle.x and self.x < paddle.x+140:
                self.velocity[1] = -self.velocity[1]
                paddle.score += 1
            
        if paddle.id == 3: # Down Paddle
            if self.y > paddle.y and self.x > paddle.x and self.x < paddle.x+140:
                self.velocity[1] = -self.velocity[1]
                paddle.score += 1

        #Termination
        if self.x > 800 or self.x < 0 or self.y > 800 or self.y < 0:
            self.done = True
            pygame.quit()

        self.x += self.velocity[0]
        self.y += self.velocity[1]

def draw_win(win,paddles,ball):
    win.fill((50,50,50))
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)
    pygame.display.update()

pygame.init()

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("QuadroPong")

run = True

ball = Ball(400,400)
paddles = [Paddle(0,200,0),Paddle(770,200,1),Paddle(200,0,2),Paddle(200,770,3)]

while run:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            #break
    for paddle in paddles:
        paddle.move_paddle()
        ball.collide(paddle)
    draw_win(win,paddles,ball)
