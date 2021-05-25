from pygame.constants import KEYUP
from assets import BG_TEST, FONT, load_assets
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
    player_bullets = pygame.sprite.Group()
    sprite_groups['player_bullets'] = player_bullets
    enemies = pygame.sprite.Group()
    sprite_groups['enemies'] = enemies

    player = Player(sprite_groups, assets)
    sprites.add(player)
    player_speed = 12
    firing = False

    enemy_count = 0
    enemy_timer = 50
    last_spawn = pygame.time.get_ticks()
    for i in range(4):
        e = Enemy(assets,ENEMY_CONFIG)
        enemies.add(e)
        sprites.add(e)
        enemy_count += 1

    score = 0

    window.fill((0,0,0))
    sprites.draw(window)
    pygame.display.update()

    state = 'GAME'
    while state == 'GAME':
        game_clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = 'QUIT'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.speedy += -player_speed
                if event.key == pygame.K_DOWN:
                    player.speedy += player_speed
                if event.key == pygame.K_RIGHT:
                    player.speedx += player_speed
                if event.key == pygame.K_LEFT:
                    player.speedx += -player_speed
                if event.key == pygame.K_SPACE:
                    firing = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.speedy += player_speed
                if event.key == pygame.K_RIGHT:
                    player.speedx += -player_speed
                if event.key == pygame.K_LEFT:
                    player.speedx += player_speed
                if event.key == pygame.K_DOWN:
                    player.speedy += -player_speed
                if event.key == pygame.K_SPACE:
                    firing = False
        if firing == True:
            player.shoot()

        bullet_hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True, pygame.sprite.collide_mask)
        for i in bullet_hits:
            i.destroy()
            enemy_count -= 1
            score += 500
        
        if player.blink == False:
            player_hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)

        if ((now - last_spawn) % enemy_timer) == 0:
            e = Enemy(assets,ENEMY_CONFIG)
            enemies.add(e)
            sprites.add(e)
            enemy_count += 1
            #enemy_timer += 1000
            last_spawn = now

        sprites.update()
        window.fill((0,0,0))

        score += 0.02
        score_num = assets[FONT].render(f"{score:.0f}", True, (255,255,255))
        score_rect = score_num.get_rect()
        score_rect.topright = (SCR_WIDTH-20,40)
        window.blit(score_num,score_rect)

        score_title = assets[FONT].render("SCORE", True, (255,255,255))
        title_rect = score_title.get_rect()
        title_rect.topright = (SCR_WIDTH-20,20)
        window.blit(score_title,title_rect)

        sprites.draw(window)
        pygame.display.update()
