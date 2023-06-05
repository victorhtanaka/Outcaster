import pygame, sys
from settings import *

class EscapeMenu:
    def __init__(self):
#####################################################################
        self.state = "Start"
        self.display = pygame.display.get_surface()
        self.offset = - 50
        self.offsetR = - 120
        self.music = 0.5
        self.sfx = 2
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.startx, self.starty = WIDTH / 2, HEIGHT / 2
        self.optionsx, self.optionsy = WIDTH / 2, HEIGHT / 2 + 50
        self.creditsx, self.creditsy = WIDTH / 2, HEIGHT / 2 + 100
        self.sairx, self.sairy = WIDTH / 2, HEIGHT / 2 + 150
        
        self.cursor_rect = pygame.Rect(0, 0, 80, 20)
        self.cursor_rectR = pygame.Rect(0, 0, 80, 20)
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty)

    
    def display_esc(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_text("Começar", 35, self.startx, self.starty)
            self.draw_text("Opções", 35, self.optionsx, self.optionsy)
            self.draw_text("Créditos", 35, self.creditsx, self.creditsy)
            self.draw_text("Sair", 35, self.sairx, self.sairy)
            self.draw_text("0.1.2", 40, WIDTH / 2 - 700, HEIGHT - 160)
            self.draw_cursor()
            self.draw_cursorR()
            self.blit_screen()
            self.esc_background()
    
    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,size)
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def cursor_sound(self):
        self.cursor_s = pygame.mixer.Sound('gameinfo/audio/cursor_sound.wav')
        self.cursor_s.set_volume(self.sfx)
        self.cursor_s.play()
    
    def enter_sound(self):
        self.enter_s = pygame.mixer.Sound('gameinfo/audio/enter_sound.mp3')
        self.enter_s.set_volume(self.sfx)
        self.enter_s.play()
    
    def draw_icon(self,x,y):
        icon_surface = pygame.image.load('gameinfo/graphics/cursor/sword_ico_l.png')
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)

    def draw_iconR(self,x,y):
        icon_surface = pygame.image.load('gameinfo/graphics/cursor/sword_ico_r.png')
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)

    def esc_background(self):
        self.esc_surface = pygame.image.load('gameinfo/graphics/logo/background.png').convert_alpha()
        self.esc_rect = self.esc_surface.get_rect()
        self.display.blit(self.esc_surface, (0,0))
        
    def draw_cursor(self):
        self.draw_icon(self.cursor_rect.x, self.cursor_rect.y + 5)

    def draw_cursorR(self):
        self.draw_iconR(self.cursor_rectR.x, self.cursor_rectR.y + 5)

    def blit_screen(self):
        self.display.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()

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

    def move_cursor(self):
        if self.DOWN_KEY:
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
                self.cursor_rect.midtop = (self.sairx + self.offset, self.sairy )
                self.cursor_rectR.midtop = (self.sairx - self.offsetR, self.sairy )
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty )
                self.cursor_rectR.midtop = (self.startx - self.offsetR, self.starty )
                self.state = 'Start'

        elif self.UP_KEY:
            self.cursor_sound()
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

    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            self.enter_sound()
            if self.state == 'Start':
                self.playing = True
            elif self.state == 'Options':
                self.curr_menu = self.options
            elif self.state == 'Credits':
                self.curr_menu = self.credits
            elif self.state == 'Quit':
                # fazer verificador para perguntar se o jogador deseja mesmo sair do jogo
                pygame.quit()
                sys.exit()
            self.run_display = False