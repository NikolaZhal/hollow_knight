import pygame
from settings import *
from tile import Tile, StaticTile
from player import Player
from debug import debug
from utils import map_from_csv, import_cut_graphics


class Level:
    def __init__(self):
        # взяли холст дисплея
        self.display_surface = pygame.display.get_surface()
        # создали группы спрайтов
        self.visible_sprites = YSortCameraGroup()
        main_csv_map = map_from_csv(level0["main"])
        self.main_map = self.create_group(main_csv_map, "main")
        self.player = Player((64, 128), [self.visible_sprites], self.main_map)

        # Tile((x, y), [self.visible_sprites, self.obstacles_sprites])

    def create_group(self, map, type):
        group = pygame.sprite.Group()

        for row_index, row in enumerate(map):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x, y = col_index * TILESIZE, row_index * TILESIZE
                    if type == "main":
                        terrain_tiles = import_cut_graphics("./sprites/map/tileSet.png")
                        tile_surface = terrain_tiles[int(val)]
                        sprite = StaticTile((x, y), [self.visible_sprites, group], tile_surface)
        return group

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.offset.x = player.rect.centerx - self.half_width
            self.offset.y = player.rect.centery - self.half_height
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
