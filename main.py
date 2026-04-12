import pygame
import os
import sys
import logic
from src.logic.pontuacao import GerenciadorPontuacao
from src.ui.cores import *
from src.ui.menus import exibir_menu_principal, exibir_game_over, exibir_video_intro
from src.ui.tela_jogo import exibir_gameplay

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(BASE_DIR, "assets", "fonts", "PressStart2P-Regular.ttf")

pygame.init()

# Tela e FPS
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Fontes
fonte_Grande = pygame.font.Font(CAMINHO_FONTE, 35)
fonte_Media = pygame.font.Font(CAMINHO_FONTE, 20)
fonte_Pequena = pygame.font.Font(CAMINHO_FONTE, 15)

fontes_jogo = {
    'grande': fonte_Grande,
    'media': fonte_Media,
    'pequena': fonte_Pequena
}

# Estados
intro, menu, jogando, GAME_OVER, REGISTRANDO, OPCOES = 'INTRO', 'MENU', 'JOGANDO', 'GAME_OVER', 'REGISTRANDO', 'OPCOES'

nome_input = ""
estado_Atual = intro
opcao_menu = 0
opcao_opcoes = 0
y_creditos = 600  # começa fora da tela (embaixo)

resolucoes = [
    (800, 600),
    (1280, 720),
    (1920, 1080),
    "FULLSCREEN"
]

def aplicar_resolucao(opcao):
    global tela, largura, altura

    if opcao == "FULLSCREEN":
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        largura, altura = tela.get_size()
    else:
        largura, altura = opcao
        tela = pygame.display.set_mode((largura, altura))




pontos = 0
desafio = None

sistema_pontos = GerenciadorPontuacao()
tempo_restante = 0



def desenhar_texto(texto, cor, y_offset, fonte_base, max_largura=750):
    tamanho_atual = fonte_base.get_height()
    nova_fonte = fonte_base

    while nova_fonte.size(texto)[0] > max_largura and tamanho_atual > 10:
        tamanho_atual -= 2
        nova_fonte = pygame.font.Font(CAMINHO_FONTE, tamanho_atual)

    surface = nova_fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(largura // 2, altura // 2 + y_offset))
    tela.blit(surface, rect)


# Loop principal
while True:
    if estado_Atual == intro:
        deve_continuar = exibir_video_intro(tela, "assets/videos/tupa_intro.mp4")
        if deve_continuar:
            estado_Atual = menu
        else:
            pygame.quit()
            sys.exit()
            continue

#COR
    tela.fill((PRETO))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MENU
        if estado_Atual == menu:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP:
                    opcao_menu = (opcao_menu - 1) % 2

                elif evento.key == pygame.K_DOWN:
                    opcao_menu = (opcao_menu + 1) % 2

                elif evento.key == pygame.K_RETURN:

                    if opcao_menu == 0:  # JOGAR
                        sistema_pontos.resetar_partida()
                        desafio = logic.obter_novo_desafio(sistema_pontos.score)
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                        estado_Atual = jogando

                    elif opcao_menu == 1:  # OPÇÕES
                        estado_Atual = OPCOES

        # JOGO
        elif estado_Atual == jogando:
            if evento.type == pygame.KEYDOWN:
                escolha = None
                if evento.key == pygame.K_UP: escolha = "CIMA"
                if evento.key == pygame.K_DOWN: escolha = "BAIXO"
                if evento.key == pygame.K_LEFT: escolha = "ESQUERDA"
                if evento.key == pygame.K_RIGHT: escolha = "DIREITA"

                if escolha:
                    if logic.validar_jogada(escolha, desafio["corretas"]):
                        sistema_pontos.registrar_acerto()
                        desafio = logic.obter_novo_desafio(sistema_pontos.score)
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                    else:
                        if sistema_pontos.verificar_novo_recorde():
                            estado_Atual = REGISTRANDO
                        else:
                            estado_Atual = GAME_OVER

        # GAME OVER
        elif estado_Atual == GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    sistema_pontos.resetar_partida()
                    desafio = logic.obter_novo_desafio(sistema_pontos.score)
                    tempo_restante = sistema_pontos.calcular_tempo_limite()
                    estado_Atual = jogando

                elif evento.key == pygame.K_ESCAPE:
                    estado_Atual = menu

        # REGISTRO
        elif estado_Atual == REGISTRANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if len(nome_input) == 3:
                        sistema_pontos.salvar_no_ranking(nome_input)
                        nome_input = ""
                        estado_Atual = GAME_OVER

                elif evento.key == pygame.K_BACKSPACE:
                    nome_input = nome_input[:-1]

                elif len(nome_input) < 3:
                    if evento.unicode.isalpha():
                        nome_input += evento.unicode.upper()

        # OPÇÕES
        elif estado_Atual == OPCOES:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP:
                    opcao_opcoes = (opcao_opcoes - 1) % len(resolucoes)

                elif evento.key == pygame.K_DOWN:
                    opcao_opcoes = (opcao_opcoes + 1) % len(resolucoes)

                elif evento.key == pygame.K_RETURN:
                    aplicar_resolucao(resolucoes[opcao_opcoes])

                elif evento.key == pygame.K_ESCAPE:
                    estado_Atual = menu

    # CRONÔMETRO
    if estado_Atual == jogando:
        tempo_restante -= relogio.get_time() / 1000.0

        if tempo_restante <= 0:
            if sistema_pontos.verificar_novo_recorde():
                estado_Atual = REGISTRANDO
            else:
                estado_Atual = GAME_OVER

    # RENDER
    if estado_Atual == menu:
        exibir_menu_principal(tela, desenhar_texto, fontes_jogo, opcao_menu)

    elif estado_Atual == jogando:
        exibir_gameplay(tela, desenhar_texto, fontes_jogo, desafio, sistema_pontos, tempo_restante)

    elif estado_Atual == GAME_OVER:
        exibir_game_over(tela, desenhar_texto, fontes_jogo, sistema_pontos.score, sistema_pontos.ranking)

    elif estado_Atual == REGISTRANDO:
        from src.ui.menus import exibir_registro_recorde

        exibir_registro_recorde(tela, desenhar_texto, fontes_jogo, nome_input)

    elif estado_Atual == OPCOES:
        from src.ui.menus import exibir_opcoes

        exibir_opcoes(tela, desenhar_texto, fontes_jogo, opcao_opcoes, resolucoes)

    pygame.display.flip()
    relogio.tick(60)