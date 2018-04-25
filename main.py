#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *

from camera import Camera
from blocks import Platform
from player import Player

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Platformer Title")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    hero = Player(55, 55)
    left = right = False
    up = False

    timer = pygame.time.Clock()

    entities = pygame.sprite.Group() # all objects
    platforms = [] # object to hit or stay
    entities.add(hero)

    level = [
        "----------------------------------",
        "-                                -",
        "-                       --       -",
        "-                                -",
        "-            --                  -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                            --- -",
        "-                                -",
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]

    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # real level width
    total_level_height = len(level) * PLATFORM_HEIGHT  # height
    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0, 0))

        hero.update(left, right, up, platforms)
        camera.update(hero)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)  # don't move out of left border
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)


if __name__ == "__main__":
    main()
