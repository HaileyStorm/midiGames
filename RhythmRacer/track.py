import pygame
import random
import math

class Track:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.track_width = 400
        self.segments = []
        self.total_distance = 0
        self.generate_initial_track()

    def generate_initial_track(self):
        for _ in range(20):  # Generate initial segments
            self.add_segment()

    def update(self, car):
        # Calculate forward and lateral movement based on car angle and speed
        forward_movement = math.cos(car.angle) * car.speed
        lateral_movement = math.sin(car.angle) * car.speed

        self.total_distance += forward_movement

        # Update all segment positions
        for segment in self.segments:
            segment['y'] -= forward_movement
            segment['center'] -= lateral_movement

        # Add new segments and remove old ones
        while self.total_distance >= 100:
            self.segments.pop(0)
            self.add_segment()
            self.total_distance -= 100

        # Handle backward movement
        while self.total_distance < 0:
            self.segments.insert(0, self.create_segment(self.segments[0]['y'] - 100))
            self.total_distance += 100
            if len(self.segments) > 20:  # Maintain a reasonable number of segments
                self.segments.pop()

    def create_segment(self, y):
        if not self.segments:
            center_x = self.screen_width // 2
        else:
            prev_center = self.segments[0]['center']
            center_x = max(self.track_width // 2, min(self.screen_width - self.track_width // 2,
                                                      prev_center + random.randint(-30, 30)))
        return {
            'center': center_x,
            'y': y
        }

    def add_segment(self):
        self.segments.append(self.create_segment((len(self.segments) * 100) + self.total_distance))

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

    def check_off_track(self, car):
        bottom_segment = self.segments[0]
        left_bound = bottom_segment['center'] - self.track_width // 2
        right_bound = bottom_segment['center'] + self.track_width // 2
        return car.x - car.width / 2 < left_bound or car.x + car.width / 2 > right_bound