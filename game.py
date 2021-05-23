from assets import BG_TEST, load_assets
import pygame
import random
from file_config import FPS, SCR_WIDTH, SCR_HEIGHT, QUIT
from objects import Player

def game_screen(window):
    game_clock = pygame.time.Clock()
    assets = load_assets()

    sprite_groups = {}
    sprites = pygame.sprite.Group()
    sprite_groups['sprites'] = sprites
    enemy_bullets = pygame.sprite.Group()
    sprite_groups['player_bullets'] = enemy_bullets

    player = Player(sprite_groups, assets)
    sprites.add(player)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.speedy = -12
                if event.key == pygame.K_DOWN:
                    player.speedy = 12
                if event.key == pygame.K_SPACE:
                    player.shoot()
            """elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.speedy += 12
                if event.key == pygame.K_DOWN:
                    player.speedy -= 12"""
        sprites.update()
        window.fill((0,0,0))
        sprites.draw(window)
        pygame.display.update()
