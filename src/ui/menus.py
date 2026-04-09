from src.ui.cores import * # O * importa tudo

def exibir_menu_principal(tela, desenhar_texto_func, fontes):
    # Desenha a tela inicial do jogo
    desenhar_texto_func("TupãStudios", BRANCO, -250, fontes['media'])
    desenhar_texto_func("! INDEXERROR", BRANCO, -50, fontes['grande'])
    desenhar_texto_func("Pressione ENTER para começar", CINZA_CLARO, 50, fontes['pequena'])

def exibir_game_over(tela, desenhar_texto_func, fontes, score, ranking):
    # Desenha a tela de fim de jogo com o Top 3
    tela.fill(VERMELHO_MORTE)
    
    desenhar_texto_func("GAME OVER", VERMELHO_VIVO, -180, fontes['grande'])
    desenhar_texto_func(f"Score Final: {score}", BRANCO, -100, fontes['media'])
    
    # Seção do Ranking
    desenhar_texto_func("TOP 3", ROSA_PASTEL, -30, fontes['media'])
    
    y_pos = 20 # Posição vertical inicial para o primeiro do ranking
    for i, dados in enumerate(ranking):

        texto_ranking = f"{i+1}. {dados['nome']} - {dados['pontos']}"
        
        # Cores por posição
        if i == 0:
            cor = DOURADO
        elif i == 1:
            cor = PRATA
        else:
            cor = BRONZE

        desenhar_texto_func(texto_ranking, cor, y_pos, fontes['pequena'])
        y_pos += 40 # Espaçamento entre as linhas do ranking
        
    desenhar_texto_func("Pressione R para tentar de novo", CINZA, 180, fontes['pequena'])

def exibir_registro_recorde(tela, desenhar_texto_func, fontes, nome_atual):
    # Tela para o jogador digitar as 3 iniciais
    tela.fill(PRETO)
    desenhar_texto_func("NOVO RECORDE!", AMARELO, -150, fontes['grande'])
    desenhar_texto_func("DIGITE AS INICIAIS", BRANCO, -50, fontes['media'])
    
    letras_display = nome_atual.ljust(3, "_")    # Mostra o que está sendo digitado
    letras_espacadas = " ".join(letras_display)  # Formata para dar um espacinho entre as letras
    
    desenhar_texto_func(letras_espacadas, VERDE_VIBRANTE, 50, fontes['grande'])
    desenhar_texto_func("Pressione ENTER para salvar", CINZA_CLARO, 150, fontes['pequena'])