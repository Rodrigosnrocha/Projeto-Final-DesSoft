from assets import load_assets
import pygame
import random
from file_config import FPS, SCR_WIDTH, SCR_HEIGHT
from objects import Player

def game_screen(window):
    game_clock = pygame.time.Clock()
    assets = load_assets()

    sprite_groups = {}
    sprites = pygame.sprite.Group()
    sprite_groups['sprites'] = sprites

    player = Player(sprite_groups, assets)
    sprites.add(player)

    window.fill((0,0,0))
    window.blit
    sprites.draw(window)
    pygame.display.update()
