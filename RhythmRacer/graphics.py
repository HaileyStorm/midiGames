import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Graphics:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.car_image = self.load_car_image()

    def load_car_image(self):
        # Load and scale the car image
        car_image = pygame.image.load('assets/images/car.png').convert_alpha()
        # Rotate the image 90 degrees to point upwards
        car_image = pygame.transform.rotate(car_image, 90)
        return pygame.transform.scale(car_image, (40, 80))  # Adjust size as needed

    def render_car(self, screen, car):
        rotated_car = pygame.transform.rotate(self.car_image, -car.angle * 180 / 3.14159)
        screen.blit(rotated_car, rotated_car.get_rect(center=(car.x, car.y)))
        if car.shield_active:
            pygame.draw.circle(screen, (0, 255, 255), (int(car.x), int(car.y)), int(car.width * 1.15), 2)

    def render_track(self, screen, track):
        track.draw(screen)

    def render_gui(self, screen, car, time_display, checkpoints, acceleration, points, distance, mode):
        y_offset = 10
        line_height = 40

        # Render speed
        speed_text = self.font.render(f"Speed: {car.speed * (160.0 / car.base_max_speed):.1f} km/h", True, (255, 255, 255))
        screen.blit(speed_text, (10, y_offset))
        y_offset += line_height

        # Render time
        if mode == 'timed':
            time_text = self.font.render(f"Time left: {time_display:.1f}s", True, (255, 255, 255))
        else:
            time_text = self.font.render(f"Time: {time_display:.1f}s", True, (255, 255, 255))
        screen.blit(time_text, (10, y_offset))
        y_offset += line_height

        # Render checkpoints
        checkpoint_text = self.font.render(f"Checkpoints: {checkpoints}", True, (255, 255, 255))
        screen.blit(checkpoint_text, (10, y_offset))
        y_offset += line_height

        # Render distance (convert to km)
        distance_km = distance * (160 / car.base_max_speed) / 1000
        distance_text = self.font.render(f"Distance: {distance_km:.2f} km", True, (255, 255, 255))
        screen.blit(distance_text, (10, y_offset))
        y_offset += line_height

        # Render acceleration
        accel_text = self.font.render(f"Accel: {acceleration:.2f}", True, (255, 255, 255))
        screen.blit(accel_text, (10, y_offset))
        y_offset += line_height

        # Render damage
        damage_text = self.font.render(f"Damage: {int(car.damage)}%", True, (255, 255, 255))
        screen.blit(damage_text, (10, y_offset))
        y_offset += line_height

        # Render shield status
        if car.shield_active:
            shield_text = self.font.render("Shield Active", True, (0, 255, 255))
            screen.blit(shield_text, (10, y_offset))
            y_offset += line_height

        # Render points
        points_text = self.font.render(f"Points: {int(points)}", True, (255, 255, 255))
        screen.blit(points_text, (10, y_offset))

    def render_game(self, screen, car, track, time_display, checkpoints, acceleration, points, distance, mode):
        screen.fill((0, 0, 0))  # Fill screen with black
        self.render_track(screen, track)
        self.render_car(screen, car)
        self.render_gui(screen, car, time_display, checkpoints, acceleration, points, distance, mode)
