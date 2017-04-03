"""Handles game and game-state logic."""
import pygame
from model.paddle import Position
from audio import sounds


def check_if_score(ball, paddle, screen_dim):
    """Check if a score occured, and update the score accordingly."""
    if ((ball.is_left_score(0) and paddle.position == Position.Left)
       or (ball.is_right_score(screen_dim[0])
       and paddle.position == Position.Right)):
        sounds.POINT.play()
        paddle.add_point()
        ball.reset((screen_dim[0]/2, screen_dim[1]/2))


def check_paddle_hit(ball, paddle):
    """Rebound the ball if it hits a paddle."""
    if pygame.sprite.collide_rect(ball, paddle):
        sounds.REBOUND.play()
        ball.bounce_from_paddle(paddle.get_paddle_edge())
