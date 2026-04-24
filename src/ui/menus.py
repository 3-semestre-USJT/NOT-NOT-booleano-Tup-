from math import sin
from src.ui.cores import *
import pygame
import cv2
from src.ui import botoes

def escala_tela(imagem, tela):
    largura_tela, altura_tela = tela.get_size()
    
    # Irá Redimensionar a imagem forçando ela a ter o tamanho exato da tela
    # smoothscale é utilizado para a imagem não ficar muito pixelada ao esticar
    return pygame.transform.smoothscale(imagem, (largura_tela, altura_tela))


    # Toca o video da intro
def exibir_video_intro(tela, caminho_video):
    
    #Carrega o video utilizando OpenCV
    cap = cv2.VideoCapture(caminho_video)
    relogio = pygame.time.Clock()
    fps = cap.get(cv2.CAP_PROP_FPS)

    rodando = True
    ir_para_menu = True

    while rodando and cap.isOpened():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                ir_para_menu = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tamanho = frame_rgb.shape[1::-1]
        surface_frame = pygame.image.frombuffer(frame_rgb.tobytes(),tamanho,"RGB")
        # Redimenciona o video para cobrir a tela inteira
        surface_frame = escala_tela(surface_frame,tela)

        # Mostra o video na tela
        tela.blit(surface_frame, (0,0)) 
        pygame.display.flip()
        relogio.tick(fps)

    cap.release()
    return ir_para_menu


def exibir_menu_principal(tela, desenhar_texto_func, fontes, opcao_selecionada):
    # Desenha a tela inicial do jogo
    desenhar_texto_func("TupãStudios", BRANCO, -250, fontes['media'])
    desenhar_texto_func("! INDEXERROR", BRANCO, -150, fontes['grande'])
    
    play_button, config_button, quit_button, img_mao_esc = botao_escalonado(tela)

    play_button.exibir_botao(tela)
    config_button.exibir_botao(tela)
    quit_button.exibir_botao(tela)

    # Escolhe qual botão a mãozinha vai seguir
    if opcao_selecionada == 0:
        botao_focado = play_button
    elif opcao_selecionada == 1:
        botao_focado = config_button
    else:
        botao_focado = quit_button

    # Efeito na maozinha
    tempo = pygame.time.get_ticks()  
    # 0.007 controla a velocidade, 8 controla a distância do balanço.
    oscilacao = sin(tempo * 0.007) * 8

    # Desenha a mãozinha na esquerda do botão focado
    mao_x = botao_focado.rect.right + (20 * (tela.get_width() / 800)) + oscilacao
    mao_y = botao_focado.rect.centery - (img_mao_esc.get_height() // 2)
    tela.blit(img_mao_esc, (mao_x, mao_y))

    

def botao_escalonado(tela):
    largura_tela, altura_tela = tela.get_size()

    # Calcula o multiplicador (baseado na sua tela original de 1280x720)
    escala_x = largura_tela / 1280
    escala_y = altura_tela / 720

    fator_reducao = 0.30 

    # Pega as dimensões e já aplica a redução + a escala da tela
    largura_final = int(botoes.botao_play.get_width() * escala_x * fator_reducao)
    altura_final = int(botoes.botao_play.get_height() * escala_y * fator_reducao)

    # Redimensiona as imagens dos botões para não ficarem minúsculas
    img_play = pygame.transform.smoothscale(botoes.botao_play, (largura_final, altura_final))
    img_config = pygame.transform.smoothscale(botoes.botao_config, (largura_final, altura_final))
    img_quit = pygame.transform.smoothscale(botoes.botao_sair, (largura_final, altura_final)) 
   
   # Redimensionando a mãozinha seletora
    proporcao = botoes.mao_seletora.get_width() / botoes.mao_seletora.get_height()
    altura_alvo = int(img_play.get_height() * 0.5)
    largura_alvo = int(altura_alvo * proporcao)
    img_mao = pygame.transform.smoothscale(botoes.mao_seletora, (largura_alvo, altura_alvo))

    #Transforma posições fixas em porcentagens (posições relativas)
    x = largura_tela * 0.03125

    # Transforma o Y (250, 320, 390 divididos por 720)
    y_play = altura_tela * 0.3072
    y_config = altura_tela * 0.4444
    y_quit = altura_tela * 0.5816

    # Cria e retorna as instâncias dos botões na posição certa e tamanho certo
    play_button = botoes.botao(x, y_play, img_play)
    config_button = botoes.botao(x, y_config, img_config)
    quit_button = botoes.botao(x, y_quit, img_quit)
    
    return play_button, config_button, quit_button, img_mao

def obter_botao_clicado(pos, tela): 
    play_button, config_button, quit_button, _ = botao_escalonado(tela)
    # O ' _ ' é para o python ignorar a imagem da mãozinha
    
    if play_button.clicado(pos):
        return "play"
    elif config_button.clicado(pos):
        return "config"
    elif quit_button.clicado(pos):
        return "quit"
    return None

def exibir_opcoes(tela, desenhar_texto_func, fontes, opcao_selecionada, resolucoes):
    tela.fill(PRETO)

    desenhar_texto_func("RESOLUÇÃO", BRANCO, -150, fontes['grande'])

    for i, opcao in enumerate(resolucoes):

        if opcao == "FULLSCREEN":
            texto = "FULLSCREEN"
        else:
            texto = f"{opcao[0]} x {opcao[1]}"

        cor = AMARELO if i == opcao_selecionada else BRANCO

        desenhar_texto_func(texto, cor, i * 60 -20, fontes['media'])

    desenhar_texto_func("ENTER Para aplicar", CINZA_CLARO, 180, fontes['pequena'])
    desenhar_texto_func("ESQ para voltar", CINZA_CLARO, 220, fontes['pequena']) 

def exibir_game_over(tela, desenhar_texto_func, fontes, score, ranking):
    tela.fill(VERMELHO_MORTE)

    desenhar_texto_func("GAME OVER", VERMELHO_VIVO, -180, fontes['grande'])
    desenhar_texto_func(f"Score Final: {score}", BRANCO, -100, fontes['media'])

    desenhar_texto_func("TOP 3", ROSA_PASTEL, -30, fontes['media'])

    y_pos = 20
    for i, dados in enumerate(ranking):
        texto_ranking = f"{i + 1}. {dados['nome']} - {dados['pontos']}"

        if i == 0:
            cor = DOURADO
        elif i == 1:
            cor = PRATA
        else:
            cor = BRONZE

        desenhar_texto_func(texto_ranking, cor, y_pos, fontes['pequena'])
        y_pos += 40

    desenhar_texto_func("Pressione R para tentar de novo", CINZA, 180, fontes['pequena'])


def exibir_registro_recorde(tela, desenhar_texto_func, fontes, nome_atual):
    tela.fill(PRETO)
    desenhar_texto_func("NOVO RECORDE!", AMARELO, -150, fontes['grande'])
    desenhar_texto_func("DIGITE AS INICIAIS", BRANCO, -50, fontes['media'])

    letras_display = nome_atual.ljust(3, "_")
    letras_espacadas = " ".join(letras_display)

    desenhar_texto_func(letras_espacadas, VERDE_VIBRANTE, 50, fontes['grande'])
    desenhar_texto_func("Pressione ENTER para salvar", CINZA_CLARO, 150, fontes['pequena'])