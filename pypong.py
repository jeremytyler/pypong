"""Basic pygame setup."""
import sys
import pygame
import game
from display import score
from model import ball, paddle

# Game-scope Constants
WIDTH, HEIGHT = (500, 480)
MAX_FPS = 60
PADDLE_BUFFER_X = 30

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Sprite creation
paddle_left = paddle.Paddle((PADDLE_BUFFER_X, HEIGHT/2), paddle.Position.Left)
paddle_right = paddle.Paddle((WIDTH - PADDLE_BUFFER_X, HEIGHT/2),
                             paddle.Position.Right)
ball = ball.Ball((WIDTH/2, HEIGHT/2))

paddle_sprites = pygame.sprite.Group()
paddle_sprites.add(paddle_left)
paddle_sprites.add(paddle_right)

sprites = pygame.sprite.Group()
sprites.add(paddle_sprites.sprites(), ball)

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

    # Draw score text
    score.draw_score_text(str(paddle_right.score), screen, (WIDTH-106, -46))
    score.draw_score_text(str(paddle_left.score), screen, (WIDTH/5, -46))

    sprites.update((WIDTH, HEIGHT))
    sprites.draw(screen)

    # Update logic
    for paddle_sprite in paddle_sprites:
        game.check_if_score(ball, paddle_sprite, (WIDTH, HEIGHT))
        game.check_paddle_hit(ball, paddle_sprite)

    pygame.display.flip()
