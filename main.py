"""Main game entry point."""
import pygame
import sys

from config.settings import WIDTH, HEIGHT, FPS, UI_FONT
from src.core.level import Level
from src.core.input_config import InputConfig
from src.ui.menus.menu import MainMenu, OptionsMenu, CreditsMenu, ControlsMenu, QuitMenu, LoadMenu
from src.ui.screens.objective_screen import ObjectiveScreenOp


class Game:
    """Main game class managing game loop and state."""
    
    def __init__(self):
        # Pre-initialize mixer with small buffer to reduce latency
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        
        # Load Input Config
        InputConfig.load_config()
        
        self._init_display()
        self._init_game_state()
        self._init_menus()
        self.image_cache = {}

    def _init_display(self):
        """Initialize display and clock."""
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption('Outcaster')
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((WIDTH, HEIGHT))

    def _init_game_state(self):
        """Initialize game state variables."""
        self.running = True
        self.playing = False
        self.objective = True
        
        self.level = Level()
        self.objective_screen = ObjectiveScreenOp()
        
        self.keys = {
            'up': False, 'down': False, 'left': False, 'right': False,
            'start': False, 'back': False, 'g': False
        }

    def _init_menus(self):
        """Initialize all menu screens."""
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.controls = ControlsMenu(self)
        self.quit = QuitMenu(self)
        self.load_menu = LoadMenu(self)
        self.curr_menu = self.main_menu

    def load_image(self, path, convert_alpha=True):
        """Load and cache image to avoid redundant loading."""
        if path not in self.image_cache:
            image = pygame.image.load(path)
            self.image_cache[path] = image.convert_alpha() if convert_alpha else image.convert()
        return self.image_cache[path]

    def check_events(self):
        """Process input events."""
        self.keys['g'] = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
                
    def check_events_menu_only(self):
        """Process input events for menu (doesn't consume events)."""
        self.keys['g'] = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key):
        """Handle keyboard input."""
        # Configurable binds (Gameplay keys also work for menu navigation)
        if key == InputConfig.get_key('move_up'): self.keys['up'] = True
        if key == InputConfig.get_key('move_down'): self.keys['down'] = True
        if key == InputConfig.get_key('move_left'): self.keys['left'] = True
        if key == InputConfig.get_key('move_right'): self.keys['right'] = True
        if key == InputConfig.get_key('dialogue_advance'): self.keys['start'] = True
        if key == InputConfig.get_key('journal'): self.keys['g'] = True
        
        # Hardcoded Standard Menu Keys (Always working for UI)
        if key == pygame.K_UP: self.keys['up'] = True
        if key == pygame.K_DOWN: self.keys['down'] = True
        if key == pygame.K_LEFT: self.keys['left'] = True
        if key == pygame.K_RIGHT: self.keys['right'] = True
        if key == pygame.K_RETURN: self.keys['start'] = True
        if key == pygame.K_BACKSPACE: self.keys['back'] = True
        
        if key == pygame.K_ESCAPE:
            self.keys['back'] = True

    def reset_keys(self):
        """Reset all key states."""
        for key in self.keys:
            self.keys[key] = False

    def draw_text(self, text, size, x, y):
        """Draw text on display surface."""
        font = pygame.font.Font(UI_FONT, size)
        text_surface = font.render(text, False, 'white')
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)
    
    def draw_icon(self, x, y, image_path):
        """Draw icon centered at position."""
        icon_surface = self.load_image(image_path, convert_alpha=True)
        icon_rect = icon_surface.get_rect(center=(x, y))
        self.display.blit(icon_surface, icon_rect)
    
    def draw_bg(self, image_path):
        """Draw background image."""
        bg_surface = self.load_image(image_path, convert_alpha=False)
        self.display.blit(bg_surface, (0, 0))

    def update(self, dt):
        """Update game state."""
        if self.objective:
            self.objective = self.objective_screen.display_objective()
        else:
            self.level.run(dt)

    def render(self):
        """Render game graphics."""
        if not self.objective:
            # Level renders directly to screen
            pass
        else:
            # Menu and objective use display surface
            self.screen.blit(self.display, (0, 0))
        pygame.display.update()

    def game_loop(self):
        """Main game loop."""
        while self.playing:
            # Don't consume events in main loop - let Level handle them
            pass
            # for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        self.quit_game()
            
            # Calculate delta time in seconds
            dt = self.clock.tick(FPS) / 1000.0
            
            self.update(dt)
            self.render()

    def run(self):
        """Main application loop."""
        while self.running:
            self.curr_menu.display_menu()
            
            if self.playing:
                self.game_loop()
                # Reset to main menu after game ends
                self.curr_menu = self.main_menu
                self.playing = False

    def quit_game(self):
        """Clean up and exit game."""
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
