import pygame, sys
from settings import *
from level import Level
from menu import *
from escape_menu import *
from objective_screen import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption('Outcaster')
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.playing = False
        self.objective = True

        self.level = Level() 
        self.objective_screen = ObjectiveScreenOp()
        
        self.keys = {
            'up': False,
            'down': False,
            'start': False,
            'back': False,
            'left': False,
            'right': False,
            'g': False
        }
        
        self.display = pygame.Surface((WIDTH, HEIGHT))
        
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.controls = ControlsMenu(self)
        self.quit = QuitMenu(self)
        self.curr_menu = self.main_menu
        
        self.image_cache = {}

    def load_image(self, path, convert_alpha=True):
        if path not in self.image_cache:
            if convert_alpha:
                self.image_cache[path] = pygame.image.load(path).convert_alpha()
            else:
                self.image_cache[path] = pygame.image.load(path).convert()
        return self.image_cache[path]

    def check_events(self):
        self.keys['g'] = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.keys['start'] = True
                elif event.key == pygame.K_BACKSPACE:
                    self.keys['back'] = True
                elif event.key == pygame.K_DOWN:
                    self.keys['down'] = True
                elif event.key == pygame.K_UP:
                    self.keys['up'] = True
                elif event.key == pygame.K_LEFT:
                    self.keys['left'] = True
                elif event.key == pygame.K_RIGHT:
                    self.keys['right'] = True
                elif event.key == pygame.K_g:
                    self.keys['g'] = True
                elif event.key == pygame.K_ESCAPE:
                    self.level.toggle_menu()

    def reset_keys(self):
        for key in self.keys:
            self.keys[key] = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(UI_FONT, size)
        text_surface = font.render(text, False, 'white')
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)
    
    def draw_icon(self, x, y, image_path):
        icon_surface = self.load_image(image_path, convert_alpha=True)
        icon_rect = icon_surface.get_rect(center=(x, y))
        self.display.blit(icon_surface, icon_rect)
    
    def draw_bg(self, image_path):
        bg_surface = self.load_image(image_path, convert_alpha=False)
        self.display.blit(bg_surface, (0, 0))

    def update(self):
        if self.objective:
            self.objective = self.objective_screen.display_objective()
        else:
            self.level.visible.update()
            self.level.run()

    def render(self):
        self.screen.fill(WATER_COLOR)
        self.screen.blit(self.display, (0, 0))
        pygame.display.update()

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.update()
            self.render()
            self.reset_keys()
            self.clock.tick(FPS)

    def run(self):
        while self.running:
            self.curr_menu.display_menu()
            self.playing = True
            self.game_loop()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
