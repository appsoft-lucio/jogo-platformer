import pgzrun  # Importa o framework PgZero
import os  # Para definir a posição da janela no sistema operacional
import random  # Importa a biblioteca random para movimentação aleatória

# Centraliza a janela no centro do monitor
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Define a largura e a altura da janela
WIDTH = 1000
HEIGHT = 362

# Define uma variável chao_y com a altura do chão
chao_y = HEIGHT - 130  # A altura do chão a 130 pixels do fundo

# Estado do jogo: 'menu' ou 'jogo'
estado_jogo = 'menu'

# Opções do menu
opcoes_menu = ['Iniciar Jogo', 'Som: Ligado', 'Sair']
opcao_selecionada = 0

# Variável para controlar o som
som_ligado = True

# Carregar sons
def carregar_som():
    global musica, som_moeda, som_moeda_vermelha
    musica = sounds.eep  # Carrega o som usando a biblioteca PgZero
    som_moeda = sounds.coin_audio  # Carrega o som da moeda
    som_moeda_vermelha = sounds.coin_red_audio  # Carrega o som da moeda vermelha

def tocar_som():
    if som_ligado:
        musica.play(-1)  # Toca a música em loop

def parar_som():
    musica.stop()  # Para a música

carregar_som()  # Carrega o som no início
tocar_som()  # Toca a música em loop

# Inicializa o jogador
player_sprites = ['player_000', 'player_001', 'player_002', 'player_003', 'player_004', 
                  'player_005', 'player_006', 'player_007', 'player_008', 'player_009']  # Sprites da animação
player_index = 0
player_000 = Actor(player_sprites[player_index])
player_000.pos = 200, chao_y  # Posição inicial do jogador no chão

# Inicializa as moedas
num_moedas = 5  # Define quantas moedas aparecerão
coins = [Actor('coin') for _ in range(num_moedas)]
coins_red = [Actor('coin_red') for _ in range(num_moedas)]

# Função para posicionar as moedas aleatoriamente
def posicionar_moedas():
    for coin in coins:
        coin.pos = random.randint(50, WIDTH - 50), random.randint(50, chao_y - 50)
    for coin_red in coins_red:
        coin_red.pos = random.randint(50, WIDTH - 50), random.randint(50, chao_y - 50)

# Posiciona as moedas no início do jogo
posicionar_moedas()

# Variáveis para controlar a velocidade da animação e das moedas
velocidade = 3  # Ajuste este valor para controlar a velocidade da troca de sprite
frame_counter = 0  # Contador de quadros para a animação
moeda_velocidade = 2  # Velocidade das moedas
chao_velocidade = 2  # Velocidade do chão

# Posição do chão
chao_x = 0  # Início da posição do chão

# Variáveis para o pulo
pulando = False  # Controle se o personagem está pulando
altura_pulo = 100  # Altura total do pulo
tempo_pulo = 0  # Tempo que o personagem está pulando
velocidade_pulo = 5  # Velocidade do pulo

def draw():
    screen.clear()  # Limpa a tela a cada quadro
    if estado_jogo == 'menu':
        desenhar_menu()
    elif estado_jogo == 'jogo':
        screen.clear()
        screen.blit("background", (0, 0))  # Exibe a imagem de fundo

        # Desenha o chão na posição atual
        screen.blit("chao", (chao_x, chao_y))  # Exibe o chão
        screen.blit("chao", (chao_x + WIDTH, chao_y))  # Exibe o segundo chão (para o loop)

        player_000.draw()  # Desenha o jogador
        
        # Desenha todas as moedas
        for coin in coins:
            coin.draw()  # Desenha as moedas
        for coin_red in coins_red:
            coin_red.draw()  # Desenha as moedas vermelhas

def desenhar_menu():
    screen.fill((0, 0, 0))  # Tela preta para o menu
    titulo = "Menu Principal"
    screen.draw.text(titulo, center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white")

    for i, opcao in enumerate(opcoes_menu):
        cor = "yellow" if i == opcao_selecionada else "white"
        screen.draw.text(opcao, center=(WIDTH // 2, HEIGHT // 2 + i * 50), fontsize=40, color=cor)

def update():
    global player_index, frame_counter, chao_x, pulando, tempo_pulo

    if estado_jogo == 'jogo':
        # Atualiza o contador de quadros
        frame_counter += 1

        # Muda o sprite a cada 'velocidade' quadros
        if frame_counter >= velocidade:
            if pulando:
                if tempo_pulo < altura_pulo // velocidade_pulo:  # Altura do pulo
                    player_000.y -= velocidade_pulo  # Sobe
                elif tempo_pulo < altura_pulo // velocidade_pulo + 20:  # Começa a descer
                    player_000.y += velocidade_pulo  # Desce
                else:  # O pulo terminou
                    pulando = False
                    player_000.y = chao_y  # Reseta a posição do jogador para o chão
                    player_000.image = player_sprites[player_index]  # Retorna à animação normal
                    tempo_pulo = 0  # Reseta o tempo do pulo

                tempo_pulo += 1  # Incrementa o tempo do pulo
            else:
                player_index = (player_index + 1) % len(player_sprites)  # Muda o sprite para a animação
                player_000.image = player_sprites[player_index]  # Atualiza a imagem do jogador
            
            frame_counter = 0  # Reseta o contador

        # Move as moedas da direita para a esquerda
        for coin in coins:
            coin.x -= moeda_velocidade
        for coin_red in coins_red:
            coin_red.x -= moeda_velocidade

        # Redefine a posição das moedas quando saem da tela
        for coin in coins:
            if coin.x < -50:  # A moeda saiu da tela à esquerda
                coin.x = WIDTH + random.randint(0, 100)  # Posiciona a moeda na direita da tela
                coin.y = random.randint(50, chao_y - 50)  # Nova altura aleatória

        for coin_red in coins_red:
            if coin_red.x < -50:  # A moeda vermelha saiu da tela à esquerda
                coin_red.x = WIDTH + random.randint(0, 100)  # Posiciona a moeda vermelha na direita da tela
                coin_red.y = random.randint(50, chao_y - 50)  # Nova altura aleatória

        # Move o chão da direita para a esquerda
        chao_x -= chao_velocidade
        
        # Redefine a posição do chão quando ele sair da tela
        if chao_x <= -WIDTH:  # Se o chão saiu da tela
            chao_x = 0  # Reseta a posição do chão

        # Verifica se o jogador coletou alguma moeda
        for coin in coins:
            if player_000.colliderect(coin):
                som_moeda.play()  # Toca o som da moeda
                posicionar_moedas()  # Move as moedas para novas posições aleatórias
                break  # Para evitar múltiplas colisões em um único frame

        for coin_red in coins_red:
            if player_000.colliderect(coin_red):
                som_moeda_vermelha.play()  # Toca o som da moeda vermelha
                posicionar_moedas()  # Move as moedas para novas posições aleatórias
                break  # Para evitar múltiplas colisões em um único frame

def on_key_down(key):
    global estado_jogo, opcao_selecionada, pulando

    if estado_jogo == 'menu':
        if key == keys.DOWN:
            opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_menu)
        elif key == keys.UP:
            opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_menu)
        elif key == keys.RETURN:  # Alterado para RETURN
            if opcao_selecionada == 0:
                estado_jogo = 'jogo'
            elif opcao_selecionada == 1:
                global som_ligado
                som_ligado = not som_ligado  # Alterna o estado do som
                if som_ligado:
                    tocar_som()  # Toca a música se estiver ligada
                else:
                    parar_som()  # Para a música se estiver desligada
            elif opcao_selecionada == 2:
                exit()  # Sai do jogo
    elif estado_jogo == 'jogo':
        if key == keys.SPACE and not pulando:  # Verifica se o jogador não está pulando
            pulando = True  # Começa o pulo
            player_000.y = chao_y  # Certifique-se de que o jogador está na posição do chão

# Inicia o jogo
pgzrun.go()
