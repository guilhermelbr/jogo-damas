"""
Esse módulo provê funções para levar a efeito um jogo de damas.
A interface deve usar essas funções para:
- Operar sobre o tabuleiro
- Operar sobre o turno dos jogadores
- Garantir as condições iniciais do jogo
- Verificar as condições de término do jogo

"""

from constantes import *

def constroi_tabuleiro():
    """
    Constroi um tabuleiro em formato de uma matriz de ordem constantes.TAM_TAB
    :return: Uma matriz que representa o tabuleiro
    """
    tab = []
    for i in range(TAM_TAB):
        linha = []
        for j in range(TAM_TAB):
            if (i + j) % 2 == 1:
                if i < 3:
                    linha.append(PECA_BRANCA)
                elif i > 4:
                    linha.append(PECA_PRETA)
                else:
                    linha.append(CASA_VAZIA)
            else:
                linha.append(CASA_VAZIA)
        tab.append(linha)
    return tab
    
def inicia_turno():
    """
    Escolhe o jogador de peça branca para iniciar a partida
    :return: JOG1
    """
    return PECA_BRANCA 

def troca_turno(turno):
    """
    Troca o turno dos jogadores
    :param turno: Um string que representa o jogador atual
    :return: Um string que representa o outro jogador para o qual o turno vai ser trocado
    """
    return PECA_PRETA if turno == PECA_BRANCA else PECA_BRANCA

def jogada_simples(tab, origem_x, origem_y, destino_x, destino_y):
    """
    Verifica se uma jogada é um movimento simples válido para a peça em questão.
    :param tab: O tabuleiro atual.
    :param origem_x: A linha da peça a ser movida.
    :param origem_y: A coluna da peça a ser movida.
    :param destino_x: A linha de destino da peça.
    :param destino_y: A coluna de destino da peça.
    :return: True se a jogada for válida (movimento de 1 casa na diagonal), False caso contrário.
    """
    peca_origem = tab[origem_x][origem_y]
    dist_x = destino_x - origem_x
    dist_y = destino_y - origem_y

    if peca_origem == PECA_BRANCA:
        return dist_x == 1 and abs(dist_y) == 1 #abs é de absoluto(se o valor absoluto da equa distancia = 1 ok)
    if peca_origem == PECA_PRETA:
        return dist_x == -1 and abs(dist_y) == 1 #abs é de absoluto(se o valor absoluto da equa distancia = 1 ok)

    if peca_origem == PECA_BRANCA_DAMA or peca_origem == PECA_PRETA_DAMA:
        if abs(dist_x) != abs(dist_y) or abs(dist_x) == 0: #verifica se esta se movendo na diagonal e se nao esta digitando a mesma casa
            return False
            
        passo_x = 1 if dist_x > 0 else -1 #indicam a direcao dos passos
        passo_y = 1 if dist_y > 0 else -1 #indicam a direcao dos passos
        
        for i in range(1, abs(dist_x)): # vai rodar o loop a quantidade = a equa distancia
            x_atual = origem_x + i * passo_x #pega a cordenada de origem e soma com (passo(que é 1 ou -1) + o i do loop)
            y_atual = origem_y + i * passo_y
            if tab[x_atual][y_atual] != CASA_VAZIA: #isso nao se trata se ver se a jogada é valida, e sim se é simples ou captura
                return False
        
        return True
    
    return False

def jogada_captura(tab, turno, origem_x, origem_y, destino_x, destino_y):
    """
    Verifica se uma jogada é uma captura válida.
    Para peças normais, a captura é um movimento de 2 casas na diagonal.
    Para damas, a captura é um movimento de longo alcance sobre uma única peça do adversário.
    :param tab: O tabuleiro atual.
    :param turno: O jogador da vez.
    :param origem_x: A linha da peça a ser movida.
    :param origem_y: A coluna da peça a ser movida.
    :param destino_x: A linha de destino da peça.
    :param destino_y: A coluna de destino da peça.
    :return: True se a jogada for uma captura válida, False caso contrário.
    """
    peca_origem = tab[origem_x][origem_y]
    dist_x = destino_x - origem_x
    dist_y = destino_y - origem_y
    adversario = PECA_PRETA if turno == PECA_BRANCA else PECA_BRANCA
    adversario_dama = PECA_PRETA_DAMA if turno == PECA_BRANCA else PECA_BRANCA_DAMA
      
    # Lógica para peças normais
    if peca_origem == PECA_BRANCA:
        if dist_x != 2 or abs(dist_y) != 2:
            return False
        meio_x = (origem_x + destino_x) // 2
        meio_y = (origem_y + destino_y) // 2
        peca_meio = tab[meio_x][meio_y]
        destino_vazio = False   
        if tab[destino_x][destino_y] == CASA_VAZIA:
            destino_vazio = True
        return (peca_meio == adversario or peca_meio == adversario_dama) and destino_vazio
    
    if peca_origem == PECA_PRETA:
        if dist_x != -2 or abs(dist_y) != 2:
            return False
        meio_x = (origem_x + destino_x) // 2
        meio_y = (origem_y + destino_y) // 2
        peca_meio = tab[meio_x][meio_y]
        destino_vazio = False   
        if tab[destino_x][destino_y] == CASA_VAZIA:
            destino_vazio = True
        return (peca_meio == adversario or peca_meio == adversario_dama) and destino_vazio
    
    # Lógica para damas
    if peca_origem == PECA_BRANCA_DAMA or peca_origem == PECA_PRETA_DAMA:
        if abs(dist_x) != abs(dist_y) or abs(dist_x) < 2:
            return False

        passo_x = 1 if dist_x > 0 else -1
        passo_y = 1 if dist_y > 0 else -1
        
        peca_capturada_encontrada = False
        
        for i in range(1, abs(dist_x)):
            x_atual = origem_x + i * passo_x
            y_atual = origem_y + i * passo_y
            peca_no_caminho = tab[x_atual][y_atual]
            
            if peca_no_caminho == peca_origem or \
               (turno == PECA_BRANCA and peca_no_caminho == PECA_BRANCA) or \
               (turno == PECA_PRETA and peca_no_caminho == PECA_PRETA):
                return False
            
            if (peca_no_caminho == adversario or peca_no_caminho == adversario_dama):
                if peca_capturada_encontrada: #se isso for True, significa que ja tem uma peca capturada no caminho entao essa é a segunda.
                    return False
                peca_capturada_encontrada = True #usando como regra que a dama so captura uma peca por jogada#
            
        return peca_capturada_encontrada and tab[destino_x][destino_y] == CASA_VAZIA

    return False


def promove_peca(tab, destino_x, destino_y, peca):
    """
    Verifica se uma peça normal alcançou a última linha do tabuleiro e a promove a dama.
    :param tab: O tabuleiro atual.
    :param destino_x: A linha de destino da peça.
    :param destino_y: A coluna de destino da peça.
    :param peca: O tipo de peça a ser verificada (normal branca ou preta).
    :return: Retorna o novo tipo de peça (dama) se houve promoção, caso contrário, retorna a peça original.
    """
    if peca == PECA_BRANCA and destino_x == TAM_TAB - 1: #verifica se a peca branca chegou na ultima linha (linha 8, indice 7)
        tab[destino_x][destino_y] = PECA_BRANCA_DAMA
        return PECA_BRANCA_DAMA
    elif peca == PECA_PRETA and destino_x == 0:
        tab[destino_x][destino_y] = PECA_PRETA_DAMA
        return PECA_PRETA_DAMA
    return peca # Retorna a peça original se não houver promoção


def joga(tab, turno, origem_x, origem_y, destino_x, destino_y):
    """ 
    Realiza uma jogada completa do jogador da vez, validando e executando o movimento.
    :param tab: O tabuleiro atual.
    :param turno: O jogador da vez.
    :param origem_x: A linha da peça a ser movida.
    :param origem_y: A coluna da peça a ser movida.
    :param destino_x: A linha de destino da peça.
    :param destino_y: A coluna de destino da peça.
    :return: True se a jogada foi feita com sucesso, False se a jogada for inválida.
    :raises ValueError: Se a jogada for para fora do tabuleiro, de uma casa vazia, não for a peça do jogador, ou para uma casa de destino ocupada.
    """
    
    if not (0 <= origem_x < TAM_TAB and 0 <= origem_y < TAM_TAB and
            0 <= destino_x < TAM_TAB and 0 <= destino_y < TAM_TAB):
        raise ValueError("Jogada fora do tabuleiro!") #raise interromper a execução do programa e sinalizar que algo deu errado
                                        
    peca_origem = tab[origem_x][origem_y]
    if peca_origem == CASA_VAZIA:
        raise ValueError("Casa de origem vazia!") #O ValueError é usado para indicar que uma função recebeu um argumento com um valor inválido. TypeError tipo errado


    if turno == PECA_BRANCA and not (peca_origem == PECA_BRANCA or peca_origem == PECA_BRANCA_DAMA):
        raise ValueError("Essa não é sua peça!")

    if turno == PECA_PRETA and not (peca_origem == PECA_PRETA or peca_origem == PECA_PRETA_DAMA):
        raise ValueError("Essa não é sua peça!")

    if tab[destino_x][destino_y] != CASA_VAZIA:
        raise ValueError("Casa de destino ocupada!")

    if jogada_captura(tab, turno, origem_x, origem_y, destino_x, destino_y):
        tab[destino_x][destino_y] = peca_origem
        tab[origem_x][origem_y] = CASA_VAZIA

        passo_x = 1 if destino_x > origem_x else -1  #inicio do processo para remover a peça capturada
        passo_y = 1 if destino_y > origem_y else -1

        for i in range(1, abs(destino_x - origem_x)):
            x_atual = origem_x + i * passo_x
            y_atual = origem_y + i * passo_y
            if tab[x_atual][y_atual] != CASA_VAZIA:
                tab[x_atual][y_atual] = CASA_VAZIA
                break

        # se o promove_peca() retornar damas nessa jogadas atualizamos o tabuleiro
        nova_peca = promove_peca(tab, destino_x, destino_y, peca_origem)
        tab[destino_x][destino_y] = nova_peca

        return True

    if jogada_simples(tab, origem_x, origem_y, destino_x, destino_y):
        tab[destino_x][destino_y] = peca_origem
        tab[origem_x][origem_y] = CASA_VAZIA
        
        # se o promove_peca() retornar damas nessa jogadas atualizamos o tabuleiro
        nova_peca = promove_peca(tab, destino_x, destino_y, peca_origem)
        tab[destino_x][destino_y] = nova_peca

        return True

    return False


def verifica_vitoria(tab, turno):
    """
    Verifica se o jogador atual venceu o jogo, checando se não há mais peças do adversário no tabuleiro.
    :param tab: O tabuleiro atual.
    :param jogador: O jogador que está sendo verificado.
    :return: True se o jogador venceu, False caso contrário.
    """
    adversario = PECA_PRETA if turno == PECA_BRANCA else PECA_BRANCA
    adversario_dama = PECA_PRETA_DAMA if adversario == PECA_PRETA else PECA_BRANCA_DAMA
    
    for linha in tab:
        for peca in linha:
            if peca == adversario or peca == adversario_dama:
                return False
    
    return True


def acabou(tab, turno):
    """
    Determina se o jogo chegou ao fim.
    :param tab: O tabuleiro atual.
    :param turno: O jogador da vez.
    :return: O valor do jogador que venceu (PECA_BRANCA ou PECA_PRETA) se o jogo acabou, ou None se o jogo continua.
    """
    if verifica_vitoria(tab, turno):
        return turno
    
    return None








