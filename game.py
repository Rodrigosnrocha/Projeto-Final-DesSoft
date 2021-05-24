from pygame.constants import KEYUP
from assets import BG_TEST, load_assets
import pygame
import random
from file_config import FPS, SCR_WIDTH, SCR_HEIGHT, QUIT, ENEMY_CONFIG
from objects import Enemy, Player

def game_screen(window):
    game_clock = pygame.time.Clock()
    assets = load_assets()

    sprite_groups = {}
    sprites = pygame.sprite.Group()
    sprite_groups['sprites'] = sprites
    enemies = pygame.sprite.Group()
    sprite_groups['enemies'] = enemies

    player = Player(sprite_groups, assets)
    sprites.add(player)

    for i in range(4):
        e = Enemy(assets,ENEMY_CONFIG)
        enemies.add(e)
        sprites.add(e)

    window.fill((0,0,0))
    #window.blit
    sprites.draw(window)
    pygame.display.update()

    state = 'GAME'
    while state == 'GAME':
        game_clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = 'QUIT'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.speedy += -12
                if event.key == pygame.K_DOWN:
                    player.speedy += 12
                if event.key == pygame.K_RIGHT:
                    player.speedx += 12
                if event.key == pygame.K_LEFT:
                    player.speedx += -12
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.speedy += 12
                if event.key == pygame.K_RIGHT:
                    player.speedx += -12
                if event.key == pygame.K_LEFT:
                    player.speedx += 12
                if event.key == pygame.K_DOWN:
                    player.speedy += -12
        sprites.update()
        window.fill((0,0,0))
        sprites.draw(window)
        pygame.display.update()
