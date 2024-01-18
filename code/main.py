import pygame, sys
from settings import *
from level import Level
from menu import *
from escape_menu import *
from objective_screen import *
     
class Game:
    def __init__(self):
        #setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption('Outcaster')
        self.clock = pygame.time.Clock()

        self.level = Level() 
        self.objective_screen = ObjectiveScreenOp()
        self.running, self.playing, self.objective = True, False, True
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.display = pygame.Surface((WIDTH,HEIGHT))
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.controls = ControlsMenu(self)
        self.quit = QuitMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            g.run()
            self.check_events()
            self.level.visible.update()
            self.level.run()

    def check_events(self):
        self.G_KEY = False
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
                if event.key == pygame.K_g:
                    self.G_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,size)
        text_surface = font.render(text, False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def draw_icon(self,x,y,image):
        icon_surface = pygame.image.load(image).convert_alpha()
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)
    
    def draw_bg(self,image):
        icon_surface = pygame.image.load(image)
        self.display.blit(icon_surface, [0,0])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            if self.objective:
                self.objective = self.objective_screen.display_esc()
            else:
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