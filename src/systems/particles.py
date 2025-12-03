"""Particle system for visual effects."""
import pygame
from src.core.utils import import_folder
from random import choice


class AnimationPlayer:
    """Manages particle animations and effects."""
    
    # Particle types and their paths
    PARTICLE_PATHS = {
        # Magic
        'flame': 'gameinfo/graphics/particles/flame/frames',
        'aura': 'gameinfo/graphics/particles/aura',
        'heal': 'gameinfo/graphics/particles/heal/frames',
        
        # Attacks
        'claw': 'gameinfo/graphics/particles/claw',
        'slash': 'gameinfo/graphics/particles/slash',
        'sparkle': 'gameinfo/graphics/particles/sparkle',
        'leaf_attack': 'gameinfo/graphics/particles/leaf_attack',
        'thunder': 'gameinfo/graphics/particles/thunder',
        
        # Monster deaths
        'squid': 'gameinfo/graphics/particles/smoke_orange',
        'raccoon': 'gameinfo/graphics/particles/raccoon',
        'spirit': 'gameinfo/graphics/particles/nova',
        'bamboo': 'gameinfo/graphics/particles/bamboo',
    }
    
    LEAF_VARIANTS = [
        'gameinfo/graphics/particles/leaf1',
        'gameinfo/graphics/particles/leaf2',
        'gameinfo/graphics/particles/leaf3',
        'gameinfo/graphics/particles/leaf4',
        'gameinfo/graphics/particles/leaf5',
        'gameinfo/graphics/particles/leaf6',
    ]
    
    def __init__(self):
        self.frames = self._load_all_frames()

    def _load_all_frames(self):
        """Load all particle animation frames."""
        frames = {}
        
        # Load standard particles
        for name, path in self.PARTICLE_PATHS.items():
            frames[name] = import_folder(path)
        
        # Load leaf particles with reflections
        frames['leaf'] = self._load_leaf_particles()
        
        return frames

    def _load_leaf_particles(self):
        """Load leaf particles including mirrored versions."""
        leaf_frames = []
        
        for path in self.LEAF_VARIANTS:
            frames = import_folder(path)
            leaf_frames.append(frames)
            leaf_frames.append(self._reflect_images(frames))
        
        return tuple(leaf_frames)

    def _reflect_images(self, frames):
        """Create horizontally flipped versions of frames."""
        return [pygame.transform.flip(frame, True, False) for frame in frames]
    
    def reflect_images(self, frames):
        """Legacy method for backward compatibility."""
        return self._reflect_images(frames)
    
    def create_grass_particle(self, pos, groups):
        """Create a random grass/leaf particle effect."""
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)
    
    def create_particles(self, animation_type, pos, groups):
        """Create a particle effect of specified type."""
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    """Individual particle effect sprite."""
    
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """Advance animation frame."""
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        """Update particle state."""
        self.animate()