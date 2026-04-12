from src.ui.cores import *
import pygame
import cv2

def escalar_proporcional(imagem, tela):
    largura_tela, altura_tela = tela.get_size()
    largura_img, altura_img = imagem.get_size()

    escala = min(largura_tela / largura_img, altura_tela / altura_img)

    nova_largura = int(largura_img * escala)
    nova_altura = int(altura_img * escala)

    return pygame.transform.scale(imagem, (nova_largura, nova_altura))


def exibir_video_intro(tela, caminho_video):
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
        surface_frame = pygame.image.frombuffer(frame_rgb.tobytes(), tamanho, "RGB")
        surface_frame = escalar_proporcional(surface_frame, tela)

        rect = surface_frame.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2))
        tela.blit(surface_frame, rect)
        pygame.display.flip()
        relogio.tick(fps)

    cap.release()
    return ir_para_menu


# MENU NOVO
def exibir_menu_principal(tela, desenhar_texto_func, fontes, opcao_selecionada):
    desenhar_texto_func("TupãStudios", BRANCO, -250, fontes['media'])
    desenhar_texto_func("! INDEXERROR", BRANCO, -100, fontes['grande'])

    opcoes = ["JOGAR", "OPÇÕES"]

    for i, opcao in enumerate(opcoes):
        cor = AMARELO if i == opcao_selecionada else BRANCO
        desenhar_texto_func(opcao, cor, i * 60, fontes['media'])
        desenhar_texto_func("Use ↑ ↓ e ENTER", CINZA_CLARO, 200, fontes['pequena'])



def exibir_opcoes(tela, desenhar_texto_func, fontes, opcao_selecionada, resolucoes):
    tela.fill(PRETO)

    desenhar_texto_func("RESOLUÇÃO", BRANCO, -150, fontes['grande'])

    for i, opcao in enumerate(resolucoes):

        if opcao == "FULLSCREEN":
            texto = "FULLSCREEN"
        else:
            texto = f"{opcao[0]} x {opcao[1]}"

        cor = AMARELO if i == opcao_selecionada else BRANCO

        desenhar_texto_func(texto, cor, i * 60 - 20, fontes['media'])

    desenhar_texto_func("ENTER para aplicar", CINZA_CLARO, 180, fontes['pequena'])
    desenhar_texto_func("ESC para voltar", CINZA, 220, fontes['pequena'])


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