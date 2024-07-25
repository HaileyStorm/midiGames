import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from midi_controller import MIDIController
from car import Car
from track import Track
from graphics import Graphics
from sound import Sound
from high_scores import HighScores


class Game:
    def __init__(self, mode='continuous', difficulty='medium'):
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
        self.game_duration = 12#0  # 2 minutes for timed mode
        self.start_time = pygame.time.get_ticks()
        self.game_over_flag = False
        self.sound = Sound()
        self.sound.play_music()
        self.high_scores = HighScores()
        self.game_over_screen = None
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        if difficulty == 'easy':
            self.car.max_speed = 12
            self.car.acceleration = 0.07
            self.car.steering_speed = 0.008
            self.track.track_width = 400
        elif difficulty == 'medium':
            self.car.max_speed = 15
            self.car.acceleration = 0.085
            self.car.steering_speed = 0.01
            self.track.track_width = 350
        elif difficulty == 'hard':
            self.car.max_speed = 18
            self.car.acceleration = 0.1
            self.car.steering_speed = 0.012
            self.track.track_width = 300

    def handle_event(self, event):
        if self.game_over_flag and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return "MENU"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.mode == 'continuous':
                self.game_over()
            return "MENU"

    def update(self):
        if self.game_over_flag:
            self.game_over()
            return

        self.midi_controller.update()
        self.controls = self.midi_controller.get_controls()

        self.car.update(
            steering=self.controls['steering'],
            acceleration=self.controls['acceleration'],
            brake=self.controls['brake']
        )

        if self.track.check_off_track(self.car):
            self.car.speed *= 0.99  # Slow down when off track
            self.sound.update_gravel_sound(True)
        else:
            self.points += self.car.speed / 10  # Points based on speed when on track
            self.sound.update_gravel_sound(False)

        self.track.update(self.car)

        self.total_distance += self.car.speed

        # Update engine & braking sounds
        self.sound.update_engine_sound(self.controls['acceleration'])
        self.sound.update_braking_sound(self.controls['brake'])

        # Check for new checkpoint
        if self.total_distance >= (self.checkpoints + 1) * self.checkpoint_distance + 1650:
            self.checkpoints += 1
            self.points += 100  # Bonus points for checkpoint
            self.sound.play_sound('checkpoint')

        # Check for game over in timed mode
        if self.mode == 'timed':
            if (pygame.time.get_ticks() - self.start_time) / 1000 >= self.game_duration:
                self.game_over()

    def render(self):
        if self.game_over_screen and self.game_over_flag:
            self.screen.blit(self.game_over_screen, (0, 0))
        else:
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
        self.sound.stop_engine_sound()
        self.sound.play_sound('game_over')
        self.high_scores.add_score(self.mode, int(self.points), "Player")  # You can prompt for the player's name here
        self.game_over_screen = self.create_game_over_screen()
        self.midi_controller.close()
        self.game_over_flag = True

    def create_game_over_screen(self):
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, (255, 255, 255))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {int(self.points)}", True, (255, 255, 255))
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))

        #instruction_text = font.render("Press SPACE to return to menu", True, (255, 255, 255))
        #surface.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 400))

        return surface

    def is_game_over(self):
        return self.game_over_flag

    def cleanup(self):
        self.midi_controller.close()
        self.sound.stop_engine_sound()
        self.sound.stop_music()
        self.sound.update_braking_sound(False)
        self.sound.update_braking_sound(False)
