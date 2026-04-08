import pygame
from src.ui.theme import THEME

class BattleLog: #TODO: rect, theme, font_manger removed
    def __init__(self, battle, width=440, height=180, top=360, right_padding=40):
        self.battle = battle
        self.width = width
        self.height = height
        self.top = top
        self.right_padding = right_padding

    def draw(self, screen): #TODO: removed entries
        screen_rect = screen.get_rect()

        log_rect = pygame.Rect(0, 0, self.width, self.height)
        log_rect.top = self.top
        log_rect.right = screen_rect.right - self.right_padding

        pygame.draw.rect(screen, THEME['battle_log_bg'], log_rect)
        pygame.draw.rect(screen, THEME['battle_log_border'], log_rect, 2)

        font = pygame.font.SysFont('Arial', 18) #THEME['battle_log_title_font'], #THEME['battle_log_title_font_size']
        title = font.render('Battle Log', True, THEME['battle_log_default_text'])
        screen.blit(title, (log_rect.x + 10, log_rect.y + 8))

        line_font = pygame.font.SysFont('Arial', 16)
        start_y = log_rect.y + 35

        for i, entry in enumerate(self.battle.log):
            color = entry.get("color") or (230, 230, 230)
            text = line_font.render(entry["text"], True, color)
            screen.blit(text, (log_rect.x + 10, start_y + i * 22))
