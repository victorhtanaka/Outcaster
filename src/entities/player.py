import pygame
from config.settings import *
from config.game_data import weapon_data, magic_data
from src.core.utils import import_folder
from src.entities.entity import Entity
from src.ui.dialogue_box import DialogueBox
from src.systems.inventory_system import InventorySystem

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('gameinfo/graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])
        self.dialogue_box = DialogueBox()

        # IMPORTAR PLAYER ASSETS
        self.import_player_assets()
        self.status = 'down'

        # Movimento e ataque
        self.attacking = False
        self.attack_cooldown = 600
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # Arma
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magica
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 12, 'speed': 6}
        self.inventory_data = {'coins': 10,'rock': 2,'diamonds': 3,'gold': 10}
        self.health = self.stats['health'] 
        self.energy = self.stats['energy'] 
        self.coin = 200
        self.speed = self.stats['speed']
        self.talking = False
        
        # Inventory system
        self.inventory = InventorySystem()
        self._setup_starting_inventory()

        # NPC interaction
        self.nearby_npc = None
        self.interaction_callback = None

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # Importar som
        self.weapon_attack_sound = pygame.mixer.Sound('gameinfo/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.1)

    def import_player_assets(self):
        character_path = 'gameinfo/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking and not self.talking:
            keys = pygame.key.get_pressed()

            # Input de Movimento (WASD)
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Input de ataque
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            # Input de magica
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)
            
            # Input de diálogo
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]
            
            if keys[pygame.K_g] and self.rect.colliderect(NPC1.npc_rect):
                self.talking = True
                self.dialogue_box
                print("dialogo")

    def get_status(self):

		# Status da idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')
    
    # Controle de cooldown de ataque, magica e vulnerabilidade
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown'] - 250:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # Loopar no frame index
        self.frame_index += self.animation_speed + 0.05
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #setar imagem
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.inventory_data.values())[index]
    
    def _setup_starting_inventory(self):
        """Setup player's starting inventory with default items."""
        # Add starting weapons
        self.inventory.add_item('sword', 1)
        self.inventory.add_item('axe', 1)
        
        # Add starting spells
        self.inventory.add_item('flame_scroll', 3)
        self.inventory.add_item('heal_scroll', 5)
        
        # Add starting consumables
        self.inventory.add_item('health_potion', 10)
        self.inventory.add_item('mana_potion', 5)
        self.inventory.add_item('apple', 15)
        self.inventory.add_item('bread', 8)
        
        # Add starting resources
        self.inventory.add_item('wood', 20)
        self.inventory.add_item('stone', 15)
        self.inventory.add_item('coin', 100)
    
    def use_item(self, item_data):
        """Use/consume an item from inventory."""
        if not item_data:
            return False
        
        item_type = item_data.get('type')
        
        # Handle consumables
        if item_type == 'normal':
            # Health potion/food
            if 'heal_amount' in item_data:
                heal_amount = item_data['heal_amount']
                if self.health < self.stats['health']:
                    self.health = min(self.stats['health'], self.health + heal_amount)
                    print(f"Restored {heal_amount} HP!")
                    return True
            
            # Mana potion
            if 'mana_amount' in item_data:
                mana_amount = item_data['mana_amount']
                if self.energy < self.stats['energy']:
                    self.energy = min(self.stats['energy'], self.energy + mana_amount)
                    print(f"Restored {mana_amount} MP!")
                    return True
        
        # Handle spells (cast from inventory)
        elif item_type == 'spell':
            spell_name = item_data.get('spell_name')
            mana_cost = item_data.get('mana_cost', 0)
            if self.energy >= mana_cost:
                # Cast spell (you can enhance this later)
                print(f"Cast {spell_name}!")
                return True
            else:
                print("Not enough mana!")
                return False
        
        # Handle weapons (equip)
        elif item_type == 'weapon':
            # You can add weapon switching logic here
            print(f"Equipped {item_data.get('name')}!")
            return False  # Don't consume weapon
        
        return False

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.005 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
    
    def set_nearby_npc(self, npc):
        """Set the NPC that is currently nearby."""
        self.nearby_npc = npc
    
    def clear_nearby_npc(self):
        """Clear nearby NPC reference."""
        self.nearby_npc = None
    
    def try_interact(self):
        """Try to interact with nearby NPC."""
        if self.nearby_npc and not self.talking and self.interaction_callback:
            self.interaction_callback(self.nearby_npc)
            return True
        return False
    
    def set_interaction_callback(self, callback):
        """Set callback function for NPC interaction."""
        self.interaction_callback = callback