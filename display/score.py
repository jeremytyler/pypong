"""Handles methods to display score values."""
import pygame

pygame.font.init()

SCORE_FONT = pygame.font.Font('data/font/ObelusCompact.ttf', 200)


def draw_score_text(value, screen, coordinates):
    """Generate and display the value as a score in game."""
    score_text = SCORE_FONT.render(value, False, (255, 255, 255))
    screen.blit(score_text, (coordinates[0], coordinates[1]))
