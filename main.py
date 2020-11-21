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
        self.paddle_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","paddle.png")))

    def move_paddle(self):
        if self.id == 0 or self.id == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.y >= 0:
                self.y -= self.dy
            if keys[pygame.K_DOWN] and self.y <= 660:
                self.y += self.dy

    def draw(self,win):
        win.blit(self.paddle_img,(self.x,self.y))

class Ball:
    def __init__(self,x,y):
        self.velocity = [randint(4,8),randint(-8,8)]
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.ball_img = pygame.transform.scale(pygame.image.load(os.path.join("images","ball.png")),(12,12))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    # def move_ball(self):
    #     if self.x>=790:
    #         self.velocity[0] = -self.velocity[0]
    #     if self.x<=0:
    #         self.velocity[0] = -self.velocity[0]
    #     if self.y>790:
    #         self.velocity[1] = -self.velocity[1]
    #     if self.y<0:
    #         self.velocity[1] = -self.velocity[1] 
    #     self.x += self.velocity[0]
    #     self.y += self.velocity[1]

    def draw(self,win):
        win.blit(self.ball_img,(self.x,self.y))

    def collide(self,paddle):
        if paddle.id == 0:
            if self.x < paddle.x+30 and self.y > paddle.y and self.y < paddle.y+140:
                self.velocity[0] = -self.velocity[0]
                paddle.score += 1
            if self.x>=790:
                self.velocity[0] = -self.velocity[0]
            if self.y>790:
                self.velocity[1] = -self.velocity[1]
            if self.y<0:
                self.velocity[1] = -self.velocity[1]
        self.x += self.velocity[0]
        self.y += self.velocity[1]

def draw_win(win,paddle,ball):
    win.fill((50,50,50))
    paddle.draw(win)
    ball.draw(win)
    pygame.display.update()

pygame.init()

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("QuadroPong")

run = True

ball = Ball(400,400)
paddle_L = Paddle(0,200,0)

while run:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            #break
    paddle_L.move_paddle()
    ball.collide(paddle_L)
    draw_win(win,paddle_L,ball)
