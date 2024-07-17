import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # angle in radians
        self.speed = 0
        self.max_speed = 7
        self.acceleration = 0.125
        self.deceleration = 0.03333
        self.steering_speed = 0.015
        self.width = 40
        self.height = 70

    def update(self, steering, acceleration, brake):
        # Update speed
        acceleration_force = self.acceleration * acceleration
        brake_force = self.deceleration * 3 if brake else 0

        if self.speed > 0 or acceleration > brake:
            net_force = acceleration_force - brake_force - self.deceleration
            self.speed += net_force
        else:
            self.speed = 0

        self.speed = max(0, min(self.speed, self.max_speed))

        # Update angle
        self.angle += steering * self.steering_speed * self.speed

        # Update position
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

        # Keep the car on screen (temporary boundary check)
        self.x = max(0, min(self.x, SCREEN_WIDTH))
        self.y = max(0, min(self.y, SCREEN_HEIGHT))

    def draw(self, screen):
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, (255, 0, 0), (0, 0, self.width, self.height))
        rotated_car = pygame.transform.rotate(car_surface, math.degrees(-self.angle))
        screen.blit(rotated_car, rotated_car.get_rect(center=(self.x, self.y)))