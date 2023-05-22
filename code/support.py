from csv import reader
import os
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    surface_list = []
    for file_name in os.listdir(path):
        full_path = os.path.join(path, file_name)
        if os.path.isfile(full_path):
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list