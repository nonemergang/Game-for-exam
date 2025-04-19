import pygame
import constants as c

# Класс игрока (рыбы)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([32, 32])
        self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.jump_force = -15

    def update(self):
        self.rect.x += self.speed_x

        # Вертикальное движение (гравитация и прыжки)
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Проверка на столкновение с землей (простой пример)
        if self.rect.y >= c.SCREEN_HEIGHT - self.rect.height:
            self.rect.y = c.SCREEN_HEIGHT - self.rect.height
            self.speed_y = 0

    def jump(self):
        # Прыжок (только если на земле)
        if self.rect.y == c.SCREEN_HEIGHT - self.rect.height:
            self.speed_y = self.jump_force

    def attack(self):
        # TODO:  Логика атаки шипами
        print("Рыба атакует!")
