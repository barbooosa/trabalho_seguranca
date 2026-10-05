# Criptografia Clássica — Implementações em Python

Repositório acadêmico voltado ao estudo prático dos fundamentos da segurança da informação e da criptografia clássica. O projeto implementa em Python quatro das cifras mais emblemáticas da história, divididas em duas grandes famílias: **cifras de substituição** e **cifras de transposição**.

Este documento reúne a fundamentação teórica, a análise linha por linha de cada script do repositório, exemplos práticos reais passo a passo, tabela comparativa, guia de execução e um roteiro completo de perguntas e respostas para apresentações e avaliações.

---

## 📌 Sumário
1. [Conceitos Fundamentais](#-1-conceitos-fundamentais)
   - [As Duas Famílias Clássicas (Substituição vs. Transposição)](#as-duas-famílias-clássicas)
   - [Mapeamento Letra $\leftrightarrow$ Número](#mapeamento-letra--número)
   - [Aritmética Modular (`% 26`)](#aritmética-modular--26)
   - [Confusão e Difusão (Shannon)](#confusão-e-difusão-shannon)
2. [Estrutura Comum dos Programas](#-2-estrutura-comum-dos-programas)
3. [Análise Detalhada Linha por Linha e Exemplos Reais](#-3-análise-detalhada-linha-por-linha-e-exemplos-reais)
   - [3.1 Cifra de César (`cesar.py`)](#31-cifra-de-césar-cesarpy)
   - [3.2 Cifra de Vigenère (`vigenere.py`)](#32-cifra-de-vigenère-vigenerepy)
   - [3.3 Cifra de Substituição Monoalfabética (`substituicao.py`)](#33-cifra-de-substituição-monoalfabética-substituicaopy)
   - [3.4 Cifra de Transposição Colunar (`transposicao.py`)](#34-cifra-de-transposição-colunar-transposicaopy)
4. [Tabela Comparativa dos Métodos](#-4-tabela-comparativa-dos-métodos)
5. [Relação com a Criptografia Moderna (AES)](#-5-relação-com-a-criptografia-moderna-aes)
6. [Como Executar os Scripts](#-6-como-executar-os-scripts)
7. [Perguntas e Respostas para Apresentação / Banca](#-7-perguntas-e-respostas-para-apresentação--banca)

---

## 🧠 1. Conceitos Fundamentais

### As Duas Famílias Clássicas
Toda a criptografia clássica pode ser classificada em duas técnicas essenciais:
* **Substituição:** Mantém as posições originais das letras intactas na frase, mas substitui cada caractere por outro (ou por símbolos/números). Exemplos: *Cifra de César*, *Cifra de Vigenère* e *Substituição Monoalfabética*.
* **Transposição:** Mantém intacta a identidade das letras originais da mensagem, mas altera a ordem física em que elas aparecem (embaralhamento espacial). Exemplo: *Transposição Colunar*.

### Mapeamento Letra $\leftrightarrow$ Número
Na criptografia em código, o alfabeto canônico de 26 letras maiúsculas ($A$ a $Z$) é indexado matematicamente de $0$ a $25$:

| Letra | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Índice** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |

No código Python:
* `alfabeto.index("I")` retorna `8`.
* `alfabeto[8]` retorna `"I"`.

### Aritmética Modular (`% 26`)
O operador de resto da divisão (`% 26`) garante o comportamento circular do alfabeto (efeito carrossel). Se somarmos ou subtrairmos uma chave e o valor ultrapassar o fim do alfabeto ($Z = 25$), a conta recomeça em $A = 0$:
$$\text{Exemplo (Avanço): } \text{Y}\,(24) + 3 = 27 \implies 27 \pmod{26} = 1 \implies \text{B}$$
$$\text{Exemplo (Retrocesso): } \text{B}\,(1) - 3 = -2 \implies -2 \pmod{26} = 24 \implies \text{Y}$$

> **Nota técnica:** Em Python, o operador `%` sobre números negativos calcula o resto matemático euclidiano: `(-2) % 26 == 24`. Isso torna a decifração extremamente simples e elegante sem precisar de condicionais manuais.

### Confusão e Difusão (Shannon)
Em 1949, o matemático Claude Shannon demonstrou que um sistema criptográfico seguro requer duas propriedades fundamentais:
1. **Confusão:** Dificultar ao máximo descobrir a relação entre a chave secreta e o texto cifrado. Cifras de substituição operam gerando confusão.
2. **Difusão:** Espalhar a estrutura estatística do texto claro por todo o texto cifrado, para que a redundância da mensagem seja diluída. Cifras de transposição operam gerando difusão.

---

## 🖥️ 2. Estrutura Comum dos Programas

Todos os quatro programas (`cesar.py`, `vigenere.py`, `substituicao.py`, `transposicao.py`) seguem uma arquitetura padronizada:
1. **Função `criptografar(texto, chave)`:** Recebe o texto limpo e o segredo, retornando o texto cifrado.
2. **Função `descriptografar(texto, chave)`:** Recebe o texto cifrado e o segredo, revertendo a operação e retornando o texto original.
3. **Tratamento de texto:** Utilização de `.upper()` para normalizar todas as entradas em letras maiúsculas. Caracteres que não sejam letras (como espaços e pontuações) são preservados sem corrupção.
4. **Interface de linha de comando com `while True:`:** Apresenta um menu interativo que só é interrompido quando o usuário digita a opção de saída (`break`).

---

## 🔍 3. Análise Detalhada Linha por Linha e Exemplos Reais

---

### 3.1 Cifra de César (`cesar.py`)

#### Conceito
A Cifra de César é uma técnica de substituição monoalfabética onde cada caractere do texto é deslocado por um valor constante fixo no alfabeto. A chave é esse número inteiro.

#### Código Completo e Explicação Linha por Linha

```python
1: # Cifra de Cesar
2: # cada letra anda X posicoes no alfabeto (X = chave)
3: 
4: alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```
* **Linhas 1-2:** Comentários descrevendo a ideia da cifra.
* **Linha 4:** Declaração da string com as 26 letras em maiúsculo, indexadas de 0 (`A`) a 25 (`Z`).

```python
7: def criptografar(texto, chave):
8:     texto = texto.upper()
9:     resultado = ""
10:     for letra in texto:
11:         if letra in alfabeto:
12:             posicao = alfabeto.index(letra)
13:             nova_posicao = (posicao + chave) % 26
14:             resultado = resultado + alfabeto[nova_posicao]
15:         else:
16:             resultado = resultado + letra
17:     return resultado
```
* **Linha 7:** Definição da função `criptografar` com parâmetros `texto` e `chave`.
* **Linha 8 (`texto = texto.upper()`):** Converte o texto para letras maiúsculas para manter compatibilidade com a string `alfabeto`.
* **Linha 9 (`resultado = ""`):** Cria uma string vazia para acumular o texto processado.
* **Linha 10 (`for letra in texto:`):** Laço que percorre cada caractere da mensagem um por um.
* **Linha 11 (`if letra in alfabeto:`):** Valida se o caractere atual é uma letra do alfabeto.
* **Linha 12 (`posicao = alfabeto.index(letra)`):** Descobre a posição numérica atual da letra no alfabeto (0 a 25).
* **Linha 13 (`nova_posicao = (posicao + chave) % 26`):** Desloca a letra somando o valor da chave e aplica o módulo 26 para reiniciar em A quando ultrapassar Z.
* **Linha 14 (`resultado = resultado + alfabeto[nova_posicao]`):** Busca a letra na nova posição e concatena ao resultado.
* **Linhas 15-16 (`else: resultado = resultado + letra`):** Se for espaço, número ou símbolo de pontuação, mantém o caractere original inalterado.
* **Linha 17 (`return resultado`):** Devolve a string criptografada ao chamador.

```python
20: def descriptografar(texto, chave):
21:     texto = texto.upper()
22:     resultado = ""
23:     for letra in texto:
24:         if letra in alfabeto:
25:             posicao = alfabeto.index(letra)
26:             nova_posicao = (posicao - chave) % 26
27:             resultado = resultado + alfabeto[nova_posicao]
28:         else:
29:             resultado = resultado + letra
30:     return resultado
```
* **Linhas 20-25 e 27-30:** Estrutura idêntica à de criptografia.
* **Linha 26 (`nova_posicao = (posicao - chave) % 26`):** Realiza a operação inversa: subtrai a chave para fazer a letra recuar no alfabeto até a posição original.

```python
33: print("--- CIFRA DE CESAR ---")
34: 
35: while True:
36:     print()
37:     print("1 - Criptografar")
38:     print("2 - Descriptografar")
39:     print("3 - Sair")
40:     opcao = input("Escolha: ")
41: 
42:     if opcao == "3":
43:         print("Saindo...")
44:         break
45:     elif opcao == "1" or opcao == "2":
46:         texto = input("Digite o texto: ")
47:         chave = int(input("Digite a chave (numero): "))
48:         if opcao == "1":
49:             print("Texto cifrado:", criptografar(texto, chave))
50:         else:
51:             print("Texto original:", descriptografar(texto, chave))
52:     else:
53:         print("Opcao invalida")
```
* **Linha 35 (`while True:`):** Loop infinito que exibe o menu até comando de saída.
* **Linhas 36-40:** Mostra opções e lê a escolha do usuário via terminal.
* **Linhas 42-44:** Se a opção digitada for `"3"`, exibe mensagem e executa `break` para fechar o programa.
* **Linhas 45-47:** Se a opção for `"1"` ou `"2"`, lê o texto e converte a chave informada para número inteiro com `int()`.
* **Linhas 48-51:** Executa `criptografar` ou `descriptografar` conforme a opção e imprime o resultado.
* **Linhas 52-53:** Caso seja digitada uma opção inexistente, exibe `"Opcao invalida"` e retorna ao início do menu.

#### Exemplo Real Passo a Passo
* **Texto claro:** `ATAQUE`
* **Chave:** `3`

| Letra Clara | Posição ($P$) | Cálculo: $(P + 3) \pmod{26}$ | Nova Posição | Letra Cifrada |
|:---:|:---:|:---:|:---:|:---:|
| **A** | 0 | $(0 + 3) \pmod{26} = 3$ | 3 | **D** |
| **T** | 19 | $(19 + 3) \pmod{26} = 22$ | 22 | **W** |
| **A** | 0 | $(0 + 3) \pmod{26} = 3$ | 3 | **D** |
| **Q** | 16 | $(16 + 3) \pmod{26} = 19$ | 19 | **T** |
| **U** | 20 | $(20 + 3) \pmod{26} = 23$ | 23 | **X** |
| **E** | 4 | $(4 + 3) \pmod{26} = 7$ | 7 | **H** |

* **Resultado Cifrado:** `DWDTXH`
* **Decifração:** Ao subtrair 3: $D\,(3) - 3 = 0 \implies A$, restaurando `ATAQUE`.

---

### 3.2 Cifra de Vigenère (`vigenere.py`)

#### Conceito
A Cifra de Vigenère é uma cifra de substituição **polialfabética**. Diferente de César, cada letra do texto sofre um deslocamento diferente, determinado pelas letras de uma palavra-chave (senha). Se a mensagem for mais longa que a senha, a senha é repetida ciclicamente.

#### Código Completo e Explicação Linha por Linha

```python
1: # Cifra de Vigenere
2: # parecida com a de Cesar, mas cada letra usa um deslocamento diferente,
3: # que vem da letra da senha naquela posicao
4: 
5: alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```
* **Linhas 1-5:** Comentários introdutórios e definição da lista ordenada de letras.

```python
8: def criptografar(texto, senha):
9:     texto = texto.upper()
10:     senha = senha.upper()
11:     resultado = ""
12:     i = 0  # posicao atual na senha
13:     for letra in texto:
14:         if letra in alfabeto:
15:             pos_letra = alfabeto.index(letra)
16:             pos_senha = alfabeto.index(senha[i % len(senha)])
17:             nova_posicao = (pos_letra + pos_senha) % 26
18:             resultado = resultado + alfabeto[nova_posicao]
19:             i = i + 1
20:         else:
21:             resultado = resultado + letra
22:     return resultado
```
* **Linha 8:** Define a função com parâmetros `texto` e `senha`.
* **Linhas 9-10:** Converte ambos para letras maiúsculas.
* **Linha 11:** Inicializa a string `resultado`.
* **Linha 12 (`i = 0`):** Cria um contador de posições para a senha.
* **Linha 13 (`for letra in texto:`):** Itera sobre os caracteres da mensagem.
* **Linha 14 (`if letra in alfabeto:`):** Checa se o caractere atual é uma letra alfabética.
* **Linha 15 (`pos_letra = alfabeto.index(letra)`):** Identifica a posição da letra do texto no alfabeto.
* **Linha 16 (`pos_senha = alfabeto.index(senha[i % len(senha)])`):** **Linha central do algoritmo.** O operador `i % len(senha)` repete a senha ciclicamente. Se a senha tem 4 letras (`COMP`), para $i = 0, 1, 2, 3, 4, 5$, os índices na senha serão $0, 1, 2, 3, 0, 1$. Em seguida, obtém a posição numérica dessa letra da senha.
* **Linha 17 (`nova_posicao = (pos_letra + pos_senha) % 26`):** Soma o deslocamento da senha à letra da frase com aritmética modular.
* **Linha 18 (`resultado = resultado + alfabeto[nova_posicao]`):** Adiciona o caractere criptografado ao resultado.
* **Linha 19 (`i = i + 1`):** Avança o ponteiro da senha para a próxima letra.
* **Linhas 20-21 (`else: resultado = resultado + letra`):** Preserva espaços e pontuações sem mexer no contador `i`, mantendo o alinhamento da senha.
* **Linha 22:** Retorna o texto cifrado.

```python
25: def descriptografar(texto, senha):
26:     texto = texto.upper()
27:     senha = senha.upper()
28:     resultado = ""
29:     i = 0
30:     for letra in texto:
31:         if letra in alfabeto:
32:             pos_letra = alfabeto.index(letra)
33:             pos_senha = alfabeto.index(senha[i % len(senha)])
34:             nova_posicao = (pos_letra - pos_senha) % 26
35:             resultado = resultado + alfabeto[nova_posicao]
36:             i = i + 1
37:         else:
38:             resultado = resultado + letra
39:     return resultado
```
* **Linhas 25-33 e 35-39:** Estrutura idêntica à de cifragem.
* **Linha 34 (`nova_posicao = (pos_letra - pos_senha) % 26`):** Subtrai o valor da senha da letra cifrada para desfazer a rotação e restaurar o texto original.

```python
42: print("--- CIFRA DE VIGENERE ---")
44: while True:
...
56:         senha = input("Digite a senha (so letras): ")
...
```
* **Linhas 42-62:** Menu interativo que solicita a senha em formato textual e aciona a cifragem ou decifragem.

#### Exemplo Real Passo a Passo
* **Texto claro:** `INFO`
* **Senha:** `COMP`

| Índice $i$ | Letra Frase | Pos. Frase ($P$) | Letra Senha | Pos. Senha ($K$) | Conta: $(P + K) \pmod{26}$ | Letra Cifrada |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | **I** | 8 | **C** | 2 | $(8 + 2) \pmod{26} = 10$ | **K** |
| 1 | **N** | 13 | **O** | 14 | $(13 + 14) = 27 \pmod{26} = 1$ | **B** |
| 2 | **F** | 5 | **M** | 12 | $(5 + 12) \pmod{26} = 17$ | **R** |
| 3 | **O** | 14 | **P** | 15 | $(14 + 15) = 29 \pmod{26} = 3$ | **D** |

* **Resultado Cifrado:** `KBRD`
* **Analogia da Tabela de Vigenère (Batalha Naval no Excel):** A letra da mensagem é a linha ($I = \text{linha 10}$), a letra da senha é a coluna ($C = \text{coluna D}$) e a letra cifrada é o cruzamento da célula `D10` = `K`.

---

### 3.3 Cifra de Substituição Monoalfabética (`substituicao.py`)

#### Conceito
Em vez de utilizar uma fórmula matemática com rotação periódica, esta técnica utiliza uma **permutação arbitrária de todas as 26 letras do alfabeto**. Cada letra original é mapeada para uma letra fixa da chave embaralhada.

#### Código Completo e Explicação Linha por Linha

```python
1: alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```
* **Linha 1:** Alfabeto padrão ordenado.

```python
4: def chave_valida(chave):
5:     if len(chave) != 26:
6:         return False
7:     for letra in alfabeto:
8:         if letra not in chave:
9:             return False
10:     return True
```
* **Linha 4:** Função que avalia se a chave fornecida pelo usuário é matematicamente válida para cifragem e decifragem bijetora.
* **Linhas 5-6 (`if len(chave) != 26:`):** Se a chave não contiver exatamente 26 caracteres, retorna `False`.
* **Linhas 7-9 (`for letra in alfabeto: if letra not in chave:`):** Percorre as 26 letras do alfabeto padrão e verifica se alguma delas está ausente na chave. Se faltar qualquer letra (o que também indica que outra está repetida), retorna `False`.
* **Linha 10 (`return True`):** Se atender aos dois critérios, a chave é uma permutação válida do alfabeto.

```python
13: def criptografar(texto, chave):
14:     texto = texto.upper()
15:     resultado = ""
16:     for letra in texto:
17:         if letra in alfabeto:
18:             posicao = alfabeto.index(letra)
19:             resultado = resultado + chave[posicao]
20:         else:
21:             resultado = resultado + letra
22:     return resultado
```
* **Linha 18 (`posicao = alfabeto.index(letra)`):** Identifica a posição da letra da frase dentro do alfabeto padrão normal.
* **Linha 19 (`resultado = resultado + chave[posicao]`):** Substitui diretamente pelo caractere que ocupa o mesmo índice na string `chave`. Não envolve cálculos numéricos ou módulo, é uma troca direta por mapa de substituição.
* **Linhas 20-21:** Preserva caracteres especiais.

```python
25: def descriptografar(texto, chave):
26:     texto = texto.upper()
27:     resultado = ""
28:     for letra in texto:
29:         if letra in chave:
30:             posicao = chave.index(letra)
31:             resultado = resultado + alfabeto[posicao]
32:         else:
33:             resultado = resultado + letra
34:     return resultado
```
* **Linha 29 (`if letra in chave:`):** Confere se a letra cifrada pertence à chave.
* **Linha 30 (`posicao = chave.index(letra)`):** Localiza em que posição a letra cifrada está na chave secreta.
* **Linha 31 (`resultado = resultado + alfabeto[posicao]`):** Recupera a letra correspondente do alfabeto oficial ordenado na mesma posição.

```python
37: print("--- CIFRA DE SUBSTITUICAO MONOALFABETICA ---")
38: print("Exemplo de chave: QWERTYUIOPASDFGHJKLZXCVBNM")
...
52:         chave = input("Digite a chave (26 letras sem repetir): ").upper()
53:         if not chave_valida(chave):
54:             print("Chave invalida! Precisa ter as 26 letras, sem repetir.")
...
```
* **Linhas 37-60:** Menu interativo com a chamada obrigatória à função `chave_valida(chave)` para impedir falhas de mapeamento antes de criptografar ou descriptografar.

#### Exemplo Real Passo a Passo
* **Alfabeto padrão:** `A B C D E F G H I J K L M N O P Q R S T U V W X Y Z`
* **Chave:** `Q W E R T Y U I O P A S D F G H J K L Z X C V B N M`
* **Texto claro:** `SEGURANCA`

Mapeando caractere por caractere:
* `S` (índice 18) $\to$ chave[18] = **`L`**
* `E` (índice 4) $\to$ chave[4] = **`T`**
* `G` (índice 6) $\to$ chave[6] = **`U`**
* `U` (índice 20) $\to$ chave[20] = **`X`**
* `R` (índice 17) $\to$ chave[17] = **`K`**
* `A` (índice 0) $\to$ chave[0] = **`Q`**
* `N` (índice 13) $\to$ chave[13] = **`F`**
* `C` (índice 2) $\to$ chave[2] = **`E`**
* `A` (índice 0) $\to$ chave[0] = **`Q`**

* **Resultado Cifrado:** `LTUXKQFEQ`

---

### 3.4 Cifra de Transposição Colunar (`transposicao.py`)

#### Conceito
Diferente das anteriores, esta cifra **não troca nenhuma letra por outra**. Ela escreve a mensagem horizontalmente em uma grade retangular com número fixo de colunas (a chave) e depois lê verticalmente coluna por coluna, embaralhando a ordem espacial do texto.

#### Código Completo e Explicação Linha por Linha

```python
1: def criptografar(texto, chave):
2:     texto = texto.upper()
3:     # completa com # para fechar todas as linhas
4:     while len(texto) % chave != 0:
5:         texto = texto + "#"
6: 
7:     resultado = ""
8:     for coluna in range(chave):
9:         posicao = coluna
10:         while posicao < len(texto):
11:             resultado = resultado + texto[posicao]
12:             posicao = posicao + chave
13:     return resultado
```
* **Linha 1:** Define `criptografar` recebendo a mensagem e a quantidade de colunas (`chave`).
* **Linhas 4-5 (*Padding*):** Se o total de letras da mensagem não for divisível pelo número de colunas (`len(texto) % chave != 0`), concatena o caractere `#` até completar a última linha da matriz.
* **Linha 8 (`for coluna in range(chave):`):** Itera coluna a coluna, da coluna 0 até `chave - 1`.
* **Linhas 9-12:** Para cada coluna, começa no índice inicial `posicao = coluna` e salta de `chave` em `chave` posições (`posicao = posicao + chave`), lendo verticalmente todas as linhas daquela coluna.
* **Linha 13:** Retorna a junção de todas as colunas lidas.

```python
16: def descriptografar(texto, chave):
17:     texto = texto.upper()
18:     linhas = len(texto) // chave
19: 
20:     resultado = ""
21:     for linha in range(linhas):
22:         for coluna in range(chave):
23:             resultado = resultado + texto[coluna * linhas + linha]
24: 
25:     # tira os # que foram colocados na criptografia
26:     resultado = resultado.replace("#", "")
27:     return resultado
```
* **Linha 18 (`linhas = len(texto) // chave`):** Descobre quantas linhas a grade possui, dividindo o tamanho total do texto cifrado pelo número de colunas.
* **Linhas 21-23:** Reconstitui a leitura original horizontal (linha por linha, da esquerda para a direita). No texto cifrado, cada coluna completa ocupa um bloco sequencial contíguo de tamanho `linhas`. Portanto, a letra da linha `L` e coluna `C` é calculada com:
$$\text{Índice} = \text{coluna} \times \text{linhas} + \text{linha}$$
* **Linha 26 (`resultado.replace("#", "")`):** Remove todos os caracteres `#` inseridos durante a cifragem.
* **Linha 27:** Retorna o texto original restaurado.

```python
30: print("--- CIFRA DE TRANSPOSICAO COLUNAR ---")
...
44:         chave = int(input("Digite a chave (numero de colunas): "))
...
```
* **Linhas 30-50:** Menu interativo padronizado recebendo a chave como número inteiro de colunas.

#### Exemplo Real 1 (Sem Padding)
* **Texto claro:** `SEGURANCA` (9 letras)
* **Chave:** `3` (colunas) $\to$ Matriz $3 \times 3$:

| Coluna 0 | Coluna 1 | Coluna 2 |
|:---:|:---:|:---:|
| **S** | **E** | **G** |
| **U** | **R** | **A** |
| **N** | **C** | **A** |

* Leitura vertical por colunas:
  * Coluna 0: `S` + `U` + `N` = `SUN`
  * Coluna 1: `E` + `R` + `C` = `ERC`
  * Coluna 2: `G` + `A` + `A` = `GAA`
* **Resultado Cifrado:** `SUNERCGAA`

#### Exemplo Real 2 (Com Padding `#`)
* **Texto claro:** `COMPUTADOR` (10 letras)
* **Chave:** `4` colunas.
* $10 \pmod 4 = 2$ (não é zero). O algoritmo adiciona dois `#` para fechar em 12 caracteres: `COMPUTADOR##`.

Grade $3 \times 4$:
```
C  O  M  P
U  T  A  D
O  R  #  #
```
* Coluna 0: `CUO` | Coluna 1: `OTR` | Coluna 2: `MA#` | Coluna 3: `PD#`
* **Cifrado:** `CUOOTRMA#PD#`
* Na decifração, a grade é reconstruída e o `.replace("#", "")` elimina os `#`, devolvendo `COMPUTADOR`.

---

## 📊 4. Tabela Comparativa dos Métodos

| Cifra | Família | O que é modificado? | Formato da Chave | Espaço de Chaves Possíveis | Principal Forma de Quebra |
|---|---|---|---|---|---|
| **César** | Substituição Monoalfabética | A identidade da letra (todas andam igual) | Número inteiro ($1 \dots 25$) | 25 chaves | **Força Bruta** (testar as 25 chaves em instantes) |
| **Vigenère** | Substituição Polialfabética | A identidade da letra (cada uma anda diferente) | Palavra/Texto (ex: `COMP`) | $26^L$ ($L$ = tamanho da senha) | **Teste de Kasiski + Análise de Frequência por blocos** |
| **Substituição** | Substituição Monoalfabética Geral | A identidade da letra (alfabeto embaralhado) | Permutação de 26 letras | $26! \approx 4 \times 10^{26}$ | **Análise de Frequência de Letras e Dígrafos** |
| **Transposição** | Transposição (Permutação Espacial) | A posição física da letra no texto | Número inteiro (quantidade de colunas) | Limitado (divisores e tamanhos de grade) | **Anagramas e Testagem de Dimensões de Grade** |

---

## 🛡️ 5. Relação com a Criptografia Moderna (AES)

Por que o estudo de cifras clássicas é indispensável se nenhuma delas oferece segurança militar nos dias de hoje?

Porque os algoritmos criptográficos modernos mais seguros do mundo (como o **AES - Advanced Encryption Standard**, empregado em certificados SSL/TLS, redes Wi-Fi WPA3 e bancos) combinam exatamente as mesmas duas primitivas clássicas:
* A etapa **`SubBytes`** do AES é uma substituição não linear implementada através de tabelas chamadas *S-Boxes* (**Confusão**).
* As etapas **`ShiftRows`** e **`MixColumns`** do AES realizam permutações espaciais e operações matriciais sobre os bytes (**Difusão**).

A diferença crucial é que o AES realiza essa combinação sucessiva de substituições e transposições por 10, 12 ou 14 rodadas (*rounds*), operando sobre blocos de bits com chaves criptográficas de 128, 192 ou 256 bits.

---

## 💻 6. Como Executar os Scripts

### Pré-requisitos
* Ter o Python 3 instalado no computador.

### Comandos de Execução
No terminal (PowerShell, CMD ou Bash), navegue até a pasta do projeto e execute o script desejado:

```bash
# Executar a Cifra de César
python cesar.py

# Executar a Cifra de Vigenère
python vigenere.py

# Executar a Cifra de Substituição Monoalfabética
python substituicao.py

# Executar a Cifra de Transposição Colunar
python transposicao.py
```

### Dica para Demonstração em Apresentação
1. Escolha a opção `1` para criptografar uma frase de exemplo.
2. Copie o resultado cifrado exibido no console.
3. No mesmo menu, escolha a opção `2`, cole a mensagem cifrada e informe a mesma chave para comprovar a descriptografia perfeita em tempo real.

---

## ❓ 7. Perguntas e Respostas para Apresentação / Banca

Abaixo estão reunidas as respostas detalhadas para as perguntas do PDF de referência e eventuais questionamentos de examinadores:

#### Q1. Para que serve o `% 26` nos códigos de César e Vigenère?
**Resposta:** Serve para implementar a aritmética modular do alfabeto. Como o alfabeto tem 26 letras (posições 0 a 25), o operador `% 26` faz o alfabeto se comportar como um círculo: ao ultrapassar a letra `Z` (índice 25), o cálculo dá a volta e recomeça na letra `A` (índice 0). Por exemplo: `Y (24) + 3 = 27`, e `27 % 26 = 1 (letra B)`.

#### Q2. Qual a diferença conceitual entre a Cifra de César e a Cifra de Vigenère?
**Resposta:** A Cifra de César é **monoalfabética**: todas as letras da mensagem sofrem rigorosamente o mesmo deslocamento fixo. A Cifra de Vigenère é **polialfabética**: cada letra sofre um deslocamento diferente, determinado pelas letras da palavra-chave (senha) naquela posição, que se repete ciclicamente.

#### Q3. Por que a Cifra de César é considerada fraca e insegura?
**Resposta:** Porque existem apenas 25 chaves úteis possíveis (já que deslocamentos de 0 ou 26 deixam o texto inalterado). Um atacante consegue testar todas as 25 chaves em poucos segundos através de um ataque de **força bruta**, seja manualmente ou por computador.

#### Q4. Por que a Cifra de Substituição Monoalfabética é quebrável mesmo tendo cerca de 400 septilhões de chaves ($26!$)?
**Resposta:** Porque a força bruta não é a única forma de quebrar uma cifra. Como cada letra clara sempre se transforma na mesma letra cifrada ao longo de todo o texto, a frequência natural das letras do idioma é preservada. Um analista compara a frequência das letras cifradas com a frequência média da língua (no português, **A**, **E**, **O** são as mais frequentes) e deduz as trocas rapidamente por **análise de frequência**.

#### Q5. O que diferencia a Transposição das outras três cifras?
**Resposta:** As outras três cifras são de **substituição** (trocam a identidade do caractere, mantendo sua posição). A transposição é uma cifra de **permutação espacial**: ela não altera nenhuma letra, apenas modifica a ordem em que elas estão posicionadas na mensagem.

#### Q6. Por que o código de transposição utiliza o caractere `#`?
**Resposta:** O `#` serve como preenchimento (*padding*). Como a transposição organiza a mensagem em uma matriz retangular de tamanho fixo, caso o número total de letras não seja múltiplo do número de colunas, a última linha ficaria incompleta. O `#` completa a grade para permitir a leitura das colunas. Na descriptografia, a função `.replace("#", "")` remove os marcadores automaticamente.

#### Q7. O que acontece com espaços, pontuações e números nos scripts de substituição?
**Resposta:** Os códigos contam com a condicional `if letra in alfabeto:`. Caracteres que não pertençam ao alfabeto padrão (como espaços, números e pontuações) caem no bloco `else:` e são mantidos como estão. Além disso, em Vigenère, o índice da chave `i` só avança quando uma letra válida é cifrada, impedindo que espaços causem desalinhamento da senha.

#### Q8. Como o programa repete o menu de opções?
**Resposta:** O programa utiliza a estrutura `while True:`, que cria uma repetição contínua. Ele só é encerrado quando o usuário escolhe a opção `"3"`, que aciona o comando `break`. Se o usuário digitar qualquer outra opção fora do esperado, o bloco `else:` imprime `"Opcao invalida"` e o menu é reapresentado sem travar ou fechar o programa.

#### Q9. Qual a diferença entre a Cifra de Vigenère e a variante Beaufort citada no PDF?
**Resposta:** Em Vigenère, a cifragem soma as posições $(\text{letra} + \text{senha}) \pmod{26}$ e a decifragem subtrai $(\text{letra} - \text{senha}) \pmod{26}$. Na Cifra de Beaufort, a operação é invertida: calcula-se $(\text{senha} - \text{letra}) \pmod{26}$ tanto para cifrar quanto para decifrar. Isso torna a Cifra de Beaufort recíproca (involutória), usando exatamente o mesmo algoritmo nos dois sentidos.

#### Q10. O que aconteceria se a chave de Vigenère tivesse o tamanho da mensagem e fosse verdadeiramente aleatória?
**Resposta:** A cifra se tornaria a **Cifra de Vernam**, popularmente conhecida como **One-Time Pad** (bloco de uso único). O One-Time Pad é o único sistema criptográfico comprovadamente com **segurança incondicional perfeita** (teorema de Claude Shannon), pois torna impossível para qualquer computador deduzir a mensagem original, já que todos os textos claros de mesmo tamanho são estatisticamente equiprováveis.

#### Q11. Como um criptoanalista quebra a Cifra de Vigenère historicamente?
**Resposta:** Através do **Exame de Kasiski** ou do **Índice de Coincidência de Friedman**. Identificam-se sequências de letras repetidas no texto cifrado para descobrir a distância entre elas e encontrar os divisores comuns, revelando o tamanho da senha. Descoberto o tamanho da senha $L$, a mensagem é dividida em $L$ grupos independentes, cada um dos quais é quebrado como uma Cifra de César simples por análise de frequência.
