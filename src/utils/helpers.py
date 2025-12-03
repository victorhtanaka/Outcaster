"""Utility functions."""
from csv import reader
from pathlib import Path
from typing import List
import pygame


def import_csv_layout(path: str) -> List[List[str]]:
    """Import CSV layout for tilemap."""
    terrain_map = []
    try:
        with open(path) as level_map:
            layout = reader(level_map, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
    except FileNotFoundError:
        print(f"CSV file not found: {path}")
    
    return terrain_map


def import_folder(path: str) -> List[pygame.Surface]:
    """Import all images from a folder."""
    surface_list = []
    folder = Path(path)
    
    if not folder.exists():
        print(f"Folder not found: {path}")
        return surface_list
    
    for img_file in sorted(folder.iterdir()):
        if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            try:
                image_surf = pygame.image.load(str(img_file)).convert_alpha()
                surface_list.append(image_surf)
            except pygame.error as e:
                print(f"Error loading image {img_file}: {e}")
    
    return surface_list
