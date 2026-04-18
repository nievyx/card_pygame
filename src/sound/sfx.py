import os
import pygame

class SFX:
    def __init__(self, base_path='src/assets/sfx'):
        pygame.mixer.init()
        self.base_path = base_path
        self.cache = {}

        self.volume = 0.5
        self.set_volume(self.volume)

    def play(self, spell):
        sounds_name = spell.sfx_name
        sound_path = os.path.join(self.base_path, 'spells',f'{sounds_name}.wav')

        if not os.path.exists(sound_path):
            print(f"[SFX WARNING] Missing sound: {sound_path}")
            return

        if sound_path not in self.cache:
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(self.volume)
            self.cache[sound_path] = sound

        self.cache[sound_path].play()

    def set_volume(self, volume):
        self.volume = volume
        for sound in self.cache.values():
            sound.set_volume(volume)