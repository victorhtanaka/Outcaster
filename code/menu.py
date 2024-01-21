import pygame, sys
from settings import *

class Menu():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)
        self.offset = - 120
        self.offsetR = - 195
        self.music = 4
        self.sfx = 4
        self.menu_enter_sound = 'gameinfo/audio/confirm_ui.wav'
        self.menu_cursor_sound = 'gameinfo/audio/back_ui.wav'
        self.menu_config_sound = 'gameinfo/audio/change_ui.wav'

    def menu_button_sound(self,sound):
        self.cursor_s = pygame.mixer.Sound(sound)
        self.cursor_s.set_volume(self.sfx / 10)
        self.cursor_s.play()

    def draw_cursor(self):
        self.game.draw_icon(self.cursor_rect.x, self.cursor_rect.y,'gameinfo/graphics/ui/cursor.png')

    def draw_cursorR(self):
        self.game.draw_icon(self.cursor_rectR.x, self.cursor_rectR.y,'gameinfo/graphics/ui/cursor.png')
    
    def draw_background(self,bg):
        self.game.draw_bg(bg)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 50
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.sairx, self.sairy = self.mid_w, self.mid_h + 200

        self.title_sound = pygame.mixer.Sound('gameinfo/audio/Menu_Music.wav')
        self.title_sound.set_volume(self.music / 20)
        self.title_sound.play(loops = -1)
        
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background('gameinfo/graphics/ui/main_menu.png')
            self.game.draw_text("Começar o jogo", 35, self.startx, self.starty)
            self.game.draw_text("Opções", 35, self.optionsx, self.optionsy)
            self.game.draw_text("Créditos", 35, self.creditsx, self.creditsy)
            self.game.draw_text("Sair do Jogo", 35, self.sairx, self.sairy)
            self.game.draw_text("V0.1.2", 20, WIDTH / 2 - 640, HEIGHT/ 2 + 360)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy )
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR, self.optionsy )
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR, self.creditsy )
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.sairx + self.offset, self.sairy )
                self.cursor_rectR.midtop = (self.sairx - self.offsetR, self.sairy )
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty )
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty )
                self.state = 'Start'

        elif self.game.UP_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.sairx + self.offset, self.sairy )
                self.cursor_rectR.midtop = (self.sairx - self.offsetR, self.sairy )
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR, self.creditsy )
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy )
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR, self.optionsy )
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty )
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty )
                self.state = 'Start'

        if self.game.LEFT_KEY:
            self.menu_button_sound(self.menu_cursor_sound)
            if self.state == 'Sim':
                self.cursor_rect.midtop = (self.sairx + self.offset, self.sairy )
                self.cursor_rectR.midtop = (self.sairx - self.offsetR, self.sairy )
                self.state = 'Não'
            elif self.state == 'Não':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR, self.creditsy )
                self.state = 'Sim'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Start':
                self.title_sound.fadeout(2000)
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.quit
            self.run_display = False

class QuitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Não"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.optionsx, self.optionsy = self.mid_w - 100, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w + 100, self.mid_h + 100
        
        self.cursor_rect.midtop = (self.creditsx + self.offset + 80, self.creditsy)
        self.cursor_rectR.midtop = (self.creditsx - self.offsetR - 80, self.creditsy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background('gameinfo/graphics/ui/main_menu.png')
            self.game.draw_text("Deseja sair do jogo?", 35, self.startx, self.starty)
            self.game.draw_text("Sim", 35, self.optionsx, self.optionsy)
            self.game.draw_text("Não", 35, self.creditsx, self.creditsy)
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
        if self.game.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Sim':
                pygame.quit()
                sys.exit()
            elif self.state == 'Não':
                self.game.curr_menu = self.game.main_menu
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Música'
        self.volx, self.voly = self.mid_w, self.mid_h - 100
        self.music_volx, self.music_voly = self.mid_w, self.mid_h -50
        self.sfx_volx, self.sfx_voly = self.mid_w, self.mid_h + 50
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 150

        #cursor pos
        self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly)
        self.cursor_rectR.midtop = (self.music_volx - self.offsetR, self.music_voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.menu_button_sound(self.menu_cursor_sound)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.ast_m = "*" * (int(self.music))
            self.ast_s = "*" * (int(self.sfx))
            self.game.check_events()
            self.check_input()
            self.draw_background('gameinfo/graphics/ui/options.png')
            self.game.draw_text("Volume", 45, WIDTH / 2, HEIGHT / 2 - 100)
            self.game.draw_text("Música", 35, self.music_volx, self.music_voly)
            self.game.draw_text(f"{self.music} {self.ast_m}", 30, self.volx, self.voly + 85)
            self.game.draw_text("SFX", 35, self.sfx_volx, self.sfx_voly)
            self.game.draw_text(f"{self.sfx} {self.ast_s}", 30, self.volx, self.voly + 185)
            self.game.draw_text('Controles', 35, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.draw_cursorR() 
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
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
        elif self.game.UP_KEY:
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
        elif self.game.LEFT_KEY:
            if self.state == 'Música':
                if self.music != 0:
                    self.menu_button_sound(self.menu_config_sound)
                    self.music -= 1
            elif self.state == 'SFX':
                if self.sfx != 0:
                    self.menu_button_sound(self.menu_config_sound)
                    self.sfx -= 1
        elif self.game.RIGHT_KEY:
            if self.state == 'Música':
                if self.music != 10:
                    self.menu_button_sound(self.menu_config_sound)
                    self.music += 1
            elif self.state == 'SFX':
                if self.sfx != 10:
                    self.menu_button_sound(self.menu_config_sound)
                    self.sfx += 1
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            if self.state == 'Controles':
                self.game.curr_menu = self.game.controls
            self.run_display = False

            
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.menu_button_sound(self.menu_cursor_sound)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.draw_background('gameinfo/graphics/ui/credits.png')
            self.game.draw_text('Victor Hideyuki Tanaka', 35, WIDTH / 2, HEIGHT / 2 - 120)
            self.game.draw_text('Yan Ferreira David', 35, WIDTH / 2, HEIGHT / 2 - 70)
            self.game.draw_text('Matheus Machado Pereira', 35, WIDTH / 2, HEIGHT / 2 - 20)
            self.game.draw_text('Cláudio Colombo', 35, WIDTH / 2, HEIGHT / 2 + 30)
            self.game.draw_text('Amanda Milleo', 35, WIDTH / 2, HEIGHT / 2 + 80)
            self.blit_screen()


class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.draw_background('gameinfo/graphics/ui/keybinds.png')
            # self.game.draw_text('Créditos', 40, WIDTH / 2, HEIGHT / 2 - 200)
            # self.game.draw_text('Design de Interface:', 40, WIDTH / 2, HEIGHT / 2 - 120)
            # self.game.draw_text('Yan Ferreira', 35, WIDTH / 2, HEIGHT / 2 - 50)
            self.game.check_events()
            if self.game.BACK_KEY:
                self.menu_button_sound(self.menu_enter_sound)
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.blit_screen()