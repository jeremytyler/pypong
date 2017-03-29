"""Basic pygame setup."""
import sys
import pygame
from model import ball, paddle
from display import score

# Game-scope Constants
WIDTH, HEIGHT = (500, 480)
WHITE = (255, 255, 255)
MAX_FPS = 60
PADDLE_BUFFER_X = 30

# Game tech/resource initialization
pygame.mixer.init(48000, -16, 2, 2048)

REBOUND_SOUND = pygame.mixer.Sound('data/sound/rebound.ogg')
BOUNCE_SOUND = pygame.mixer.Sound('data/sound/bounce.ogg')
POINT_SOUND = pygame.mixer.Sound('data/sound/point.ogg')

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Sprite creation
paddle_left = paddle.Paddle((PADDLE_BUFFER_X, HEIGHT/2))
paddle_right = paddle.Paddle((WIDTH - PADDLE_BUFFER_X, HEIGHT/2))
ball = ball.Ball((WIDTH/2, HEIGHT/2))

sprites = pygame.sprite.Group()
sprites.add(paddle_left)
sprites.add(paddle_right)
sprites.add(ball)

# Main Game Loop
while True:
    clock.tick(MAX_FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw background and score display
    screen.fill((0, 0, 0))

    # Draw the dashed "net" in the middle of the play area
    current_y = 0
    while current_y < HEIGHT:
        pygame.draw.line(
            screen, (255, 255, 255), (WIDTH/2, current_y),
            (WIDTH/2, current_y+9))
        current_y += 18
    score.draw_score_text(str(paddle_right.score), screen, (WIDTH-106, -46))
    score.draw_score_text(str(paddle_left.score), screen, (WIDTH/5, -46))

    # Ball logic - TODO - Move to Ball.update
    if ball.is_at_edge(HEIGHT):
        BOUNCE_SOUND.play()
        ball.bounce_from_edge()

    if ball.is_left_score(0):
        POINT_SOUND.play()
        paddle_left.add_point()
        ball.reset((WIDTH/2, HEIGHT/2))
    elif ball.is_right_score(WIDTH):
        POINT_SOUND.play()
        paddle_right.add_point()
        ball.reset((WIDTH/2, HEIGHT/2))

    # Paddle logic - TODO - Move to Paddle.update
    if pygame.sprite.collide_rect(ball, paddle_left):
        REBOUND_SOUND.play()
        # TODO - encapsulate
        ball.bounce_from_paddle(paddle_left.rect.right)
    if pygame.sprite.collide_rect(ball, paddle_right):
        REBOUND_SOUND.play()
        # TODO - encapsulate
        ball.bounce_from_paddle(paddle_right.rect.left - 7)

    sprites.update((WIDTH, HEIGHT))
    sprites.draw(screen)

    pygame.display.flip()
