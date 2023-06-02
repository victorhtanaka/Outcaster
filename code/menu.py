import pygame
from settings import *

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)
        self.offset = - 100
        self.offsetR = - 175

        self.music = 5
        self.sfx = 10

        self.title_sound = pygame.mixer.Sound('gameinfo/audio/fallen.wav')
        self.title_sound.set_volume(self.music // 10)
        self.title_sound.play(loops = -1)

    def cursor_sound(self):
        self.cursor_s = pygame.mixer.Sound('gameinfo/audio/cursor_sound.wav')
        self.cursor_s.set_volume(self.sfx)
        self.cursor_s.play()
    
    def enter_sound(self):
        self.enter_s = pygame.mixer.Sound('gameinfo/audio/enter_sound.mp3')
        self.enter_s.set_volume(self.sfx)
        self.enter_s.play()
        
    def draw_cursor(self):
        self.game.draw_icon(self.cursor_rect.x, self.cursor_rect.y + 5)

    def draw_cursorR(self):
        self.game.draw_iconR(self.cursor_rectR.x, self.cursor_rectR.y + 5)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h 
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 100
        
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.cursor_sound()
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy )
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR, self.optionsy )
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR, self.creditsy )
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty )
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty )
                self.state = 'Start'
        elif self.game.UP_KEY:
            self.cursor_sound()
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy )
                self.cursor_rectR.midtop = (self.creditsx - self.offsetR, self.creditsy )
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty )
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty )
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy )
                self.cursor_rectR.midtop = (self.optionsx - self.offsetR, self.optionsy )
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.enter_sound()
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
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
            if self.game.START_KEY or self.game.BACK_KEY:
                self.enter_sound()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.ast_m = "*" * (self.music)
            self.ast_s = "*" * (self.sfx)
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Opções', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Volume", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Música", 15, self.music_volx, self.music_voly)
            self.game.draw_text(f"{self.music} {self.ast_m}", 15, self.volx, self.voly + 85)
            self.game.draw_text("SFX", 15, self.sfx_volx, self.sfx_voly)
            self.game.draw_text(f"{self.sfx} {self.ast_s}", 15, self.volx, self.voly + 185)
            self.game.draw_text("Controles", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def check_input(self):
        if self.game.DOWN_KEY:
            self.cursor_sound()
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
            self.cursor_sound()
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
            self.cursor_sound()
            if self.state == 'Música':
                if self.music != 0:
                    self.music -= 1
            elif self.state == 'SFX':
                if self.sfx != 0:
                    self.sfx -= 1
        elif self.game.RIGHT_KEY:
            self.cursor_sound()
            if self.state == 'Música':
                if self.music != 10:
                    self.music += 1
            elif self.state == 'SFX':
                if self.sfx != 10:
                    self.sfx += 1
            
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.enter_sound()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Créditos', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text('Design de Interface:', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 120)
            self.game.draw_text('Yan Ferreira', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.blit_screen()