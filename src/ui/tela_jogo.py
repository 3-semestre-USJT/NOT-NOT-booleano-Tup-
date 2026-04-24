from src.ui.cores import * # O * importa tudo
import pygame

def exibir_gameplay(tela, desenhar_texto_func, fontes, desafio, sistema_pontos, tempo_restante, imagem_gameplay, animacao_perso, deslocamento_perso):
    # Desenha os elementos da gameplay ativa
    # Cor de fundo baseada no nível
    # idx_cor = min(sistema_pontos.score // 500, 4)
    
    
    tela.blit(imagem_gameplay, (0,0))
    
    tempo_atual = pygame.time.get_ticks()
    # Pega o tempo atual e divide por 500ms. O '% 2' faz o valor alternar entre 0 e 1
    frame_atual = (tempo_atual // 500) % 2
    imagem_exibir = animacao_perso[frame_atual]

    # Calcula o centro da tela
    largura_tela, altura_tela = tela.get_size()
    centro_x = (largura_tela // 2) - (imagem_exibir.get_width() // 2)
    centro_y = (altura_tela // 2) - (imagem_exibir.get_height() // 2)

    # Aplica o deslocamento (para a imagem ir na direção selecionada)
    pos_x = centro_x + deslocamento_perso[0]
    pos_y = centro_y + deslocamento_perso[1]

    # Desenha a imagem animada
    tela.blit(imagem_exibir, (pos_x, pos_y))
    
    
    # Textos do jogo
    desenhar_texto_func(desafio["texto"], BRANCO, 250, fontes['grande'], max_largura=760)
    desenhar_texto_func(f"Score: {sistema_pontos.score}", VERDE_VIBRANTE, -270, fontes['pequena'])
    desenhar_texto_func(f"Combo: {sistema_pontos.combo}x (Mult: {sistema_pontos.multiplicador}x)", AMARELO, -310, fontes['pequena'])
    
    # Cronômetro
    desenhar_texto_func(f"Tempo: {tempo_restante:.1f}s", VERMELHO_VIVO, 300, fontes['pequena'])
