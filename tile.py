import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./sprites/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)


class StaticTile(Tile):
    def __init__(self, pos, groups, surface):
        super().__init__(pos, groups)
        self.image = surface
