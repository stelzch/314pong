import sys
import pygame
from .paddle import Paddle
from .ball import Ball
from .settings import Settings

class Game(object):
    def __init__(self, width, height):
        """Initialize game display surface and entities."""
        pygame.init()
        
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        self.statusHeight = 30
        self.canvas = pygame.Surface((int(self.width), int(self.height - self.statusHeight)))

        # Initialize Joystick Inputs
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            print("Found new joystick: {}".format(joystick.get_name()))
            joystick.init()

        # Construct Paddles
        self.marginX = 5
        self.marginY = 5
        paddle_width = 5
        paddle_height = 40
        self.paddle1 = Paddle(self.marginX, 0, self.canvas.get_height(),
                              paddle_width, paddle_height)
        self.paddle2 = Paddle(width-self.marginX-paddle_width, 0, self.canvas.get_height(),
                              paddle_width, paddle_height)

        # Load settings
        self.settings = Settings()
        self.load_settings()

        # Add the ball
        self.ball = Ball(int(width/2), int(height/2), 10, 10, self.ballSpeed)


        # Score values
        self.score_p1 = 0
        self.score_p2 = 0

        # Add clock for timing
        self.clock = pygame.time.Clock()

        # Load additional assets
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)

    def change_gameplay(self, paddle_height, ball_speed, move_factor, spread_factor):
        """Change gameplay related variables."""
        self.ballSpeed = ball_speed
        self.ball.speed = ball_speed
        self.paddle1.move(-9999)  # Reset the paddles to the starting point
        self.paddle2.move(-9999)
        self.paddle1.rect.height = paddle_height
        self.paddle2.rect.height = paddle_height
        self.moveFactor = move_factor
        self.spreadFactor = spread_factor

    def load_settings(self):
        """Read settings from json file and set class parameters."""
        self.moveFactor = self.settings.get_gameplay_var("MOVE_FACTOR")
        self.spreadFactor = self.settings.get_gameplay_var("SPREAD_FACTOR")
        self.ballSpeed = self.settings.get_gameplay_var("BALL_SPEED")

    def mainloop(self):
        """Process events and display a frame."""
        Δt = self.clock.tick(60) # 60 FPS -- PC Master Race
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.JOYBUTTONDOWN:
                joystick = self.joysticks[event.joy]
                pos = joystick.get_axis(1)
                self.paddle1.move(Δt*pos*self.moveFactor)

        # Update paddle positions
        p1d = self.joysticks[self.settings.get_input_device("PLAYER1_DOWN")] \
                .get_button(self.settings.get_input_button("PLAYER1_DOWN"))
        p1u = self.joysticks[self.settings.get_input_device("PLAYER1_UP")] \
                .get_button(self.settings.get_input_button("PLAYER1_UP"))
        p2d = self.joysticks[self.settings.get_input_device("PLAYER2_DOWN")] \
                .get_button(self.settings.get_input_button("PLAYER2_DOWN"))
        p2u = self.joysticks[self.settings.get_input_device("PLAYER2_UP")] \
                .get_button(self.settings.get_input_button("PLAYER2_UP"))
        if p1d:
            self.paddle1.move(self.moveFactor * Δt * -1)
        elif p1u:
            self.paddle1.move(self.moveFactor * Δt)
        if p2d:
            self.paddle2.move(self.moveFactor * Δt * -1)
        elif p2u:
            self.paddle2.move(self.moveFactor * Δt)

        # Move the ball
        if self.ball.rect.top <= 0:
            self.ball.bounce(False)
        elif self.ball.rect.bottom >= self.canvas.get_height():
            self.ball.bounce(False)
        if self.ball.rect.left <= self.paddle1.rect.right:
            # Ball has reached left side. Check for paddle collision
            if self.ball.rect.bottom > self.paddle1.rect.top and self.ball.rect.top < self.paddle1.rect.bottom:
                centerOffset = self.ball.rect.centery - self.paddle1.rect.centery
                print(centerOffset)
                print("Left paddle bouncing")
                newAngle = centerOffset / self.paddle1.rect.height * self.spreadFactor
                self.ball.set_orientation(newAngle*-1)
                self.ball.step()
            else:
                self.score_p2 += 1
                self.ball.reset(self.canvas.get_width(), self.canvas.get_height())
        elif self.ball.rect.right >= self.paddle2.rect.left:
            if self.ball.rect.centery in range(self.paddle2.rect.top, self.paddle2.rect.bottom):
                centerOffset = self.ball.rect.centery - self.paddle2.rect.centery
                print(centerOffset)
                print("Right paddle bouncing")
                newAngle = 180 + centerOffset / self.paddle2.rect.height * self.spreadFactor
                self.ball.set_orientation(newAngle*-1)
                self.ball.step()
            else:
                self.score_p1 += 1
                self.ball.reset(self.canvas.get_width(), self.canvas.get_height())
        else:
            self.ball.step()

        # Clear the screen using a black color
        self.screen.fill((0, 0, 0))
        self.canvas.fill((0, 0, 0))

        # Draw paddles and the ball
        self.paddle1.draw(self.canvas)
        self.paddle2.draw(self.canvas)
        self.ball.draw(self.canvas)

        # Display the player scores
        score1 = self.font.render(str(self.score_p1), False, (255,255,255))
        score2 = self.font.render(str(self.score_p2), False, (255,255,255))
        score1y = (self.statusHeight - score1.get_height()) / 2
        score2y = (self.statusHeight - score2.get_height()) / 2
        score2x = self.width - score2.get_width() - self.marginX

        self.screen.blit(score1, (self.marginX, score1y))
        self.screen.blit(score2, (score2x, score2y))
        self.screen.blit(self.canvas, (0, self.statusHeight))
        pygame.draw.line(self.screen, (255,255,255), (0, self.statusHeight), (self.width, self.statusHeight))

        pygame.display.flip()
