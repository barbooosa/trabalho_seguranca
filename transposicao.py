def criptografar(texto, chave):
    texto = texto.upper()
    # completa com # para fechar todas as linhas
    while len(texto) % chave != 0:
        texto = texto + "#"

    resultado = ""
    for coluna in range(chave):
        posicao = coluna
        while posicao < len(texto):
            resultado = resultado + texto[posicao]
            posicao = posicao + chave
    return resultado


def descriptografar(texto, chave):
    texto = texto.upper()
    linhas = len(texto) // chave

    resultado = ""
    for linha in range(linhas):
        for coluna in range(chave):
            resultado = resultado + texto[coluna * linhas + linha]

    # tira os # que foram colocados na criptografia
    resultado = resultado.replace("#", "")
    return resultado


print("--- CIFRA DE TRANSPOSICAO COLUNAR ---")

while True:
    print()
    print("1 - Criptografar")
    print("2 - Descriptografar")
    print("3 - Sair")
    opcao = input("Escolha: ")

    if opcao == "3":
        print("Saindo...")
        break
    elif opcao == "1" or opcao == "2":
        texto = input("Digite o texto: ")
        chave = int(input("Digite a chave (numero de colunas): "))
        if opcao == "1":
            print("Texto cifrado:", criptografar(texto, chave))
        else:
            print("Texto original:", descriptografar(texto, chave))
    else:
        print("Opcao invalida")