import os
import pygame

class SFX:
    #TODO: debug fireball.mp3 added to sfx for testing
    def __init__(self, base_path='assets/sfx'):
        pygame.mixer.init()
        self.base_path = base_path
        self.cache = {}

        self.volume = 0.5
        self.set_volume(self.volume)

    def play(self, spell):
        sounds_name = spell.sfx_name
        sound_path = os.path.join(self.base_path, 'spells',f'{sounds_name}.wav')

        if not os.path.exists(sound_path):
            return

        if sound_path not in self.cache:
            self.cache[sound_path] = pygame.mixer.Sound(sound_path)

        self.cache[sound_path].mixer.Sound(sound_path)

    def set_volume(self, volume):
        self.volume = volume
        for sound in self.cache.values():
            sound.set_volume(volume)