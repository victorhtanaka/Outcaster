import pygame, sys
from settings import *
from level import Level
from menu import *
        
class Game:
    def __init__(self):
        
        #setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Jogo')
        self.clock = pygame.time.Clock()

        self.level = Level() 

        #sound
        main_sound = pygame.mixer.Sound('gameinfo/audio/main2.wav')
        title_sound = pygame.mixer.Sound('gameinfo/audio/fallen.wav')
        title_sound.set_volume(0.2)
        main_sound.set_volume(0.4)
        main_sound.play(loops = -1)

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = ('gameinfo/graphics/font/m5x7.ttf')
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            g.run()

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

    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.level.toggle_inventory()

            self.screen.fill(WATER_COLOR)
            self.level.run()        
            pygame.display.update()
            self.clock.tick(FPS)

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

if __name__ == '__main__':
    game = Game()
    game.run()