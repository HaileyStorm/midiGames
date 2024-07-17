import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Track:
    def __init__(self):
        self.width = 100  # Width of the track
        self.center_points = self.generate_track_points()
        self.inner_points = self.generate_boundary(self.center_points, -self.width/2)
        self.outer_points = self.generate_boundary(self.center_points, self.width/2)

    def generate_track_points(self):
        # Generate a simple oval track
        points = []
        for i in range(0, 360, 5):
            angle = math.radians(i)
            x = SCREEN_WIDTH/2 + math.cos(angle) * (SCREEN_WIDTH/3)
            y = SCREEN_HEIGHT/2 + math.sin(angle) * (SCREEN_HEIGHT/3)
            points.append((x, y))
        return points

    def generate_boundary(self, center_points, offset):
        boundary_points = []
        for i in range(len(center_points)):
            p1 = center_points[i]
            p2 = center_points[(i+1) % len(center_points)]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            ux = -dy/length
            uy = dx/length
            boundary_points.append((p1[0] + ux*offset, p1[1] + uy*offset))
        return boundary_points

    def draw(self, screen):
        pygame.draw.lines(screen, (255, 255, 255), True, self.inner_points, 2)
        pygame.draw.lines(screen, (255, 255, 255), True, self.outer_points, 2)

    def check_collision(self, car):
        # Simple collision check: if car is outside the track boundaries
        return not self.point_inside_track(car.x, car.y)

    def point_inside_track(self, x, y):
        return self.point_inside_polygon(x, y, self.outer_points) and not self.point_inside_polygon(x, y, self.inner_points)

    def point_inside_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside