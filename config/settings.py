"""Game settings and constants."""
from pathlib import Path

# Display settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TILESIZE = 64

# Hitbox offsets
HITBOX_OFFSET = {
    'player': -26,
    'object': -80,
    'grass': -10,
    'invisible': 0
}

# UI settings
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'gameinfo/graphics/font/main_font.ttf'
UI_FONT_THIN = 'gameinfo/graphics/font/DigitalDiscoThin.ttf'
UI_FONT_SIZE = 64
UI_FONT_SIZE_THIN = 32

# Gameplay
INTERACTION_DISTANCE = 150

# Colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# Verificador
VER = 0
