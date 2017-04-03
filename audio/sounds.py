"""Sound initialization and repository."""
import pygame

# Game tech/resource initialization
pygame.mixer.init(48000, -16, 2, 2048)

REBOUND = pygame.mixer.Sound('data/sound/rebound.ogg')
BOUNCE = pygame.mixer.Sound('data/sound/bounce.ogg')
POINT = pygame.mixer.Sound('data/sound/point.ogg')
