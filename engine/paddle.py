import pygame

class Paddle(object):
    def __init__(self, x, minY ,maxY, width, height):
        self.minY = minY
        self.maxY = maxY
        self.height = height
        self.rect = pygame.Rect(x, minY, width, height)

    def move(self, distance):
        """Move the paddle into a direction."""
        if self.rect.bottom + distance > self.maxY:
            self.rect.bottom = self.maxY
        elif self.rect.top + distance < self.minY:
            self.rect.top = self.minY
        else:
            self.rect.y = self.rect.y + distance

    def draw(self, surface):
        pygame.draw.rect(surface, (255,255,255), self.rect)

    def ball_collision(self, ball):
        if ball.x >= self.rect.x and ball.x <= self.rect.x+self.rect.height:
            return True
        return False