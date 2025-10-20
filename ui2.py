"""
Módulo que faz a interface com o usuário
"""
from jogo_damas2 import *
from constantes import *
from termcolor import colored

def imprime_tabuleiro(tab):
    """
    Imprime um tabuleiro com cores de fundo para diferenciar as casas.
    :param tab: O tabuleiro a ser impresso.
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
    Verifica se uma jogada de damas tem um formato 'xyzw', onde
    'xy' é a coordenada de origem e 'zw' é a coordenada de destino.
    :param j: Um string que representa a jogada.
    :return: True se o formato for válido, False caso contrário.
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
        print(colored(f"Jogador {t}, é a sua vez!", "green"))
        print("Digite a jogada no formato COCD, onde CO é a coordenada de origem e CD a de destino:")
        print("Exemplo: '3243' moveria a peça de (3,2) para (4,3).")
        jogada = input()
        if jogada_formato_valido(jogada):
            break
        print(colored("Jogada fora do formato correto (ex: 3243)!", "red"))
        imprime_tabuleiro(tab)
    
    #-1 para converter a jogada de 1-8 para 0-7
    origem_x = int(jogada[0]) - 1 
    origem_y = int(jogada[1]) - 1
    destino_x = int(jogada[2]) - 1
    destino_y = int(jogada[3]) - 1
    
    return origem_x, origem_y, destino_x, destino_y

def main():
    """
    Função principal que gerencia o fluxo do jogo.
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
                print(colored("Jogada inválida! Tente novamente.", "red"))

        except ValueError as erro:
            print(colored(f"Erro: {erro}", "red"))

    imprime_tabuleiro(tabuleiro)
    if resultado == EMPATE:
        print(colored("O jogo empatou!", "blue"))
    else:
        print(colored(f"Jogador {resultado} ganhou!", "blue"))

if __name__ == "__main__":
    main()