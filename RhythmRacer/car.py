import math
import pygame


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # angle in radians
        self.speed = 0.0
        self.max_speed = 15.0
        self.acceleration = 0.085
        self.deceleration = self.acceleration * 0.55
        self.steering_speed = 0.01
        self.width = 40
        self.height = 70
        self.damage = 0
        self.max_damage = 100
        self.shield_active = False
        self.base_max_speed = self.max_speed

    def update(self, steering, acceleration, brake):
        # Update speed
        if acceleration > 0:
            self.speed += self.acceleration * acceleration
            self.speed = max(0.0, min(self.speed, self.max_speed))
        if brake:
            brake_force = self.deceleration * 2
            if self.speed > 0:
                self.speed = max(0.0, self.speed - brake_force)
        self.speed = max(0.0, min(self.speed, self.max_speed))

        # Update angle
        self.angle += steering * self.steering_speed * self.speed
        # Limit angle to ±90 degrees (±π/2 radians) - no pointing backward
        self.angle = max(-math.pi / 2, min(math.pi / 2, self.angle))

        # Check for game over due to damage
        if self.damage >= self.max_damage:
            return True  # Signal game over

        return False  # Game continues

    def set_max_speed(self, multiplier):
        self.max_speed = self.base_max_speed * multiplier

    def activate_shield(self):
        self.shield_active = True

    def deactivate_shield(self):
        self.shield_active = False

    def take_damage(self, amount):
        if not self.shield_active:
            self.damage = min(self.max_damage, self.damage + amount)

    def repair(self, amount):
        self.damage = max(0, self.damage - amount)
