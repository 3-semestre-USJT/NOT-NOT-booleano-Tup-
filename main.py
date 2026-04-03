import pygame 
import sys    # Biblioteca usada para fechar a janela do jogo  
import logic  # Importa a ponte de lógica que criamos

#inicializa os modulos do pygame
pygame.init() 

# Tela e FPS
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock() # Controla a velocidade do jogo

# Fontes 
fonte_Grande = pygame.font.SysFont('Arial', 60, bold=True)
fonte_Pequena = pygame.font.SysFont('Arial', 30)

# Possíveis estados do jogo
menu, jogando, GAME_OVER = 'MENU', 'JOGANDO', 'GAME_OVER'
estado_Atual = menu
pontos = 0
desafio = None # A variavel precisa existir, por isso 'None' que vai ser substituido depois

def desenhar_texto(texto, cor, y_offset, fonte):
    # Função para ajudar na centralização dos textos na tela
    surface = fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(largura // 2, altura // 2 + y_offset))
    tela.blit(surface, rect)

# Loop principal do jogo
while True:
    tela.fill((20, 20, 25)) # Pinta o fundo de azul

    # Captura dos eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Se clicar no X da janela
            pygame.quit() # Encerra o pygame
            sys.exit() # Fecha o programa 

        if estado_Atual == menu: # Jogador está no menu
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # ENTER começa
                    pontos = 0
                    desafio = logic.obter_novo_desafio(pontos) # Busca o primeiro desafio
                    estado_Atual = jogando

        elif estado_Atual == jogando: # Jogador está jogando
            if evento.type == pygame.KEYDOWN:
                # Isso aqui "transforma" as setinhas em Strings
                escolha = None
                if evento.key == pygame.K_UP:      escolha = "UP"
                if evento.key == pygame.K_DOWN:    escolha = "DOWN"
                if evento.key == pygame.K_LEFT:    escolha = "LEFT"
                if evento.key == pygame.K_RIGHT:   escolha = "RIGHT"

                if escolha: # Confere a resposta do jogador
                    # Valida a resposta usando o novo logic.py
                    if logic.validar_jogada(escolha, desafio["corretas"]):
                        pontos += 1
                        desafio = logic.obter_novo_desafio(pontos) # Atualiza o desafio e o nível
                    else:
                        estado_Atual = GAME_OVER

        elif estado_Atual == GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:   # R reinicia o jogo
                    pontos = 0
                    desafio = logic.obter_novo_desafio(pontos)
                    estado_Atual = jogando
                elif evento.key == pygame.K_ESCAPE: # ESC volta pro menu
                    estado_Atual = menu
    
    # Escreve na tela 
    if estado_Atual == menu:
        desenhar_texto("Tupã BOOLEAN GAME", (255, 255, 255), -50, fonte_Grande)
        desenhar_texto("Presione ENTER para começar", (150, 150, 150), 50, fonte_Pequena)
    
    elif estado_Atual == jogando:
        cores_niveis = [(20,20,25), (30,50,30), (50,30,30), (30,30,50), (50,50,20)] # Cores base por nivel
        idx_cor = min(pontos // 5, 4) # Aqui vai até 4 porque listas começam no 0
        tela.fill(cores_niveis[idx_cor]) # Pinta o fundo com a cor do nível
        desenhar_texto(desafio["texto"], (255, 255, 255), -30, fonte_Grande)
        desenhar_texto(f"Pontos: {pontos}", (0, 255, 100), 100, fonte_Pequena)

    elif estado_Atual == GAME_OVER:
        tela.fill((50, 10, 10)) # Fundo avermelhado para o fim de jogo
        desenhar_texto("GAME OVER", (255, 50, 50), -50, fonte_Grande)
        desenhar_texto(f"Score Final: {pontos}", (255, 255, 255), 20, fonte_Pequena)
        desenhar_texto("Pressione R para tentar de novo", (100, 100, 100), 100, fonte_Pequena)

    pygame.display.flip() # Atualiza o desenho na tela do computador
    relogio.tick(60) # Jogo roda a 60 FPS