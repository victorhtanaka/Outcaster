import pygame, sys
from settings import *
from level import Level
 
class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Jogo')
        self.clock = pygame.time.Clock()

        self.level = Level()
 
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()        
            pygame.display.update()
            self.clock.tick(FPS)
#pinto de borracha
if __name__ == '__main__':
    game = Game()
    game.run()