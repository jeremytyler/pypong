"""Basic pygame setup."""
import sys
import random
import pygame

# Game-scope Constants
WIDTH, HEIGHT = (500, 480)
WHITE = (255, 255, 255)
MAX_FPS = 60
PADDLE_BUFFER_X = 30
PADDLE_BUFFER_Y = 27


class Paddle(pygame.sprite.Sprite):
    """Paddle sprite definition."""

    def __init__(self, start_coords, score=0, speed=5):
        """Constructor with starting x,y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 36])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_coords[0]
        self.rect.y = start_coords[1]
        self.score = 0
        self.speed = 5

    def add_point(self):
        """Increase the paddle/player's score by 1."""
        self.score += 1

    def update(self, screen):
        """Update and draw the paddle position."""
        if (pygame.key.get_pressed()[pygame.K_UP] != 0
                and self.rect.y > 0 + PADDLE_BUFFER_Y):
            self.rect.y -= self.speed
        elif (pygame.key.get_pressed()[pygame.K_DOWN] != 0
                and self.rect.y < HEIGHT
                - self.rect.height
                - PADDLE_BUFFER_Y):
            self.rect.y += self.speed

        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    """Ball sprite definition."""

    speeds = (2, 4, 6)

    def __init__(self, start_coords, speed=[speeds[1], speeds[1]]):
        """Construction with starting x, y coordinates."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([7, 9])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_coords[0]
        self.rect.y = start_coords[1]
        self.speed = speed

    def update(self, screen):
        """Update and draw the ball position."""
        self.rect = self.rect.move(self.speed)
        screen.blit(self.image, self.rect)

    def bounce_from_edge(self):
        """Method to change y velocity if ball hits edge of the play area."""
        self.speed[1] = -self.speed[1]

    def bounce_from_paddle(self, paddle_front_edge_x):
        """Change the ball direction and speed when paadle collision occurs."""
        # Prevent the ball from being "stuck" in the paddle.
        self.rect.x = paddle_front_edge_x

        new_speed_x = self.speeds[random.randrange(0, len(self.speeds))]
        new_speed_y = (self.speeds[random.randrange(0, len(self.speeds))]
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

    def is_at_edge(self, play_area_height):
        """Test to determine if ball has his edge of play area."""
        return self.rect.top < 0 or self.rect.bottom > play_area_height

    def is_left_score(self, left_x):
        """Test if ball passed the left side of the screen."""
        return self.rect.left < left_x

    def is_right_score(self, right_x):
        """Test if ball passed the left side of the screen."""
        return self.rect.right > right_x

    def reset(self):
        """Reset the ball after a score occurs."""
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
        new_speed_x = (self.speeds[random.randrange(0, len(self.speeds))]
                       * random.randrange(-1, 2, 2))
        new_speed_y = (self.speeds[random.randrange(0, len(self.speeds))]
                       * random.randrange(-1, 2, 2))
        self.speed = [new_speed_x, new_speed_y]


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
rebound_sound = pygame.mixer.Sound('sound/rebound.ogg')
bounce_sound = pygame.mixer.Sound('sound/bounce.ogg')
point_sound = pygame.mixer.Sound('sound/point.ogg')

pygame.font.init()
SCORE_FONT = pygame.font.Font('font/ObelusCompact.ttf', 200)
score_surface = SCORE_FONT.render('10', False, WHITE)

player_score = 0
computer_score = 0

# Sprite creation
paddle_left = Paddle((PADDLE_BUFFER_X, HEIGHT/2))
paddle_right = Paddle((WIDTH - PADDLE_BUFFER_X, HEIGHT/2))
ball = Ball((WIDTH/2, HEIGHT/2))

left_player_score = SCORE_FONT.render(str(paddle_left.score), False, WHITE)
right_player_score = SCORE_FONT.render(str(paddle_right.score), False, WHITE)

# Main Game Loop
while True:
    clock.tick(MAX_FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw background
    screen.fill((0, 0, 0))
    draw_net()

    # Ball logic
    if ball.is_at_edge(HEIGHT):
        bounce_sound.play()
        ball.bounce_from_edge()

    if ball.is_left_score(0):
        point_sound.play()
        paddle_left.add_point()
        left_player_score = SCORE_FONT.render(str(paddle_left.score),
                                              False, WHITE)
        ball.reset()
    elif ball.is_right_score(WIDTH):
        point_sound.play()
        paddle_right.add_point()
        right_player_score = SCORE_FONT.render(str(paddle_right.score),
                                               False, WHITE)
        ball.reset()

    # Paddle logic
    if pygame.sprite.collide_rect(ball, paddle_left):
        rebound_sound.play()
        ball.bounce_from_paddle(paddle_left.rect.right)
    if pygame.sprite.collide_rect(ball, paddle_right):
        rebound_sound.play()
        ball.bounce_from_paddle(paddle_right.rect.left - 7)

    ball.update(screen)
    paddle_left.update(screen)
    paddle_right.update(screen)

    screen.blit(left_player_score, (WIDTH-106, - 46))
    screen.blit(right_player_score, (WIDTH/5, - 46))
    pygame.display.flip()
