alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def chave_valida(chave):
    if len(chave) != 26:
        return False
    for letra in alfabeto:
        if letra not in chave:
            return False
    return True


def criptografar(texto, chave):
    texto = texto.upper()
    resultado = ""
    for letra in texto:
        if letra in alfabeto:
            posicao = alfabeto.index(letra)
            resultado = resultado + chave[posicao]
        else:
            resultado = resultado + letra
    return resultado


def descriptografar(texto, chave):
    texto = texto.upper()
    resultado = ""
    for letra in texto:
        if letra in chave:
            posicao = chave.index(letra)
            resultado = resultado + alfabeto[posicao]
        else:
            resultado = resultado + letra
    return resultado


print("--- CIFRA DE SUBSTITUICAO MONOALFABETICA ---")
print("Exemplo de chave: QWERTYUIOPASDFGHJKLZXCVBNM")

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
        chave = input("Digite a chave (26 letras sem repetir): ").upper()
        if not chave_valida(chave):
            print("Chave invalida! Precisa ter as 26 letras, sem repetir.")
        elif opcao == "1":
            print("Texto cifrado:", criptografar(texto, chave))
        else:
            print("Texto original:", descriptografar(texto, chave))
    else:
        print("Opcao invalida")