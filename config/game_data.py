"""Game data definitions."""

# Weapon data
WEAPON_DATA = {
    'sword': {
        'cooldown': 100,
        'damage': 15,
        'graphic': 'gameinfo/graphics/weapons/sword/full.png'
    }
}

# Magic data
MAGIC_DATA = {
    'flame': {
        'strength': 12,
        'cost': 20,
        'graphic': 'gameinfo/graphics/particles/flame/fire.png'
    },
    'heal': {
        'strength': 20,
        'cost': 20,
        'graphic': 'gameinfo/graphics/particles/heal/heal.png'
    }
}

# Monster data
MONSTER_DATA = {
    'squid': {
        'health': 100,
        'coin': 100,
        'damage': 20,
        'attack_type': 'slash',
        'attack_sound': 'gameinfo/audio/attack/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 80,
        'notice_radius': 360
    },
    'raccoon': {
        'health': 300,
        'coin': 250,
        'damage': 40,
        'attack_type': 'claw',
        'attack_sound': 'gameinfo/audio/attack/claw.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 120,
        'notice_radius': 400
    },
    'spirit': {
        'health': 100,
        'coin': 110,
        'damage': 8,
        'attack_type': 'thunder',
        'attack_sound': 'gameinfo/audio/attack/fireball.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 350
    },
    'bamboo': {
        'health': 70,
        'coin': 120,
        'damage': 6,
        'attack_type': 'leaf_attack',
        'attack_sound': 'gameinfo/audio/attack/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 300
    }
}

# Item types
ITEM_TYPES = {
    'WEAPON': 'weapon',
    'SPELL': 'spell',
    'TOOL': 'tool',
    'NORMAL': 'normal'
}

# Item data - Complete item database
ITEM_DATA = {
    # Weapons
    'sword': {
        'name': 'Espada',
        'type': ITEM_TYPES['WEAPON'],
        'description': 'Uma espada afiada de aço. Perfeita para combate corpo a corpo.',
        'icon': 'gameinfo/graphics/weapons/sword/full.png',
        'damage': 15,
        'cooldown': 100,
        'stackable': False
    },
    'axe': {
        'name': 'Machado',
        'type': ITEM_TYPES['WEAPON'],
        'description': 'Um machado pesado. Causa grande dano mas é mais lento.',
        'icon': 'gameinfo/graphics/weapons/sword/full.png',  # TODO: Add axe icon
        'damage': 20,
        'cooldown': 150,
        'stackable': False
    },
    
    # Spells
    'flame_scroll': {
        'name': 'Pergaminho de Chamas',
        'type': ITEM_TYPES['SPELL'],
        'description': 'Pergaminho mágico que invoca chamas para atacar inimigos.',
        'icon': 'gameinfo/graphics/particles/flame/fire.png',
        'spell_name': 'flame',
        'mana_cost': 20,
        'stackable': True,
        'max_stack': 10
    },
    'heal_scroll': {
        'name': 'Pergaminho de Cura',
        'type': ITEM_TYPES['SPELL'],
        'description': 'Pergaminho sagrado que restaura sua saúde.',
        'icon': 'gameinfo/graphics/particles/heal/heal.png',
        'spell_name': 'heal',
        'mana_cost': 20,
        'stackable': True,
        'max_stack': 10
    },
    
    # Tools
    'pickaxe': {
        'name': 'Picareta',
        'type': ITEM_TYPES['TOOL'],
        'description': 'Ferramenta para minerar rochas e coletar recursos.',
        'icon': 'gameinfo/graphics/weapons/sword/full.png',  # TODO: Add pickaxe icon
        'durability': 100,
        'stackable': False
    },
    'fishing_rod': {
        'name': 'Vara de Pesca',
        'type': ITEM_TYPES['TOOL'],
        'description': 'Uma vara simples para pescar. Útil perto de corpos d\'água.',
        'icon': 'gameinfo/graphics/weapons/sword/full.png',  # TODO: Add fishing rod icon
        'durability': 50,
        'stackable': False
    },
    
    # Normal items
    'health_potion': {
        'name': 'Poção de Vida',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Poção vermelha que restaura 50 pontos de vida imediatamente.',
        'icon': 'gameinfo/graphics/items/uva (1).png',
        'heal_amount': 50,
        'stackable': True,
        'max_stack': 20
    },
    'mana_potion': {
        'name': 'Poção de Mana',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Poção azul que restaura 30 pontos de mana imediatamente.',
        'icon': 'gameinfo/graphics/items/uva (2).png',
        'mana_amount': 30,
        'stackable': True,
        'max_stack': 20
    },
    'coin': {
        'name': 'Moedas de Ouro',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Moedas valiosas. Podem ser usadas para comprar itens.',
        'icon': 'gameinfo/graphics/items/uva (3).png',
        'stackable': True,
        'max_stack': 999
    },
    'apple': {
        'name': 'Maçã',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Uma maçã fresca. Restaura 20 pontos de vida.',
        'icon': 'gameinfo/graphics/items/uva (4).png',
        'heal_amount': 20,
        'stackable': True,
        'max_stack': 50
    },
    'bread': {
        'name': 'Pão',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Pão quentinho. Restaura 30 pontos de vida.',
        'icon': 'gameinfo/graphics/items/uva (5).png',
        'heal_amount': 30,
        'stackable': True,
        'max_stack': 50
    },
    'wood': {
        'name': 'Madeira',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Toras de madeira. Material básico para construção.',
        'icon': 'gameinfo/graphics/items/uva (6).png',
        'stackable': True,
        'max_stack': 99
    },
    'stone': {
        'name': 'Pedra',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Pedras resistentes. Material para construção e crafting.',
        'icon': 'gameinfo/graphics/items/uva (7).png',
        'stackable': True,
        'max_stack': 99
    },
    'iron_ore': {
        'name': 'Minério de Ferro',
        'type': ITEM_TYPES['NORMAL'],
        'description': 'Minério valioso. Pode ser fundido para criar ferramentas.',
        'icon': 'gameinfo/graphics/items/uva (8).png',
        'stackable': True,
        'max_stack': 50
    },
}

# Legacy inventory data for backward compatibility
INVENTORY_DATA = {
    'uva1': 10, 'uva2': 2, 'uva3': 3, 'uva4': 10, 'uva5': 4,
    'uva6': 10, 'uva7': 2, 'uva8': 3, 'uva9': 10, 'uva10': 4
}

INVENTORY_IMAGES = {
    f'uva{i}': f'gameinfo/graphics/items/uva ({i}).png'
    for i in range(1, 11)
}

# Aliases for backward compatibility
weapon_data = WEAPON_DATA
magic_data = MAGIC_DATA
monster_data = MONSTER_DATA
inventory_data = INVENTORY_DATA
inventory_images = INVENTORY_IMAGES
item_data = ITEM_DATA
item_types = ITEM_TYPES
