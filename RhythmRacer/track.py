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
        self.checkpoint_y = None
        self.power_ups = []

    def generate_initial_track(self):
        for _ in range(int(self.screen_height / self.segment_length) + 2):  # Ensure track extends beyond screen
            self.add_segment()

    def spawn_power_up(self, power_up):
        segment = random.choice(self.segments)
        x = random.uniform(segment['center'] - self.track_width // 4, segment['center'] + self.track_width // 4)
        self.power_ups.append({'power_up': power_up, 'x': x, 'y': segment['y']})

    def update(self, car, sound):
        forward_movement = math.cos(car.angle) * car.speed
        lateral_movement = math.sin(car.angle) * car.speed

        self.total_distance += forward_movement

        # Update all segment positions
        for segment in self.segments:
            segment['y'] -= forward_movement
            segment['center'] -= lateral_movement

        # Update checkpoint position
        if self.checkpoint_y is not None:
            self.checkpoint_y += forward_movement

        # Check if we've passed the checkpoint
        if self.total_distance >= self.next_checkpoint:
            self.next_checkpoint += self.checkpoint_distance
            self.checkpoint_y = 0  # Place the new checkpoint at the top of the screen

        # Remove segments that are completely off-screen
        while self.segments and self.segments[0]['y'] + self.segment_length < 0:
            self.segments.pop(0)

        # Add new segments to keep the track extending beyond the screen
        while self.segments[-1]['y'] < self.screen_height:
            self.add_segment()

        # Update power-up positions
        for power_up in self.power_ups:
            power_up['y'] -= forward_movement
            power_up['x'] -= lateral_movement

        # Remove off-screen power-ups
        self.power_ups = [pu for pu in self.power_ups if pu['y'] > -50]

        # Check for power-up collection
        #print(self.power_ups)
        for power_up in self.power_ups:
            if (abs(car.x - power_up['x']) < 30 and
                    abs(self.screen_height - power_up['y'] - car.y) < 30):
                power_up['power_up'].collect()
                self.power_ups.remove(power_up)
                sound.play_sound('power_up_collect')

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

        # Draw checkpoint if it's on screen
        if self.checkpoint_y is not None and 0 <= self.checkpoint_y <= self.screen_height:
            pygame.draw.line(screen, (255, 255, 0), (0, self.checkpoint_y), (self.screen_width, self.checkpoint_y),
                             5)

        # Reset checkpoint if it's gone off screen
        if self.checkpoint_y is not None and self.checkpoint_y > self.screen_height:
            self.checkpoint_y = None

        # Draw power-ups
        for power_up in self.power_ups:
            pygame.draw.circle(screen, (0, 255, 0),
                               (int(power_up['x']), int(self.screen_height - power_up['y'])), 10)

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