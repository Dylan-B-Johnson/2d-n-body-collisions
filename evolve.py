import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import numpy as np
import actor as act
import pygame
import random

# controls:
# w/s (while mousing over circle): increase/decrease circle radius
# a/d (while mousing over circle): decrease/increase circle speed
# q/e: decrease/increase step size
# up arrow/down arrow: increase/decrease all circle radii
# left arrow/right arrow: decrease/increase all circle speeds
n = 20
screen_width, screen_height = 1920, 1080
act.h = 2
res = (screen_width, screen_height)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
done = False
clock = pygame.time.Clock()
msElapsed = clock.tick(30)
positions = act.actor_positions(n, res)
rand = [random.random() * 5 for i in range(n)]
rand_s = [random.random() * 5 ** 0.5 for i in range(n)]
actors = [
    act.Actor(screen, np.array(positions[i]), act.actor_directions(positions, res)[i], s=1 + rand_s[i],
              chars={'r': 10 + rand[i] ** 0.5, 'm': 1 + rand[i]},
              res=res) for i in range(n)]
while not done:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        for i in actors: i.v *= 1.05
    if pressed[pygame.K_LEFT]:
        for i in actors: i.v /= 1.05
    if pressed[pygame.K_q]:
        act.Actor.h /= 1.05
    if pressed[pygame.K_e]:
        act.Actor.h *= 1.05
    if pressed[pygame.K_w]:
        for i in actors:
            if np.linalg.norm(i.x - np.array(pygame.mouse.get_pos())) < i.chars['r']:
                i.chars['m'] *= 1.05
                i.chars['r'] *= 1.05 ** 0.5
    if pressed[pygame.K_s]:
        for i in actors:
            if np.linalg.norm(i.x - np.array(pygame.mouse.get_pos())) < i.chars['r']:
                i.chars['m'] /= 1.05
                i.chars['r'] /= 1.05 ** 0.5
    if pressed[pygame.K_a]:
        for i in actors:
            if np.linalg.norm(i.x - np.array(pygame.mouse.get_pos())) < i.chars['r']:
                i.v /= 1.05
    if pressed[pygame.K_d]:
        for i in actors:
            if np.linalg.norm(i.x - np.array(pygame.mouse.get_pos())) < i.chars['r']:
                i.v *= 1.05
    if pressed[pygame.K_UP]:
        for i in actors:
            i.chars['m'] *= 1.05
            i.chars['r'] *= 1.05 ** 0.5
    if pressed[pygame.K_DOWN]:
        for i in actors:
            i.chars['m'] /= 1.05
            i.chars['r'] /= 1.05 ** 0.5
    screen.fill((10, 10, 10))
    for i in actors: i.update()
    a = np.array([i.x for i in actors])
    d_actors = np.linalg.norm(a - a[:, None], axis=-1)
    # E = 0
    for i in range(len(actors)):
        actors[i].calc_next(d_actors[i], actors)
    #     for j in range(i + 1, len(actors), 1):
    #         E -= act.Actor.G / d_actors[i][j] * actors[i].chars['m'] * actors[j].chars['m']
    # for i in actors:
    #     E+=0.5*i.v[0]**2+i.v[1]**2*i.chars['m']
    # print(E)  #All this E stuff was to see if energy is conserved: It's not
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
