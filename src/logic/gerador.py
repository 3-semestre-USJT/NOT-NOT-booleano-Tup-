from random import choice 

def sortear_desafio(nivel=1): 
    # nivel=1 porque começa aqui. Não precisa declarar os outros, o Python já vai atualizando conforme os pontos
    # O nome disso é Default Argument 

    direcoes = ['UP', 'DOWN', 'LEFT', 'RIGHT' ] # As direcoes possiveis
    alvo = choice(direcoes) # Escolhe uma das direcoes para ser o alvo

# nivel 1 tem só NOT
    if nivel == 1:
        NOT = choice([True, False]) # Decidindo se vai ter NOT ou não

        if NOT:
            return {
                'texto': f'! {alvo}', 
                'corretas': [d for d in direcoes if d != alvo] # Escolhe todas as direcoes diferente da do alvo
            }               # "O que guarda" for "O que é avaliado" in direcoes  
                            # O nome dessa parada é List Comprehension
        
        return { 'texto': alvo, 'corretas': [alvo] }
    
# nivel 2 tem OR 
    elif nivel == 2:
        # sortear duas direcoes diferentes
        alvo2 = choice([d for d in direcoes if d != alvo])
        return {
            'texto': f'{alvo} OR {alvo2}',
            'corretas': [alvo, alvo2]
        }

    # Mistura NOT com OR
    elif nivel == 3:
        # Duas direçoes proibidas foram sorteadas antes
        proibida1 = alvo # Já sorteado lá em cima
        proibida2 = choice([d for d in direcoes if d != proibida1])

        return {
            'texto': f'! ({proibida1} OR {proibida2})',
            # EX de texto: " ! (UP OR DOWN)"
            'corretas': [d for d in direcoes if d != proibida1 and d != proibida2]
            # Pega as direções que não são as proibidas 
        }
    
    # Adicioina o AND
    elif nivel == 4:
        alvo1 = alvo
        alvo2 = choice([d for d in direcoes if d != alvo1])

        return {
            'texto': f'! {alvo1} AND ! {alvo2}',
            'corretas': [d for d in direcoes if d != alvo1 and d != alvo2]
        }
    
    # Mistura tudo
    elif nivel >= 5:
        tipo = choice(['dupla_negacao', 'complexa', 'tripla'])

        if tipo == 'dupla_negacao':
            # Ex: ! ! UP 
            return {
                'texto': f'! ! {alvo}',
                'corretas': [alvo]
            }
        elif tipo == 'complexa':
            # Ex: ! (! UP AND DOWN) = UP, LEFT or RIGHT
            alvo2 = choice([d for d in direcoes if d != alvo])
            return {
                'texto': f'! (! {alvo} AND {alvo2})',
                'corretas': [d for d in direcoes if not (d != alvo and d == alvo2)]
            }
        else: # Tripla
            # Ex: ! ! ! UP = DOWN, LEFT or RIGHT
            return {
                'texto': f'! ! ! {alvo}',
                'corretas': [d for d in direcoes if d != alvo]
            }



