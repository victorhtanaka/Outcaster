"""Resource paths."""
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'gameinfo'
GRAPHICS_DIR = ASSETS_DIR / 'graphics'
AUDIO_DIR = ASSETS_DIR / 'audio'
MAP_DIR = ASSETS_DIR / 'map'

# Font paths
UI_FONT = str(GRAPHICS_DIR / 'font' / 'main_font.ttf')
UI_FONT_THIN = str(GRAPHICS_DIR / 'font' / 'DigitalDiscoThin.ttf')

# Graphics paths
PLAYER_GRAPHICS = GRAPHICS_DIR / 'player'
MONSTER_GRAPHICS = GRAPHICS_DIR / 'monsters'
WEAPON_GRAPHICS = GRAPHICS_DIR / 'weapons'
PARTICLE_GRAPHICS = GRAPHICS_DIR / 'particles'
UI_GRAPHICS = GRAPHICS_DIR / 'ui'
TILEMAP_GRAPHICS = GRAPHICS_DIR / 'tilemap'

# Map paths
MAP_FLOOR = MAP_DIR / 'map_Floor.csv'
MAP_FLOOR_BLOCKS = MAP_DIR / 'map_FloorBlocks.csv'
MAP_GRASS = MAP_DIR / 'map_Grass.csv'
MAP_OBJECTS = MAP_DIR / 'map_Objects.csv'
MAP_ENTITIES = MAP_DIR / 'map_Entities.csv'
MAP_DETAILS = MAP_DIR / 'map_Details.csv'
