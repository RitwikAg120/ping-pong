import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # 🔊 Load sound effects
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.bounce_sound = pygame.mixer.Sound("assets/sounds/bounce.wav")
        self.score_sound = pygame.mixer.Sound("assets/sounds/score.wav")

        # Optional volume tuning
        self.hit_sound.set_volume(0.6)
        self.bounce_sound.set_volume(0.4)
        self.score_sound.set_volume(0.7)

    def move(self):
        """Move the ball and bounce on top/bottom walls."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top or bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.bounce_sound.play()  # 🔊 Wall bounce sound

    def check_collision(self, player, ai):
        """Check collision with paddles."""
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1
            self.hit_sound.play()  # 🔊 Paddle hit sound

    def reset(self, direction=None):
        """Reset ball to center. Optionally set serve direction."""
        self.score_sound.play()  # 🔊 Scoring sound

        self.x = self.original_x
        self.y = self.original_y

        # Serve direction control
        if direction is not None:
            # direction: 1 → toward player, -1 → toward AI
            self.velocity_x = 5 * direction
        else:
            self.velocity_x *= -1

        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        """Return pygame.Rect for collision checks."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
