import pygame

class ImageCache:
    def __init__(self):
        self.monster_image_cache = {}

    def get_monster_image(self, image_path: str) -> pygame.Surface:
        """
        :param image_path:
        :return:
        """
        if image_path not in self.monster_image_cache:
            image = pygame.image.load(image_path).convert_alpha()
            cropped_rect = image.get_bounding_rect()
            image = image.subsurface(cropped_rect).copy()
            image = pygame.transform.smoothscale(image, (80, 90))
            self.monster_image_cache[image_path] = image

        return self.monster_image_cache[image_path]