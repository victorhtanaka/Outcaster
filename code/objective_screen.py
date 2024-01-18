import pygame, sys
from settings import *
from time import sleep

class ObjectiveScreen():
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
        
        self.ver_music = 0
    
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

class ObjectiveScreenOp(ObjectiveScreen):
    def __init__(self):
        ObjectiveScreen.__init__(self)
        self.startx, self.starty = self.mid_w, self.mid_h - 80
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80


    def display_esc(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.run_display = self.check_input()
            self.draw_background('gameinfo/graphics/ui/escape.png')
            self.draw_text("Objetivo", 70, self.startx, self.starty)
            self.draw_text("Mate todos os inimigos", 50, self.optionsx, self.optionsy)
            # Música
            if self.ver_music == 0:
                self.sound = 'gameinfo/audio/main2.wav'
                self.game_music = pygame.mixer.Sound(self.sound)
                self.game_music.set_volume(0.4)
                self.game_music.play(loops = -1)
                self.ver_music += 1
            self.blit_screen()
            sleep(4)

    def check_input(self):
        if self.START_KEY:
            self.menu_button_sound(self.menu_enter_sound)
            return True