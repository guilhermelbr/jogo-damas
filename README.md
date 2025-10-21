# PROJETO JOGO DAMAS

Este repositório contém a evolução de um jogo de Damas em Python, desde a versão base até a implementação de regras complexas como captura obrigatória e empate.

Cada pasta representa um "mini-projeto" independente que pode ser executado.

## Como Rodar este Projeto (Instruções)

Para executar qualquer uma das versões do jogo, você precisará ter o Python instalado e seguir estes passos:

1.  **Clone o repositório** (ou baixe os arquivos).
2.  **Crie um ambiente virtual** na pasta raiz:
    ```bash
    python -m venv .venv
    ```
3.  **Ative o ambiente virtual**:
    * No Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
    * No macOS/Linux: `source .venv/bin/activate`
4.  **Instale as dependências** (pacotes) necessárias:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Navegue e execute** a versão desejada. Por exemplo, para rodar a Versão 1 (jogo base):
    ```bash
    cd 1_jogo_base
    python ui.py
    ```
    *(Para rodar as outras versões, basta trocar o `cd` para `2_captura_obrigatoria` ou `3_final_com_empate`)*

## Versões do Projeto

Eu organizei o projeto em pastas para mostrar a progressão
(cada nova versão não exclui oque tinha na anterior):

### 1. `1_jogo_base`
Esta é a versão "neutra" e inicial do jogo. Contém:
* Movimentação simples de peças e damas.
* Captura simples (mas não obrigatória).
* promoção de peças quando atravessam o tabuleiro.
* Verificação de vitória por eliminação de peças.

### 2. `2_captura_obrigatoria`
Esta versão adiciona a regra de captura obrigatória, uma das principais mecânicas do jogo de Damas.
* O jogador é forçado a realizar uma captura se ela estiver disponível.

### 3. `3_final_com_empate`
Esta é a versão final e mais completa, que adiciona a regra de empate.
* A regra de captura obrigatória da Versão 2 está mantida.
* O jogo é declarado "Empate" se ocorrerem 40 lances consecutivos sem captura.
* Testes Automatizados: Contém o arquivo `test_regras.py` (usando `pytest`) para verificar as regras do jogo. Este teste é executado automaticamente pelo GitHub Actions (veja nota abaixo).

---
### Nota sobre os Arquivos do Repositório

* `.github/workflows`: Esta pasta contém o workflow de **Teste Automático (GitHub Actions)**. O arquivo `teste-python.yml` define um trabalho que, a cada `push`, instala o projeto e roda os testes (da pasta `3_final_com_empate`) em 3 versões diferentes do Python. Isso garante que o código funciona e não foi "quebrado" por uma nova mudança.
* `requirements.txt`: Lista todos os pacotes Python (como o `termcolor`) necessários para este projeto. O comando `pip install -r requirements.txt` usa este arquivo para instalar tudo de uma vez.
* `.gitignore`: Este é um arquivo de configuração do Git. Ele diz ao Git para ignorar arquivos locais (como o `.venv`), mantendo o repositório limpo e funcional para todos que o baixarem.