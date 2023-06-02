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

    def draw_cursor(self):
        self.game.draw_icon(self.cursor_rect.x, self.cursor_rect.y)

    def draw_cursorR(self):
        self.game.draw_iconR(self.cursor_rectR.x, self.cursor_rectR.y)

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
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h - 100
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        self.cursor_rectR.midtop = (self.volx - self.offsetR, self.voly)
        

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.music = 45
            self.sfx = 86
            self.ast_m = "*" * (self.music // 10)
            self.ast_s = "*" * (self.sfx // 10)
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Música", 15, self.volx, self.voly + 50)
            self.game.draw_text(f"{self.music} {self.ast_m}", 15, self.volx, self.voly + 85)
            self.game.draw_text("SFX", 15, self.volx, self.voly + 150)
            self.game.draw_text(f"{self.sfx} {self.ast_s}", 15, self.volx, self.voly + 185)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.cursor_rectR.midtop = (self.controlsx - self.offsetR, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.cursor_rectR.midtop = (self.volx - self.offsetR, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Créditos', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text('Design de Interface:', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 120)
            self.game.draw_text('Yan Ferreira', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.blit_screen()