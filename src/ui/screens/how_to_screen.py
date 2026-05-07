import pygame
from src.utils.read_txt import read_txt
from src.ui.panel import Panel
from src.ui.theme import THEME

def draw_how_to_play(screen, back_button) -> None:
    back_button.draw(screen)

    panel = Panel(1600, 600)
    rect = panel.draw_panel(screen, 'How To Play')

    font = pygame.font.SysFont(THEME['primary_font'], 40)
    text_content = read_txt('instructions.txt')

    x = 180
    y = 300
    line_spacing = 48

    for line in text_content:

        text = font.render(line, 1, THEME['text_primary'], )
        screen.blit(text, (x, y))
        y += line_spacing

