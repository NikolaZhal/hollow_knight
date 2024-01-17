import pygame
from settings import *
from utils import get_speed


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("sprites/wizard.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.rect.Rect(self.rect.x + 20, self.rect.y + 12, 24, 40)

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
        self.clock = pygame.time.Clock()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.on_ground:
                self.on_ground = False
                self.vertical_speed = -get_speed(3 * 64, self.g_const)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        if keys[pygame.K_E] and not self.is_dashing:
            self.is_dashing = True
            self.dash_start_time = pygame.time.get_ticks()

        # Проверка продолжительности рывка
        if self.is_dashing:
            elapsed_time = pygame.time.get_ticks() - self.dash_start_time
            if elapsed_time < self.dash_duration:
                self.hitbox.x += self.dash_distance * (elapsed_time / self.dash_duration) * self.direction.x
            else:
                self.is_dashing = False

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
        # self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center
        self.collision("vertical")

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

    def update(self):
        self.input()
        self.move()
