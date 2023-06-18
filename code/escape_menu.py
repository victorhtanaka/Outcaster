import pygame, sys
from settings import *

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
        self.cursor_s = pygame.mixer.Sound(sound)
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
        self.startx, self.starty = self.mid_w, self.mid_h -50
        self.optionsx, self.optionsy = self.mid_w, self.mid_h
        self.sairx, self.sairy = self.mid_w, self.mid_h + 50

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)

    def display_esc(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.exit_state = self.check_input()
            self.draw_background('gameinfo/graphics/ui/escape.png')
            self.draw_text("Voltar ao Jogo", 35, self.startx, self.starty)
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
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)
                self.state = 'Voltar ao Jogo'

    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Voltar ao Jogo':
                return True
            elif self.state == 'Opcoes':
                EscapeOptionsMenu()
                
            elif self.state == 'Sair':
                EscapeQuitMenu()
            self.run_display = True

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
            self.draw_background('gameinfo/graphics/ui/keybinds.png')
            self.blit_screen()