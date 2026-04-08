import pygame
from src.ui.theme import THEME

class Panel:
    def __init__(self, width, height, top=None, right_padding=None):
        self.width = width
        self.height = height
        self.top = top
        self.right_padding = right_padding

    def get_rect(self, screen):
        pass