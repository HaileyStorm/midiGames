import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from midi_controller import MIDIController

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display=1)
        pygame.display.set_caption("Rhythm Racer")
        self.clock = pygame.time.Clock()
        self.midi_controller = MIDIController()
        self.midi_controller.connect()

    def handle_event(self, event):
        # TODO: Implement event handling (will be expanded later)
        pass

    def update(self):
        self.midi_controller.update()
        controls = self.midi_controller.get_controls()

        # TODO: Use controls to update game state
        #print(
        #    f"Steering: {controls['steering']:.2f}, Acceleration: {controls['acceleration']:.2f}, Brake: {controls['brake']}")

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        # TODO: Add rendering of game objects

        # Temporary: render control values on screen
        font = pygame.font.Font(None, 36)
        controls = self.midi_controller.get_controls()
        text = font.render(f"Steering: {controls['steering']:.2f}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        text = font.render(f"Acceleration: {controls['acceleration']:.2f}", True, (255, 255, 255))
        self.screen.blit(text, (10, 50))
        text = font.render(f"Brake: {controls['brake']}", True, (255, 255, 255))
        self.screen.blit(text, (10, 90))