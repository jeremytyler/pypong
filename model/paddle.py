"""Class which represents a paddle."""
import pygame


class Position:
    """Enum to represent the paddle's position."""

    Left, Right = range(2)


class Paddle(pygame.sprite.Sprite):
    """Paddle sprite definition."""

    def __init__(self, start_coords, position, score=0, speed=5,
                 paddle_buffer_y=27):
        """Constructor with starting x,y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 36])
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = start_coords[0]
        self.rect.y = start_coords[1]

        self.position = position
        self.score = 0
        self.speed = 5
        self.paddle_buffer_y = paddle_buffer_y

    def add_point(self):
        """Increase the paddle/player's score by 1."""
        self.score += 1

    def get_paddle_edge(self):
        """Get the x coordinate edge of the front of the paddle paddle."""
        if self.position == Position.Left:
            return self.rect.right
        else:
            return self.rect.left - self.rect.width

    def update(self, screen_dim):
        """Update and draw the paddle position."""
        if (pygame.key.get_pressed()[pygame.K_UP] != 0
                and self.rect.y > 0 + self.paddle_buffer_y):
            self.rect.y -= self.speed
        elif (pygame.key.get_pressed()[pygame.K_DOWN] != 0
                and self.rect.y < screen_dim[1]
                - self.rect.height
                - self.paddle_buffer_y):
            self.rect.y += self.speed
