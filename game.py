# Importa todos os objetos necessários
from assets import FONT, load_assets
import pygame
import random
import time
from os import path
from file_config import FPS, SCR_WIDTH, SCR_HEIGHT, ENEMY_CONFIG, SND
from objects import Enemy, Player, Cloud


def game_screen(window,save_data):
    game_clock = pygame.time.Clock()

    assets = load_assets() # Carrega todos os assets

    # Criamos um dicionário com todos os sprite groups
    sprite_groups = {}
    # Grupo com todos os sprites
    sprites = pygame.sprite.Group()
    sprite_groups['sprites'] = sprites
    # Grupo com as balas atiradas pelo jogador
    player_bullets = pygame.sprite.Group()
    sprite_groups['player_bullets'] = player_bullets
    # Grupo com todos os inimigos
    enemies = pygame.sprite.Group()
    sprite_groups['enemies'] = enemies
    # Grupo com as nuvens
    clouds = pygame.sprite.Group()
    sprite_groups['clouds'] = clouds

    # Criamos o jogador
    player = Player(sprite_groups, assets, save_data)
    sprites.add(player)
    player_speed = 8
    firing = False

    # Criamos os inimigos e definimos suas variáveis
    enemy_count = 0
    base_timer = 6500
    enemy_timer = base_timer
    last_spawn = pygame.time.get_ticks()
    for i in range(3):
        e = Enemy(assets,ENEMY_CONFIG)
        enemies.add(e)
        sprites.add(e)
        enemy_count += 1

    # Variáveis do jogo
    score = 0 # Distância percorrida
    lscore = 0 # Igual ao score, mas volta a 0 quando ganha uma vida extra
    coinframe = 0 # Frame de animação do contador de moedas
    coins = save_data['coins']
    heartframe = 0 # Frame de animação do contador de vidas
    lives = 3
    keys_pressed = {} # Quais teclas já foram pressionadas
    extralifei = 0
    difficulty = 6
    cloudtimer = 0 # Timer de geração de nuvens
    cloudtimetocreate = 200

    # Prepara a tela
    window.fill((125, 190, 215))
    sprites.draw(window)
    pygame.display.update()

    # Inicia a musica
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.25)


    state = 'GAME'
    Running = True
    while Running:
        while state == 'GAME':
            game_clock.tick(FPS) # Define limite de frames por segundo
            now = pygame.time.get_ticks() # Ticks percorridos até o loop atual

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Sai do loop do jogo e retorna para o launcher
                    state = 'QUIT'
                    Running = False
                if event.type == pygame.KEYDOWN:
                    keys_pressed[event.key] = True # Adiciona a tecla pressionada ao dicionário
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
                        # Se a tecla existir no dicionário subtraimos a velocidade ganha ao pressionar a tecla
                        # Se a tecla não estiver no dicionário, não modificamos a velocidade para evitar bugs
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

            # Cria nuvens aleatóriamente
            cloudtimer += 1
            if cloudtimer >= cloudtimetocreate:
                speed = random.randint(4,5)
                centery = random.randint(30, SCR_HEIGHT-30)
                new_cloud = Cloud(assets, centery, speed)
                clouds.add(new_cloud)
                cloudtimer = 0
                cloudtimetocreate = random.randint(50, 300)

            # Colisao entre tiros e inimigos
            bullet_hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True, pygame.sprite.collide_mask)
            for i in bullet_hits:
                i.destroy()
                enemy_count -= 1
                coins += 1

            # Colisao entre Player e inimigos
            if player.blink == False:
                player_hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
                if len(player_hits) > 0:
                    lives -= 1
                    # Quando tomar dano, o jogador pisca por alguns segundos
                    player.blink = True
                    player.blink_timer = 0
            elif player.blink == True:
                player.blink_timer += 1
              
            enemy_timer = base_timer - score * difficulty # Reduz o timer dos inimigos com o tempo, com a dificulade controlando a diferença
            if enemy_timer < 100:
                # Se o timer ficaria menor que 100 ticks, retorna a 100 para evitar timers negativos
                enemy_timer = 100
            
            # Cria novos inimigos, desde que não passe do limite
            if enemy_count <= 40:
                if (now - last_spawn) > enemy_timer:
                    for i in range(3):
                        # Cria novos inimigos
                        e = Enemy(assets,ENEMY_CONFIG)
                        enemies.add(e)
                        sprites.add(e)
                        enemy_count += 1
                    last_spawn = now

            # Update das nuvens, sprites e background
            clouds.update()
            sprites.update()
            window.fill((125, 190, 215))

            # Aumenta score e lscore a cada tick
            score += 0.2
            lscore += 0.2

            # Display o score
            score_num = assets[FONT].render(f"{score:.0f}", True, (255,255,255))
            score_rect = score_num.get_rect()
            score_rect.topright = (SCR_WIDTH-20,40)
            window.blit(score_num,score_rect)

            # Animação da moeda
            coinframe += 1
            canimframe = coinframe//10
            ccoin = assets['coin_anim'][canimframe]
            coin_rect = ccoin.get_rect()
            coin_rect.topleft = (10, 10)
            window.blit(assets['coin_anim'][canimframe], (10, 10))
            if coinframe >= 58:
                coinframe = 0

            # Display animação e valor das moedas
            coin_title = assets[FONT].render('X {}'.format(str(coins)), True, (255,255,255))
            title_rect = coin_title.get_rect()
            title_rect.topleft = (55, 18)
            window.blit(coin_title,title_rect)

            # Vida extra a cada 500 pontos
            if lscore > 500:
                lives += 1
                lscore = 0
                extralifei = 1

            # Aviso de vida extra por 2 segundos
            if extralifei > 0:
                extralifei += 1
                extralife_title = assets['FONT3'].render('vida extra!', True, (255,50,50))
                title_rect = extralife_title.get_rect()
                title_rect.center = (SCR_WIDTH/2, 60)
                window.blit(extralife_title,title_rect)
                if extralifei > 120:
                    extralifei = 0

            # Animação vidas
            heartframe += 1
            hanimframe = heartframe//10
            cheart = assets['heart_anim'][hanimframe]
            heart_rect = cheart.get_rect()
            heart_rect.midtop = (180, 18)
            window.blit(assets['heart_anim'][hanimframe], heart_rect)
            if heartframe >= 39:
                heartframe = 0
            # Display animação e número de vidas
            score_title = assets[FONT].render("SCORE", True, (255,255,255))
            title_rect = score_title.get_rect()
            title_rect.topright = (SCR_WIDTH-20,20)
            window.blit(score_title,title_rect)

            text_surface = assets[FONT].render('X {}'.format(lives), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (215, 18)
            window.blit(text_surface, text_rect)

            # Checa se morreu (acabaram as vidas), encerra o jogo, inicia Loja
            if lives <= 0:
                state = "DEAD"

                # Muito importante redefinir essas variáveis aos valores iniciais
                # Se não forem reiniciadas, causa diversos bugs
                keys_pressed = {}
                firing = False
                player.speedx = 0
                player.speedy = 0
                lives = 0
                enemy_count = 0
                for i in enemies:
                    i.destroy()

                pygame.mixer.music.fadeout(2900) # Transiciona a música
                # Cria tela de morte
                if score > save_data['high_score']:
                    save_data['high_score'] = score
                text_surface = assets['FONT4'].render('Perdeu', True, (255, 30, 30))
                text_rect = text_surface.get_rect()
                text_rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)
                window.blit(text_surface, text_rect)
                pygame.display.update()

                # Espera 2 segundos, troca de música
                time.sleep(2)
                pygame.mixer.music.load(path.join(SND, 'Menumusic.mp3'))
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(loops=-1)

            # Desenha nuvens e sprites, atualiza o display
            clouds.draw(window)
            sprites.draw(window)
            pygame.display.update()
        
        while state == "DEAD":
            # Roda a tela de loja/menu

            game_clock.tick(FPS) # Limite de FPS

            window.blit(assets['BGLoja'],(0,0)) # Desenha o background
            # Animação e número de moedas
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

            # Display score dessa vida
            text_surface = assets['FONT2'].render('score: {:.0f}'.format(score), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.midleft = (900, 190)
            window.blit(text_surface, text_rect)
            # Display highscore
            text_surface = assets['FONT2'].render('high score: {:.0f}'.format(save_data['high_score']), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.midleft = (900, 220)
            window.blit(text_surface, text_rect)

            # Escreve "Aperte R para jogar"
            text_surface = assets['FONT3'].render('Aperte R para jogar', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.bottomright = (SCR_WIDTH-25, SCR_HEIGHT-15)
            window.blit(text_surface, text_rect)

            # Display upgrade de vidas
            text_surface = assets['FONT2'].render('1 - VIDA EXTRA [10 moedas]', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (60, 340)
            window.blit(text_surface, text_rect)
            text_surface = assets[FONT].render('adiciona uma vida (vidas: {})'.format(lives+3), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (70, 370)
            window.blit(text_surface, text_rect)

            # Display upgrade de dificuldade
            text_surface = assets['FONT2'].render('2 - FREIO ABS [15 moedas]', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (60, 420)
            window.blit(text_surface, text_rect)
            text_surface = assets[FONT].render('diminui a aceleracao dos inimigos (max quatro compras)', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (70, 450)
            window.blit(text_surface, text_rect)

            # Display upgrade de tiro
            text_surface = assets['FONT2'].render('3 - TREINAMENTO DE UZI [6 moedas]', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (60, 500)
            window.blit(text_surface, text_rect)
            text_surface = assets[FONT].render('levemente diminui o tempo para atirar (max sete compras)', True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (70, 530)
            window.blit(text_surface, text_rect)

            # Update na tela
            pygame.display.update()

            # Trata eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'QUIT'
                    Running = False
                if event.type == pygame.KEYDOWN:
                    # R volta ao jogo
                    if event.key == pygame.K_r:
                        state = "GAME"
                        pygame.mixer.music.load(path.join(SND, 'Gamemusic.mp3'))
                        pygame.mixer.music.set_volume(0.25)
                        pygame.mixer.music.play(loops=-1)
                        keys_pressed = {}
                        player.rect.left = 90
                        player.rect.centery = SCR_HEIGHT/2
                        player.speedx = 0
                        player.speedy = 0
                        lives += 3
                        score = 0
                        lscore = 0
                    # Tecla 1 compra upgrade de vidas
                    if event.key == pygame.K_1:
                        if coins >= 10:
                            lives += 1
                            coins -= 10
                    # Tecla 2 compra upgrade de dificuldade
                    if event.key == pygame.K_2:
                         if coins >= 15 and save_data['difficulty'] > 2:
                             save_data['difficulty'] -= 1
                             coins -= 15
                    # Tecla 3 compra upgrade de tiros
                    if event.key == pygame.K_3:
                         if coins >= 6 and save_data['shoot_speed'] < 7:
                            player.shoot_ticks -=100
                            save_data['shoot_speed'] += 1
                            coins -= 6
    
    save_data['coins'] = coins # Atualiza as moedas totais que o jogador possui
    return save_data # Retorna os novos valores para o save