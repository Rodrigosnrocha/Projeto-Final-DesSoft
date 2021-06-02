from pygame.constants import KEYUP
from assets import BG_TEST, FONT, load_assets
import pygame
import random
import time
from os import path
from file_config import FPS, SCR_WIDTH, SCR_HEIGHT, QUIT, ENEMY_CONFIG, SND
from objects import Enemy, Player, Cloud


def game_screen(window,save_data):
    game_clock = pygame.time.Clock()
    assets = load_assets()

    sprite_groups = {}
    sprites = pygame.sprite.Group()
    sprite_groups['sprites'] = sprites
    player_bullets = pygame.sprite.Group()
    sprite_groups['player_bullets'] = player_bullets
    enemies = pygame.sprite.Group()
    sprite_groups['enemies'] = enemies
    clouds = pygame.sprite.Group()
    sprite_groups['clouds'] = clouds

    player = Player(sprite_groups, assets, save_data)
    sprites.add(player)
    player_speed = 8
    firing = False

    enemy_count = 0
    base_timer = 6500
    enemy_timer = base_timer
    last_spawn = pygame.time.get_ticks()
    for i in range(3):
        e = Enemy(assets,ENEMY_CONFIG)
        enemies.add(e)
        sprites.add(e)
        enemy_count += 1

    score = 0
    lscore = 0
    coinframe = 0
    coins = save_data['coins']
    heartframe = 0
    lives = 3
    keys_pressed = {}
    extralifei = 0
    difficulty = 6
    cloudtimer = 0
    cloudtimetocreate = 200

    window.fill((125, 190, 198))
    sprites.draw(window)
    pygame.display.update()

    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.25)

    state = 'GAME'
    Running = True
    while Running:
        while state == 'GAME':
            game_clock.tick(FPS)
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'QUIT'
                    Running = False
                if event.type == pygame.KEYDOWN:
                    keys_pressed[event.key] = True
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
                    if event.key in keys_pressed and keys_pressed[event.key]:
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

            cloudtimer += 1
            if cloudtimer >= cloudtimetocreate:
                speed = random.randint(4,5)
                centery = random.randint(30, SCR_HEIGHT-30)
                new_cloud = Cloud(assets, centery, speed)
                clouds.add(new_cloud)
                cloudtimer = 0
                cloudtimetocreate = random.randint(50, 300)

            bullet_hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True, pygame.sprite.collide_mask)
            for i in bullet_hits:
                i.destroy()
                enemy_count -= 1
                coins += 1

            
            if player.blink == False:
                player_hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
                if len(player_hits) > 0:
                    lives -= 1
                    player.blink = True
                    player.blink_timer = 0
            elif player.blink == True:
                player.blink_timer += 1
              

            enemy_timer = base_timer - score * difficulty
            if enemy_timer < 100:
                enemy_timer = 100
                
            if enemy_count <= 40:
                if (now - last_spawn) > enemy_timer:
                    for i in range(3):
                        e = Enemy(assets,ENEMY_CONFIG)
                        enemies.add(e)
                        sprites.add(e)
                        enemy_count += 1
                    last_spawn = now

            clouds.update()
            sprites.update()
            window.fill((125, 190, 198))

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
                extralifei = 1

            if extralifei > 0:
                extralifei += 1
                extralife_title = assets['FONT3'].render('vida extra!', True, (255,50,50))
                title_rect = extralife_title.get_rect()
                title_rect.center = (SCR_WIDTH/2, 60)
                window.blit(extralife_title,title_rect)
                if extralifei > 120:
                    extralifei = 0


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
                keys_pressed = {}
                firing = False
                state = "DEAD"
                player.speedx = 0
                player.speedy = 0
                lives = 0
                enemy_count = 0
                for i in enemies:
                    i.destroy()
                pygame.mixer.music.fadeout(2900)
                if score > save_data['high_score']:
                    save_data['high_score'] = score
                text_surface = assets['FONT4'].render('Perdeu', True, (255, 30, 30))
                text_rect = text_surface.get_rect()
                text_rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)
                window.blit(text_surface, text_rect)
                pygame.display.update()
                time.sleep(3)
                pygame.mixer.music.load(path.join(SND, 'Menumusic.mp3'))
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(loops=-1)

            clouds.draw(window)
            sprites.draw(window)
            pygame.display.update()
        
        while state == "DEAD":
            game_clock.tick(FPS)
            #window.fill((5, 74, 117))
            window.blit(assets['BGLoja'],(0,0))

            coinframe += 1
            canimframe = coinframe//10
            ccoin = assets['coin_anim'][canimframe]
            ccoin_rect = ccoin.get_rect()
            ccoin_rect.midleft = (50, 275)
            window.blit(assets['coin_anim'][canimframe], ccoin_rect)
            if coinframe >= 58:
                coinframe = 0
            coin_title = assets['FONT2'].render('X {}'.format(str(coins)), True, (255,255,255))
            title_rect = coin_title.get_rect()
            title_rect.midleft = (100, 280)
            window.blit(coin_title,title_rect)

            text_surface = assets['FONT2'].render('score: {:.0f}'.format(score), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.midleft = (900, 190)
            window.blit(text_surface, text_rect)

            text_surface = assets['FONT2'].render('high score: {:.0f}'.format(save_data['high_score']), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.midleft = (900, 220)
            window.blit(text_surface, text_rect)

            text_surface = assets['FONT3'].render('Aperte R para jogar', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.bottomright = (SCR_WIDTH-25, SCR_HEIGHT-15)
            window.blit(text_surface, text_rect)

            text_surface = assets['FONT2'].render('1 - VIDA EXTRA [10 moedas]', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (60, 340)
            window.blit(text_surface, text_rect)
            text_surface = assets[FONT].render('adiciona uma vida (vidas: {})'.format(lives+3), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (70, 370)
            window.blit(text_surface, text_rect)

            text_surface = assets['FONT2'].render('2 - FREIO ABS [15 moedas]', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (60, 420)
            window.blit(text_surface, text_rect)
            text_surface = assets[FONT].render('diminui a aceleracao dos inimigos (max quatro compras)', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (70, 450)
            window.blit(text_surface, text_rect)

            text_surface = assets['FONT2'].render('3 - TREINAMENTO DE UZI [6 moedas]', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (60, 500)
            window.blit(text_surface, text_rect)
            text_surface = assets[FONT].render('levemente diminui o tempo para atirar (max sete compras)', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (70, 530)
            window.blit(text_surface, text_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'QUIT'
                    Running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = "GAME"
                        pygame.mixer.music.load(path.join(SND, 'Gamemusic.mp3'))
                        pygame.mixer.music.set_volume(0.03)
                        pygame.mixer.music.play(loops=-1)
                        keys_pressed = {}
                        player.rect.left = 90
                        player.rect.centery = SCR_HEIGHT/2
                        player.speedx = 0
                        player.speedy = 0
                        lives += 3
                        score = 0
                        lscore = 0
                    if event.key == pygame.K_1:
                        if coins >= 10:
                            lives += 1
                            coins -= 10
                    if event.key == pygame.K_2:
                         if coins >= 15 and save_data['difficulty'] > 2:
                             save_data['difficulty'] -= 1
                             coins -= 15
                    if event.key == pygame.K_3:
                         if coins >= 6 and save_data['shoot_speed'] < 7:
                            player.shoot_ticks -=100
                            save_data['shoot_speed'] += 1
                            coins -= 6
    save_data['coins'] = coins
    return save_data