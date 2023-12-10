import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("sprites/kitty.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -26)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.jump_speed = 10
        self.gravity = 1
        self.on_ground = False
        self.is_jumping = False
        self.obstacles_sprites = obstacles_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.on_ground:
                self.is_jumping = True
                self.jump_speed = 10

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

        if not self.is_jumping and not self.on_ground:
            # Возвращаем игрока на землю, если он не прыгает и не находится на земле
            self.hitbox.y += self.gravity
            self.collision("vertical")

        if self.is_jumping:
            self.hitbox.y -= self.jump_speed
            self.jump_speed -= self.gravity

            if self.jump_speed < 0:
                self.is_jumping = False

        self.hitbox.y += self.direction.y * self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center



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
                    if self.direction.y == 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.on_ground = True
                        self.is_jumping = False
                        self.jump_speed = 0
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom


    def update(self):
        self.input()
        self.move()
