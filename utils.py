from csv import reader
import pygame
from settings import TILESIZE


def map_from_csv(path):
    with open(path) as file:
        data = list(reader(file, delimiter=","))
    return data


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    iter_x = int(surface.get_size()[0] / TILESIZE)
    iter_y = int(surface.get_size()[1] / TILESIZE)
    tiles = []
    for row in range(iter_y):
        for col in range(iter_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surf = pygame.Surface((TILESIZE, TILESIZE), flags=pygame.SRCALPHA)
            # new_surf.fill("grey")?
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            tiles.append(new_surf)

    return tiles


def get_speed(height, g_const):
    return int(abs((2 * g_const * height) ** 0.5))
