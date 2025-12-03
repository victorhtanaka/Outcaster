import pygame
from config.settings import *
from src.entities.tile import Tile
from src.entities.player import Player
from src.entities.npc import NPC
from src.core.utils import *
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

class Level():
    def __init__(self):

        self.display = pygame.display.get_surface()

        # npc
        self.visible = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()

        # superfície de exibição
        self.display_surface = pygame.display.get_surface()

        # Inventario e Menu Pause
        self.inventory_open = False
        self.menu_open = False

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
        

    def draw_bg(self,image):
        icon_surface = pygame.image.load(image)
        self.display.blit(icon_surface, [0,0])
    
    def _setup_npcs(self):
        """Setup NPCs with dialogues (example NPCs)."""
        # Example: Create an NPC at position
        # You can add NPCs in create_map instead if using tilemap
        
        # Register dialogues for NPCs
        self.dialogue_system.register_dialogue(
            'village_elder',
            [
                "Bem-vindo, viajante!",
                "Esta terra foi assolada por criaturas das trevas.",
                "Você deve ser corajoso para estar aqui.",
                "Cuidado ao explorar as florestas ao norte."
            ],
            "Ancião da Vila"
        )
        
        self.dialogue_system.register_dialogue(
            'merchant',
            [
                "Olá! Procurando itens raros?",
                "Tenho as melhores poções da região!",
                "Volte quando tiver mais moedas."
            ],
            "Mercador"
        )
    
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
        if self.dialogue_system.is_active() or self.inventory_open:
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
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            if self.player.health > 0:
                self.player.health -= amount
            else:
                self.player.health = 0
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
			# spawn particles
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
    
    def add_coin(self,amount):

        self.player.coin += amount

    def toggle_inventory(self):

        self.inventory_open = not self.inventory_open

    def toggle_menu(self):

        self.menu_open = not self.menu_open

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        # Get events and keys
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        
        # Track key presses this frame
        key_i_pressed = False
        key_esc_pressed = False
        other_events = []
        
        # Process events once
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    key_i_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    key_esc_pressed = True
                else:
                    other_events.append(event)
            else:
                other_events.append(event)
        
        # PRIORITY 1: Handle ESC (highest priority)
        if key_esc_pressed:
            if self.inventory_open:
                self.inventory_open = False
            elif not self.menu_open:
                self.menu_open = True
        
        # PRIORITY 2: Handle I key (toggle inventory)
        elif key_i_pressed and not self.menu_open and not self.dialogue_system.is_active():
            self.inventory_open = not self.inventory_open
        
        # PRIORITY 3: Handle active menus
        if self.menu_open:
            self.menu_open = self.escape_main_menu.display_esc()
        elif self.player.health == 0:
            self.death_screen.display_esc()
        elif self.inventory_open:
            # Draw inventory UI
            self.inventory_ui.draw()
            
            # Handle inventory input
            for event in other_events:
                if event.type == pygame.KEYDOWN:
                    action = self.inventory_ui.handle_input(keys, event.key)
                    if action == 'use_item':
                        # Use selected item
                        item_data = self.player.inventory.use_selected_item()
                        if item_data:
                            self.player.use_item(item_data)
        
        # PRIORITY 4: Handle dialogue (if no other menu open)
        elif self.dialogue_system.is_active():
            # Show dialogue
            current_msg = self.dialogue_system.get_current_message()
            if current_msg:
                self.dialogue_box.draw_dialogue(
                    current_msg.speaker,
                    current_msg.text,
                    show_continue=True
                )
            
            # Advance dialogue with SPACE
            if keys[pygame.K_SPACE]:
                pygame.time.wait(200)  # Debounce
                self.advance_dialogue()
        
        # PRIORITY 5: Normal gameplay
        else:
            # Check NPC proximity and show interaction prompt (only if inventory closed)
            if not self.inventory_open:
                self.check_npc_proximity()
                
                if self.player.nearby_npc:
                    npc_screen_pos = self.player.nearby_npc.get_screen_position(
                        self.visible_sprites.offset
                    )
                    self.dialogue_box.draw_interaction_prompt(npc_screen_pos)
                    
                    # Try to interact with E key
                    if keys[pygame.K_e]:
                        pygame.time.wait(200)  # Debounce
                        self.player.try_interact()
        
        # Only update game if not in any menu or dialogue
        if not self.dialogue_system.is_active() and not self.inventory_open and not self.menu_open and self.player.health > 0:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        # setup geral
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
        # criar chão
        self.floor_surf = pygame.image.load('gameinfo/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        
        # ajustar o deslocamento
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

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
        