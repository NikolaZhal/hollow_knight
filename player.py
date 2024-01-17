import pygame
from settings import *
from utils import get_speed


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("sprites/wizard.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -26)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        # 9.8 м/с2 * на размер тайла (типо игровой метр) / на fps
        self.g_const = int(1.8 * 64 / 60)
        self.vertical_speed = 0
        self.on_ground = False
        self.is_jumping = False
        self.obstacles_sprites = obstacles_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.on_ground:
                self.on_ground = False
                self.vertical_speed = -get_speed(3 * 64, self.g_const)

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
