"""Basic pygame setup."""
import sys
import pygame

# Constants
WIDTH, HEIGHT = (500, 480)
WHITE = (255, 255, 255)
PADDLE_BUFFER = 30
MAX_FPS = 60


class Paddle(pygame.sprite.Sprite):
    """Paddle sprite definition."""

    def __init__(self):
        """Basic no-parameter constructor."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 36])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()


class Ball(pygame.sprite.Sprite):
    """Ball sprite definition."""

    speed = [2, 2]

    def __init__(self):
        """Basic no-parameter constructor."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 9])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()


clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Sprite creation
paddle_sprite = Paddle()
ball_sprite = Ball()

left_paddle = paddle_sprite.image.get_rect()
right_paddle = left_paddle.copy()
ball = ball_sprite.image.get_rect()

# Initial positioning
left_paddle.y = right_paddle.y = HEIGHT/2
left_paddle.x = PADDLE_BUFFER
right_paddle.x = WIDTH - PADDLE_BUFFER

ball.x = WIDTH/2
ball.y = HEIGHT/2

# Main Game Loop
while True:
    clock.tick(MAX_FPS)
    print clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))

    # Should isloate this logic to the ball sprite in a "move" method
    ball = ball.move(ball_sprite.speed)
    if ball.left < 0 or ball.right > WIDTH:
        ball_sprite.speed[0] = -ball_sprite.speed[0]
    if ball.top < 0 or ball.bottom > HEIGHT:
        ball_sprite.speed[1] = -ball_sprite.speed[1]

    screen.blit(ball_sprite.image, ball)
    screen.blit(paddle_sprite.image, left_paddle)
    screen.blit(paddle_sprite.image, right_paddle)
    pygame.display.flip()
