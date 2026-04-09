import json
import os

class GerenciadorPontuacao:
# Responsável por toda a lógica numérica, multiplicadores e persistência de recordes (Ranking Top 3) do jogo.
    
    def __init__(self):
        # Gerenciamento de caminhos para a pasta 'data'
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        raiz_projeto = os.path.dirname(os.path.dirname(base_dir))
        self.caminho_ranking = os.path.join(raiz_projeto, "data", "ranking.json")
        
        # Estado atual da partida
        self.score = 0
        self.combo = 0
        self.multiplicador = 1
        
        # Configurações de Balanceamento
        self.PONTOS_BASE = 100
        self.ACERTOS_PARA_LEVEL_UP = 5
        self.TEMPO_INICIAL = 5.0
        self.TEMPO_MINIMO = 0.8
        
        # Carrega o ranking e define o high_score como o 1º lugar da lista
        self.ranking = self.carregar_ranking()
        self.high_score = self.ranking[0]['pontos']

    def registrar_acerto(self):
        # Incrementa pontos e gerencia o multiplicador de combo.
        self.combo += 1
        
        # A cada 5 acertos, o multiplicador aumenta (1x -> 2x -> 3x...)
        if self.combo % self.ACERTOS_PARA_LEVEL_UP == 0:
            self.multiplicador += 1
            
        self.score += self.PONTOS_BASE * self.multiplicador

    def calcular_tempo_limite(self) -> float:
    # Calcula o tempo disponível para a próxima jogada. A dificuldade aumenta (tempo diminui) conforme o score sobe.
    # Reduz 0.3s a cada 1000 pontos acumulados
        reducao = (self.score // 1000) * 0.3
        tempo_calculado = self.TEMPO_INICIAL - reducao
        
        return max(tempo_calculado, self.TEMPO_MINIMO)

    def carregar_ranking(self) -> list:
        # Lê o ranking do arquivo JSON. Retorna lista padrão se não existir.
        if not os.path.exists(self.caminho_ranking):
            return [
                {"nome": "---", "pontos": 0},
                {"nome": "---", "pontos": 0},
                {"nome": "---", "pontos": 0}
            ]
            
        try:
            with open(self.caminho_ranking, 'r') as arquivo:
                return json.load(arquivo)
        except (json.JSONDecodeError, IOError):
            return [{"nome": "---", "pontos": 0}] * 3

    def verificar_novo_recorde(self) -> bool:
        # Retorna True se o score atual entrar no Top 3
        return self.score > self.ranking[-1]['pontos']

    def salvar_no_ranking(self, nome_iniciais):
        # Adiciona o novo recorde, ordena o Top 3 e salva no disco.
        # Adiciona a nova pontuação à lista
        self.ranking.append({"nome": nome_iniciais.upper(), "pontos": self.score})
        
        # Ordena do maior para o menor e mantém apenas os 3 melhores
        self.ranking = sorted(self.ranking, key=lambda x: x['pontos'], reverse=True)[:3]
        
        # Atualiza o high_score histórico para bater com o novo 1º lugar
        self.high_score = self.ranking[0]['pontos']
        
        try:
            # Garante que a pasta 'data' existe antes de salvar
            os.makedirs(os.path.dirname(self.caminho_ranking), exist_ok=True)
            with open(self.caminho_ranking, 'w') as arquivo:
                json.dump(self.ranking, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar ranking: {erro}")

    def resetar_partida(self):
        # Reseta os valores para uma nova rodada (sem apagar o recorde)
        self.score = 0
        self.combo = 0
        self.multiplicador = 1