import pygame
import numpy as np
from scipy import signal

class Sound:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sounds = {
            'checkpoint': pygame.mixer.Sound('assets/sounds/checkpoint.mp3'),
            'game_over': pygame.mixer.Sound('assets/sounds/game_over.mp3'),
            'acceleration': pygame.mixer.Sound('assets/sounds/engine.wav'),
            'braking': pygame.mixer.Sound('assets/sounds/braking.wav'),
            'background_music': pygame.mixer.Sound('assets/sounds/background_music.wav')
        }
        self.channels = {
            'effects': pygame.mixer.Channel(0),
            'music': pygame.mixer.Channel(1),
            'engine': pygame.mixer.Channel(2),
            'braking': pygame.mixer.Channel(3)
        }
        self.global_volume = 0.5
        self.channel_volumes = {
            'effects': 1.0,
            'music': 0.25,
            'engine': 1.0,
            'braking': 0.7
        }
        self.engine_baseline_volume = 0.6667
        self.engine_sound_length = self.sounds['acceleration'].get_length()
        self.engine_sound_array = pygame.sndarray.array(self.sounds['acceleration'])
        self.engine_last_resample_time = 0
        self.is_engine_playing = False
        self.is_braking_playing = False

    def set_global_volume(self, volume):
        self.global_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_channel_volume(self, channel, volume):
        if channel in self.channel_volumes:
            self.channel_volumes[channel] = max(0.0, min(1.0, volume))
            self._update_volumes()

    def _update_volumes(self):
        for channel, volume in self.channel_volumes.items():
            self.channels[channel].set_volume(volume * self.global_volume)

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.channels['effects'].play(self.sounds[sound_name])

    def play_music(self):
        self.channels['music'].play(self.sounds['background_music'], loops=-1)

    def stop_music(self):
        self.channels['music'].stop()

    def update_engine_sound(self, acceleration):
        current_time = pygame.time.get_ticks()
        volume = self.engine_baseline_volume + acceleration * 0.6667
        self.channels['engine'].set_volume(volume * self.global_volume)

        if not self.is_engine_playing:
            self.channels['engine'].play(self.sounds['acceleration'], loops=-1)
            self.is_engine_playing = True

        if current_time - self.engine_last_resample_time > self.engine_sound_length * 1000:
            pitch = 1.0 + acceleration * 0.6667
            resampled = signal.resample(self.engine_sound_array, int(len(self.engine_sound_array) / pitch))
            sound = pygame.sndarray.make_sound(resampled.astype(np.int16))
            self.channels['engine'].play(sound, loops=-1)
            self.engine_last_resample_time = current_time
            self.engine_sound_length = sound.get_length()

    def stop_engine_sound(self):
        self.channels['engine'].stop()
        self.is_engine_playing = False

    def update_braking_sound(self, is_braking):
        if is_braking and not self.is_braking_playing:
            self.channels['braking'].play(self.sounds['braking'], loops=-1)
            self.is_braking_playing = True
        elif not is_braking and self.is_braking_playing:
            self.channels['braking'].stop()
            self.is_braking_playing = False
