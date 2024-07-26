import random

class Obstacle:
    def __init__(self, x, y, obstacle_type):
        self.x = x
        self.y = y
        self.type = obstacle_type
        self.width = 60 if obstacle_type in ['oil', 'debris'] else 30  # Double for oil/debris
        self.height = 60 if obstacle_type in ['oil', 'debris'] else 30  # Double for oil/debris

    @staticmethod
    def generate(track_width, y):
        x = random.uniform(track_width * 0.25, track_width * 0.75)
        obstacle_type = random.choice(['oil', 'rock', 'debris'])
        return Obstacle(x, y, obstacle_type)

    @staticmethod
    def generate_type():
        return random.choice(['oil', 'rock', 'debris'])

    def update(self, forward_movement, lateral_movement):
        self.y -= forward_movement
        self.x -= lateral_movement

    def collides_with(self, car, screen_height):
        return (abs(self.x - car.x) < (self.width + car.width) / 2.5 and
                abs((screen_height - self.y) - car.y) < (self.height + car.height) / 2.5)

    def apply_effect(self, car):
        if self.type == 'oil':
            car.set_speed(min(car.speed, max(car.base_max_speed / 4.0, car.speed * 0.925)))
            car.apply_oil_effect()
        elif self.type == 'rock':
            car.take_damage(10.0)
        elif self.type == 'debris':
            car.take_damage(1.0)
            car.set_speed(min(car.speed, max(car.base_max_speed / 4.0, car.speed * 0.975)))
