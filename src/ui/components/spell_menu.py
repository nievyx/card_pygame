import pygame
from src.ui.theme import THEME
from src.ui.panel import Panel

class SpellMenu(Panel):
    def __init__(self, width=440, height=180, top=None, right_padding=None):
        super().__init__(width, height, top, right_padding)
        self.line_height = 30

    def get_spell_rects(self, screen, monster):
        menu_rect = screen.get_rect(screen)
        rects = []
        start_y = menu_rect.y + 40
        for i, _spell in enumerate(monster.known_spells):
            rects.append(pygame.Rect(menu_rect.x + 16, start_y + i * self.line_height - 2, menu_rect.width - 32, self.line_height))
        return rects




    def draw(self, screen, monster, selected_index=None):
        #screen.blit(monster.image)

        box_rect = self.draw_panel(screen, "Select Spell")
        line_font = pygame.font.SysFont(THEME['primary_font'], 16)
        start_y = box_rect.y + 40

        for i, spell in enumerate(monster.known_spells):
            prefix = ">" if i == selected_index else " "
            text_str = f"{prefix} {spell.name} ({spell.mana_cost} MP)"
            text = line_font.render(text_str, True, THEME['battle_log_default_text'])
            text_rect = text.get_rect(midtop=(box_rect.centerx, start_y + i * 24))
            screen.blit(text, text_rect)





