import pygame
import math
from camera import Camera
import constants as c
from primitives import Pose
import random

class Cloud:


    def __init__(self, surf, position=(0,0)):
        self.surf = surf
        self.position = Pose(position)
        self.velocity = Pose((-20, 0))


    def update(self,surface,offset=(0,0)):
        self.position += self.velocity*dt

    def draw(self,surface,offset=(0,0)):
        w = self.surf.get_width()
        h = self.surf.get_height()
        x = self.position.x - offset[0] - w // 2
        y = self.position.y - offset[1] - h // 2

        if x < -w or x > c.WINDOW_WIDTH:
            return
        if y < -h or y > c.WINDOW_HEIGHT:
            return

        in_world = Camera.screen_to_world(self.position.get_position())
        if w//2 < in_world.x < c.ARENA_WIDTH - w//2:
            if h//2 < in_world.y < c.ARENA_HEIGHT - h//2:
                return

        surface.blit(self.surf, (x,y))


class Background:
    




