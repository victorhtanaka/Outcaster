import pygame, sys
from config.settings import *
from src.core.resource_manager import ResourceManager

class EscapeMenu():
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.offset = - 120
        self.offsetR = - 195
        self.ver = VER
        if self.ver == 0:
            self.music = 2
            self.sfx = 2
            self.ver += 1
        
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.menu_enter_sound = 'gameinfo/audio/confirm_ui.wav'
        self.menu_cursor_sound = 'gameinfo/audio/back_ui.wav'
        self.menu_config_sound = 'gameinfo/audio/change_ui.wav'
    
    def menu_button_sound(self,sound):
        self.cursor_s = ResourceManager().load_sound(sound)
        self.cursor_s.set_volume(self.sfx / 10)
        self.cursor_s.play()

    def blit_screen(self):
        self.display.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()

    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,size)
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def draw_icon(self,x,y):
        icon_surface = pygame.image.load('gameinfo/graphics/ui/cursor.png')
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)

    def draw_iconR(self,x,y):
        icon_surface = pygame.image.load('gameinfo/graphics/ui/cursor.png')
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)
    
    def draw_cursor(self):
        self.draw_icon(self.cursor_rect.x, self.cursor_rect.y + 2)

    def draw_cursorR(self):
        self.draw_iconR(self.cursor_rectR.x, self.cursor_rectR.y + 2)
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

    def draw_bg(self,image):
        icon_surface = pygame.image.load(image)
        self.display.blit(icon_surface, [0,0])

    def draw_background(self,bg):
        self.draw_bg(bg)

class EscapeMainMenu(EscapeMenu):
    def __init__(self):
        EscapeMenu.__init__(self)
        self.state = "Voltar ao Jogo"
        self.startx, self.starty = self.mid_w, self.mid_h - 70
        self.savex, self.savey = self.mid_w, self.mid_h - 20
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 30
        self.sairx, self.sairy = self.mid_w, self.mid_h + 80

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)

    def display_esc(self, level):
        self.run_display = True
        save_feedback_timer = 0
        
        while self.run_display:
            if save_feedback_timer > 0:
                save_feedback_timer -= 1

            self.check_events()
            self.exit_state = self.check_input(level)
            
            # Handle save feedback signal
            if self.exit_state == 'saved':
                save_feedback_timer = 60
                self.exit_state = None

            self.draw_background('gameinfo/graphics/ui/escape.png')
            self.draw_text("Voltar ao Jogo", 35, self.startx, self.starty)
            
            if save_feedback_timer > 0:
                self.draw_text("Jogo Salvo!", 35, self.savex, self.savey)
            else:
                self.draw_text("Salvar Jogo", 35, self.savex, self.savey)
            
            self.draw_text("Opções", 35, self.optionsx, self.optionsy)
            self.draw_text("Sair", 35, self.sairx, self.sairy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()
            
            if self.exit_state:
                return False
    
    def move_cursor(self):
        if self.DOWN_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Voltar ao Jogo':
                self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
                self.cursor_rectR.midtop = (self.savex - self.offsetR, self.savey)
                self.state = 'Salvar Jogo'
            elif self.state == 'Salvar Jogo':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR, self.optionsy)
                self.state = 'Opcoes'
            elif self.state == 'Opcoes':
                self.cursor_rect.midtop = (self.sairx + self.offset, self.sairy)
                self.cursor_rectR.midtop = (self.sairx - self.offsetR, self.sairy)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)
                self.state = 'Voltar ao Jogo'

        elif self.UP_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Voltar ao Jogo':
                self.cursor_rect.midtop = (self.sairx + self.offset, self.sairy)
                self.cursor_rectR.midtop = (self.sairx - self.offsetR, self.sairy)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR, self.optionsy)
                self.state = 'Opcoes'
            elif self.state == 'Opcoes':
                self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
                self.cursor_rectR.midtop = (self.savex - self.offsetR, self.savey)
                self.state = 'Salvar Jogo'
            elif self.state == 'Salvar Jogo':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)
                self.state = 'Voltar ao Jogo'

    def check_input(self, level):
        self.move_cursor()
        if self.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Voltar ao Jogo':
                return True
            elif self.state == 'Salvar Jogo':
                # Open Save Slot Menu
                save_menu = EscapeSaveMenu(level)
                if save_menu.display_menu():
                    return 'saved'
                self.run_display = True # Ensure loop continues if backed out
                return False 
            elif self.state == 'Opcoes':
                # Assuming EscapeOptionsMenu exists and works
                EscapeOptionsMenu() 
                self.run_display = True
            elif self.state == 'Sair':
                EscapeQuitMenu()
                self.run_display = True
        return False

class EscapeSaveMenu(EscapeMenu):
    def __init__(self, level):
        EscapeMenu.__init__(self)
        self.level = level
        self.state = "Slot 1"
        self.slots = []

    def display_menu(self):
        self.run_display = True
        # Refresh slots
        if hasattr(self.level, 'save_system'):
            self.slots = self.level.save_system.get_all_slots()
        else:
            self.slots = [{"slot": 1, "empty": True}, {"slot": 2, "empty": True}, {"slot": 3, "empty": True}]

        while self.run_display:
            self.check_events()
            
            # Additional Mouse Logic since base check_events doesn't do it
            mouse_clicked = pygame.mouse.get_pressed()[0]
            if self.BACK_KEY: 
                # Also check right click or backspace if needed
                self.run_display = False
                return False

            self.check_input_logic()

            self.draw_background('gameinfo/graphics/ui/escape.png')
            self.draw_text("Salvar Jogo", 50, self.mid_w, self.mid_h - 150)

            # Draw slots - Styled as rectangles
            mouse_pos = pygame.mouse.get_pos()
            pass # Continue below 
            
            y_start = self.mid_h - 50
            for i, slot_info in enumerate(self.slots):
                y = y_start + (i * 90)
                slot_id = slot_info['slot']
                slot_name = f"Slot {slot_id}"
                
                # Format Text
                if slot_info.get("empty"):
                    display_text = f"{slot_name}: Vazio (Salvar)"
                else:
                    ts = slot_info.get("timestamp", "").split('.')[0]
                    display_text = f"{slot_name}\n{ts}"

                # Draw Rectangle
                rect_width = 400
                rect_height = 80
                rect_x = self.mid_w - rect_width // 2
                rect_y = y - rect_height // 2
                slot_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                
                # Hover logic
                is_hovered = slot_rect.collidepoint(mouse_pos)
                border_color = 'yellow' if is_hovered or self.state == slot_name else 'white'
                bg_color = (50, 50, 50, 180)
                
                # Draw Box
                s = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
                s.fill(bg_color)
                self.display.blit(s, (rect_x, rect_y))
                pygame.draw.rect(self.display, border_color, slot_rect, 3) 

                # Draw Text Inside
                lines = display_text.split('\n')
                for j, line in enumerate(lines):
                    line_y = y - 10 if len(lines) > 1 else y
                    if j > 0: line_y += 25
                    self.draw_text_custom(line, 25, self.mid_w, line_y)

                if is_hovered:
                    if self.state != slot_name:
                        self.menu_button_sound(self.menu_cursor_sound)
                        self.state = slot_name
                    
                    if mouse_clicked:
                        self.START_KEY = True
                        self.check_input_logic()
                        if not self.run_display: return True

            # Draw Back Text
            # self.draw_text usually centers, let's use custom one
            back_rect = self.draw_text_custom("Voltar", 30, 100, HEIGHT - 50, return_rect=True)
            if back_rect.collidepoint(mouse_pos):
                 self.draw_text_custom("Voltar", 30, 100, HEIGHT - 50, color='yellow')
                 if mouse_clicked:
                     self.run_display = False
                     return False
            else:
                 pass # Already drawn inside draw_text_custom if I didn't return rect only... API mismatch.
                 
            self.blit_screen()
        return False

    def draw_text_custom(self, text, size, x, y, color='white', return_rect=False):
        font = pygame.font.Font(UI_FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        if return_rect and not color == 'white': # Hacky check if we just want rect
             pass 
        self.display.blit(text_surface, text_rect)
        return text_rect

    def move_cursor(self):
        if self.DOWN_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            try:
                current = int(self.state.split(' ')[1])
                next_slot = (current % 3) + 1
                self.state = f"Slot {next_slot}"
            except:
                self.state = "Slot 1"
            self.DOWN_KEY = False
            
        elif self.UP_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            try:
                current = int(self.state.split(' ')[1])
                next_slot = ((current - 2) % 3) + 1
                self.state = f"Slot {next_slot}"
            except:
                self.state = "Slot 1"
            self.UP_KEY = False

    def check_input_logic(self):
        self.move_cursor()
        if self.START_KEY:
            self.START_KEY = False
            try:
                slot_num = int(self.state.split(' ')[1])
                self.menu_button_sound(self.menu_enter_sound)
                if hasattr(self.level, 'save_system'):
                    self.level.save_system.save_game(self.level, slot=slot_num)
                    self.run_display = False
                    return True
            except Exception as e:
                print(f"Save Error: {e}")
        return False
            

class EscapeQuitMenu(EscapeMenu):
    def __init__(self):
        EscapeMenu.__init__(self)
        self.state = "nao"
        self.startx, self.starty = self.mid_w, self.mid_h - 50
        self.optionsx, self.optionsy = self.mid_w - 100, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w + 100, self.mid_h + 50
        
        self.cursor_rect.midtop = (self.creditsx + self.offset + 80, self.creditsy)
        self.cursor_rectR.midtop = (self.creditsx - self.offsetR - 80, self.creditsy)
        self.display_menu()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_background('gameinfo/graphics/ui/escape.png')
            self.draw_text("Desejar sair do jogo?", 35, self.startx, self.starty)
            self.draw_text("Sim", 35, self.optionsx, self.optionsy)
            self.draw_text("Não", 35, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()
        
    def move_cursor(self):
        if self.LEFT_KEY or self.RIGHT_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'nao':
                self.cursor_rect.midtop = (self.optionsx + self.offset+80, self.optionsy )
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR-80, self.optionsy )
                self.state = 'sim'
            elif self.state == 'sim':
                self.cursor_rect.midtop = (self.creditsx + self.offset+80, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR-80, self.creditsy )
                self.state = 'nao'

    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'sim':
                pygame.quit()
                sys.exit()
            elif self.state == 'nao':
                self.run_display = False


class EscapeOptionsMenu(EscapeMenu):
    def __init__(self):
        self.state = 'musica'
        EscapeMenu.__init__(self)
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        
        self.START_KEY = False
        self.volx, self.voly = self.mid_w, self.mid_h - 100
        self.music_volx, self.music_voly = self.mid_w, self.mid_h -50
        self.sfx_volx, self.sfx_voly = self.mid_w, self.mid_h + 50
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 150
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)

        #cursor pos
        self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly)
        self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly)
        self.display_menu()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.menu_button_sound(self.menu_enter_sound)
            if self.BACK_KEY:
                self.run_display = False
            self.ast_m = "*" * (int(self.music))
            self.ast_s = "*" * (int(self.sfx))
            self.check_events()
            self.check_input_op()
            self.draw_background('gameinfo/graphics/ui/options.png')
            self.draw_text("Volume", 45, WIDTH / 2, HEIGHT / 2 - 100)
            self.draw_text("Música", 35, self.music_volx, self.music_voly)
            self.draw_text(f"{self.music} {self.ast_m}", 30, self.volx, self.voly + 85)
            self.draw_text("SFX", 35, self.sfx_volx, self.sfx_voly)
            self.draw_text(f"{self.sfx} {self.ast_s}", 30, self.volx, self.voly + 185)
            self.draw_text('Controles', 35, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.draw_cursorR() 
            self.blit_screen()
    
    def check_input_op(self):
        self.move_cursor()
        if self.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'musica':
                return True
            elif self.state == 'sfx':
                pass    
            elif self.state == 'controles':
                EscapeControlsMenu()
                self.run_display = True
                      

    def move_cursor(self):
        if self.DOWN_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'musica':
                self.cursor_rect.midtop = (self.sfx_volx + self.offset, self.sfx_voly )
                self.cursor_rectR.midtop = (self.sfx_volx - self.offsetR, self.sfx_voly )
                self.state = 'sfx'
            elif self.state == 'sfx':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy )
                self.cursor_rectR.midtop = (self.controlsx - self.offsetR, self.controlsy )
                self.state = 'controles'
            elif self.state == 'controles':
                self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly )
                self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly )
                self.state = 'musica'
        elif self.UP_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'musica':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy )
                self.cursor_rectR.midtop = (self.controlsx - self.offsetR, self.controlsy )
                self.state = 'controles'
            elif self.state == 'sfx':
                self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly )
                self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly )
                self.state = 'musica'
            elif self.state == 'controles':
                self.cursor_rect.midtop = (self.sfx_volx + self.offset, self.sfx_voly )
                self.cursor_rectR.midtop = (self.sfx_volx - self.offsetR, self.sfx_voly )
                self.state = 'sfx'

        # mudar barra de som
        elif self.LEFT_KEY:
            if self.state == 'musica':
                if self.music != 0:
                    self.menu_button_sound(self.menu_cursor_sound)
                    self.music -= 1
            elif self.state == 'sfx':
                if self.sfx != 0:
                    self.menu_button_sound(self.menu_cursor_sound)
                    self.sfx -= 1
        elif self.RIGHT_KEY:
            if self.state == 'musica':
                if self.music != 10:
                    self.menu_button_sound(self.menu_cursor_sound)
                    self.music += 1
            elif self.state == 'SFX':
                if self.sfx != 10:
                    self.menu_button_sound(self.menu_cursor_sound)
                    self.sfx += 1
    
class EscapeControlsMenu(EscapeMenu):
    def __init__(self):
        EscapeMenu.__init__(self)
        self.display_menu()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.menu_button_sound(self.menu_enter_sound)
            if self.BACK_KEY:
                self.run_display = False
            self.blit_screen()
            self.blit_screen()