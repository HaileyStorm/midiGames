import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from midi_controller import MIDIController
from car import Car
from track import Track

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display=1)
        pygame.display.set_caption("Rhythm Racer")
        self.clock = pygame.time.Clock()
        self.midi_controller = MIDIController()
        self.midi_controller.connect()
        self.track = Track(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.car = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    def handle_event(self, event):
        # TODO: Implement event handling (will be expanded later)
        pass

    def update(self):
        self.midi_controller.update()
        controls = self.midi_controller.get_controls()

        self.car.update(
            steering=controls['steering'],
            acceleration=controls['acceleration'],
            brake=controls['brake']
        )

        if self.track.check_collision(self.car):
            print("collide")
        #    self.car.speed *= 0.9  # Slow down when off track

        self.track.update(self.car.speed)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.track.draw(self.screen)
        self.car.draw(self.screen)

        # Render control values (as before)
        font = pygame.font.Font(None, 36)
        controls = self.midi_controller.get_controls()
        text = font.render(f"Steering: {controls['steering']:.2f}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        text = font.render(f"Acceleration: {controls['acceleration']:.2f}", True, (255, 255, 255))
        self.screen.blit(text, (10, 50))
        text = font.render(f"Brake: {controls['brake']}", True, (255, 255, 255))
        self.screen.blit(text, (10, 90))
        text = font.render(f"Speed: {self.car.speed}", True, (255, 255, 255))
        self.screen.blit(text, (10, 130))
