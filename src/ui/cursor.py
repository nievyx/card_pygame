import pygame
from src.ui import THEME

class Cursor:
    def __init__(self):
        debug = 0
        if not debug:
            pygame.mouse.set_visible(False)
        self.size = (32,32)

        self.default_path = 'src/assets/cursors/01.png'
        self.attack_path = 'src/assets/icons/fc721.png'
        self.paths = {
            'default': self.default_path,
            'attack': self.attack_path,
            'valid_target': None,
            'invalid_target': None,
        }

        self.spr = self._load_image(self.default_path)

        self.x, self.y = 0, 0
        self.rect = pygame.rect.Rect(self.x, self.y, *self.size)

        # Cursor Message
        self.cursor_message = None
        self.cursor_message_pos = None
        self.cursor_message_until = 0

    def show_cursor_message(self,
                            text: str,
                            pos: tuple[int,int],
                            duration=900
                            ) -> None:
        """
        Display a message beside the cursor

        :param text: Message text to display
        :param pos: Mouse position (x, y)
        :param duration: Duration in milliseconds
        """
        self.cursor_message = text
        self.cursor_message_pos = pos
        self.cursor_message_until = pygame.time.get_ticks() + duration

    def _load_image(self, path):
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            self.size
        )

    def _set_path(self, path:str) -> None:
       self.spr = self._load_image(path)

    def use_default(self):
        self._set_path(self.default_path)

    def use_spell(self, spell):
        self._set_path(spell.icon_path)

    def use_attack(self):
        self._set_path(self.attack_path)

    def _is_cursor_msg(self) -> bool:
        """Check if there is a cursor message to display"""
        pass #TODO:

    def display_cursor_message(self, text) -> None:
        """Display a message beside the cursor"""
        pass #TODO:

    def draw(self, screen):
        screen.blit(self.spr, (self.x, self.y))

        #TODO:
        # Only draw cursor msg if there is one
        if (
            self.cursor_message
            and pygame.time.get_ticks() < self.cursor_message_until
        ):
            font = pygame.font.SysFont(
                THEME['cursor_text']['font'],
                THEME['cursor_text']['font_size']
                )

            text_surface = font.render(
                self.cursor_message,
                True,
                THEME['cursor_text']['color']
            )
            screen.blit(text_surface, (
                self.x  + 24,
                self.y - 10
            )
                        )
        else:
            self.cursor_message = None



    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.x = mx - self.size[0] // 2
        self.y = my - self.size[1] // 2
        self.rect = pygame.rect.Rect(self.x, self.y, 32, 32)
