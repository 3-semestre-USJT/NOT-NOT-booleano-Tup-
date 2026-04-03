import json
import os

class GerenciadorPontuacao:
    """
    Responsável por toda a lógica numérica, multiplicadores e 
    persistência de recordes do jogo.
    """
    
    def __init__(self, caminho_save="save.json"):
        self.caminho_save = caminho_save
        
        # Estado atual da partida
        self.score = 0
        self.combo = 0
        self.multiplicador = 1
        
        # Configurações de Balanceamento
        self.PONTOS_BASE = 100
        self.ACERTOS_PARA_LEVEL_UP = 5
        self.TEMPO_INICIAL = 5.0
        self.TEMPO_MINIMO = 0.8
        
        # Carrega o recorde histórico
        self.high_score = self.carregar_recorde()

    def registrar_acerto(self):
        """Incrementa pontos e gerencia o multiplicador de combo."""
        self.combo += 1
        
        # A cada 5 acertos, o multiplicador aumenta (1x -> 2x -> 3x...)
        if self.combo % self.ACERTOS_PARA_LEVEL_UP == 0:
            self.multiplicador += 1
            
        self.score += self.PONTOS_BASE * self.multiplicador

    def calcular_tempo_limite(self) -> float:
        """
        Calcula o tempo disponível para a próxima jogada.
        A dificuldade aumenta (tempo diminui) conforme o score sobe.
        """
        # Reduz 0.3s a cada 1000 pontos acumulados
        reducao = (self.score // 1000) * 0.3
        tempo_calculado = self.TEMPO_INICIAL - reducao
        
        return max(tempo_calculado, self.TEMPO_MINIMO)

    def carregar_recorde(self) -> int:
        """Lê o recorde do arquivo JSON. Retorna 0 se o arquivo não existir."""
        if not os.path.exists(self.caminho_save):
            return 0
            
        try:
            with open(self.caminho_save, 'r') as arquivo:
                dados = json.load(arquivo)
                return dados.get("recorde_maximo", 0)
        except (json.JSONDecodeError, IOError):
            return 0

    def salvar_recorde(self):
        """Verifica se o score atual é o novo recorde e salva no disco."""
        if self.score > self.high_score:
            self.high_score = self.score
            dados = {"recorde_maximo": self.high_score}
            
            try:
                with open(self.caminho_save, 'w') as arquivo:
                    json.dump(dados, arquivo, indent=4)
            except IOError as erro:
                print(f"Erro ao salvar recorde: {erro}")

    def resetar_partida(self):
        """Reseta os valores para uma nova rodada (sem apagar o recorde)."""
        self.score = 0
        self.combo = 0
        self.multiplicador = 1