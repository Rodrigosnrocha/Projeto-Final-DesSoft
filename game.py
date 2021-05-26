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
    player_speed = 9
    firing = False

    enemy_count = 0
    enemy_timer = 8000
    last_spawn = pygame.time.get_ticks()
    for i in range(3):
        e = Enemy(assets,ENEMY_CONFIG)
        enemies.add(e)
        sprites.add(e)
        enemy_count += 1

    score = 0
    lscore = 0
    coins = 0
    coinframe = 0
    heartframe = 0
    lives = 3

    window.fill((65, 65, 65))
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
            coins += 1
        
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
        if len(hits) > 0:
            lives -= 1
        
        if player.blink == False:
            player_hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)

        if (now - last_spawn) > enemy_timer:
            e = Enemy(assets,ENEMY_CONFIG)
            enemies.add(e)
            sprites.add(e)
            enemy_count += 1
            last_spawn = now

        sprites.update()
        window.fill((65, 65, 65))

        score += 0.2
        lscore += 0.2
        score_num = assets[FONT].render(f"{score:.0f}", True, (255,255,255))
        score_rect = score_num.get_rect()
        score_rect.topright = (SCR_WIDTH-20,40)
        window.blit(score_num,score_rect)

        coinframe += 1
        canimframe = coinframe//10
        ccoin = assets['coin_anim'][canimframe]
        coin_rect = ccoin.get_rect()
        coin_rect.topleft = (10, 10)
        window.blit(assets['coin_anim'][canimframe], (10, 10))
        if coinframe >= 58:
            coinframe = 0

        coin_title = assets[FONT].render('X {}'.format(str(coins)), True, (255,255,255))
        title_rect = coin_title.get_rect()
        title_rect.topleft = (55, 18)
        window.blit(coin_title,title_rect)

        if lscore > 500:
            lives += 1
            lscore = 0

        heartframe += 1
        hanimframe = heartframe//10
        cheart = assets['heart_anim'][hanimframe]
        heart_rect = cheart.get_rect()
        heart_rect.midtop = (180, 18)
        window.blit(assets['heart_anim'][hanimframe], heart_rect)
        if heartframe >= 39:
            heartframe = 0
        
        score_title = assets[FONT].render("SCORE", True, (255,255,255))
        title_rect = score_title.get_rect()
        title_rect.topright = (SCR_WIDTH-20,20)
        window.blit(score_title,title_rect)

        text_surface = assets[FONT].render('X {}'.format(lives), True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (215, 18)
        window.blit(text_surface, text_rect)

        if lives <= 0:
            state = "DEAD"

        sprites.draw(window)
        pygame.display.update()
