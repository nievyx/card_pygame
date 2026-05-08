CARD_RENDER_THEME = {
    'bg': (21, 30, 61),
    'selected': (255, 255, 0),
    'text': (255, 255, 255),
    'secondary_text': (230, 230, 230),
    'stat_text': (255, 255, 255),
    'low_stat': (255, 0, 0),
    'mid_stat': (255, 200, 0),
    'font': 'Arial',
    'shadow': (0, 0, 0, 100)
}

BATTLE_LOG_COLORS = {
    'PLAYER_LOG_COLOR': (255, 255, 255),
    'ENEMY_LOG_COLOR': (240, 80, 16),
    'PLAYER_ENERGY_LOW_COLOR': (255, 255, 255),
}

THEME = {
    'battle_log': BATTLE_LOG_COLORS,

    'PLAYER_LOG_COLOR': (255, 255, 255), #TODO: stop using these
    'ENEMY_LOG_COLOR': (240, 80, 16), #TODO: stop using these

    'background': (21, 30, 61),

    'card_color': (80 , 50 , 50, 100), # Gray (50,50,50)

    'panel_bg': (35, 35, 35, 80),
    'panel_border': (200, 200, 200),

    'text_primary': (255, 255, 255),
    'text_secondary': (230, 230, 230),

    'primary_font' : 'Arial', #THEME['primary_font']

    'card_bg': (50, 50, 50),
    'card_selected': (255, 255, 0),

    'card_stat_text': (255, 255, 255),
    'card_stat_low' : (255, 0, 0),

    # BUTTONS
    # (Used in ui/buttons.py)
    'button_font' : 'consolas',
    'button_text_color' : (0, 0 , 0),
    'how_to_color': (170, 90, 10),
    'back_button_color': (200, 200, 200),
    'main_menu_color' : (200, 200, 200),
    'quit_color' : (200, 200, 200),


    # BATTLE LOG
    # (Used in ui/components/battle_log.py)
    'battle_log_bg' :  (35, 35, 35), #Make green (20, 35, 35),
    'battle_log_border': (200, 200, 200),

    'battle_log_default_text' : (255, 255, 255),

    'battle_log_title_font': 'Arial', #TODO: not in use
    'battle_log_title_font_size' : 16, #TODO: not in use

    'battle_log_font': 'Arial', #TODO: not in use
    'battle_log_text_size' : 16, #TODO: not in use
    'battle_log_text_color' : (0, 0 , 0),
}

