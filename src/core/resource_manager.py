"""Resource manager with caching and lazy loading."""
import pygame
from pathlib import Path
from typing import Dict, Optional
from functools import lru_cache


class ResourceManager:
    """Singleton resource manager for loading and caching game assets."""
    
    _instance: Optional['ResourceManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[tuple, pygame.font.Font] = {}
        self._animations: Dict[str, list] = {}
        self._initialized = True
    
    def load_image(self, path: str, convert_alpha: bool = True) -> pygame.Surface:
        """Load and cache an image."""
        if path not in self._images:
            try:
                if convert_alpha:
                    self._images[path] = pygame.image.load(path).convert_alpha()
                else:
                    self._images[path] = pygame.image.load(path).convert()
            except pygame.error as e:
                print(f"Error loading image {path}: {e}")
                # Return a placeholder surface
                self._images[path] = pygame.Surface((64, 64))
                self._images[path].fill((255, 0, 255))
        
        return self._images[path]
    
    def load_sound(self, path: str, volume: float = 1.0) -> pygame.mixer.Sound:
        """Load and cache a sound."""
        if path not in self._sounds:
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(volume)
                self._sounds[path] = sound
            except pygame.error as e:
                print(f"Error loading sound {path}: {e}")
                # Return a dummy sound
                self._sounds[path] = pygame.mixer.Sound(buffer=bytes(100))
        
        return self._sounds[path]
    
    def load_font(self, path: str, size: int) -> pygame.font.Font:
        """Load and cache a font."""
        key = (path, size)
        if key not in self._fonts:
            try:
                self._fonts[key] = pygame.font.Font(path, size)
            except pygame.error as e:
                print(f"Error loading font {path}: {e}")
                self._fonts[key] = pygame.font.Font(None, size)
        
        return self._fonts[key]
    
    def load_animation(self, folder_path: str) -> list:
        """Load and cache animation frames from a folder."""
        if folder_path not in self._animations:
            frames = []
            folder = Path(folder_path)
            
            if not folder.exists():
                print(f"Animation folder not found: {folder_path}")
                return frames
            
            for img_file in sorted(folder.iterdir()):
                if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    frames.append(self.load_image(str(img_file)))
            
            self._animations[folder_path] = frames
        
        return self._animations[folder_path]
    
    def clear_cache(self):
        """Clear all cached resources."""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        self._animations.clear()
    
    def get_cache_size(self) -> Dict[str, int]:
        """Get the number of cached items for each resource type."""
        return {
            'images': len(self._images),
            'sounds': len(self._sounds),
            'fonts': len(self._fonts),
            'animations': len(self._animations)
        }


# Global instance
resource_manager = ResourceManager()
