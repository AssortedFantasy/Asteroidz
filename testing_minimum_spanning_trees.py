# This file isn't really mean't to do anything. But it does show off Kruskals theorum.

import pygame as pg
import algorithms
import random

pg.init()
WIDTH, HEIGHT = 1280, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True


points = []
lines = []


# Controls:
# Spacebar adds a random point
# P adds 10 random points.
# Mouseclicks adds a point at the mouse location
# Q (re)computes the Minimum spanning tree
# W clears all points.

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            points.append((int(x), int(y)))
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                points.append((int(random.random()*WIDTH), int(random.random()*HEIGHT)))
            elif event.key == pg.K_p:
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
                points.append((int(random.random() * WIDTH), int(random.random() * HEIGHT)))
            elif event.key == pg.K_q:

                lines = []

                connected_graph = algorithms.prims_algorithm(points)
                for point in connected_graph[1:]:
                    p0 = int(point.x), int(point.y)
                    p1 = int(point.nearest.x), int(point.nearest.y)

                    lines.append((p0, p1))
            elif event.key == pg.K_w:
                points = []

    screen.fill((255, 255, 255))

    for point in points:
        pg.draw.circle(screen, (255, 0, 0), point, 5, 0)

    for p0, p1 in lines:
        pg.draw.line(screen, (0, 128, 128), p0, p1, 2)

    pg.display.flip()
    clock.tick(60)
