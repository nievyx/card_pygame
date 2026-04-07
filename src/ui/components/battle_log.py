import pygame
from src.ui.theme import THEME

class BattleLog:
    def __init__(self, battle): #TODO: rect, theme, font_manger removed
        self.battle = battle

    def draw(self, screen): #TODO: removed entries
        log_rect = pygame.Rect(720, 360, 440, 180)  # left, top, width, height
        pygame.draw.rect(screen, THEME['battle_log_bg'], log_rect)
        pygame.draw.rect(screen, THEME['battle_log_border'], log_rect, 2)

        font = pygame.font.SysFont('Arial', 18)
        title = font.render('Battle Log', True, THEME['battle_log_default_text'])
        screen.blit(title, (log_rect.x + 10, log_rect.y + 8))

        line_font = pygame.font.SysFont('Arial', 16)
        start_y = log_rect.y + 35

        for i, entry in enumerate(self.battle.log):
            color = entry.get("color") or (230, 230, 230)
            text = line_font.render(entry["text"], True, color)
            screen.blit(text, (log_rect.x + 10, start_y + i * 22))
