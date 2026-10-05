# Cifra de Vigenere
# parecida com a de Cesar, mas cada letra usa um deslocamento diferente,
# que vem da letra da senha naquela posicao

alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def criptografar(texto, senha):
    texto = texto.upper()
    senha = senha.upper()
    resultado = ""
    i = 0  # posicao atual na senha
    for letra in texto:
        if letra in alfabeto:
            pos_letra = alfabeto.index(letra)
            pos_senha = alfabeto.index(senha[i % len(senha)])
            nova_posicao = (pos_letra + pos_senha) % 26
            resultado = resultado + alfabeto[nova_posicao]
            i = i + 1
        else:
            resultado = resultado + letra
    return resultado


def descriptografar(texto, senha):
    texto = texto.upper()
    senha = senha.upper()
    resultado = ""
    i = 0
    for letra in texto:
        if letra in alfabeto:
            pos_letra = alfabeto.index(letra)
            pos_senha = alfabeto.index(senha[i % len(senha)])
            nova_posicao = (pos_letra - pos_senha) % 26
            resultado = resultado + alfabeto[nova_posicao]
            i = i + 1
        else:
            resultado = resultado + letra
    return resultado


print("--- CIFRA DE VIGENERE ---")

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
        senha = input("Digite a senha (so letras): ")
        if opcao == "1":
            print("Texto cifrado:", criptografar(texto, senha))
        else:
            print("Texto original:", descriptografar(texto, senha))
    else:
        print("Opcao invalida")