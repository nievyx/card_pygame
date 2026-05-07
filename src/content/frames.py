import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAME_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets', 'frame'))

RARITY_FRAMES = {
    'common': FRAME_DIR + '/100.png',
    'uncommon': FRAME_DIR + '/200.png',
    'rare': FRAME_DIR + '/300.png',
    'epic': FRAME_DIR + '/400.png',
    'legendary': FRAME_DIR + '/500.png',
}