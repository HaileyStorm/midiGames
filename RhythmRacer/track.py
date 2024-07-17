import math
import random
import pygame


class Track:
    def __init__(self, screen_width, screen_height, checkpoint_distance):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.track_width = 350
        self.segments = []
        self.total_distance = 0
        self.desired_direction = 0
        self.direction_change_countdown = 0
        self.segment_length = 75
        self.generate_initial_track()
        self.checkpoint_distance = checkpoint_distance
        self.next_checkpoint = self.checkpoint_distance

    def generate_initial_track(self):
        for _ in range(int(self.screen_height / self.segment_length) + 2):  # Ensure track extends beyond screen
            self.add_segment()

    def update(self, car):
        forward_movement = math.cos(car.angle) * car.speed
        lateral_movement = math.sin(car.angle) * car.speed

        self.total_distance += forward_movement

        # Update all segment positions
        for segment in self.segments:
            segment['y'] -= forward_movement
            segment['center'] -= lateral_movement

        # Remove segments that are completely off-screen
        while self.segments and self.segments[0]['y'] + self.segment_length < 0:
            self.segments.pop(0)

        # Add new segments to keep the track extending beyond the screen
        while self.segments[-1]['y'] < self.screen_height:
            self.add_segment()

        # Update next checkpoint
        if self.total_distance >= self.next_checkpoint:
            self.next_checkpoint += self.checkpoint_distance

    def create_segment(self, y):
        if not self.segments:
            center_x = self.screen_width // 2
        else:
            self.update_desired_direction()
            prev_center = self.segments[-1]['center']

            # Smooth transition towards desired direction
            max_deviation = 25
            deviation = random.uniform(-max_deviation, max_deviation)
            direction_influence = self.desired_direction * max_deviation

            center_x = prev_center + direction_influence + deviation
            center_x = max(self.track_width // 2, min(self.screen_width - self.track_width // 2, center_x))

        return {
            'center': center_x,
            'y': y
        }

    def update_desired_direction(self):
        self.direction_change_countdown -= 1
        if self.direction_change_countdown <= 0:
            self.desired_direction = random.uniform(-1, 1)
            self.direction_change_countdown = random.randint(5, 20)  # Change direction every 5-15 segments

    def add_segment(self):
        new_y = self.segments[-1]['y'] + self.segment_length if self.segments else 0
        self.segments.append(self.create_segment(new_y))

    def draw(self, screen):
        for i in range(len(self.segments) - 1):
            segment = self.segments[i]
            next_segment = self.segments[i + 1]

            left = segment['center'] - self.track_width // 2
            right = segment['center'] + self.track_width // 2
            y = self.screen_height - segment['y']

            next_left = next_segment['center'] - self.track_width // 2
            next_right = next_segment['center'] + self.track_width // 2
            next_y = self.screen_height - next_segment['y']

            # Calculate control points for the curve
            mid_y = (y + next_y) / 2
            ctrl_left = (left + next_left) / 2
            ctrl_right = (right + next_right) / 2

            # Draw left curve
            self.draw_curve(screen, (255, 255, 255),
                            (left, y), (ctrl_left, mid_y), (next_left, next_y))

            # Draw right curve
            self.draw_curve(screen, (255, 255, 255),
                            (right, y), (ctrl_right, mid_y), (next_right, next_y))

            # Draw checkpoint if it's in this segment
            if self.next_checkpoint - self.total_distance <= segment['y'] and \
                    self.next_checkpoint - self.total_distance > next_segment['y']:
                print("checkpoint")
                checkpoint_y = self.screen_height - (segment['y'] - (self.next_checkpoint - self.total_distance))
                pygame.draw.line(screen, (255, 255, 0), (0, checkpoint_y), (self.screen_width, checkpoint_y), 5)

    def draw_curve(self, screen, color, start, control, end):
        steps = 10
        for i in range(steps):
            t = i / steps
            x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
            y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]

            next_t = (i + 1) / steps
            next_x = (1 - next_t) ** 2 * start[0] + 2 * (1 - next_t) * next_t * control[0] + next_t ** 2 * end[0]
            next_y = (1 - next_t) ** 2 * start[1] + 2 * (1 - next_t) * next_t * control[1] + next_t ** 2 * end[1]

            pygame.draw.line(screen, color, (int(x), int(y)), (int(next_x), int(next_y)), 2)

    def check_off_track(self, car):
        bottom_segment = self.segments[0]
        left_bound = bottom_segment['center'] - self.track_width // 2
        right_bound = bottom_segment['center'] + self.track_width // 2
        return car.x - car.width / 2 < left_bound or car.x + car.width / 2 > right_bound