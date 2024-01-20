import os
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


def get_tile_part(orig_surf, new_width, x=0, y=0, width=TILESIZE, height=TILESIZE):
    new_surf = pygame.Surface((new_width, TILESIZE), flags=pygame.SRCALPHA)
    new_surf.blit(
        orig_surf,
        (0, 0),
        pygame.Rect(x, y, width, height),
    )
    return new_surf


def get_speed(height, g_const):
    return int(abs((2 * g_const * height) ** 0.5))


def wizhard_walk():
    tiles = []
    for el in os.listdir("./sprites/WizardWalk"):
        path = "./sprites/WizardWalk/" + el
        surface = pygame.image.load(path).convert_alpha()
        tiles.append(surface)

    return tiles
