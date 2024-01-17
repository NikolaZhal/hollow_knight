import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./sprites/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)


class StaticTile(Tile):
    def __init__(self, pos, groups, surface, x_offset=0, y_offset=0):
        pos[0] += x_offset
        pos[1] += y_offset
        super().__init__(pos, groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        # self.mask = pygame.mask.from_surface(pygame.Surface((TILESIZE, TILESIZE)))
        # self.vivi = self.rect.copy()
        # self.vivi.y = 0
        # self.vivi.x = 0
        # pygame.draw.rect(self.image, (64, 128, 255), self.vivi, 2)
