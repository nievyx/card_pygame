from src.ui.theme import CARD_RENDER_THEME
import pygame

class CardRenderer:
    def __init__(self, battle, players, screen):
        self.screen = screen
        self.battle = battle
        self.players = players

        # ❌ TODO: Temp! Move to src/assets/image_cache.py
        # self.monster_image_cache = monster_image_cache


        self.card_frame = pygame.image.load('assets/frame/1.png').convert_alpha()
        self.card_frame = pygame.transform.smoothscale(self.card_frame, (112, 220))  # try 112, 220

    # ❌ TODO: Temp! Move to src/assets/image_cache.py
    def get_monster_image(self, image_path: str) -> pygame.Surface:
        """
        :param image_path:
        :return:
        """
        image = pygame.image.load(image_path).convert_alpha()
        cropped_rect = image.get_bounding_rect()
        image = image.subsurface(cropped_rect).copy()
        image = pygame.transform.smoothscale(image, (80, 90))

        return image

    def get_stat_color(self, current, max_value):
        """Toggles stat colors to highlight low stats"""
        if max_value <= 0:
            return CARD_RENDER_THEME['text']
        percent = 0.3
        return CARD_RENDER_THEME['low_stat'] if current / max_value <= percent else CARD_RENDER_THEME['secondary_text']

    def draw_monster_card(self, monster, card_rect):
        card_x, card_y = card_rect.topleft

        # draw card background
        pygame.draw.rect(self.screen, CARD_RENDER_THEME['bg'], card_rect)

        # Highlight selected card
        if monster == self.battle.selected_monster:
            pygame.draw.rect(self.screen, CARD_RENDER_THEME['selected'], card_rect, 3)

        # load + scale monster image
        monster_img = self.get_monster_image(monster.image)

        image_rect = monster_img.get_rect()
        image_rect.centerx = card_rect.centerx
        image_rect.top = card_y + 40

        # draw text
        card_name_font = pygame.font.SysFont('Arial', 20, bold=False)
        name_text = card_name_font.render(f'{monster.name}', True, (255, 255, 255))

        # TODO: use a stats variable and get it from themes / create it and then move it to themes

        hp_text_font = pygame.font.SysFont('Arial', 16)  # TODO: add font to config
        hp_color = self.get_stat_color(monster.hp, monster.max_hp)
        hp_text = hp_text_font.render(f'HP: {monster.hp}/{monster.max_hp}', True, hp_color)

        card_strength_font = pygame.font.SysFont('Arial', 16, bold=False)
        strength_text = card_strength_font.render(f'STR: {monster.strength}', True, CARD_RENDER_THEME['stat_text'])

        card_energy_font = pygame.font.SysFont('Arial', 16, bold=False)
        energy_text = card_energy_font.render(f'ENG: {monster.energy}/{monster.max_energy}', True,
                                              CARD_RENDER_THEME['stat_text'])
        mp_text = card_energy_font.render(
            f'MP: {monster.mp}/{monster.max_mp}', True, CARD_RENDER_THEME['stat_text']
        )

        # display monster's image and hp #TODO: For positioning for stats could do +30 each time in a for loop, also card creation could get a class
        name_offset = card_x + 26
        card_offset = card_x + 8
        self.screen.blit(name_text, (name_offset, card_y + 8))  # Name
        self.screen.blit(monster_img, image_rect)  # Image

        self.screen.blit(hp_text, (card_offset, card_y + 130))  # HP
        self.screen.blit(strength_text, (card_offset, card_y + 150))  # STR
        self.screen.blit(energy_text, (card_offset, card_y + 170))  # ENG
        self.screen.blit(mp_text, (card_offset, card_y + 190))  # MP


        #Add frame
        self.screen.blit(self.card_frame, card_rect.topleft)

    def print_cards(self) -> list:
        screen_rect = self.screen.get_rect()
        card_rects = []
        space_between_cards = 10
        card_width, card_height = 112, 220

        for row_index, (player, monsters) in enumerate(self.players.items()):
            alive_monsters = [monster for monster in monsters if monster.is_alive()]
            num_cards = len(alive_monsters)

            total_width = num_cards * card_width + (num_cards - 1) * space_between_cards

            row_rect = pygame.Rect(0, 0, total_width, card_height)
            row_rect.centerx = screen_rect.centerx
            # row_rect.y = initial_y + (row_index * y_offset)

            top_row_y = 80
            bottom_row_y = screen_rect.bottom - card_height - 80

            # Choose which player goes on top / bottom
            if row_index == 1:
                row_rect.y = top_row_y  # enemy
            else:
                row_rect.y = bottom_row_y  # player

            x = row_rect.left

            for monster in alive_monsters:
                # create rect for card (used for clicking)
                card_x = x
                card_y = row_rect.y
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                card_rects.append((card_rect, player, monster))
                self.draw_monster_card(monster, card_rect)

                x += card_width + space_between_cards

        return card_rects