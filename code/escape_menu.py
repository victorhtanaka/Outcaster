import pygame, sys
from settings import *

class EscapeMenu():
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.offset = - 105
        self.offsetR = - 185
        self.music = 0.5
        self.sfx = 2
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.menu_enter_sound = 'gameinfo/audio/confirm_ui.wav'
        self.menu_cursor_sound = 'gameinfo/audio/back_ui.wav'
        self.menu_config_sound = 'gameinfo/audio/change_ui.wav'
        self.icon_left = 'gameinfo/graphics/cursor/sword_ico_l.png'
        self.icon_right = 'gameinfo/graphics/cursor/sword_ico_r.png'
    
    def menu_button_sound(self,sound):
        self.cursor_s = pygame.mixer.Sound(sound)
        self.cursor_s.set_volume(self.sfx)
        self.cursor_s.play()

    def draw_cursor(self):
        self.draw_icon(self.cursor_rect.x, self.cursor_rect.y + 2,self.icon_left)

    def draw_cursorR(self):
        self.draw_icon(self.cursor_rectR.x, self.cursor_rectR.y + 2,self.icon_right)

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
    
    def draw_icon(self,x,y,icon):
        icon_surface = pygame.image.load(icon)
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)
    
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

class EscapeMainMenu(EscapeMenu):
    def __init__(self):
        EscapeMenu.__init__(self)
        self.state = "Voltar ao jogo"
        self.startx, self.starty = self.mid_w, self.mid_h -50
        self.optionsx, self.optionsy = self.mid_w, self.mid_h
        self.sairx, self.sairy = self.mid_w, self.mid_h + 50

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)

    def display_esc(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.display.fill('black')
            self.draw_text("Voltar ao Jogo", 35, self.startx, self.starty)
            self.draw_text("Opções", 35, self.optionsx, self.optionsy)
            self.draw_text("Sair", 35, self.sairx, self.sairy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()
    
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
                self.level.menu_open = False
            elif self.state == 'Opcoes':
                EscapeOptionsMenu()
            elif self.state == 'Sair':
                EscapeQuitMenu()
                pygame.quit()
                sys.exit()
            self.run_display = False

class EscapeQuitMenu(EscapeMenu):
    def __init__(self):
        EscapeMenu.__init__(self)
        self.state = "Sim"
        self.startx, self.starty = self.mid_w, self.mid_h - 100
        self.optionsx, self.optionsy = self.mid_w - 100, self.mid_h
        self.creditsx, self.creditsy = self.mid_w + 100, self.mid_h
        
        self.cursor_rect.midtop = (self.optionsx + self.offset + 80, self.optionsy)
        self.cursor_rectR.midtop = (self.optionsx - self.offsetR - 80, self.optionsy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.display.fill('black')
            self.draw_text("Desejar sair do jogo?", 35, self.startx, self.starty)
            self.draw_text("Sim", 35, self.optionsx, self.optionsy)
            self.draw_text("Não", 35, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()
        
    def move_cursor(self):
        if self.game.LEFT_KEY or self.game.RIGHT_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Não':
                self.cursor_rect.midtop = (self.optionsx + self.offset+80, self.optionsy )
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR-80, self.optionsy )
                self.state = 'Sim'
            elif self.state == 'Sim':
                self.cursor_rect.midtop = (self.creditsx + self.offset+80, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR-80, self.creditsy )
                self.state = 'Não'

    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Sim':
                pygame.quit()
                sys.exit()
            elif self.state == 'Não':
                self.curr_menu = self.main_menu
            self.run_display = False

class EscapeOptionsMenu(EscapeMenu):
    def __init__(self):
        self.state = 'Música'
        self.volx, self.voly = self.mid_w, self.mid_h - 100
        self.music_volx, self.music_voly = self.mid_w, self.mid_h -50
        self.sfx_volx, self.sfx_voly = self.mid_w, self.mid_h + 50
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 150
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)

        #cursor pos
        self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly)
        self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.menu_button_sound(self.menu_enter_sound)
                self.curr_menu = self.main_menu
                self.run_display = False
            self.ast_m = "*" * (int(self.music))
            self.ast_s = "*" * (int(self.sfx))
            self.check_events()
            self.check_input()
            self.display.fill('black')
            self.draw_text('Opções', 45, WIDTH / 2, HEIGHT / 2 - 200)
            self.draw_text("Volume", 45, WIDTH / 2, HEIGHT / 2 - 100)
            self.draw_text("Música", 35, self.music_volx, self.music_voly)
            self.draw_text(f"{self.music} {self.ast_m}", 30, self.volx, self.voly + 85)
            self.draw_text("SFX", 35, self.sfx_volx, self.sfx_voly)
            self.draw_text(f"{self.sfx} {self.ast_s}", 30, self.volx, self.voly + 185)
            self.draw_text('Controles', 35, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.draw_cursorR() 
            self.blit_screen()

    def move_cursor(self):
        if self.DOWN_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Música':
                self.cursor_rect.midtop = (self.sfx_volx + self.offset, self.sfx_voly )
                self.cursor_rectR.midtop = (self.sfx_volx - self.offsetR, self.sfx_voly )
                self.state = 'SFX'
            elif self.state == 'SFX':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy )
                self.cursor_rectR.midtop = (self.controlsx - self.offsetR, self.controlsy )
                self.state = 'Controles'
            elif self.state == 'Controles':
                self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly )
                self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly )
                self.state = 'Música'
        elif self.UP_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Música':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy )
                self.cursor_rectR.midtop = (self.controlsx - self.offsetR, self.controlsy )
                self.state = 'Controles'
            elif self.state == 'SFX':
                self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly )
                self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly )
                self.state = 'Música'
            elif self.state == 'Controles':
                self.cursor_rect.midtop = (self.sfx_volx + self.offset, self.sfx_voly )
                self.cursor_rectR.midtop = (self.sfx_volx - self.offsetR, self.sfx_voly )
                self.state = 'SFX'

        # mudar barra de som
        elif self.LEFT_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Música':
                if self.music != 0:
                    self.music -= 1
            elif self.state == 'SFX':
                if self.sfx != 0:
                    self.sfx -= 1
        elif self.RIGHT_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Música':
                if self.music != 10:
                    self.music += 1
            elif self.state == 'SFX':
                if self.sfx != 10:
                    self.sfx += 1
    
class EscapeControlsMenu(EscapeMenu):
    def __init__(self):
        EscapeMenu.__init__(self)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.menu_button_sound(self.menu_enter_sound)
                self.curr_menu = self.main_menu
                self.run_display = False
            self.display.fill('black')
            self.draw_text('Créditos', 40, WIDTH / 2, HEIGHT / 2 - 200)
            self.draw_text('Design de Interface:', 40, WIDTH / 2, HEIGHT / 2 - 120)
            self.draw_text('Yan Ferreira', 35, WIDTH / 2, HEIGHT / 2 - 50)
            self.blit_screen()