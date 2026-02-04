import pygame
import sys
from config.settings import *
from src.entities.tile import Tile
from src.entities.player import Player
from src.entities.npc import NPC
from src.core.utils import *
from src.core.resource_manager import ResourceManager
from random import choice, randint
from src.systems.weapon import Weapon
from src.systems.dialogue_system import DialogueSystem
from src.ui.game_ui import UI
from src.ui.dialogue_box import DialogueBox
from src.ui.inventory_ui import InventoryUI
from src.entities.enemy import Enemy
from src.systems.particles import AnimationPlayer
from src.systems.magic import MagicPlayer
from src.ui.inventory import Inventory
from src.ui.menus.escape_menu import *
from src.ui.screens.death_screen import *
from src.systems.save_system import SaveSystem
from src.core.input_config import InputConfig

class Level():
    def __init__(self):

        self.display = pygame.display.get_surface()

        # npc
        self.visible = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()

        # superfície de exibição
        self.display_surface = pygame.display.get_surface()

        # Inventario e Menu Pause
        self.state = 'playing' # playing, paused, inventory, dialogue
        self.save_system = SaveSystem()

        # titulo
        self.title_ver = True

        # setup de grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
    
        # SPRITES DE ATAQUE
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # SETUP SPRITES
        self.create_map()
        
        # Create example NPCs (since they're not in the tilemap yet)
        self._create_example_npcs()

        # INTERFACE DO USUÁRIO
        self.ui = UI()
        self.dialogue_box = DialogueBox()
        self.inventory = Inventory(self.player)
        self.inventory_ui = InventoryUI(self.player.inventory)
        self.escape_menu = EscapeMenu()
        self.escape_main_menu = EscapeMainMenu()
        self.death_screen = DeathScreenOp()

        # Dialogue system
        self.dialogue_system = DialogueSystem()
        self._setup_npcs()
        
        # Set player interaction callback
        self.player.set_interaction_callback(self.start_npc_dialogue)

        # Particulas
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        
        # Screen Shake, Hit Stop e Slow Motion
        self.hit_stop_duration = 0
        self.slow_motion_duration = 0
        self.slow_motion_scale = 1.0

    def trigger_hit_stop(self, duration):
        """Para o jogo por alguns frames para dar impacto (Hit Stop)."""
        self.hit_stop_duration = duration
    
    def trigger_slow_motion(self, duration, scale=0.5):
        """Deixa o jogo em câmera lenta."""
        self.slow_motion_duration = duration
        self.slow_motion_scale = scale
    
    def trigger_shake(self, intensity=5, duration=10):
        """Ativa o tremor da câmera."""
        self.visible_sprites.shake(intensity, duration)

    def draw_bg(self,image):
        icon_surface = ResourceManager().load_image(image, convert_alpha=False)
        self.display.blit(icon_surface, [0,0])
    
    def _setup_npcs(self):
        """Setup NPCs with dialogues (example NPCs)."""
        # Load dialogues from external JSON
        self.dialogue_system.load_from_json('gameinfo/data/dialogue.json')
    
    def _create_example_npcs(self):
        """Create example NPCs in the world."""
        # Create Village Elder NPC near spawn
        elder = NPC(
            (2500, 2500),
            [self.visible_sprites, self.npc_sprites],
            self.obstacle_sprites,
            'village_elder'
        )
        
        # Create Merchant NPC
        merchant = NPC(
            (3000, 2500),
            [self.visible_sprites, self.npc_sprites],
            self.obstacle_sprites,
            'merchant'
        )
    
    def start_npc_dialogue(self, npc):
        """Start dialogue with an NPC."""
        if self.dialogue_system.start_dialogue(npc.npc_id, npc):
            self.player.talking = True
    
    def advance_dialogue(self):
        """Advance to next dialogue message."""
        if not self.dialogue_system.advance_dialogue():
            # Dialogue ended
            self.player.talking = False
    
    def check_npc_proximity(self):
        """Check if player is near any NPC."""
        # Don't check while in dialogue or inventory
        if self.state != 'playing':
            return
        
        nearby_npc = None
        for npc in self.npc_sprites:
            if npc.check_player_proximity(self.player.rect.center):
                nearby_npc = npc
                break
        
        if nearby_npc:
            self.player.set_nearby_npc(nearby_npc)
        else:
            self.player.clear_nearby_npc() 

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('gameinfo/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('gameinfo/map/map_Grass.csv'),
            'object': import_csv_layout('gameinfo/map/map_Objects.csv'),
            'entities': import_csv_layout('gameinfo/map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('gameinfo/graphics/Grass'),
            'objects': import_folder('gameinfo/graphics/objects')
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',random_grass_image)

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
									(x,y),
									[self.visible_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic)
                            elif col == '395':
                                # NPC - Village Elder
                                npc = NPC(
                                    (x, y),
                                    [self.visible_sprites, self.npc_sprites],
                                    self.obstacle_sprites,
                                    'village_elder'
                                )
                            elif col == '396':
                                # NPC - Merchant
                                npc = NPC(
                                    (x, y),
                                    [self.visible_sprites, self.npc_sprites],
                                    self.obstacle_sprites,
                                    'merchant'
                                )
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'
                                Enemy(
									monster_name,
									(x,y),
									[self.visible_sprites,self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_coin)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particle(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            if target_sprite.get_damage(self.player,attack_sprite.sprite_type):
                                # EFEITOS DE IMPACTO (Hit Stop + Shake leve) - Só quando acerta de verdade
                                self.trigger_hit_stop(6)
                                self.trigger_shake(2, 5)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            if self.player.health > 0:
                self.player.health -= amount
            else:
                self.player.health = 0
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            
            # EFEITOS DE DANO NO PLAYER (Shake forte + Hit stop)
            self.trigger_shake(8, 12)
            self.trigger_hit_stop(8)
            
			# spawn particles
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
        
        # EFEITO DE MORTE (Slow Motion)
        self.trigger_slow_motion(30, 0.3) # 0.5s (a 60fps) de 30% da velocidade
    
    def add_coin(self,amount):

        self.player.coin += amount

    def run(self, dt=1.0):
        # 1. Draw World (always visible)
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        # 2. Check Game Over
        if self.player.health <= 0:
            self.state = 'game_over'

        # 3. State Machine Dispatch
        if self.state == 'paused':
            # Blocking Menu Call
            still_open = self.escape_main_menu.display_esc(self)
            if not still_open:
                self.state = 'playing'
            return

        if self.state == 'game_over':
            # Blocking Death (Reset handled inside? or stuck?)
            self.death_screen.display_esc()
            return
            
        # 4. Handle Inputs for Non-Blocking States
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Global State Transitions
            if event.type == pygame.KEYDOWN:
                if event.key == InputConfig.get_key('menu'):
                    if self.state == 'playing':
                         self.state = 'paused'
                    elif self.state == 'inventory':
                         self.state = 'playing'
                    elif self.state == 'dialogue':
                         # Optional: Allow escaping dialogue? 
                         pass 

        # 5. Update based on State
        if self.state == 'playing':
            self.update_playing(dt, events)
        elif self.state == 'inventory':
            self.update_inventory(events)
        elif self.state == 'dialogue':
            self.update_dialogue(events)

    def update_playing(self, dt, events):
        
        # 1. Hit Stop Logic (Congela updates mas processa inputs básicos se necessário)
        if self.hit_stop_duration > 0:
            self.hit_stop_duration -= 1
            return # Pula atualização de movimento, animação, etc.

        # 2. Slow Motion Logic
        if self.slow_motion_duration > 0:
            dt *= self.slow_motion_scale
            self.slow_motion_duration -= 1

        # Input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == InputConfig.get_key('inventory'):
                    self.state = 'inventory'
                elif event.key == InputConfig.get_key('interact'):
                    # InteractDebounce check?
                    self.player.try_interact()
        
        # Logic
        self.visible_sprites.update(dt)
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        
        # Dialogue Triggered?
        if self.dialogue_system.is_active():
            self.state = 'dialogue'
            return

        # Interaction Prompt
        self.check_npc_proximity()
        if self.player.nearby_npc:
            npc_screen_pos = self.player.nearby_npc.get_screen_position(
                self.visible_sprites.offset
            )
            self.dialogue_box.draw_interaction_prompt(npc_screen_pos)

    def update_inventory(self, events):
        self.inventory_ui.draw()
        
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == InputConfig.get_key('inventory'):
                    self.state = 'playing'
                else:
                    action = self.inventory_ui.handle_input(keys, event.key)
                    if action == 'use_item':
                        item_data = self.player.inventory.use_selected_item()
                        if item_data:
                            self.player.use_item(item_data)

    def update_dialogue(self, events):
        if not self.dialogue_system.is_active():
            self.state = 'playing'
            return
            
        current_msg = self.dialogue_system.get_current_message()
        if current_msg:
            self.dialogue_box.draw_dialogue(
                current_msg.speaker,
                current_msg.text,
                show_continue=True
            )
        
        keys = pygame.key.get_pressed()
        if keys[InputConfig.get_key('dialogue_advance')]:
             # Simple debounce needed or handled by dialogue system?
             # Previous code had: pygame.time.wait(200)
             pygame.time.wait(200)
             self.advance_dialogue()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        # setup geral
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        # Shake config
        self.shake_amount = 0
        self.shake_duration = 0
    
        # criar chão
        self.floor_surf = pygame.image.load('gameinfo/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def shake(self, intensity=5, duration=10):
        self.shake_amount = intensity
        self.shake_duration = duration

    def custom_draw(self, player):
        
        # ajustar o deslocamento
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Aplicar Screen Shake
        if self.shake_duration > 0:
            self.shake_duration -= 1
            x_offset = randint(-self.shake_amount, self.shake_amount)
            y_offset = randint(-self.shake_amount, self.shake_amount)
            self.offset.x += x_offset
            self.offset.y += y_offset

        # desenhar o chão
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        