"""
This module provides functions to implement a checkers game.
The interface should use these functions to:
- Operate on the game board
- Manage the players' turns
- Ensure the initial conditions of the game
- Check the game termination conditions
- Check the need for capture

"""

from constants import *

def constroi_tabuleiro():
    """
    Build a game board in the form of a matrix of constant order TAM_TAB.
    :return: A matrix representing the game board
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
    Choose the player with the white pieces to start the game.
    :return: PLAYER1
    """
    return PECA_BRANCA 

def troca_turno(turno):
    """
    Switches the turn between players
    :param turno: A string representing the current player
    :return: A string representing the other player to whom the turn will be switched
    """
    return PECA_PRETA if turno == PECA_BRANCA else PECA_BRANCA

def jogada_simples(tab, origem_x, origem_y, destino_x, destino_y):
    """
    Checks if a move is a valid simple move for the piece in question. 
    :param tab: The current board. 
    :param origem_x: The row of the piece to be moved. 
    :param origem_y: The column of the piece to be moved. 
    :param destino_x: The destination row of the piece. 
    :param destino_y: The destination column of the piece. 
    :return: True if the move is valid (1-square diagonal movement), False otherwise.
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
    Checks if a move is a valid capture. 
    For normal pieces, a capture is a 2-square diagonal move. 
    For kings (queens), a capture is a long-range move over a single opponent's piece. 
    :param tab: The current board. 
    :param turno: The current player. 
    :param origem_x: The row of the piece to be moved. 
    :param origem_y: The column of the piece to be moved. 
    :param destino_x: The destination row of the piece. 
    :param destino_y: The destination column of the piece. 
    :return: True if the move is a valid capture, False otherwise.
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




def captura_obrigatoria(tab, turno):
    """
    Checks if the current player has any capture moves available on the board. 
    :param tab: The current board. 
    :param turno: The current player (WHITE_PIECE or BLACK_PIECE). 
    :return: True if there is at least one possible capture, False otherwise.
    """
    for x in range(TAM_TAB):
        for y in range(TAM_TAB):
            peca = tab[x][y]
            
            # Checa se a peça na posição (x,y) pertence ao jogador atual
            if (turno == PECA_BRANCA and (peca == PECA_BRANCA or peca == PECA_BRANCA_DAMA)) or \
               (turno == PECA_PRETA and (peca == PECA_PRETA or peca == PECA_PRETA_DAMA)):
                
                # Para cada peça do jogador, verifica todas as 4 direções de captura
                for dx in [-2, 2]: # representa sempre a distancia de captura, que sao duas casas na diagonal
                    for dy in [-2, 2]:# representa sempre a distancia de captura, que sao duas casas na diagonal
                        destino_x = x + dx
                        destino_y = y + dy
                        
                        # Garante que a coordenada de destino está dentro do tabuleiro
                        if 0 <= destino_x < TAM_TAB and 0 <= destino_y < TAM_TAB:
                            
                            # Usa a função jogada_captura() para verificar se a jogada é válida
                            if jogada_captura(tab, turno, x, y, destino_x, destino_y):
                                return True  # Se uma captura for encontrada, retorna True imediatamente

    # Se o loop terminar sem encontrar nenhuma captura
    return False




def promove_peca(tab, destino_x, destino_y, peca):
    """
    Checks if a regular piece has reached the last row of the board and promotes it to a queen. 
    :param tab: The current board. 
    :param destino_x: The destination row of the piece. 
    :param destino_y: The destination column of the piece. 
    :param peca: The type of piece to be checked (white or black regular piece). 
    :return: Returns the new piece type (queen) if a promotion occurred, otherwise returns the original piece.
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
    Performs a complete move for the current player, validating and executing the movement. 
    :param tab: The current board. 
    :param turno: The current player. 
    :param origem_x: The row of the piece to be moved. 
    :param origem_y: The column of the piece to be moved. 
    :param destino_x: The destination row of the piece. 
    :param destino_y: The destination column of the piece. 
    :return: True if the move was successful, False if the move is invalid. 
    :raises ValueError: If the move is outside the board, from an empty square, not the player's piece, or to an occupied destination square.
    """
    if not (0 <= origem_x < TAM_TAB and 0 <= origem_y < TAM_TAB and
            0 <= destino_x < TAM_TAB and 0 <= destino_y < TAM_TAB):
        raise ValueError("Jogada fora do tabuleiro!")
                                
    peca_origem = tab[origem_x][origem_y]
    if peca_origem == CASA_VAZIA:
        raise ValueError("Casa de origem vazia!")

    if turno == PECA_BRANCA and not (peca_origem == PECA_BRANCA or peca_origem == PECA_BRANCA_DAMA):
        raise ValueError("Essa não é sua peça!")

    if turno == PECA_PRETA and not (peca_origem == PECA_PRETA or peca_origem == PECA_PRETA_DAMA):
        raise ValueError("Essa não é sua peça!")

    if tab[destino_x][destino_y] != CASA_VAZIA:
        raise ValueError("Casa de destino ocupada!")

    # 1. Tenta validar a jogada do usuário como uma captura.
    if jogada_captura(tab, turno, origem_x, origem_y, destino_x, destino_y):
        tab[destino_x][destino_y] = peca_origem
        tab[origem_x][origem_y] = CASA_VAZIA

        passo_x = 1 if destino_x > origem_x else -1
        passo_y = 1 if destino_y > origem_y else -1

        for i in range(1, abs(destino_x - origem_x)):
            x_atual = origem_x + i * passo_x
            y_atual = origem_y + i * passo_y
            if tab[x_atual][y_atual] != CASA_VAZIA:
                tab[x_atual][y_atual] = CASA_VAZIA
                break

        nova_peca = promove_peca(tab, destino_x, destino_y, peca_origem)
        tab[destino_x][destino_y] = nova_peca

        return True

    # 2. Se a jogada não foi uma captura, verifica se havia uma captura obrigatória no tabuleiro.
    if captura_obrigatoria(tab, turno):
        # Se houver captura obrigatória e a jogada não foi uma, a jogada é inválida.
        return False
    
    # 3. Se não houver captura obrigatória, tenta validar a jogada como um movimento simples.
    if jogada_simples(tab, origem_x, origem_y, destino_x, destino_y):
        tab[destino_x][destino_y] = peca_origem
        tab[origem_x][origem_y] = CASA_VAZIA
        
        nova_peca = promove_peca(tab, destino_x, destino_y, peca_origem)
        tab[destino_x][destino_y] = nova_peca

        return True

    # 4. Se nada acima for válido, a jogada é inválida.
    return False


def verifica_vitoria(tab, turno):
    """
    Checks if the current player has won the game by checking if there are no more of the opponent's pieces on the board. 
    :param tab: The current board. 
    :param jogador: The player being checked. 
    :return: True if the player has won, False otherwise.
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
    Determines if the game has ended. 
    :param tab: The current board. 
    :param turno: The current player. 
    :return: The value of the winning player (WHITE_PIECE or BLACK_PIECE) if the game is over, or None if the game continues.
    """
    if verifica_vitoria(tab, turno):
        return turno
    
    return None