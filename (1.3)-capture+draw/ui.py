"""
Module that provides the user interface.
"""
from checkers_game import *
from constants import *
from termcolor import colored

def imprime_tabuleiro(tab):
    """
    Prints a board with background colors to differentiate the squares. 
    :param tab: The board to be printed.
    """
    print()
    print("   ", end="")
    for j in range(TAM_TAB):
        print(f" {j + 1} ", end="")
    print()

    for i in range(TAM_TAB):
        print(f" {i + 1} ", end="")
        for j in range(TAM_TAB):
            if (i + j) % 2 == 1:
                cor_fundo = 'on_grey'
            else:
                cor_fundo = 'on_white'
            
            peca = tab[i][j]
            cor_peca = 'white'
            
            if peca == PECA_PRETA or peca == PECA_PRETA_DAMA:
                cor_peca = 'red'
            elif peca == PECA_BRANCA or peca == PECA_BRANCA_DAMA:
                cor_peca = 'blue'
            else:
                peca = CASA_VAZIA
                cor_peca = 'white'

            print(colored(f" {peca} ", cor_peca, cor_fundo), end="")
        print()
    print()


def jogada_formato_valido(j):
    """
    Checks if a checkers move has the format 'xyzw', where
    'xy' is the origin coordinate and 'zw' is the destination coordinate. 
    :param j: A string representing the move. 
    :return: True if the format is valid, False otherwise.
    """
    return j.isnumeric() and len(j) == 4


def recebe_jogada(t, tab):
    """
    Recebe uma jogada de damas da entrada padrão.
    :param t: O turno do jogador (PECA_BRANCA ou PECA_PRETA).
    :param tab: O tabuleiro para que seja feita a impressão dele se a jogada for inválida.
    :return: As coordenadas de origem e destino (origem_x, origem_y, destino_x, destino_y).
    """
    while True:
        print()
        print(colored(f"player {t}, its your turn!", "green"))
        print("Enter your move in the format SCDC, where SC is the starting coordinate and DC is the destination coordinate:")
        print("Example: '3243' would move the piece from (3,2) to (4,3).")
        jogada = input()
        if jogada_formato_valido(jogada):
            break
        print(colored("Input entered in the wrong format (ex: 3243)!", "red"))
        imprime_tabuleiro(tab)
    
    #-1 para converter a jogada de 1-8 para 0-7
    origem_x = int(jogada[0]) - 1 
    origem_y = int(jogada[1]) - 1
    destino_x = int(jogada[2]) - 1
    destino_y = int(jogada[3]) - 1
    
    return origem_x, origem_y, destino_x, destino_y

def main():
    """
    The main function that manages the game flow.
    """
    tabuleiro = constroi_tabuleiro()
    turno = inicia_turno()
    resultado = None
    lances_sem_captura = 0  # Novo contador para a lógica de empate

    while True:
        imprime_tabuleiro(tabuleiro)
        
        origem_x, origem_y, destino_x, destino_y = recebe_jogada(turno, tabuleiro)
        
        try:
            jogada_valida, eh_captura = joga(tabuleiro, turno, origem_x, origem_y, destino_x, destino_y)
            
            if jogada_valida:
                if eh_captura:
                    lances_sem_captura = 0 # Zera o contador após uma captura ou promoção
                else:
                    lances_sem_captura += 1 # Incrementa se não foi captura
                
                resultado = acabou(tabuleiro, turno, lances_sem_captura)
                
                if resultado is not None:
                    break
                else:
                    turno = troca_turno(turno)
            else:
                print(colored("Invalid move. Please try again.", "red"))

        except ValueError as erro:
            print(colored(f"Erro: {erro}", "red"))

    imprime_tabuleiro(tabuleiro)
    if resultado == EMPATE:
        print(colored("The game ended in a tie!", "blue"))
    else:
        print(colored(f"Player {resultado} won!", "blue"))

if __name__ == "__main__":
    main()