import pygame

class Cursor:
    def __init__(self):
        # pygame.mouse.set_visible(False) # TODO: Use this to Hide mouse cursor
        self.size = (32,32)
        self.spr = pygame.transform.scale(
            pygame.image.load('assets/icons/fc721.png').convert_alpha(),
            self.size
        )
        self.default_path = 'assets/icons/fc721.png'

        self.x = 0
        self.y = 0
        self.rect = pygame.rect.Rect(self.x, self.y, 32, 32)

    def draw(self, screen):
        screen.blit(self.spr, (self.x, self.y))

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.x = mx - self.size[0] // 2
        self.y = my - self.size[1] // 2
        self.rect = pygame.rect.Rect(self.x, self.y, 32, 32)
