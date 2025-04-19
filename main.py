
import pygame
import sys
import constants as c
from Player import Player


pygame.init()



screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("рыбка")


player = Player(50, c.SCREEN_HEIGHT-50)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
            if event.key == pygame.K_x:
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



    all_sprites.update()


    screen.fill(c.BLACK)
    all_sprites.draw(screen)


    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()
