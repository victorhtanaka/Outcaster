# setup
WIDTH    = 1366
HEIGHT   = 768
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -80,
    'grass': -10,
    'invisible': 0
}

#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'gameinfo/graphics/font/DigitalDisco.ttf'
UI_FONT_THIN = 'gameinfo/graphics/font/DigitalDiscoThin.ttf'
UI_FONT_SIZE = 64
UI_FONT_SIZE_THIN = 32

#DISTANCIA DE DIALOGO
INTERACTION_DISTANCE = 600

#CORES GERAIS
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#CORES DA UI
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# Armas
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'gameinfo/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 500, 'damage': 30,'graphic':'gameinfo/graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'gameinfo/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'gameinfo/graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'gameinfo/graphics/weapons/sai/full.png'}}

# Mágica
magic_data = {
    'flame': {'strength': 12,'cost': 20,'graphic':'gameinfo/graphics/particles/flame/fire.png'},
    'heal': {'strength': 20,'cost': 20,'graphic':'gameinfo/graphics/particles/heal/heal.png'}}

# Inimigo
monster_data = {
	'squid': {'health': 100,'coin':100,'damage':20,'attack_type': 'slash', 'attack_sound':'gameinfo/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'coin':250,'damage':40,'attack_type': 'claw',  'attack_sound':'gameinfo/audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'coin':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'gameinfo/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'coin':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'gameinfo/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

# Inventário
inventory_data = {'coins': 10,'rock': 2,'diamonds': 3,'gold': 10}