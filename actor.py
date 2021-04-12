import pygame
import numpy as np
import random
import math as m


# generates initial positions around the screen clockwise
def actor_positions(n, res=(1920, 1080)):
    perimeter = 2 * res[0] + 2 * res[1]
    separation = perimeter / n
    pos = []
    for i in range(n):
        if i * separation < res[0]:
            pos.append((i * separation, 0))
        elif i * separation - res[0] < res[1]:
            pos.append((res[0], i * separation - res[0]))
        elif i * separation - res[0] - res[1] < res[0]:
            pos.append((i * separation - res[0] - res[1], res[1]))
        elif i * separation - 2 * res[0] - res[1] < res[0]:
            pos.append((0, i * separation - 2 * res[0] - res[1]))
    return pos


def actor_directions(positions, res=(1920, 1080)):
    d = []
    for i in positions:
        if i[1] == 0:
            theta = random.random() * m.pi
        if i[0] == res[0]:
            theta = random.random() * 1.5 * m.pi + m.pi * 0.5
        if i[1] == res[1]:
            theta = random.random() * m.pi * -1
        if i[0] == 0:
            theta = random.random() * 1.5 * m.pi + m.pi * 0.5 * -1
        d.append((m.cos(theta), m.sin(theta)))
    return d


class Actor:
    h = 1
    G = 10

    def __init__(self, screen, x, d, s=1, chars={'m': 1, 'r': 10}, res=(1920, 1080), rgb=(14, 242, 208)):
        self.x = x
        self.res = res
        self.v = np.array(d) * s * 0
        self.vtmp = self.v
        self.chars = chars
        self.a = np.array([0.0, 0.0])
        self.r, self.g, self.b = rgb
        self.screen = screen
        pygame.draw.circle(self.screen, (self.r, self.g, self.b), (self.x[0], self.x[1]), self.chars['r'])

    def calc_next(self, d_actors, actors):
        if np.all(self.vtmp == self.v):
            i2 = 0
            for i in d_actors:
                # This assumes that no two balls will make it to the same position
                if i == 0:
                    pass
                else:
                    m1, m2 = self.chars['m'], actors[i2].chars['m']
                    v1, v2, x1, x2 = self.v, actors[i2].v, self.x, actors[i2].x
                    if i <= (actors[i2].chars['r'] + self.chars['r']) and np.dot(actors[i2].x - self.x,
                                                                                 self.v - actors[i2].v) > 0:
                        # calculating collision
                        self.vtmp = v1 - np.dot(v1 - v2, x1 - x2) * np.linalg.norm(x1 - x2) ** -2 * (
                                x1 - x2) * 2 * m2 / (
                                            m1 + m2)
                        actors[i2].vtmp = v2 - np.dot(v2 - v1, x2 - x1) * np.linalg.norm(x2 - x1) ** -2 * (
                                x2 - x1) * 2 * m1 / (
                                                  m1 + m2)
                    # calculating acceleration
                    r_diff = x2 - x1
                    self.a += r_diff * Actor.G * m2 / (i ** 3.0)
                i2 += 1

        if self.x[0] < 0:
            self.x[0] = 0
        if self.x[1] < 0:
            self.x[1] = 0
        if self.x[0] > self.res[0]:
            self.x[0] = self.res[0]
        if self.x[1] > self.res[1]:
            self.x[1] = self.res[1]
        if self.x[1] == 0:
            self.vtmp[1] *= -1
        if self.x[0] == self.res[0]:
            self.vtmp[0] *= -1
        if self.x[1] == self.res[1]:
            self.vtmp[1] *= -1
        if self.x[0] == 0:
            self.vtmp[0] *= -1

    def update(self):
        self.v = self.vtmp
        self.v += self.a * Actor.h
        self.x += (self.v + self.vtmp) * 0.5 * Actor.h
        self.a = np.array([0.0, 0.0])
        pygame.draw.circle(self.screen, (self.r, self.g, self.b), (self.x[0], self.x[1]), self.chars['r'])
