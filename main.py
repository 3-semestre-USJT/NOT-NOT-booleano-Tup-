import pygame 
import sys    # Biblioteca usada para fechar a janela do jogo  
import logic  # Importa a ponte de lógica que criamos
from src.logic.pontuacao import GerenciadorPontuacao 

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

# Instancia o motor de pontuação
sistema_pontos = GerenciadorPontuacao()
tempo_restante = 0 # Variável pro cronômetro da rodada

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
                    sistema_pontos.resetar_partida() # Zera o score e combo
                    desafio = logic.obter_novo_desafio(sistema_pontos.score)

                    # ENCHE O CRONÔMETRO ANTES DE COMEÇAR!
                    tempo_restante = sistema_pontos.calcular_tempo_limite()

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
                        # Se a resposta estiver correta, aumenta os pontos usando o sistema de pontuação
                        sistema_pontos.registrar_acerto() 
                        # Atualiza o desafio passando o novo score
                        desafio = logic.obter_novo_desafio(sistema_pontos.score) 
                        # Atualiza o tempo restante baseado no score atual
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                    else:
                        # SE ERROU A TECLA
                        sistema_pontos.salvar_recorde()
                        estado_Atual = GAME_OVER

        elif estado_Atual == GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:   # R reinicia o jogo
                    sistema_pontos.resetar_partida() # Zera o score e combo
                    desafio = logic.obter_novo_desafio(sistema_pontos.score)
                    
                    # ENCHE O CRONÔMETRO DE NOVO AQUI TAMBÉM!
                    tempo_restante = sistema_pontos.calcular_tempo_limite()

                    estado_Atual = jogando
                elif evento.key == pygame.K_ESCAPE: # ESC volta pro menu
                    estado_Atual = menu

    # CRONÔMETRO: Diminui o tempo a cada frame

    if estado_Atual == jogando:
        tempo_restante -= relogio.get_time() / 1000.0 
        
        if tempo_restante <= 0: # O tempo esgotou!
            sistema_pontos.salvar_recorde()
            estado_Atual = GAME_OVER
    
    # Escreve na tela 
    if estado_Atual == menu:
        desenhar_texto("Tupã BOOLEAN GAME", (255, 255, 255), -50, fonte_Grande)
        desenhar_texto("Presione ENTER para começar", (150, 150, 150), 50, fonte_Pequena)
    
    elif estado_Atual == jogando:
        cores_niveis = [(20,20,25), (30,50,30), (50,30,30), (30,30,50), (50,50,20)] # Cores base por nivel
        idx_cor = min(sistema_pontos.score // 500, 4) # Aqui vai até 4 porque listas começam no 0
        tela.fill(cores_niveis[idx_cor]) # Pinta o fundo com a cor do nível
        desenhar_texto(desafio["texto"], (255, 255, 255), -30, fonte_Grande)
        desenhar_texto(f"Score: {sistema_pontos.score}", (0, 255, 100), 100, fonte_Pequena)
        desenhar_texto(f"Combo: {sistema_pontos.combo}x (Mult: {sistema_pontos.multiplicador}x)", (255, 200, 0), 140, fonte_Pequena)
        
        # Desenha o cronômetro
        desenhar_texto(f"Tempo: {tempo_restante:.1f}s", (255, 50, 50), 180, fonte_Pequena)

    elif estado_Atual == GAME_OVER:
        tela.fill((50, 10, 10)) # Fundo avermelhado para o fim de jogo
        desenhar_texto("GAME OVER", (255, 50, 50), -50, fonte_Grande)
        desenhar_texto(f"Score Final: {sistema_pontos.score}", (255, 255, 255), 20, fonte_Pequena)
        desenhar_texto(f"Recorde Máximo: {sistema_pontos.high_score}", (255, 215, 0), 60, fonte_Pequena)
        desenhar_texto("Pressione R para tentar de novo", (100, 100, 100), 100, fonte_Pequena)

    pygame.display.flip() # Atualiza o desenho na tela do computador
    relogio.tick(60) # Jogo roda a 60 FPS