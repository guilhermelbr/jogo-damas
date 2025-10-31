from jogo_damas import *
from constantes import *
import pygame

# --- Configurações Iniciais ---
pygame.init()

# Tamanho em pixels
TAMANHO_QUADRADO = 80 
LARGURA = TAM_TAB * TAMANHO_QUADRADO
ALTURA = TAM_TAB * TAMANHO_QUADRADO
TAMANHO_TELA = (LARGURA, ALTURA)

# Cores (em RGB)
COR_BEGE = (237, 232, 208)
COR_PRETA = (0, 0, 0)
COR_MARROM = (101, 67, 33)

COR_BRANCA_PECA = (240, 240, 240)  
COR_PRETA_PECA = (20, 20, 20)     
COR_BORDA = (101, 67, 33)          


tela = pygame.display.set_mode(TAMANHO_TELA)
pygame.display.set_caption("Jogo de Damas")

# --- Carregar Imagens ---

# Define o tamanho que a coroa terá na tela
RAIO_PECA = (TAMANHO_QUADRADO // 2) - 10  # 30 pixels
TAMANHO_COROA = int(RAIO_PECA * 1.5)     # 45 pixels

# Inicializa as imagens como None
IMG_COROA_PRETA = None
IMG_COROA_BRANCA = None

try:
    # Carrega a Coroa PRETA (apenas load, pygame deve gerenciar a transparência do PNG)
    IMG_COROA_PRETA_ORIG = pygame.image.load('queen_black.png')
    IMG_COROA_PRETA = pygame.transform.scale(IMG_COROA_PRETA_ORIG, (TAMANHO_COROA, TAMANHO_COROA))
except FileNotFoundError:
    print("AVISO: 'queen_black.png' (Coroa Preta) não encontrada. Dama preta será 'DP'.")
except pygame.error as e: # Adicionado para capturar outros erros de imagem
    print(f"ERRO ao carregar 'queen_black.png': {e}. Dama preta será 'DP'.")

try:
    # Carrega a Coroa BRANCA (apenas load, pygame deve gerenciar a transparência do PNG)
    IMG_COROA_BRANCA_ORIG = pygame.image.load('queen_white.png')
    IMG_COROA_BRANCA = pygame.transform.scale(IMG_COROA_BRANCA_ORIG, (TAMANHO_COROA, TAMANHO_COROA))
except FileNotFoundError:
    print("AVISO: 'queen_white.png' (Coroa Branca) não encontrada. Dama branca será 'DB'.")
except pygame.error as e: # Adicionado para capturar outros erros de imagem
    print(f"ERRO ao carregar 'queen_white.png': {e}. Dama branca será 'DB'.")


# --- Funções de Desenho ---

def desenha_tabuleiro(tab):
    """Desenha as casas do tabuleiro na tela."""
    tela.fill(COR_BEGE) # Pinta o fundo
    for linha in range(TAM_TAB):
        for col in range(TAM_TAB):
            # (linha + col) % 2 == 1 significa que é uma casa "jogável" (escura)
            if (linha + col) % 2 == 1:
                cor = COR_MARROM
            else:
                cor = COR_BEGE

            # Desenha o quadrado
            # (col * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO) -> Posição (x, y) do canto
            # (TAMANHO_QUADRADO, TAMANHO_QUADRADO) -> Largura e Altura
            pygame.draw.rect(tela, cor, (col * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
            #linha de cima é do gemini

def desenha_pecas(tab):
    """Varre o tabuleiro e desenha as peças (círculos) na tela."""
    
    raio = (TAMANHO_QUADRADO // 2) - 10 # Deixa uma margem de 10 pixels
    
    for linha in range(TAM_TAB):
        for col in range(TAM_TAB):
            peca = tab[linha][col]
            
            if peca == CASA_VAZIA:
                continue

            centro_x = col * TAMANHO_QUADRADO + (TAMANHO_QUADRADO // 2)
            centro_y = linha * TAMANHO_QUADRADO + (TAMANHO_QUADRADO // 2)
            
            
            # --- LÓGICA DE DESENHO CORRIGIDA ---
            
            if peca == PECA_BRANCA_DAMA:
                if IMG_COROA_BRANCA: 
                    # É DAMA BRANCA: Desenha SÓ a imagem da Dama Branca
                    img_rect = IMG_COROA_BRANCA.get_rect(center=(centro_x, centro_y))
                    tela.blit(IMG_COROA_BRANCA, img_rect)
                else:
                    # Fallback (Plano B se 'queen_white.png' não for encontrada)
                    pygame.draw.circle(tela, COR_BORDA, (centro_x, centro_y), raio + 2)
                    pygame.draw.circle(tela, COR_BRANCA_PECA, (centro_x, centro_y), raio)
                    fonte_dama = pygame.font.SysFont('Arial', 24, bold=True)
                    texto_surf = fonte_dama.render('DB', True, COR_PRETA_PECA)
                    texto_rect = texto_surf.get_rect(center=(centro_x, centro_y))
                    tela.blit(texto_surf, texto_rect)
            
            elif peca == PECA_PRETA_DAMA:
                if IMG_COROA_PRETA: 
                    # É DAMA PRETA: Desenha SÓ a imagem da Dama Preta
                    img_rect = IMG_COROA_PRETA.get_rect(center=(centro_x, centro_y))
                    tela.blit(IMG_COROA_PRETA, img_rect)
                else:
                    # Fallback (Plano B se 'queen_black.png' não for encontrada)
                    pygame.draw.circle(tela, COR_BORDA, (centro_x, centro_y), raio + 2)
                    pygame.draw.circle(tela, COR_PRETA_PECA, (centro_x, centro_y), raio)
                    fonte_dama = pygame.font.SysFont('Arial', 24, bold=True)
                    texto_surf = fonte_dama.render('DP', True, COR_BRANCA_PECA)
                    texto_rect = texto_surf.get_rect(center=(centro_x, centro_y))
                    tela.blit(texto_surf, texto_rect)
            
            else:
                # É UMA PEÇA NORMAL (NÃO-DAMA)
                # Define a cor do círculo da peça
                if peca == PECA_BRANCA:
                    cor_peca = COR_BRANCA_PECA
                else: # peca == PECA_PRETA
                    cor_peca = COR_PRETA_PECA
                
                # Desenha o círculo normal
                pygame.draw.circle(tela, COR_BORDA, (centro_x, centro_y), raio + 2)
                pygame.draw.circle(tela, cor_peca, (centro_x, centro_y), raio)


def main():
    tabuleiro = constroi_tabuleiro()
    turno = inicia_turno()
    
    # --- variáveis para controlar os cliques ---
    peca_selecionada = None  # Guarda a tupla (linha, col) da peça de origem
    origem_x, origem_y = -1, -1
    
    # --- Variáveis para o loop ---
    rodando = True
    clock = pygame.time.Clock()
    lances_sem_captura = 0 # Para a regra de empate

    while rodando:
        # --- 1. Checar Eventos do Usuário ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            # Detecta o clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Pega a posição (x, y) do clique em pixels
                x_mouse, y_mouse = pygame.mouse.get_pos()
                
                # Converte o clique (pixels) para (linha, coluna) do tabuleiro
                linha_clicada = y_mouse // TAMANHO_QUADRADO
                col_clicada = x_mouse // TAMANHO_QUADRADO
                
                # --- LÓGICA DA JOGADA ---
                
                if peca_selecionada is None:
                    # É O PRIMEIRO CLIQUE (SELEÇÃO DE ORIGEM)
                    peca = tabuleiro[linha_clicada][col_clicada]
                    
                    # Verifica se o jogador clicou em uma peça válida (dele mesmo)
                    if (turno == PECA_BRANCA and (peca == PECA_BRANCA or peca == PECA_BRANCA_DAMA)) or \
                       (turno == PECA_PRETA and (peca == PECA_PRETA or peca == PECA_PRETA_DAMA)):
                        
                        peca_selecionada = (linha_clicada, col_clicada)
                        origem_x, origem_y = linha_clicada, col_clicada
                        print(f"Peça selecionada: ({origem_x + 1}, {origem_y + 1})")
                    else:
                        print("Casa vazia ou peça do adversário. Selecione sua peça.")
                
                else:
                    # É O SEGUNDO CLIQUE (SELEÇÃO DE DESTINO)
                    destino_x, destino_y = linha_clicada, col_clicada
                    print(f"Destino selecionado: ({destino_x + 1}, {destino_y + 1})")

                    try:
                        # Tenta realizar a jogada usando o seu motor de regras!
                        # (Vamos usar a versão 3 do 'joga', que retorna duas coisas)
                        jogada_valida, foi_captura = joga(tabuleiro, turno, origem_x, origem_y, destino_x, destino_y)
                        
                        if jogada_valida:
                            # --- A JOGADA FOI VÁLIDA ---
                            
                            # Atualiza contador de empate
                            if foi_captura:
                                lances_sem_captura = 0
                            else:
                                lances_sem_captura += 1
                                
                            # Verifica se o jogo acabou
                            resultado = acabou(tabuleiro, turno, lances_sem_captura)
                            if resultado is not None:
                                print(f"FIM DE JOGO! Vencedor: {resultado}")
                                # (Aqui você pode desenhar o vencedor na tela)
                                rodando = False # Por enquanto, só fecha o jogo
                            
                            # Troca o turno
                            turno = troca_turno(turno)
                            
                        else:
                            print("Jogada inválida. Tente novamente.")
                    
                    except ValueError as erro:
                        # Isso pega os erros que sua função joga() levanta
                        print(f"Erro: {erro}. Tente novamente.")
                    
                    # Limpa a seleção para a próxima jogada
                    peca_selecionada = None
                    origem_x, origem_y = -1, -1


        # --- 2. Desenhar a Tela ---
        desenha_tabuleiro(tabuleiro)  # Desenha os quadrados
        desenha_pecas(tabuleiro)      # Desenha as peças
        
        # (Opcional) Desenha um destaque na peça selecionada
        if peca_selecionada is not None:
            linha, col = peca_selecionada
            # Desenha um retângulo verde em volta da peça selecionada
            pygame.draw.rect(tela, (0, 255, 0), (col * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 4)

        # --- 3. Atualizar a Tela ---
        pygame.display.flip() 
        clock.tick(60)
        
    pygame.quit()



if __name__ == "__main__":
    main()