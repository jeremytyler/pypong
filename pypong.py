"""Basic pygame setup."""
import sys
import pygame

SIZE = WIDTH, HEIGHT = (500, 480)
PADDLE_BUFFER = 30

screen = pygame.display.set_mode(SIZE)

# Sprite creation
paddle_img = pygame.image.load("img/paddle.png")
ball_img = pygame.image.load("img/ball.png")

left_paddle = paddle_img.get_rect()
right_paddle = left_paddle.copy()
ball = ball_img.get_rect()

# Initial positioning
left_paddle.y = right_paddle.y = HEIGHT/2
left_paddle.x = PADDLE_BUFFER
right_paddle.x = WIDTH - PADDLE_BUFFER

ball.x = WIDTH/2
ball.y = HEIGHT/2

# Main Game Loop
while True:
    for event in pygame.event.get():
        print pygame.event.event_name(event.type)
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    screen.blit(ball_img, ball)
    screen.blit(paddle_img, left_paddle)
    screen.blit(paddle_img, right_paddle)
    pygame.display.flip()
