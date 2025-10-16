import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Create paddles and ball
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5  # Can be changed from main.py
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)

        # Game state
        self.game_over = False
        self.winner_text = None

    def handle_input(self):
        """Handle player input (W/S keys)."""
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.height)

    def update(self):
        """Update game objects, check for scoring and game over."""
        if self.game_over:
            return

        # Move ball and check collisions
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        brect = self.ball.rect()

        # Scoring logic
        if brect.left <= 0:
            self.ai_score += 1
            self.ball.reset(direction=1)  # Serve toward player (right)
        elif brect.right >= self.width:
            self.player_score += 1
            self.ball.reset(direction=-1)  # Serve toward AI (left)

        # Simple AI movement
        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over()

    def check_game_over(self):
        """End the game when someone reaches the target score."""
        if self.player_score >= self.target_score:
            self.game_over = True
            self.winner_text = "Player Wins!"
        elif self.ai_score >= self.target_score:
            self.game_over = True
            self.winner_text = "AI Wins!"

    def render(self, screen):
        """Draw paddles, ball, midline, and score."""
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
