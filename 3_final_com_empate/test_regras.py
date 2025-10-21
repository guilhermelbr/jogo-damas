# Importa as funções e constantes do seu arquivo jogo_damas
# O "." antes de jogo_damas significa "do mesmo diretório"
from jogo_damas import troca_turno, PECA_BRANCA, PECA_PRETA
# O nome da função de teste DEVE começar com "test_"
def test_troca_turno_de_branca_para_preta():
    # "assert" significa "afirmar que". O teste passa se a afirmação for verdadeira.
    assert troca_turno(PECA_BRANCA) == PECA_PRETA

def test_troca_turno_de_preta_para_branca():
    assert troca_turno(PECA_PRETA) == PECA_BRANCA

# Você pode adicionar mais testes aqui, como test_jogada_simples, test_captura, etc.