import random

class PowerUp:
    def __init__(self, name, duration, effect):
        self.name = name
        self.duration = duration
        self.effect = effect
        self.available = False
        self.active = False
        self.time_left = 0

    def collect(self):
        self.available = True

    def activate(self):
        if self.available:
            self.active = True
            self.available = False
            self.time_left = self.duration

    def update(self, dt):
        if self.active:
            self.time_left -= dt
            if self.time_left <= 0:
                self.active = False

class PowerUpSystem:
    def __init__(self, difficulty):
        self.power_ups = [
            PowerUp("Speed Boost", 5, lambda car: setattr(car, 'max_speed', car.max_speed * 1.5)),
            PowerUp("Shield", 7, lambda car: None),  # Implement shield logic in car.py
            PowerUp("Score Multiplier", 10, lambda game: setattr(game, 'score_multiplier', 2)),
            PowerUp("Repair", 1, lambda car: setattr(car, 'damage', max(0, car.damage - 50)))
        ]
        self.spawn_interval = self.get_spawn_interval(difficulty)
        self.time_since_last_spawn = 0

    def get_spawn_interval(self, difficulty):
        if difficulty == 'easy':
            return 15
        elif difficulty == 'medium':
            return 20
        else:  # hard
            return 25

    def update(self, dt, game):
        self.time_since_last_spawn += dt
        if self.time_since_last_spawn >= self.spawn_interval:
            self.spawn_power_up(game)
            self.time_since_last_spawn = 0

        for power_up in self.power_ups:
            power_up.update(dt)
            if power_up.active:
                power_up.effect(game.car if power_up.name != "Score Multiplier" else game)

    def spawn_power_up(self, game):
        unavailable_power_ups = [pu for pu in self.power_ups if not pu.available and not pu.active]
        if unavailable_power_ups:
            power_up = random.choice(unavailable_power_ups)
            game.track.spawn_power_up(power_up)

    def activate_power_up(self, index):
        if 0 <= index < len(self.power_ups) and self.power_ups[index].available:
            self.power_ups[index].activate()
            return True
        return False

    def get_power_up_status(self):
        return [127 if pu.active else (64 if pu.available else 0) for pu in self.power_ups]