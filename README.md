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

### 3. `3_com_empate`
Esta é a versão final e mais completa, que adiciona a regra de empate.
* A regra de captura obrigatória da Versão 2 está mantida.
* O jogo é declarado "Empate" se ocorrerem 40 lances consecutivos sem captura.
* Testes Automatizados: Contém o arquivo `test_regras.py` (usando `pytest`) para verificar as regras do jogo. Este teste é executado automaticamente pelo GitHub Actions (veja nota abaixo).

---
### Nota sobre os Arquivos do Repositório

* `.github/workflows`: Esta pasta contém o workflow de **Teste Automático (GitHub Actions)**. O arquivo `teste-python.yml` define um trabalho que, a cada `push`, instala o projeto e roda os testes (da pasta `3_final_com_empate`) em 3 versões diferentes do Python. Isso garante que o código funciona e não foi "quebrado" por uma nova mudança.
* `requirements.txt`: Lista todos os pacotes Python (como o `termcolor`) necessários para este projeto. O comando `pip install -r requirements.txt` usa este arquivo para instalar tudo de uma vez.
* `.gitignore`: Este é um arquivo de configuração do Git. Ele diz ao Git para ignorar arquivos locais (como o `.venv`), mantendo o repositório limpo e funcional para todos que o baixarem.




# PROJETO JOGO DE DAMAS (com Interface Gráfica Pygame)

Este repositório contém a versão final de um jogo de Damas desenvolvido em Python, utilizando a biblioteca Pygame para criar uma interface gráfica do usuário (GUI) completa e interativa.

O projeto também documenta a evolução do desenvolvimento, incluindo as versões anteriores baseadas em terminal, que podem ser encontradas nas outras pastas `(1.x)`.

## Versão Final (2.0) - Interface Gráfica (GUI)

Esta é a versão principal e mais completa do projeto, localizada na pasta `(2.0)-versao_final_GUI/`.

### Funcionalidades
* **Interface Gráfica Completa:** O tabuleiro e as peças são renderizados em uma janela de aplicativo usando Pygame.
* **Controles Intuitivos:** Movimentação de peças via clique do mouse (selecionando a origem e o destino).
* **Lógica de Regras Completa:**
    * Movimentação simples de peças e damas.
    * **Captura Obrigatória:** O jogador é forçado a realizar uma captura se ela estiver disponível.
    * **Promoção para Dama:** Peças normais são promovidas a Damas ao alcançar o lado oposto, recebendo um ícone de coroa personalizado (das imagens `queen_black.png` e `queen_white.png`).
    * **Regra de Empate:** O jogo é declarado "Empate" se ocorrerem 40 lances consecutivos sem nenhuma captura.

## Como Rodar o Jogo (Versão 2.0 GUI)

1.  **Clone o repositório** para o seu computador.
2.  **Crie um ambiente virtual** na pasta raiz do projeto:
    ```bash
    python -m venv .venv
    ```
3.  **Ative o ambiente virtual**:
    * No Windows (PowerShell):
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
    * No macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
4.  **Instale as dependências** (pacotes) necessárias:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Navegue para a pasta da GUI e execute:**
    ```powershell
    cd "(2.0)-final_version_GUI"
    python main_gui.py
    ```

---
## Evolução do Projeto (Versões Anteriores de Terminal)

Este repositório também contém a evolução da lógica do jogo. **Cada pasta `(1.x)` representa um "mini-projeto" independente e executável (via terminal)**, mostrando a progressão das regras:

### 1. `(1.0)-game_base`
Esta é a versão "neutra" e inicial do jogo. Contém:
* Movimentação simples de peças e damas.
* Captura simples (mas não obrigatória).
* Promoção de peças quando atravessam o tabuleiro.
* Verificação de vitória por eliminação de peças.

### 2. `(1.2)-mandatory_capture`
Esta versão adiciona a regra de captura obrigatória, uma das principais mecânicas do jogo de Damas.
* O jogador é forçado a realizar uma captura se ela estiver disponível.

### 3. `(1.3)-capture+draw`
Esta é a versão final da lógica de terminal, que adiciona a regra de empate.
* A regra de captura obrigatória da Versão 2 está mantida.
* O jogo é declarado "Empate" se ocorrerem 40 lances consecutivos sem captura.

**Para rodar estas versões de terminal:** Após o Passo 4 (instalar dependências), navegue para a pasta desejada (ex: `cd "(1.3)-capture+draw"`) e execute `python ui.py`.

---
### Nota sobre os Arquivos do Repositório

* **`requirements.txt`**: Lista os pacotes Python (`pygame`, `termcolor`) necessários para rodar todos os projetos.
* **`.gitignore`**: Um arquivo de configuração do Git que o instrui a ignorar arquivos e pastas locais (como `.venv` e `__pycache__`), mantendo o repositório limpo e funcional para todos que o baixarem.