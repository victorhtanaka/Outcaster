import pygame
from menu import *

class Music:

    def stop_music():
        pygame.mixer.stop()
        
    def play_game_music(self):
        self.main_sound = pygame.mixer.Sound('gameinfo/audio/main2.wav')
        self.main_sound.set_volume()
        self.main_sound.play(loops = -1)
    
    def play_menu_music(self):
        self.title_sound = pygame.mixer.Sound('gameinfo/audio/fallen.wav')
        self.title_sound.set_volume()
        self.main_sound.play(loops = -1)
    
    def change_music():
        pass
    
    def change_sfx():
        pass
