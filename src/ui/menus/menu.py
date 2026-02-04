import pygame, sys
import math
from config.settings import *
from src.core.resource_manager import ResourceManager
from src.core.input_config import InputConfig

import random

class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)
        self.offset = -120
        self.offsetR = -195
        self.music = 4
        self.sfx = 4
        self.menu_enter_sound = 'gameinfo/audio/confirm_ui.wav'
        self.menu_cursor_sound = 'gameinfo/audio/back_ui.wav'
        self.menu_config_sound = 'gameinfo/audio/change_ui.wav'

    def menu_button_sound(self, sound):
        cursor_s = ResourceManager().load_sound(sound)
        cursor_s.set_volume(self.sfx / 10)
        cursor_s.play()

    def draw_cursor(self):
        self.game.draw_icon(self.cursor_rect.x, self.cursor_rect.y, 'gameinfo/graphics/ui/cursor.png')

    def draw_cursorR(self):
        self.game.draw_icon(self.cursor_rectR.x, self.cursor_rectR.y, 'gameinfo/graphics/ui/cursor.png')

    def draw_background(self, bg):
        self.game.draw_bg(bg)

    def draw_text_hover(self, text, size, x, y, color_normal='white', color_hover='yellow'):
        """Draw text that changes color on hover and returns rect and hover state."""
        font = pygame.font.Font(UI_FONT, size)
        
        # Determine if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        temp_surface = font.render(text, True, color_normal)
        rect = temp_surface.get_rect(center=(x, y))
        
        is_hovered = rect.collidepoint(mouse_pos)
        color = color_hover if is_hovered else color_normal
        
        text_surface = font.render(text, True, color)
        self.game.display.blit(text_surface, rect)
        
        return rect, is_hovered

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "Start"
        
        # Menu options configuration
        self.options = [
            {"text": "Começar o jogo", "state": "Start", "y_offset": 50},
            {"text": "Carregar Jogo", "state": "Load", "y_offset": 90},
            {"text": "Opções", "state": "Options", "y_offset": 130},
            {"text": "Créditos", "state": "Credits", "y_offset": 170},
            {"text": "Sair do Jogo", "state": "Quit", "y_offset": 210}
        ]
        
        self.title_sound = ResourceManager().load_sound('gameinfo/audio/Panacea.ogg')
        self.title_sound.set_volume(self.music / 20)
        self.title_sound.play(loops=-1)

    def draw_main_menu_background(self):
        """Draws the main menu generative art background."""
        self.game.display.fill((5, 5, 10)) # Almost black
        
        t = pygame.time.get_ticks() / 1000.0
        
        # Center at top-left corner (0,0) - or slightly offset if desired. 
        # User said "primeiro pixel da tela", so (0,0).
        cx, cy = 0, 0
        
        # --- Kaleidoscope Rings (Larger scale since it's in the corner) ---
        num_rings = 8
        base_radius = 400
        
        for i in range(num_rings):
            radius = base_radius + (i * 150)
            sides = 12 + i
            angle_speed = 5 if i % 2 == 0 else -5
            rotation = (t * angle_speed) % 360
            
            # Draw Rings
            points = []
            for j in range(sides + 1): # +1 to close loop smoothly in calculation
                angle = math.radians(rotation + (360 / sides) * j)
                x = cx + math.cos(angle) * radius
                y = cy + math.sin(angle) * radius
                points.append((x, y))
            
            # Gray/Blueish lines
            color_val = 60 - (i * 5)
            if color_val < 20: color_val = 20
            color = (color_val, color_val, color_val + 10)
            
            pygame.draw.lines(self.game.display, color, False, points, 2)
            
            # Geometric Connections (Rune style)
            if i % 2 == 0:
                for k in range(0, len(points)-1, 2):
                    p1 = points[k]
                    # Connect to center-ish or previous ring
                    start_angle = math.radians(rotation + (360 / sides) * k)
                    inner_r = radius - 100
                    p_inner = (cx + math.cos(start_angle) * inner_r, cy + math.sin(start_angle) * inner_r)
                    pygame.draw.line(self.game.display, (30, 30, 40), p1, p_inner, 1)

        # Generate static random text for rune rings if not already done
        if not hasattr(self, 'rune_texts'):
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
            self.rune_texts = []
            for _ in range(5):
                self.rune_texts.append("".join(random.choices(chars, k=100)))

        # --- Rotating Text Rings ---
        # Multiple layers of text at different speeds and radii
        rings_config = [
            {'radius': 300, 'speed': 15, 'size': 20, 'text_idx': 0, 'color': (80, 80, 100)},
            {'radius': 500, 'speed': -10, 'size': 25, 'text_idx': 1, 'color': (100, 100, 120)},
            {'radius': 700, 'speed': 8, 'size': 15, 'text_idx': 2, 'color': (70, 70, 80)},
            {'radius': 900, 'speed': -5, 'size': 35, 'text_idx': 3, 'color': (50, 50, 60)},
        ]

        for ring in rings_config:
            font = pygame.font.Font(UI_FONT, ring['size'])
            text_content = self.rune_texts[ring['text_idx']] * 3 # Repeat to fill circle
            rotation_speed = ring['speed']
            current_rotation = (t * rotation_speed)
            
            # Angle step depends on font size roughly
            angle_step = ring['size'] * 0.4 
            
            for i, char in enumerate(text_content):
                char_angle_deg = current_rotation + (i * angle_step)
                
                # Check bounds loosely to avoid drawing off-screen too much
                # Optimization: Only draw if angle puts it in visible quadrant (0 to 90 degrees essentially, since center is 0,0)
                # But allow some buffer
                normalized_angle = char_angle_deg % 360
                if not (-20 < normalized_angle < 110):
                    continue

                char_angle_rad = math.radians(char_angle_deg)
                
                x = cx + math.cos(char_angle_rad) * ring['radius']
                y = cy + math.sin(char_angle_rad) * ring['radius']
                
                # Double check screen bounds
                if -50 <= x <= WIDTH+50 and -50 <= y <= HEIGHT+50:
                    char_surf = font.render(char, True, ring['color'])
                    rotation_angle = -char_angle_deg - 90 
                    rotated_surf = pygame.transform.rotate(char_surf, rotation_angle)
                    
                    rect = rotated_surf.get_rect(center=(x, y))
                    self.game.display.blit(rotated_surf, rect)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # self.draw_background('gameinfo/graphics/ui/main_menu.png')
            self.draw_main_menu_background()
            
            mouse_clicked = False
            if pygame.mouse.get_pressed()[0]: # Left click
                mouse_clicked = True

            # Draw options and handle mouse interaction
            for opt in self.options:
                x, y = self.mid_w, self.mid_h + opt["y_offset"]
                rect, hovered = self.draw_text_hover(opt["text"], 35, x, y)
                
                # Update state on hover
                if hovered:
                    if self.state != opt["state"]:
                        self.menu_button_sound(self.menu_cursor_sound)
                        self.state = opt["state"]
                    
                    # Handle click
                    if mouse_clicked:
                        self.game.keys['start'] = True
                        self.check_input() # Re-check input to trigger action

            # Draw cursors based on current state
            # Find current option y position
            current_y = next((self.mid_h + o["y_offset"] for o in self.options if o["state"] == self.state), self.mid_h)
            
            self.cursor_rect.midtop = (self.mid_w + self.offset, current_y)
            self.cursor_rectR.midtop = (self.mid_w - self.offsetR, current_y)
            
            self.game.draw_text("V0.1.2", 20, WIDTH / 2 - 640, HEIGHT / 2 + 360)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def move_cursor(self):
        # Keyboard navigation
        idx = next((i for i, o in enumerate(self.options) if o["state"] == self.state), 0)
        
        if self.game.keys['down']:
            self.menu_button_sound(self.menu_cursor_sound)
            idx = (idx + 1) % len(self.options)
            self.state = self.options[idx]["state"]
            self.game.keys['down'] = False # Consume key
            
        elif self.game.keys['up']:
            self.menu_button_sound(self.menu_cursor_sound)
            idx = (idx - 1) % len(self.options)
            self.state = self.options[idx]["state"]
            self.game.keys['up'] = False # Consume key

    def check_input(self):
        self.move_cursor()
        if self.game.keys['start']:
            self.game.keys['start'] = False # Reset key
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Start':
                self.title_sound.fadeout(2000)
                self.game.playing = True
                self.game.objective = True
                self.run_display = False
            elif self.state == 'Load':
                self.game.curr_menu = self.game.load_menu
                self.run_display = False
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
                self.run_display = False
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
                self.run_display = False
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.quit
                self.run_display = False


class QuitMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "Não"
        self.options = [
            {"text": "Sim", "state": "Sim", "x_offset": -100, "y_offset": 100},
            {"text": "Não", "state": "Não", "x_offset": 100,  "y_offset": 100}
        ]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background('gameinfo/graphics/ui/main_menu.png')
            self.game.draw_text("Deseja sair do jogo?", 35, self.mid_w, self.mid_h)
            
            mouse_clicked = False
            if pygame.mouse.get_pressed()[0]:
                mouse_clicked = True
            
            for opt in self.options:
                x = self.mid_w + opt["x_offset"]
                y = self.mid_h + opt["y_offset"]
                rect, hovered = self.draw_text_hover(opt["text"], 35, x, y)
                
                if hovered:
                    if self.state != opt["state"]:
                        self.menu_button_sound(self.menu_cursor_sound)
                        self.state = opt["state"]
                    if mouse_clicked:
                        self.game.keys['start'] = True
                        self.check_input()

            # Update cursor position
            current_opt = next((o for o in self.options if o["state"] == self.state), self.options[1])
            cx = self.mid_w + current_opt["x_offset"]
            cy = self.mid_h + current_opt["y_offset"]
            
            self.cursor_rect.midtop = (cx + self.offset + 80, cy)
            self.cursor_rectR.midtop = (cx - self.offsetR - 80, cy)
            
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def move_cursor(self):
        if self.game.keys['left'] or self.game.keys['right']:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Não':
                self.state = 'Sim'
            elif self.state == 'Sim':
                self.state = 'Não'
            
            # Reset keys
            self.game.keys['left'] = False
            self.game.keys['right'] = False

    def check_input(self):
        self.move_cursor()
        if self.game.keys['start']:
            self.game.keys['start'] = False
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Sim':
                pygame.quit()
                sys.exit()
            elif self.state == 'Não':
                self.game.curr_menu = self.game.main_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Música'
        
        # Layout config
        self.items = [
            {"label": "Música", "state": "Música", "y_offset": -50},
            {"label": "SFX", "state": "SFX", "y_offset": 50},
            {"label": "Controles", "state": "Controles", "y_offset": 150}
        ]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.keys['back']:
                self.menu_button_sound(self.menu_cursor_sound)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                continue

            self.ast_m = "*" * int(self.music)
            self.ast_s = "*" * int(self.sfx)
            self.check_input()
            
            self.draw_background('gameinfo/graphics/ui/options.png')
            self.game.draw_text("Volume", 45, self.mid_w, self.mid_h - 150)
            
            # Interactive elements
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            for item in self.items:
                y = self.mid_h + item["y_offset"]
                # Draw label
                rect, hovered = self.draw_text_hover(item["label"], 35, self.mid_w, y)
                
                if hovered:
                    if self.state != item["state"]:
                         self.menu_button_sound(self.menu_cursor_sound)
                         self.state = item["state"]
                    if mouse_clicked and self.state == 'Controles':
                        self.game.keys['start'] = True

                # Draw value/extra info if applicable
                if item["state"] == "Música":
                    self.game.draw_text(f"{self.music} {self.ast_m}", 30, self.mid_w, y + 35)
                elif item["state"] == "SFX":
                    self.game.draw_text(f"{self.sfx} {self.ast_s}", 30, self.mid_w, y + 35)

            # Draw cursor
            current_item = next((i for i in self.items if i["state"] == self.state), self.items[0])
            cy = self.mid_h + current_item["y_offset"]
            
            self.cursor_rect.midtop = (self.mid_w + self.offset, cy)
            self.cursor_rectR.midtop = (self.mid_w - self.offsetR, cy)
            
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def move_cursor(self):
        # Keyboard navigation logic simplified
        states = [i["state"] for i in self.items]
        try:
            curr_idx = states.index(self.state)
        except ValueError:
            curr_idx = 0
            
        if self.game.keys['down']:
            self.menu_button_sound(self.menu_cursor_sound)
            self.state = states[(curr_idx + 1) % len(states)]
            self.game.keys['down'] = False
        elif self.game.keys['up']:
            self.menu_button_sound(self.menu_cursor_sound)
            self.state = states[(curr_idx - 1) % len(states)]
            self.game.keys['up'] = False

        # Value adjustment
        elif self.game.keys['left']:
            self.game.keys['left'] = False
            if self.state == 'Música' and self.music > 0:
                self.menu_button_sound(self.menu_config_sound)
                self.music -= 1
            elif self.state == 'SFX' and self.sfx > 0:
                self.menu_button_sound(self.menu_config_sound)
                self.sfx -= 1

        elif self.game.keys['right']:
            self.game.keys['right'] = False
            if self.state == 'Música' and self.music < 10:
                self.menu_button_sound(self.menu_config_sound)
                self.music += 1
            elif self.state == 'SFX' and self.sfx < 10:
                self.menu_button_sound(self.menu_config_sound)
                self.sfx += 1

    def check_input(self):
        self.move_cursor()
        if self.game.keys['start']:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Controles':
                self.game.curr_menu = self.game.controls
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.keys['back']:
                self.menu_button_sound(self.menu_cursor_sound)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                continue
            self.draw_background('gameinfo/graphics/ui/credits.png')
            self.game.draw_text('Victor Hideyuki Tanaka', 35, WIDTH / 2, HEIGHT / 2 - 120)
            self.game.draw_text('Yan Ferreira David', 35, WIDTH / 2, HEIGHT / 2 - 70)
            self.game.draw_text('Matheus Machado Pereira', 35, WIDTH / 2, HEIGHT / 2 - 20)
            self.game.draw_text('Cláudio Colombo', 35, WIDTH / 2, HEIGHT / 2 + 30)
            self.game.draw_text('Amanda Milleo', 35, WIDTH / 2, HEIGHT / 2 + 80)
            self.blit_screen()


class ControlsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.selected_action = None
        self.waiting_for_key = False
        
        # Define display order and labels
        self.bindings = [
            ('move_up', 'Mover Cima'),
            ('move_down', 'Mover Baixo'),
            ('move_left', 'Mover Esquerda'),
            ('move_right', 'Mover Direita'),
            ('attack', 'Atacar'),
            ('magic', 'Magia'),
            ('interact', 'Interagir (NPC)'),
            ('switch_magic', 'Trocar Magia'),
            ('dash', 'Dash'),
            ('inventory', 'Inventario'),
            ('dialogue_advance', 'Avancar Dialogo'),
            # ('menu', 'Menu'), # Avoid rebinding Menu (Escape) to prevent lockouts
        ]

    def draw_generated_background(self):
        """Draws a procedural kaleidoscope/rune background."""
        self.game.display.fill((10, 10, 15)) # Very dark background (almost black)
        
        cx, cy = self.mid_w, self.mid_h
        t = pygame.time.get_ticks() / 1000.0
        
        # Color palette (Greys)
        color = (60, 60, 65)
        
        # 1. Concentric Rotating Rings
        num_rings = 4
        for i in range(num_rings):
            radius = 200 + (i * 120)
            sides = 8 + (i * 2)
            angle_speed = 10 if i % 2 == 0 else -10
            rotation = (t * angle_speed) % 360
            
            points = []
            for j in range(sides):
                angle = math.radians(rotation + (360 / sides) * j)
                x = cx + math.cos(angle) * radius
                y = cy + math.sin(angle) * radius
                points.append((x, y))
            
            # Connect points to form polygon
            pygame.draw.lines(self.game.display, color, True, points, 2)
            
            # Connect vertices to form stars/runes
            if sides >= 6:
                for k in range(len(points)):
                    p1 = points[k]
                    p2 = points[(k + 3) % len(points)] # Skip points to make star
                    pygame.draw.line(self.game.display, (40, 40, 45), p1, p2, 1)

        # 2. Central Pulse Rune
        pulse = (math.sin(t * 2) + 1.5) * 0.5 # 0.25 to 1.25
        center_points = []
        radius_center = 100 * pulse
        for j in range(8):
            angle = math.radians(-t * 30 + (360 / 8) * j)
            x = cx + math.cos(angle) * radius_center
            y = cy + math.sin(angle) * radius_center
            center_points.append((x, y))
            # Draw lines to center
            # pygame.draw.line(self.game.display, (80, 80, 90), (cx, cy), (x, y), 2)
        
        pygame.draw.lines(self.game.display, (80, 80, 90), True, center_points, 3)

    def display_menu(self):
        self.run_display = True
        self.waiting_for_key = False
        self.selected_action = None
        
        while self.run_display:
            if self.waiting_for_key:
                # Special Event Loop for Binding
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game.quit_game()
                    if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                            self.waiting_for_key = False
                            self.selected_action = None
                         else:
                            InputConfig.set_key(self.selected_action, event.key)
                            self.waiting_for_key = False
                            self.selected_action = None
            else:
                self.game.check_events()
            
            # Back Logic (Standard)
            if self.game.keys['back'] and not self.waiting_for_key:
                self.menu_button_sound(self.menu_enter_sound)
                self.game.curr_menu = self.game.options
                self.run_display = False
                InputConfig.save_config() # Save on exit
                continue
            
            # Draw
            # self.draw_background('gameinfo/graphics/ui/keybinds.png')
            self.draw_generated_background()
            
            # Title
            self.game.draw_text("Configuracao de Teclas", 40, self.mid_w, self.mid_h - 250)
            self.game.draw_text("Clique na acao para alterar", 20, self.mid_w, self.mid_h - 210)
            
            # Draw Scrolling List (Simple static list for now)
            spacing = 45
            total_height = len(self.bindings) * spacing
            start_y = self.mid_h - (total_height // 2) + 20
            
            col1_x = self.mid_w - 200
            col2_x = self.mid_w + 200
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]

            for i, (action, label) in enumerate(self.bindings):
                y = start_y + (i * spacing)
                
                # Highlight row background
                row_rect = pygame.Rect(self.mid_w - 300, y - 20, 600, 40)
                if row_rect.collidepoint(mouse_pos) and not self.waiting_for_key:
                    s = pygame.Surface((600, 40), pygame.SRCALPHA)
                    s.fill((255, 255, 255, 30))
                    self.game.display.blit(s, (self.mid_w - 300, y - 20))
                
                # Action Name
                self.game.draw_text(label, 25, col1_x, y)
                
                # Key Button
                key_name = InputConfig.get_key_name(action)
                key_text = f"[{key_name}]"
                if self.waiting_for_key and self.selected_action == action:
                    key_text = "[ Pressione... ]"
                    color = 'red'
                else:
                    color = 'cyan'

                # Draw Key Text
                font = pygame.font.Font(UI_FONT, 25)
                text_surf = font.render(key_text, True, color)
                button_rect = text_surf.get_rect(center=(col2_x, y))
                
                self.game.display.blit(text_surf, button_rect)
                
                # Click logic
                if row_rect.collidepoint(mouse_pos) and mouse_clicked and not self.waiting_for_key:
                    pygame.time.wait(200) # Debounce
                    self.selected_action = action
                    self.waiting_for_key = True

            # Draw Overlay if waiting
            if self.waiting_for_key:
                s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 200))
                self.game.display.blit(s, (0,0))
                
                self.game.draw_text(f"Pressione nova tecla para:", 40, self.mid_w, self.mid_h - 50)
                self.game.draw_text(f"'{next((l for a, l in self.bindings if a == self.selected_action), '?')}'", 50, self.mid_w, self.mid_h + 10)
                self.game.draw_text("(ESC para cancelar)", 30, self.mid_w, self.mid_h + 80)
            
            # Draw Back Button (Manual to ensure it appears)
            if not self.waiting_for_key:
                 back_rect, hovered = self.draw_text_hover("Voltar", 30, 80, HEIGHT - 50) # Moved to left
                 if hovered and mouse_clicked:
                    self.game.keys['back'] = True

            self.blit_screen()


class LoadMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "Slot 1"
        self.slots = []

    def display_menu(self):
        self.run_display = True
        # Refresh slots data
        if hasattr(self.game.level, 'save_system'):
            self.slots = self.game.level.save_system.get_all_slots()
        else:
             self.slots = [{"slot": 1, "empty": True}, {"slot": 2, "empty": True}, {"slot": 3, "empty": True}]
        
        while self.run_display:
            self.game.check_events()
            
            # Back Button
            if self.game.keys['back']:
                self.menu_button_sound(self.menu_cursor_sound)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                continue

            self.check_input() # Keyboard logic

            self.draw_background('gameinfo/graphics/ui/main_menu.png')
            self.game.draw_text("Carregar Jogo", 50, self.mid_w, self.mid_h - 150)
            
            # Draw slots - Styled as rectangles
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            y_start = self.mid_h - 50
            for i, slot_info in enumerate(self.slots):
                y = y_start + (i * 90)
                slot_id = slot_info['slot']
                slot_name = f"Slot {slot_id}"
                
                # Format Text
                if slot_info.get("empty"):
                    display_text = f"{slot_name}: Vazio"
                    color = (100, 100, 100) # Grid color
                else:
                    ts = slot_info.get("timestamp", "").split('.')[0]
                    display_text = f"{slot_name}\n{ts}"
                    color = (200, 200, 200)

                # Draw Rectangle
                rect_width = 400
                rect_height = 80
                rect_x = self.mid_w - rect_width // 2
                rect_y = y - rect_height // 2
                slot_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                
                # Hover logic
                is_hovered = slot_rect.collidepoint(mouse_pos)
                border_color = 'yellow' if is_hovered or self.state == slot_name else 'white'
                bg_color = (50, 50, 50, 180) # Semi-transparent background
                
                # Draw Box
                s = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
                s.fill(bg_color)
                self.game.display.blit(s, (rect_x, rect_y))
                pygame.draw.rect(self.game.display, border_color, slot_rect, 3) # Border

                # Draw Text Inside
                lines = display_text.split('\n')
                for j, line in enumerate(lines):
                    line_y = y - 10 if len(lines) > 1 else y
                    if j > 0: line_y += 25
                    self.game.draw_text(line, 25, self.mid_w, line_y)
                
                if is_hovered:
                    if self.state != slot_name:
                        self.menu_button_sound(self.menu_cursor_sound)
                        self.state = slot_name
                    
                    if mouse_clicked and not slot_info.get("empty"):
                        # Direct action on click
                        self.game.keys['start'] = True
                        self.check_input() # Execute load logic immediately
            
            # Draw Back Text
            back_rect, back_hover = self.draw_text_hover("Voltar", 30, 100, HEIGHT - 50)
            if back_hover and mouse_clicked:
                 self.game.keys['back'] = True

            self.blit_screen()

    def move_cursor(self):
        if self.game.keys['down']:
            self.menu_button_sound(self.menu_cursor_sound)
            try:
                current = int(self.state.split(' ')[1])
                next_slot = (current % 3) + 1
                self.state = f"Slot {next_slot}"
            except:
                self.state = "Slot 1"
            self.game.keys['down'] = False
            
        elif self.game.keys['up']:
            self.menu_button_sound(self.menu_cursor_sound)
            try:
                current = int(self.state.split(' ')[1])
                next_slot = ((current - 2) % 3) + 1
                self.state = f"Slot {next_slot}"
            except:
                self.state = "Slot 1"
            self.game.keys['up'] = False

    def check_input(self):
        self.move_cursor()
        if self.game.keys['start']:
            self.game.keys['start'] = False
            try:
                slot_num = int(self.state.split(' ')[1])
                # Check if slot is empty
                is_empty = next((s.get('empty', False) for s in self.slots if s['slot'] == slot_num), True)
                
                if not is_empty:
                    self.menu_button_sound(self.menu_enter_sound)
                    if hasattr(self.game.level, 'save_system'):
                        if self.game.level.save_system.load_game(self.game.level, slot=slot_num):
                            print(f"Loaded Slot {slot_num}")
                            self.game.main_menu.title_sound.fadeout(2000)
                            self.game.playing = True
                            self.game.objective = False
                            
                            # Critical: Ensure MainMenu knows we are done AND starting game
                            self.run_display = False
                            self.game.main_menu.run_display = False 
                        else:
                            print("Load returned False")
                    else:
                        print("No save system on level")
                else:
                    # Empty slot sound or feedback
                    print("Slot empty")
            except Exception as e:
                print(f"Load Error: {e}")
