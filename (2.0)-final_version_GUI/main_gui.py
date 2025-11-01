"""
Module that provides the user interface.
"""
from checkers_game import *
from constants import *
import pygame

# --- Initial Settings ---
pygame.init()

# Size in pixels
TAMANHO_QUADRADO = 80 
LARGURA = TAM_TAB * TAMANHO_QUADRADO
ALTURA = TAM_TAB * TAMANHO_QUADRADO
TAMANHO_TELA = (LARGURA, ALTURA)

# Colors (in RGB)
COR_BEGE = (237, 232, 208)
COR_PRETA = (0, 0, 0)
COR_MARROM = (101, 67, 33)

COR_BRANCA_PECA = (240, 240, 240)  
COR_PRETA_PECA = (20, 20, 20)     
COR_BORDA = (101, 67, 33)          


tela = pygame.display.set_mode(TAMANHO_TELA)
pygame.display.set_caption("Checkers Game")

# --- Upload Images ---

# Defines the size the crown will have on the screen
RAIO_PECA = (TAMANHO_QUADRADO // 2) - 10  # 30 pixels
TAMANHO_COROA = int(RAIO_PECA * 1.5)     # 45 pixels

# Initialize the images as None
IMG_COROA_PRETA = None
IMG_COROA_BRANCA = None

try:
    # Loads the BLACK crown (load only, pygame should handle the PNG transparency)
    IMG_COROA_PRETA_ORIG = pygame.image.load('kings/king_black.png')
    IMG_COROA_PRETA = pygame.transform.scale(IMG_COROA_PRETA_ORIG, (TAMANHO_COROA, TAMANHO_COROA))
except FileNotFoundError:
    print("WARNING: 'king_black.png' (Black Crown) not found. Black king will be 'BK'.")
except pygame.error as e: # Added to capture other image errors
    print(f"ERROR loading 'king_black.png': {e}. Black King will be 'BK'.")

try:
    # Loads the WHITE crown (load only, pygame should handle the PNG transparency)
    IMG_COROA_BRANCA_ORIG = pygame.image.load('kings/king_white.png')
    IMG_COROA_BRANCA = pygame.transform.scale(IMG_COROA_BRANCA_ORIG, (TAMANHO_COROA, TAMANHO_COROA))
except FileNotFoundError:
    print("WARNING: 'king_white.png' (white Crown) not found. white king will be 'WK'.")
except pygame.error as e: # Added to capture other image errors
    print(f"ERROR loading 'king_white.png': {e}. White King will be 'WK'.")


# --- Drawing Functions ---

def desenha_tabuleiro(tab):
    """Draw the houses of the game board on the screen."""
    tela.fill(COR_BEGE) # Paint the background
    for linha in range(TAM_TAB):
        for col in range(TAM_TAB):
            # (row + column) % 2 == 1 means it's a "playable" (dark) square
            if (linha + col) % 2 == 1:
                cor = COR_MARROM
            else:
                cor = COR_BEGE

            # Draws the square
            # (with * SQUARE_SIZE, line * SQUARE_SIZE) -> Position (x, y) of the corner
            # (SQUARE_SIZE, SQUARE_SIZE) -> Width and Height
            pygame.draw.rect(tela, cor, (col * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

def desenha_pecas(tab):
    """Clear the board and draw the pieces (circles) on the screen."""
    
    raio = (TAMANHO_QUADRADO // 2) - 10 # Leave a margin of 10 pixels
    
    for linha in range(TAM_TAB):
        for col in range(TAM_TAB):
            peca = tab[linha][col]
            
            if peca == CASA_VAZIA:
                continue

            centro_x = col * TAMANHO_QUADRADO + (TAMANHO_QUADRADO // 2)
            centro_y = linha * TAMANHO_QUADRADO + (TAMANHO_QUADRADO // 2)
            
            if peca == PECA_BRANCA_DAMA:
                if IMG_COROA_BRANCA: 
                    img_rect = IMG_COROA_BRANCA.get_rect(center=(centro_x, centro_y))
                    tela.blit(IMG_COROA_BRANCA, img_rect)
                else:
                    pygame.draw.circle(tela, COR_BORDA, (centro_x, centro_y), raio + 2)
                    pygame.draw.circle(tela, COR_BRANCA_PECA, (centro_x, centro_y), raio)
                    fonte_dama = pygame.font.SysFont('Arial', 24, bold=True)
                    texto_surf = fonte_dama.render('WK', True, COR_PRETA_PECA)
                    texto_rect = texto_surf.get_rect(center=(centro_x, centro_y))
                    tela.blit(texto_surf, texto_rect)
            
            elif peca == PECA_PRETA_DAMA:
                if IMG_COROA_PRETA: 
                    img_rect = IMG_COROA_PRETA.get_rect(center=(centro_x, centro_y))
                    tela.blit(IMG_COROA_PRETA, img_rect)
                else:
                    pygame.draw.circle(tela, COR_BORDA, (centro_x, centro_y), raio + 2)
                    pygame.draw.circle(tela, COR_PRETA_PECA, (centro_x, centro_y), raio)
                    fonte_dama = pygame.font.SysFont('Arial', 24, bold=True)
                    texto_surf = fonte_dama.render('bk', True, COR_BRANCA_PECA)
                    texto_rect = texto_surf.get_rect(center=(centro_x, centro_y))
                    tela.blit(texto_surf, texto_rect)
            
            else:
                if peca == PECA_BRANCA:
                    cor_peca = COR_BRANCA_PECA
                else: 
                    cor_peca = COR_PRETA_PECA
                
                pygame.draw.circle(tela, COR_BORDA, (centro_x, centro_y), raio + 2)
                pygame.draw.circle(tela, cor_peca, (centro_x, centro_y), raio)


def main():
    tabuleiro = constroi_tabuleiro()
    turno = inicia_turno()
    
    peca_selecionada = None
    origem_x, origem_y = -1, -1
    
    rodando = True
    clock = pygame.time.Clock()
    lances_sem_captura = 0 

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                linha_clicada = y_mouse // TAMANHO_QUADRADO
                col_clicada = x_mouse // TAMANHO_QUADRADO
                
                
                if peca_selecionada is None:
                    peca = tabuleiro[linha_clicada][col_clicada]
                    if (turno == PECA_BRANCA and (peca == PECA_BRANCA or peca == PECA_BRANCA_DAMA)) or \
                       (turno == PECA_PRETA and (peca == PECA_PRETA or peca == PECA_PRETA_DAMA)):
                        
                        peca_selecionada = (linha_clicada, col_clicada)
                        origem_x, origem_y = linha_clicada, col_clicada
                        print(f"Checker selected: ({origem_x + 1}, {origem_y + 1})")
                    else:
                        print("Empty square or opponent's piece. Select your piece.")
                
                else:
                    destino_x, destino_y = linha_clicada, col_clicada
                    print(f"Selected destination: ({destino_x + 1}, {destino_y + 1})")

                    try:
                        jogada_valida, foi_captura = joga(tabuleiro, turno, origem_x, origem_y, destino_x, destino_y)
                        
                        if jogada_valida:
                            if foi_captura:
                                lances_sem_captura = 0
                            else:
                                lances_sem_captura += 1
                                
                            resultado = acabou(tabuleiro, turno, lances_sem_captura)
                            if resultado is not None:
                                print(f"END GAME! Winner: {resultado}")
                                rodando = False 
                        
                            turno = troca_turno(turno)
                            
                        else:
                            print("Invalid move. Please try again.")
                    
                    except ValueError as erro:
                        print(f"Erro: {erro}. Please try again.")
                    
                    peca_selecionada = None
                    origem_x, origem_y = -1, -1


        desenha_tabuleiro(tabuleiro)  
        desenha_pecas(tabuleiro) 
        
        if peca_selecionada is not None:
            linha, col = peca_selecionada
            pygame.draw.rect(tela, (139, 0, 0), (col * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 4)
       
        pygame.display.flip() 
        clock.tick(60)
        
    pygame.quit()



if __name__ == "__main__":
    main()