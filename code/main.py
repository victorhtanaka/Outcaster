import pygame, sys
from settings import *
from level import Level
from menu import *
from npc import NPC1
from escape_menu import *
     
class Game:
    def __init__(self):
    
        #setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption('Outcaster')
        self.clock = pygame.time.Clock()

        self.level = Level() 
        self.running, self.playing = True, False
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
            player_rect = self.level.player.rect
            self.checking_interaction(player_rect)
            self.execute_dialogue(self)
            self.level.run()

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
                keys = pygame.key.get_pressed()
                if keys[pygame.K_g]:
                    self.G_KEY = True

    def checking_interaction(self,player):
        for npc in self.level.visible_sprites:
            if isinstance(npc, NPC1):
                npc.update()
                if player.colliderect(npc.rect):
                    if self.G_KEY == True:
                        self.execute_dialogue(npc)
                    
    def execute_dialogue(self):
            print("NPC Dialogue: Hello World!")

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

################ DA PRA OTIMIZAR ESSA PARTE #################
    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,size)
        text_surface = font.render(text, False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
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
    
    def menu_logo(self,x,y):
        logo_surface = pygame.image.load('gameinfo/graphics/logo/menu_logo.png')
        logo_rect = logo_surface.get_rect()
        logo_rect.center = (x,y)
        self.display.blit(logo_surface, logo_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.level.toggle_inventory()
                    elif event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()

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