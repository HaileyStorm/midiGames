import pygame
import random

class Track:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.track_width = 300
        self.segments = []
        self.total_distance = 0
        self.generate_initial_track()

    def generate_initial_track(self):
        for _ in range(20):  # Generate initial segments
            self.add_segment()

    def add_segment(self):
        if not self.segments:
            center_x = self.screen_width // 2
        else:
            prev_center = self.segments[-1]['center']
            center_x = max(self.track_width//2, min(self.screen_width - self.track_width//2,
                           prev_center + random.randint(-50, 50)))
        self.segments.append({
            'center': center_x,
            'y': len(self.segments) * 100  # Each segment is 100 pixels tall
        })

    def update(self, speed):
        self.total_distance += speed
        while self.total_distance >= 100:
            self.segments.pop(0)
            self.add_segment()
            self.total_distance -= 100

        # Adjust all segment y-positions
        for segment in self.segments:
            segment['y'] -= speed

    def draw(self, screen):
        for i, segment in enumerate(self.segments):
            left = segment['center'] - self.track_width // 2
            right = segment['center'] + self.track_width // 2
            y = self.screen_height - (segment['y'] - self.total_distance)

            if i < len(self.segments) - 1:
                next_segment = self.segments[i + 1]
                next_left = next_segment['center'] - self.track_width // 2
                next_right = next_segment['center'] + self.track_width // 2
                next_y = self.screen_height - (next_segment['y'] - self.total_distance)

                pygame.draw.line(screen, (255, 255, 255), (left, y), (next_left, next_y), 2)
                pygame.draw.line(screen, (255, 255, 255), (right, y), (next_right, next_y), 2)

    def check_collision(self, car):
        bottom_segment = self.segments[0]
        left_bound = bottom_segment['center'] - self.track_width // 2
        right_bound = bottom_segment['center'] + self.track_width // 2
        return car.x - car.width / 2 < left_bound or car.x + car.width / 2 > right_bound