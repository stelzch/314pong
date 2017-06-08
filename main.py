import sys
import pygame
from engine.game import Game

if __name__ == '__main__':
    g = Game(480, 240)
    while True:
        g.mainloop()

"""
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())
    joystick.init()
size = width, height = 640, 480

paddle_width = 2
paddle_height = 50
paddle1 = paddle.Paddle(10, 5, height-paddle_height-5, paddle_width, paddle_height)
paddle2 = paddle.Paddle(470, 5, height-paddle_height-5, paddle_width, paddle_height)

screen = pygame.display.set_mode(size)
ock = pygame.time.Clock()
ticksLastFrame = pygame.time.get_ticks()
while 1:
    t = pygame.time.get_ticks()
    deltaTime = (t - ticksLastFrame) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.JOYAXISMOTION:
            joystick = joysticks[event.joy]
            pos = joystick.get_axis(1)
            print("NewVal: {}".format(pos))
            if event.joy == 0:
                paddle1.move(pos*deltaTime)
            elif event.joy == 1:
                paddle2.move(pos*deltaTime)
    screen.fill((0,0,0))
    paddle1.move(0.5)
    paddle1.draw(screen)
    paddle2.draw(screen)
    pygame.display.flip()"""
