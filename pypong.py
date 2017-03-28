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

    def __init__(self, start_x, start_y):
        """Constructor with starting x,y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 36])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self, screen):
        """Update and draw the paddle position."""
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    """Ball sprite definition."""

    speed = [2, 2]

    def __init__(self, start_x, start_y):
        """Construction with starting x, y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 9])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self, screen):
        """Update and draw the ball position."""
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]
        screen.blit(self.image, self.rect)


def draw_net():
    """
    Method to draw the dashed "net" in the middle of the screen.

    Ideally find a more efficient way to update each game loop
    """
    current_y = 0
    while current_y < HEIGHT:
        pygame.draw.line(
            screen, WHITE, (WIDTH/2, current_y), (WIDTH/2, current_y+9))
        current_y += 18


clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Sprite creation
paddle_left = Paddle(PADDLE_BUFFER, HEIGHT/2)
paddle_right = Paddle(WIDTH - PADDLE_BUFFER, HEIGHT/2)
ball = Ball(WIDTH/2, HEIGHT/2)

# Main Game Loop
while True:
    clock.tick(MAX_FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    draw_net()

    ball.update(screen)
    paddle_left.update(screen)
    paddle_right.update(screen)
    pygame.display.flip()
