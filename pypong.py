"""Basic pygame setup."""
import sys
import random
import pygame

# Constants
WIDTH, HEIGHT = (500, 480)
WHITE = (255, 255, 255)
MAX_FPS = 60
PADDLE_BUFFER_X = 30
PADDLE_BUFFER_Y = 27


class Paddle(pygame.sprite.Sprite):
    """Paddle sprite definition."""

    PADDLE_SPEED = 5

    def __init__(self, start_x, start_y):
        """Constructor with starting x,y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 36])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.score = 0

    def update(self, screen):
        """Update and draw the paddle position."""
        if (pygame.key.get_pressed()[pygame.K_UP] != 0
                and self.rect.y > 0 + PADDLE_BUFFER_Y):
            self.rect.y -= self.PADDLE_SPEED
        elif (pygame.key.get_pressed()[pygame.K_DOWN] != 0
                and self.rect.y < HEIGHT
                - self.rect.height
                - PADDLE_BUFFER_Y):
            self.rect.y += self.PADDLE_SPEED

        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    """Ball sprite definition."""

    SPEEDS = (2, 4, 6)
    speed = [SPEEDS[1], SPEEDS[1]]

    def __init__(self, start_x, start_y):
        """Construction with starting x, y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 9])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.start_x = start_x
        self.rect.x = start_x
        self.rect.y = start_y
        # TODO -isolate sound logic better
        self.rebound_sound = pygame.mixer.Sound('sound/rebound.ogg')
        self.bounce_sound = pygame.mixer.Sound('sound/bounce.ogg')
        self.point_sound = pygame.mixer.Sound('sound/point.ogg')

    def update(self, screen):
        """Update and draw the ball position."""
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.point_sound.play()
            self.rect.x = WIDTH/2
            self.rect.y = HEIGHT/2
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.bounce_sound.play()
            self.speed[1] = -self.speed[1]

        screen.blit(self.image, self.rect)

    def rebound(self, paddle_edge):
        """Change the ball direction and speed when paadle collision occurs."""
        self.rebound_sound.play()

        # Prevent the ball from being "stuck" in the paddle.
        self.rect.x = paddle_edge

        new_speed_x = self.SPEEDS[random.randrange(0, len(self.SPEEDS))]
        new_speed_y = (self.SPEEDS[random.randrange(0, len(self.SPEEDS))]
                       * random.randrange(-1, 2, 2))

        self.speed[0] = -self.speed[0]
        if (self.speed[0] > 0):
            self.speed[0] = new_speed_x
        else:
            self.speed[0] = -new_speed_x

        if (self.speed[1] > 0):
            self.speed[1] = new_speed_y
        else:
            self.speed[1] = -new_speed_y


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


# Game tech initialization
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.init(48000, -16, 2, 2048)
pygame.font.init()
SCORE_FONT = pygame.font.Font('font/ObelusCompact.ttf', 200)
score_surface = SCORE_FONT.render('10', False, WHITE)

player_score = 0
computer_score = 0

# Sprite creation
paddle_left = Paddle(PADDLE_BUFFER_X, HEIGHT/2)
paddle_right = Paddle(WIDTH - PADDLE_BUFFER_X, HEIGHT/2)
ball = Ball(WIDTH/2, HEIGHT/2)

# Main Game Loop
while True:
    clock.tick(MAX_FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    draw_net()

    if pygame.sprite.collide_rect(ball, paddle_left):
        ball.rebound(paddle_left.rect.right)
    if pygame.sprite.collide_rect(ball, paddle_right):
        ball.rebound(paddle_right.rect.left - 7)

    ball.update(screen)
    paddle_left.update(screen)
    paddle_right.update(screen)
    screen.blit(score_surface, (WIDTH-106, - 46))
    screen.blit(score_surface, (WIDTH/5, - 46))
    pygame.display.flip()
