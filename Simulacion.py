import sys
from pygame.locals import *
import pymunk #1
import random
from pymunk import pygame_util
import math
import pygame
from pygame.color import *
from pymunk import Vec2d

space = pymunk.Space()
G = 6.67428e-11

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

def draw_ball(screen, ball):
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, (0,0,255), p, int(ball.radius), 2)

def add_ball(space):
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, moment) # 2
    body.position = pygame.mouse.get_pos()[0], pygame.display.get_surface().get_size()[1] - pygame.mouse.get_pos()[1] # 3
    shape = pymunk.Circle(body, radius) # 4
    space.add(body, shape) # 5
    return shape, body

#def add_ball(space):

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # pygame.FULLSCREEN)
    pygame.display.set_caption("BlueYonder challenge")
    clock = pygame.time.Clock()

    space.gravity = (0, 0)

    balls_shapes = []
    balls_bodies = []
    line_point1 = None
    static_lines = []

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            
            elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                p = (pygame.mouse.get_pos()[0], pygame.display.get_surface().get_size()[1] - pygame.mouse.get_pos()[1])
                active_shape = None 
                for s in balls_shapes:
                    dist, info = s.point_query(p)
                    if dist < 0:
                        active_shape = s
                
                if active_shape != None:
                    s = active_shape
                    r = int(s.radius)
                    pygame.draw.circle(screen, (100, 100, 100), p, r, 3)
            
            elif event.type == pygame.KEYUP:
                if active_shape != None:
                    active_shape.body.position = (pygame.mouse.get_pos()[0], pygame.display.get_surface().get_size()[1] - pygame.mouse.get_pos()[1])

            elif event.type == MOUSEBUTTONDOWN and event.button  == 1:
                ball_shape = add_ball(space)
                balls_shapes.append(ball_shape[0])
                balls_bodies.append(ball_shape[1])

            elif event.type == MOUSEBUTTONDOWN and event.button == 3: 
                if line_point1 is None:
                    line_point1 = Vec2d(pygame.mouse.get_pos()[0], pygame.display.get_surface().get_size()[1] - pygame.mouse.get_pos()[1])

            elif event.type == MOUSEBUTTONUP and event.button == 3: 
                if line_point1 is not None:
                    
                    line_point2 = Vec2d(pygame.mouse.get_pos()[0], pygame.display.get_surface().get_size()[1] - pygame.mouse.get_pos()[1])
                    body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    shape= pymunk.Segment(body, line_point1, line_point2, 0.0)
                    shape.friction = 0.99
                    space.add(shape)
                    static_lines.append(shape)
                    line_point1 = None

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        for outer_body in balls_bodies:
            dist_x = 0
            dist_y = 0
            for inner_body in balls_bodies:
                if inner_body != outer_body:
                    dist_x = outer_body.position[0] - inner_body.position[0]
                    dist_y = outer_body.position[1] - inner_body.position[1]
                    d = math.sqrt(dist_x ** 2 + dist_y ** 2)
                    f = G * outer_body.mass * inner_body.mass / (d**2)
                    
                    theta = math.atan2(dist_y, dist_x)
                    fx = math.cos(theta) * f
                    fy = math.sin(theta) * f
                    mutator = 10000000000000000
                    outer_body.apply_force_at_local_point((fx * mutator, fy * mutator), (0, 0))

            space.step(1/50.0)

            screen.fill((0,0,0))
            space.debug_draw(draw_options)

            pygame.display.flip()
            clock.tick(50)

main()
