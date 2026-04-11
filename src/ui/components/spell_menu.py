import pygame
from src.ui.theme import THEME
from src.ui.panel import Panel

class SpellMenu(Panel):
    def __init__(self, width=440, height=180, top=None, right_padding=None):
        super().__init__(width, height, top, right_padding)
        self.selected_index = 0

    def draw(self, screen, monster):
        # screen.blit(monster.image)

        box_rect = self.draw_panel(screen, "Select Spell")

        line_font = pygame.font.SysFont('Arial', 16)
        start_y = box_rect.y + 40

        for i, spell in enumerate(monster.known_spells):
            prefix = ">" if i == self.selected_index else " "
            text_str = f"{prefix} {spell.name} ({spell.mana_cost} MP)"
            text = line_font.render(text_str, True, THEME['battle_log_default_text'])
            text_rect = text.get_rect(midtop=(box_rect.centerx, start_y + i * 24))
            screen.blit(text, text_rect)





