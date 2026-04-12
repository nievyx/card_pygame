import pygame

class Cursor:
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.size = (32,32)
        self.default_path = 'assets/cursors/01.png'
        self.attack_path = 'assets/icons/fc721.png'

        self.spr = pygame.transform.scale(
            pygame.image.load(self.default_path).convert_alpha(),
            self.size
        )

        self.x, self.y = 0, 0
        self.rect = pygame.rect.Rect(self.x, self.y, 32, 32)

    def _set_path(self,path):
        self.default_path = path

    def use_spell(self, spell):
        self._set_path(spell.default_path)

    def draw(self, screen):
        screen.blit(self.spr, (self.x, self.y))

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.x = mx - self.size[0] // 2
        self.y = my - self.size[1] // 2
        self.rect = pygame.rect.Rect(self.x, self.y, 32, 32)
