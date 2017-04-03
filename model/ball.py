"""Class which represents the ball in play."""
import pygame
from random import randrange
from audio import sounds


class Ball(pygame.sprite.Sprite):
    """Ball sprite definition."""

    speeds = (2, 4, 6)

    def __init__(self, start_coords, speed=[speeds[1], speeds[1]]):
        """Construction with starting x, y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 9])
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = start_coords[0]
        self.rect.y = start_coords[1]

        self.speed = speed

    def bounce_from_paddle(self, paddle_front_edge_x):
        """Change the ball direction and speed when paadle collision occurs."""
        # Prevent the ball from being "stuck" in the paddle.
        self.rect.x = paddle_front_edge_x

        new_speed_x = self.speeds[randrange(0, len(self.speeds))]
        new_speed_y = (self.speeds[randrange(0, len(self.speeds))]
                       * randrange(-1, 2, 2))

        self.speed[0] = -self.speed[0]
        if (self.speed[0] > 0):
            self.speed[0] = new_speed_x
        else:
            self.speed[0] = -new_speed_x

        if (self.speed[1] > 0):
            self.speed[1] = new_speed_y
        else:
            self.speed[1] = -new_speed_y

    def is_left_score(self, left_x):
        """Test if ball passed the left side of the screen."""
        return self.rect.left < left_x

    def is_right_score(self, right_x):
        """Test if ball passed the left side of the screen."""
        return self.rect.right > right_x

    def reset(self, start_coords):
        """Reset the ball after a score occurs."""
        self.rect.x = start_coords[0]
        self.rect.y = start_coords[1]
        new_speed_x = (self.speeds[randrange(0, len(self.speeds))]
                       * randrange(-1, 2, 2))
        new_speed_y = (self.speeds[randrange(0, len(self.speeds))]
                       * randrange(-1, 2, 2))
        self.speed = [new_speed_x, new_speed_y]

    def update(self, screen_dim):
        """Update and draw the ball position."""
        self.rect = self.rect.move(self.speed)

        # Bounce from the top/bottom edge
        if self.rect.top < 0 or self.rect.bottom > screen_dim[1]:
            sounds.BOUNCE.play()
            self.speed[1] = -self.speed[1]
