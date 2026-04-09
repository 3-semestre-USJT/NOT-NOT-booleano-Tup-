from src.ui.cores import * # O * importa tudo

def exibir_gameplay(tela, desenhar_texto_func, fontes, desafio, sistema_pontos, tempo_restante):
    # Desenha os elementos da gameplay ativa
    # Cor de fundo baseada no nível
    idx_cor = min(sistema_pontos.score // 500, 4) 
    tela.fill(CORES_NIVEIS[idx_cor]) 
    
    # Textos do jogo
    desenhar_texto_func(desafio["texto"], BRANCO, -50, fontes['grande'], max_largura=760)
    desenhar_texto_func(f"Score: {sistema_pontos.score}", VERDE_VIBRANTE, 100, fontes['pequena'])
    desenhar_texto_func(f"Combo: {sistema_pontos.combo}x (Mult: {sistema_pontos.multiplicador}x)", AMARELO, 140, fontes['pequena'])
    
    # Cronômetro
    desenhar_texto_func(f"Tempo: {tempo_restante:.1f}s", VERMELHO_VIVO, 180, fontes['pequena'])