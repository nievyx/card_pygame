from src.content.frames import RARITY_FRAMES
from src.ui.theme import CARD_RENDER_THEME as THEME
from src.assets.image_cache import ImageCache
import pygame

class CardRenderer:
    def __init__(self, battle, players, screen):
        self.screen = screen
        self.battle = battle
        self.players = players

        self.image_cache = ImageCache()

        self.card_width, self.card_height = 118, 250

        self.anim_positions = {}
        self.deck_pos = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.animation_speed = 0.18

    def get_dealt_cards(self, monster, target_rect):#TODO add typing
        if monster not in self.anim_positions:
            self.anim_positions[monster] = [
                self.deck_pos[0],
                self.deck_pos[1]
            ]

            pos = self.anim_positions[monster]

            pos[0] += (target_rect.x - pos[0]) * self.animation_speed
            pos[1] += (target_rect.y - pos[0]) * self.animation_speed

            if abs(pos[0] - target_rect.x) < 1:
                pos[0] = target_rect.x
            if abs(pos[1] - target_rect.y) < 1:
                pos[1] = target_rect.y

            dealt_rect = target_rect.copy()
            dealt_rect.x = round(pos[0])
            dealt_rect.y = round(pos[1])
            return dealt_rect
        return None

    # TODO: Cache frames
    def get_card_frame(self, monster) -> pygame.Surface:
        """Checks monsters rarity attribute and returns card frame"""
        frame_path = RARITY_FRAMES.get(monster.rarity, RARITY_FRAMES["common"])
        frame = pygame.image.load(frame_path).convert_alpha()
        frame = pygame.transform.smoothscale(frame, (self.card_width, self.card_height))
        # print(monster.name, monster.rarity)
        return frame

    def get_stat_color(self, current, max_value):
        """Toggles stat colors to highlight low stats"""
        if max_value <= 0:
            return THEME['text']
        mid_threshold = 0.5
        low_threshold = 0.3
        return (THEME['low_stat'] if current / max_value <= low_threshold else
                THEME['mid_stat'] if current / max_value <= mid_threshold else
                THEME['secondary_text'])

    def draw_monster_stats(self, monster, card_x, card_y):
        """Displays stats for a monster on the card"""
        monster_stats = {'HP': (monster.hp, monster.max_hp),
                         'STR': (monster.strength, monster.max_strength),
                         'ENG': (monster.energy, monster.max_energy),
                         'MP': (monster.mp, monster.max_mp),
                         }
        card_offset = card_x + 8
        offset_y = 130
        font_ = pygame.font.SysFont(THEME['font'], 16)
        for stat, (stat_current, stat_max) in monster_stats.items():
            color = self.get_stat_color(stat_current, stat_max)
            antialias = True

            card_stat = font_.render(f'{stat}: {stat_current}/{stat_max}', antialias, color)
            self.screen.blit(card_stat, (card_offset, card_y + offset_y))
            offset_y += 20

    def draw_monster_card(self, monster, card_rect):
        card_x, card_y = card_rect.topleft

        # draw card background
        pygame.draw.rect(self.screen, THEME['bg'], card_rect)

        # Highlight selected card
        if monster == self.battle.selected_monster:
            pygame.draw.rect(self.screen, THEME['selected'], card_rect, 12)

        # load + scale monster image
        monster_img = self.image_cache.get_monster_image(monster.image)

        image_rect = monster_img.get_rect()
        image_rect.centerx = card_rect.centerx
        image_rect.top = card_y + 40

        # draw text
        card_name_font = pygame.font.SysFont(THEME['font'], 20, bold=False)
        name_text = card_name_font.render(f'{monster.name}', True, (255, 255, 255))

        name_offset = card_x + 26

        self.screen.blit(name_text, (name_offset, card_y + 8))  # Name
        self.screen.blit(monster_img, image_rect)  # Image
        self.draw_monster_stats(monster, card_x, card_y) # Stats


        # Render Frame
        self.screen.blit(self.get_card_frame(monster), card_rect.topleft)
        #TODO: fix this so frames are caches
        #card_frame = self.image_cache.get_card_frame(monster.rarity_path, card_rect.topleft)

    def get_card_draw_rect(self, card_rect, monster):
        """Returns the visual draw rect for a monster card.
        Applies hover and selection offsets to create a lifted
        card effect without changing the original rect.
        """
        draw_rect = card_rect.copy()

        if card_rect.collidepoint(pygame.mouse.get_pos()):
            draw_rect.y -= 18

        if monster == self.battle.selected_monster:
            draw_rect.y -= 18

        if monster == self.battle.ai_active_monster:
            draw_rect.y += 18 #DEBUG

        return draw_rect

    def draw_card_shadow(self, card_rect):
        shadow_rect = card_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 10

        shadow = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)

        pygame.draw.rect(
            shadow,
            THEME['shadow'],
            shadow.get_rect(),
            border_radius=14
        )

        self.screen.blit(shadow, shadow_rect)


    def draw(self) -> list:
        screen_rect = self.screen.get_rect()
        card_rects = []
        space_between_cards = 10

        for row_index, (player, monsters) in enumerate(self.players.items()):
            alive_monsters = [monster for monster in monsters if monster.is_alive]
            num_cards = len(alive_monsters)

            total_width = num_cards * self.card_width + (num_cards - 1) * space_between_cards

            row_rect = pygame.Rect(0, 0, total_width, self.card_height)
            row_rect.centerx = screen_rect.centerx
            # row_rect.y = initial_y + (row_index * y_offset)

            top_row_y = 80
            bottom_row_y = screen_rect.bottom - self.card_height - 80

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

                card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
                draw_rect = self.get_card_draw_rect(card_rect, monster)

                # Shadow
                self.draw_card_shadow(draw_rect)

                #IMPORTANT: Draw using draw_rect
                self.draw_monster_card(monster, draw_rect)


                #IMPORTANT: keep original rect for clicking
                card_rects.append((card_rect, player, monster))


                x += self.card_width + space_between_cards

        return card_rects