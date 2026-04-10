import pygame 
import os     # Padroniza caminhos de arquivos p/ que o jogo rode em qualquer computador sem dar erro de 'Pasta não encontrada'
import sys    # Biblioteca usada para fechar a janela do jogo
import logic  # Importa a ponte de lógica que criamos
from src.logic.pontuacao import GerenciadorPontuacao 
from src.ui.cores import * # Para organizar a interface
from src.ui.menus import exibir_menu_principal, exibir_game_over, exibir_video_intro
from src.ui.tela_jogo import exibir_gameplay

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Garante o endereço para carregar a fonte do jogo
CAMINHO_FONTE = os.path.join(BASE_DIR, "assets", "fonts", "PressStart2P-Regular.ttf") # Caminho até a fonte

pygame.init() # inicializa os modulos do pygame

# Tela e FPS
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock() # Controla a velocidade do jogo

# Fontes 
fonte_Grande = pygame.font.Font(CAMINHO_FONTE, 35)
fonte_Media = pygame.font.Font(CAMINHO_FONTE, 20)
fonte_Pequena = pygame.font.Font(CAMINHO_FONTE, 15)

# Agrupando fontes para facilitar o envio para as funções de UI
fontes_jogo = {
    'grande': fonte_Grande,
    'media': fonte_Media,
    'pequena': fonte_Pequena
}

# Possíveis estados do jogo
intro, menu, jogando, GAME_OVER, REGISTRANDO = 'INTRO','MENU', 'JOGANDO', 'GAME_OVER', 'REGISTRANDO'
nome_input = "" # Variável para guardar as 3 letras que o jogador vai digitar
estado_Atual = intro #Estado Inicial do jogo
pontos = 0
desafio = None # A variavel precisa existir, por isso 'None' que vai ser substituido depois

# Instancia o motor de pontuação
sistema_pontos = GerenciadorPontuacao()
tempo_restante = 0 # Variável pro cronômetro da rodada

def desenhar_texto(texto, cor, y_offset, fonte_base, max_largura=750):
    # Se o texto for maior que a largura máxima, diminui a fonte
    tamanho_atual = fonte_base.get_height()
    nova_fonte = fonte_base
    
    # Enquanto o texto for largo demais, reduz o tamanho (mínimo de 10px)
    while nova_fonte.size(texto)[0] > max_largura and tamanho_atual > 10:
        tamanho_atual -= 2
        nova_fonte = pygame.font.Font(CAMINHO_FONTE, tamanho_atual)

    surface = nova_fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(largura // 2, altura // 2 + y_offset))
    tela.blit(surface, rect)

# Loop principal do jogo
while True:
    if estado_Atual == intro: # Jogador esta iniciando o jogo
            #  Inicia apenas a intro
            deve_continuar = exibir_video_intro(tela, "assets/videos/intro_teste.mp4")
            if deve_continuar:
                estado_Atual = menu # Video acabou ou jogador apertou ESC
            else:
                pygame.quit() # Jogador apertou (X)Janela
                sys.exit()
                continue # Continua para as outras funções (captura de eventos, estado atual...)

    tela.fill((CINZA_ESCURO)) # Pinta o fundo

    # Captura dos eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Se clicar no X da janela
            pygame.quit() # Encerra o pygame
            sys.exit() # Fecha o programa 

        if estado_Atual == menu: # Jogador está no menu
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # ENTER começa
                    sistema_pontos.resetar_partida() # Zera o score e combo
                    desafio = logic.obter_novo_desafio(sistema_pontos.score)

                    # ENCHE O CRONÔMETRO ANTES DE COMEÇAR!
                    tempo_restante = sistema_pontos.calcular_tempo_limite()

                    estado_Atual = jogando

        elif estado_Atual == jogando: # Jogador está jogando
            if evento.type == pygame.KEYDOWN:
                # Isso aqui "transforma" as setinhas em Strings
                escolha = None
                if evento.key == pygame.K_UP:      escolha = "CIMA"
                if evento.key == pygame.K_DOWN:    escolha = "BAIXO"
                if evento.key == pygame.K_LEFT:    escolha = "ESQUERDA"
                if evento.key == pygame.K_RIGHT:   escolha = "DIREITA"

                if escolha: # Confere a resposta do jogador
                    # Valida a resposta usando o novo logic.py
                    if logic.validar_jogada(escolha, desafio["corretas"]):
                        # Se a resposta estiver correta, aumenta os pontos usando o sistema de pontuação
                        sistema_pontos.registrar_acerto() 
                        # Atualiza o desafio passando o novo score
                        desafio = logic.obter_novo_desafio(sistema_pontos.score) 
                        # Atualiza o tempo restante baseado no score atual
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                    else:
                        # Se errou a tecla, verifica se foi top 3
                        if sistema_pontos.verificar_novo_recorde():
                            estado_Atual = REGISTRANDO
                        else:
                            estado_Atual = GAME_OVER

        elif estado_Atual == GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:   # R reinicia o jogo
                    sistema_pontos.resetar_partida() # Zera o score e combo
                    desafio = logic.obter_novo_desafio(sistema_pontos.score)
                    
                    # Enche o cronometro de novo
                    tempo_restante = sistema_pontos.calcular_tempo_limite()
                    estado_Atual = jogando

                elif evento.key == pygame.K_ESCAPE: # ESC volta pro menu
                    estado_Atual = menu
        
        elif estado_Atual == REGISTRANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if len(nome_input) == 3:
                        # Salva no ranking e vai para o Game Over
                        sistema_pontos.salvar_no_ranking(nome_input)
                        nome_input = "" # Limpa para a próxima vez
                        estado_Atual = GAME_OVER
                
                elif evento.key == pygame.K_BACKSPACE:
                    nome_input = nome_input[:-1] # Apaga a última letra
                
                elif len(nome_input) < 3:
                    # Captura apenas letras e transforma em maiúsculas
                    if evento.unicode.isalpha():
                        nome_input += evento.unicode.upper()

    # CRONÔMETRO: Diminui o tempo a cada frame
    if estado_Atual == jogando:
        tempo_restante -= relogio.get_time() / 1000.0 
        
        if tempo_restante <= 0:
        # Verifica se a pontuação entra no Ranking
            if sistema_pontos.verificar_novo_recorde():
                estado_Atual = REGISTRANDO # Novo estado para digitar o nome
            else:
                estado_Atual = GAME_OVER
    
    # PARTE VISUAL (REORGANIZADA)
    if estado_Atual == menu:
        exibir_menu_principal(tela, desenhar_texto, fontes_jogo)
    
    elif estado_Atual == jogando:
        exibir_gameplay(tela, desenhar_texto, fontes_jogo, desafio, sistema_pontos, tempo_restante)

    elif estado_Atual == GAME_OVER:
        exibir_game_over(tela, desenhar_texto, fontes_jogo, sistema_pontos.score, sistema_pontos.ranking)


    elif estado_Atual == REGISTRANDO:
        from src.ui.menus import exibir_registro_recorde
        exibir_registro_recorde(tela, desenhar_texto, fontes_jogo, nome_input)

    pygame.display.flip() # Atualiza o desenho na tela do computador
    relogio.tick(60) # Jogo roda a 60 FPS