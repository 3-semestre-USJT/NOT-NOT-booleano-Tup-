from src.ui.cores import * # O * importa tudo
import pygame

def escalonar_animacao(lista_imagens, largura_janela, altura_janela, proporcao=0.20):
    # Impede que 'altura_janela' seja confundida com a 'proporcao'
    # Se proporcao for maior que 1, significa que o argumento veio errado do main.py
    if proporcao > 1.0:
        proporcao = 0.20

    if largura_janela <= 0: 
        largura_janela = 1280
    
    novas_imagens = []
    
    # Pega a maior dimensão entre as imagens originais para criar a moldura
    max_w = max(img.get_width() for img in lista_imagens)
    max_h = max(img.get_height() for img in lista_imagens)
    
    # Define o tamanho do "molde" baseado na largura da janela
    largura_alvo = int(largura_janela * proporcao)
    largura_alvo = max(1, largura_alvo) # Garante tamanho mínimo de 1px
    
    proporcao_aspecto = max_h / max_w
    altura_alvo = int(largura_alvo * proporcao_aspecto)
    altura_alvo = max(1, altura_alvo) # Garante tamanho mínimo de 1px

    # Para evitar o erro de memória (Out of memory) por causa de img gigantesca
    if largura_alvo > 4000 or altura_alvo > 4000:
        largura_alvo, altura_alvo = 200, 200

    for img in lista_imagens:
        # Cria uma superfície transparente do tamanho da maior imagem (molde)
        moldura = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
        
        # Centraliza a canoa dentro dessa moldura invisível
        # Isso faz com que o centro do desenho seja o mesmo para todos os frames
        x_centralizado = (max_w - img.get_width()) // 2
        y_centralizado = (max_h - img.get_height()) // 2
        moldura.blit(img, (x_centralizado, y_centralizado))
        
        # Agora escalona a moldura, que tem sempre o mesmo tamanho fixo
        img_escalonada = pygame.transform.smoothscale(moldura, (largura_alvo, altura_alvo))
        novas_imagens.append(img_escalonada)
        
    return novas_imagens

def exibir_gameplay(tela, desenhar_texto_func, fontes, desafio, sistema_pontos, tempo_restante, imagem_gameplay, animacao_perso, deslocamento_perso):
    # Desenha o fundo da gameplay
    tela.blit(imagem_gameplay, (0,0))

    dx, dy = deslocamento_perso
    
    # Animação barco fixo
    tempo_atual = pygame.time.get_ticks()
    frame_atual = (tempo_atual // 600) % 2 
    imagem_base = animacao_perso[frame_atual]
        
    # Animação de perspectiva
    largura_tela, altura_tela = tela.get_size()
    y_referencia = (altura_tela // 2) + dy
    # O barco diminui conforme sobe (Y diminui)
    fator_perspectiva = max(0.65, min(y_referencia / (altura_tela // 2), 1.1))
    
    # Redimensiona a moldura inteira (mantendo os frames alinhados)
    nova_largura = int(imagem_base.get_width() * fator_perspectiva)
    nova_altura = int(imagem_base.get_height() * fator_perspectiva)
    
    # Usa scale para performance no loop de gameplay
    imagem_transformada = pygame.transform.scale(imagem_base, (nova_largura, nova_altura))

    # Rotação do barquinho
    angulo = 0
    if abs(dx) > abs(dy):
        angulo = 90 if dx < 0 else -90 # Esquerda / Direita
    elif dy > 0:
        angulo = 180 # Baixo
        
    imagem_final = pygame.transform.rotate(imagem_transformada, angulo)

    # Centralização baseada na moldura final
    pos_x = (largura_tela // 2) - (imagem_final.get_width() // 2) + dx
    pos_y = (altura_tela // 2) - (imagem_final.get_height() // 2) + dy

    tela.blit(imagem_final, (pos_x, pos_y))
    
    # Textos do jogo (HUD)
    desenhar_texto_func(desafio["texto"], BRANCO, 250, fontes['grande'], max_largura=760)
    desenhar_texto_func(f"Score: {sistema_pontos.score}", VERDE_VIBRANTE, -270, fontes['pequena'])
    desenhar_texto_func(f"Combo: {sistema_pontos.combo}x (Mult: {sistema_pontos.multiplicador}x)", AMARELO, -310, fontes['pequena'])
    desenhar_texto_func(f"Tempo: {tempo_restante:.1f}s", VERMELHO_VIVO, 300, fontes['pequena'])