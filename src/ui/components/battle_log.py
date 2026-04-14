import pygame
from src.ui.theme import THEME
from src.ui.panel import Panel

class BattleLog(Panel):
    def __init__(self, battle, width=440, height=180, top=360, right_padding=40):
        super().__init__(width, height, top, right_padding)
        self.battle = battle
        self.width = width
        self.height = height
        self.top = top
        self.right_padding = right_padding

    def display_monster_img(self):
        pass

    def draw(self, screen):
        log_rect = self.draw_panel(screen, 'Battle Log')

        pygame.draw.rect(screen, THEME['battle_log_bg'], log_rect)
        pygame.draw.rect(screen, THEME['battle_log_border'], log_rect, 2)

        font = pygame.font.SysFont('Arial', 18) #TODO: THEME['battle_log_title_font'], #THEME['battle_log_title_font_size']
        title = font.render('Battle Log', True, THEME['battle_log_default_text'])
        title_rect = title.get_rect(midtop=(log_rect.centerx, log_rect.top + 8))
        screen.blit(title, title_rect)

        line_font = pygame.font.SysFont('Arial', 16)
        start_y = log_rect.y + 35

        visible_entries = self.battle.log[-6:]

        for i, entry in enumerate(visible_entries):
            color = entry.get("color") or (230, 230, 230)
            text = line_font.render(entry["text"], True, color)
            text_rect = text.get_rect(midtop=(log_rect.centerx, start_y + i * 22))
            screen.blit(text, text_rect)
