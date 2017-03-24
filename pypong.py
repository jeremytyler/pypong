"""Basic pygame setup."""
import sys
import pygame

SIZE = WIDTH, HEIGHT = (320, 240)

screen = pygame.display.set_mode(SIZE)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        print event.event_name(event.type)
