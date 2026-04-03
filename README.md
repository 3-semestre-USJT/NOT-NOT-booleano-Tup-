# NOT NOT Booleano Tupã 

![Python](https://img.shields.io/badge/Python-3.12-blue.svg?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg?style=flat-square)
![USJT](https://img.shields.io/badge/USJT-3º_Semestre-red.svg?style=flat-square)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow.svg?style=flat-square)

## Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Como Jogar](#-como-jogar)
- [Instalação e Execução](#-instalação-e-execução)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Equipe Tupã](#-equipe-tupã)

## Sobre o Projeto
**NOT NOT Booleano Tupã** é um jogo de raciocínio lógico acelerado, desenvolvido como projeto acadêmico pela equipe Tupã (3º Semestre - USJT). Inspirado no clássico *Not Not*, o jogo testa a velocidade de interpretação de **Lógica Booleana** do jogador sob extrema pressão de tempo.

## Funcionalidades (Atuais)
* **Motor Lógico Dinâmico:** Geração de desafios booleanos em 5 níveis de dificuldade (Negações simples até leis de De Morgan).
* **Dificuldade Progressiva:** O tempo de resposta diminui gradativamente conforme a pontuação aumenta.
* **Sistema de Combo e Multiplicador:** Recompensa acertos consecutivos.
* **Persistência de Dados:** Salvamento automático do *High Score* local via JSON.

## Como Jogar
O cubo (ou texto central) exibirá uma instrução lógica (Ex: `! (UP OR DOWN)`). Você tem frações de segundo para processar a informação e pressionar a seta correspondente à direção **verdadeira** antes que o tempo esgote.
* **Setas do Teclado (`⬆️ ⬇️ ⬅️ ➡️`):** Movem o personagem/respondem ao desafio.
* **ENTER:** Inicia a partida.
* **R:** Reinicia após o Game Over.
* **ESC:** Retorna ao menu principal.

## Instalação e Execução

### Pré-requisitos
* Python 3.12 ou superior.
* Gerenciador de pacotes `pip`.

### Passo a passo
1. Clone o repositório:
   ```bash
   git clone [https://github.com/3-semestre-USJT/NOT-NOT-booleano-Tup-.git](https://github.com/3-semestre-USJT/NOT-NOT-booleano-Tup-.git)

 2. Crie e ative um ambiente virtual (Recomendado):
    python -m venv .venv
    source .venv/bin/activate  # No Windows use: .venv\Scripts\activate

3. Instale as dependências:
    pip install -r requirements.txt

4. Inicie o jogo: 
    python main.py

## Equipe Tupã
Projeto desenvolvido por 7 estudantes de Ciência da Computação / Análise e Desenvolvimento de Sistemas da Universidade São Judas Tadeu.