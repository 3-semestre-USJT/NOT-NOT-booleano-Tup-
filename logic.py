from src.logic.gerador import sortear_desafio
from src.logic.validador import verificar_resposta

def obter_novo_desafio(pontos):
    # Calcula o nível (1 a 5) a cada 5 pontos
    nivel_atual = min((pontos // 5) + 1, 5)
    return sortear_desafio(nivel=nivel_atual)

def validar_jogada(tecla, corretas):
    # Faz a ponte com o validador
    return verificar_resposta(tecla, corretas)

