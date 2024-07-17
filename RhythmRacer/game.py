import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from midi_controller import MIDIController
from car import Car
from track import Track
from graphics import Graphics


class Game:
    def __init__(self, mode='continuous'):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display=1)
        pygame.display.set_caption("Rhythm Racer")
        self.clock = pygame.time.Clock()
        self.midi_controller = MIDIController()
        self.midi_controller.connect()
        self.car = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.graphics = Graphics()
        self.start_time = pygame.time.get_ticks()
        self.points = 0
        self.controls = None
        self.mode = mode
        self.total_distance = 0
        self.checkpoints = 0
        self.checkpoint_distance = 10000  # Distance between checkpoints
        self.track = Track(SCREEN_WIDTH, SCREEN_HEIGHT, self.checkpoint_distance)
        self.game_duration = 120  # 2 minutes for timed mode
        self.start_time = pygame.time.get_ticks()
        self.game_over_flag = False

    def handle_event(self, event):
        # TODO: Implement event handling (will be expanded later)
        pass

    def update(self):
        self.midi_controller.update()
        self.controls = self.midi_controller.get_controls()

        self.car.update(
            steering=self.controls['steering'],
            acceleration=self.controls['acceleration'],
            brake=self.controls['brake']
        )

        if self.track.check_off_track(self.car):
            self.car.speed *= 0.99  # Slow down when off track
        else:
            self.points += self.car.speed / 10  # Points based on speed when on track

        self.track.update(self.car)

        self.total_distance += self.car.speed

        # Check for new checkpoint
        if self.total_distance // self.checkpoint_distance > self.checkpoints:
            self.checkpoints += 1
            self.points += 100  # Bonus points for checkpoint

        # Check for game over in timed mode
        if self.mode == 'timed':
            if (pygame.time.get_ticks() - self.start_time) / 1000 >= self.game_duration:
                self.game_over_flag = True

        if self.is_game_over():
            self.game_over()
            pygame.quit()

    def render(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if self.mode == 'timed':
            time_display = max(0, self.game_duration - elapsed_time)
        else:  # continuous mode
            time_display = elapsed_time

        self.graphics.render_game(
            self.screen, self.car, self.track,
            time_display, self.checkpoints,
            self.controls['acceleration'] if self.controls else 0.0,
            self.points, self.total_distance,
            self.mode
        )

    def game_over(self):
        print(f"Game Over! Mode: {self.mode}, Distance: {self.total_distance:.1f}, Points: {int(self.points)}")
        self.game_over_flag = True

    def is_game_over(self):
        return self.game_over_flag
