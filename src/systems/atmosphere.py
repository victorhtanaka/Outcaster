import pygame
import random
from config.settings import WIDTH, HEIGHT

class PostProcessing:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.width = WIDTH
        self.height = HEIGHT
        
        # --- Vignette Setup ---
        # 1. Start with a dark overlay
        self.vignette_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.vignette_surf.fill((0, 0, 0, 180)) # Dark corners intensity
        
        # 2. Create a mask (White ellipse in center)
        mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        mask.fill((0,0,0,0))
        
        # Draw solid ellipse which represents the "Clear View" area
        # We make it slightly smaller than screen to leave corners dark
        margin_x = 100
        margin_y = 50
        pygame.draw.ellipse(mask, (0, 0, 0, 255), (margin_x, margin_y, WIDTH - 2*margin_x, HEIGHT - 2*margin_y))
        
        # 3. Blur the mask heavily to create the gradient
        # Downscale -> Upscale is a fast way to blur
        scale_factor = 15
        small_mask = pygame.transform.smoothscale(mask, (WIDTH // scale_factor, HEIGHT // scale_factor))
        final_mask = pygame.transform.smoothscale(small_mask, (WIDTH, HEIGHT))
        
        # 4. "Cut" the hole in the vignette using BLEND_RGBA_SUB
        # Use simple subtraction: Current Alpha - Mask Alpha
        self.vignette_surf.blit(final_mask, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

        # --- Tilt Shift Setup ---
        self.blur_amount = 0.15 # 15% of screen top/bottom
        blur_h = int(HEIGHT * self.blur_amount)
        self.top_rect = pygame.Rect(0, 0, WIDTH, blur_h)
        self.bot_rect = pygame.Rect(0, HEIGHT - blur_h, WIDTH, blur_h)

    def draw(self):
        # 1. Tilt Shift (Blur Top/Bot)
        # This gives a miniature/focus effect
        self._blur_area(self.top_rect)
        self._blur_area(self.bot_rect)
        
        # 2. Vignette
        self.display_surface.blit(self.vignette_surf, (0,0))

    def _blur_area(self, rect):
        """Blurs a specific rectangle of the screen."""
        sub = self.display_surface.subsurface(rect)
        # Cheap blur using scaling
        small = pygame.transform.smoothscale(sub, (rect.width // 10, rect.height // 10))
        large = pygame.transform.smoothscale(small, (rect.width, rect.height))
        self.display_surface.blit(large, rect)


class DayNightCycle:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.filter = pygame.Surface((WIDTH, HEIGHT))
        self.filter.fill((16, 20, 60))  # Night Blue
        # Cycles: 0=Day, 1=Dusk, 2=Night, 3=Dawn
        self.cycle_state = 0 
        self.alpha = 0
        self.target_alpha = 0
        self.timer = 0
        self.transition_speed = 0.5
        
        # Cycle durations (frames)
        self.day_duration = 3600    # 60s at 60fps
        self.night_duration = 3600 
        self.transition_duration = 600 # 10s
        
    def update(self):
        self.timer += 1
        
        if self.cycle_state == 0: # Day
            self.target_alpha = 0
            if self.timer > self.day_duration:
                self.cycle_state = 1
                self.timer = 0
                
        elif self.cycle_state == 1: # Dusk
            self.target_alpha = 100 # Darken
            if self.timer > self.transition_duration:
                self.cycle_state = 2
                self.timer = 0
                
        elif self.cycle_state == 2: # Night
            self.target_alpha = 150 # Darkest
            if self.timer > self.night_duration:
                self.cycle_state = 3
                self.timer = 0
                
        elif self.cycle_state == 3: # Dawn
            self.target_alpha = 0
            if self.timer > self.transition_duration:
                self.cycle_state = 0
                self.timer = 0

        # Smooth transition
        if self.alpha < self.target_alpha:
            self.alpha += self.transition_speed
        elif self.alpha > self.target_alpha:
            self.alpha -= self.transition_speed
            
        self.filter.set_alpha(int(self.alpha))

    def draw(self):
        if self.alpha > 0:
            self.display_surface.blit(self.filter, (0, 0)) # Removed MULT flag

class WeatherSystem:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.particles = []
        self.weather_type = "none" # none, rain
        self.timer = 0
        
    def set_weather(self, type):
        self.weather_type = type
        
    def create_particle(self):
        if self.weather_type == "rain":
            pos_x = random.randint(0, WIDTH + 200) # +200 for slant
            pos_y = random.randint(-100, -10)
            self.particles.append([[pos_x, pos_y], [random.randint(-2, -1), random.randint(10, 15)], random.randint(2, 4)]) # [pos, vel, size]

    def update(self):
        if self.weather_type == "rain":
            self.create_particle()
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                
                # Remove if out of screen
                if particle[0][1] > HEIGHT or particle[0][0] < -50:
                    self.particles.remove(particle)

    def draw(self):
        if self.weather_type == "rain":
            for particle in self.particles:
                pygame.draw.line(self.display_surface, (200, 200, 250), particle[0], (particle[0][0] + particle[1][0], particle[0][1] + particle[1][1]), 2)
