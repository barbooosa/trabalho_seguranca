# Cifra de Cesar
# cada letra anda X posicoes no alfabeto (X = chave)

alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def criptografar(texto, chave):
    texto = texto.upper()
    resultado = ""
    for letra in texto:
        if letra in alfabeto:
            posicao = alfabeto.index(letra)
            nova_posicao = (posicao + chave) % 26
            resultado = resultado + alfabeto[nova_posicao]
        else:
            resultado = resultado + letra
    return resultado


def descriptografar(texto, chave):
    texto = texto.upper()
    resultado = ""
    for letra in texto:
        if letra in alfabeto:
            posicao = alfabeto.index(letra)
            nova_posicao = (posicao - chave) % 26
            resultado = resultado + alfabeto[nova_posicao]
        else:
            resultado = resultado + letra
    return resultado


print("--- CIFRA DE CESAR ---")

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
        chave = int(input("Digite a chave (numero): "))
        if opcao == "1":
            print("Texto cifrado:", criptografar(texto, chave))
        else:
            print("Texto original:", descriptografar(texto, chave))
    else:
        print("Opcao invalida")