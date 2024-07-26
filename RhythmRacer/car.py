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
        self.base_steering_speed = 0.01
        self.steering_speed = self.base_steering_speed
        self.width = 40
        self.height = 70
        self.damage = 0.0
        self.max_damage = 100.0
        self.shield_active = False
        self.base_max_speed = self.max_speed
        self.damage_opacity = 0  # overlay opacity for damage flash
        self.damage_cooldown = 0  # prevents cascading opacity Events
        self.oil_recovery = 1.0  # 1.0 means no oil effect
        self.shield_radius = 0.0  # New: for shield visual

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

        # Handle opacity decay
        if self.damage_opacity > 0:
            self.damage_opacity = max(0, self.damage_opacity - 15)  # Decays by 15 per frame
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 0.1  # assuming 0.1 time step, as with power-ups

        # Recovery from oil effect
        self.oil_recovery = min(1.0, self.oil_recovery + 0.01)  # Recover by 1% each frame
        self.steering_speed = self.base_steering_speed / self.oil_recovery

        # Shield visual decay
        if self.shield_active:
            self.shield_radius = max(self.width * 1.15, self.shield_radius * 0.95)  # decay towards default size
        else:
            self.shield_radius = 0.0

        # Check for game over due to damage
        if self.damage >= self.max_damage:
            return True  # Signal game over

        return False  # Game continues

    def set_max_speed(self, multiplier):
        self.max_speed = self.base_max_speed * multiplier

    def set_speed(self, speed):
        self.speed = max(0, min(speed, self.max_speed))

    def activate_shield(self):
        self.shield_active = True

    def deactivate_shield(self):
        self.shield_active = False

    def take_damage(self, amount):
        if not self.shield_active:
            self.damage = min(self.max_damage, self.damage + amount)
            if self.damage_cooldown <= 0:  # Only flash if we're not already flashing
                self.damage_opacity = 255  # Full opacity
                self.damage_cooldown = 0.5  # Half second cooldown
            return True  # Successfully applied damage
        else:
            self.shield_radius = self.width * 1.5
        return False     # Damage was blocked

    def repair(self, amount):
        self.damage = max(0.0, self.damage - amount)

    def apply_oil_effect(self):
        self.oil_recovery = max(0.65, self.oil_recovery - 0.1)  # 0.65 = minimum steering capacity
