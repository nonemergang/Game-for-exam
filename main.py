<<<<<<< HEAD
import pygame
import sys
import const as c
from Player import Player


pygame.init()



# Настройка экрана
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("рыбка")


# Создание игрока
player = Player(50, c.SCREEN_HEIGHT - 50)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_x: #или другая кнопка для атаки
                player.attack()
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            if event.key == pygame.K_RIGHT:
                player.speed_x = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.speed_x = 0
            if event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.speed_x = 0


    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill(c.BLACK)
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()

    # Контроль FPS
    clock.tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()
=======
import pygame
import sys
import const as c
pygame.init()



# Настройка экрана
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("рыбка")

# Класс игрока (рыбы)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([32, 32])  # Заменить спрайтом рыбы
        self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.jump_force = -15

    def update(self):
        # Горизонтальное движение
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


# Создание игрока
player = Player(50, c.SCREEN_HEIGHT - 50)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_x: #или другая кнопка для атаки
                player.attack()
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            if event.key == pygame.K_RIGHT:
                player.speed_x = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.speed_x = 0
            if event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.speed_x = 0


    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill(c.BLACK)
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()

    # Контроль FPS
    clock.tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()
>>>>>>> fd5d583e9897478aafaf835b4407b60f00dbfc2b
