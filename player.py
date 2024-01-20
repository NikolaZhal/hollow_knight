import pygame
from settings import *
from utils import get_speed, wizhard_walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.main_image = pygame.image.load("sprites/wizard.png").convert_alpha()
        self.image = self.main_image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.rect.Rect(self.rect.x + 20, self.rect.y + 12, 24, 40)
        self.walk_images = wizhard_walk()

        self.direction = pygame.math.Vector2()
        self.speed = 5
        # 9.8 м/с2 * на размер тайла (типо игровой метр) / на fps
        self.g_const = int(1.8 * 64 / 60)
        self.vertical_speed = 0
        self.on_ground = False
        self.is_jumping = False
        self.obstacles_sprites = obstacles_sprites
        self.dash_distance = 50  # Расстояние рывка
        self.dash_duration = 200  # Продолжительность рывка в миллисекундах
        self.is_dashing = False
        self.dash_start_time = 0
        self.clock = 0
        self.respawn_point = (200, 140)

    def change_image(self):
        self.clock += 0.50
        if self.direction.x != 0:
            self.image = self.walk_images[int(self.clock) % len(self.walk_images)]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.on_ground:
                self.on_ground = False
                self.vertical_speed = -get_speed(3 * 64, self.g_const)

        if keys[pygame.K_e] and not self.is_dashing:
            self.dash_distance = min(50, self.get_nearest_wall())
            self.is_dashing = True
            self.dash_start_time = pygame.time.get_ticks()
        if not self.is_dashing:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
            else:
                self.direction.x = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.vertical_speed += self.g_const

        self.hitbox.y += self.vertical_speed
        self.dash_func()
        # self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center
        self.collision("vertical")

        if self.rect.y > 1100:
            self.reset_position()

    def get_nearest_wall(self):
        lenght = 0
        mask = self.hitbox.copy()
        while (
            not any(
                [sprite.hitbox.colliderect(mask) for sprite in self.obstacles_sprites]
            )
            and lenght <= self.dash_distance
        ):
            lenght += 1
            mask.x += self.direction.x
        return lenght

    def collision(self, direction):
        self.on_ground = False
        if direction == "horizontal":
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        elif direction == "vertical":
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.vertical_speed < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.vertical_speed = 0
                    elif self.vertical_speed > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.vertical_speed = 0
                        self.on_ground = True
                    else:
                        self.vertical_speed += self.g_const

    def dash_func(self):
        # Проверка продолжительности рывка
        if self.is_dashing:
            elapsed_time = pygame.time.get_ticks() - self.dash_start_time
            if elapsed_time < self.dash_duration:
                self.hitbox.x += int(
                    self.dash_distance
                    * (elapsed_time / self.dash_duration)
                    * self.direction.x
                )
            else:
                self.is_dashing = False

    def reset_position(self):
        self.hitbox.x, self.hitbox.y = self.respawn_point

    def update(self):
        self.input()
        self.move()
        self.change_image()
