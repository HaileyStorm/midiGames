import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # angle in radians
        self.speed = 0
        self.max_speed = 15
        self.acceleration = 0.085
        self.deceleration = self.acceleration * 0.55
        self.steering_speed = 0.01
        self.width = 40
        self.height = 70

    def update(self, steering, acceleration, brake):
        # Update speed
        if acceleration > 0:
            self.speed += self.acceleration * acceleration
            self.speed = max(0, min(self.speed, self.max_speed))
        if brake:
            brake_force = self.deceleration * 2
            if self.speed > 0:
                self.speed = max(0.0, self.speed - brake_force)
        self.speed = max(0, min(self.speed, self.max_speed))

        # Update angle
        self.angle += steering * self.steering_speed * self.speed
        # Limit angle to ±90 degrees (±π/2 radians) - no pointing backward
        self.angle = max(-math.pi / 2, min(math.pi / 2, self.angle))
