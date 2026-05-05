#                       Atividade B1-3
#           Sim_HP12c - Pilhas RPN com Menu em py
#         Disciplina: Estruturas de Dados - Fatec SCS
#           Autor: Pedro Henrique Lopes Vilela Coelho
#                       RA: 1681432612032
#                           Data: 2026

def inicializar():
    return [0, 0, 0, 0]

def empilhar(pilha, valor):
    pilha[3] = pilha[2]
    pilha[2] = pilha[1]
    pilha[1] = pilha[0]
    pilha[0] = valor
    mostrar_pilha(pilha)
    return pilha

def desempilhar(pilha):
    x = pilha[0]
    pilha[0] = pilha[1]
    pilha[1] = pilha[2]
    pilha[2] = pilha[3]
    pilha[3] = 0
    return pilha, x

def operar(pilha, operador):
    pilha, a = desempilhar(pilha)
    pilha, b = desempilhar(pilha)

    if operador == '+':
        resultado = b + a
    elif operador == '-':
        resultado = b - a
    elif operador == '*':
        resultado = b * a
    elif operador == '/':
        if a == 0:
            print("Erro: divisão por zero não é permitido")
            resultado = 0
        else:
            resultado = b / a
    else:
        print("Erro: operador inválido ->", operador)
        resultado = 0

    pilha = empilhar(pilha, resultado)
    return pilha

def mostrar_pilha(pilha):
    print(f"T: {pilha[3]} | Z: {pilha[2]} | Y: {pilha[1]} | X: {pilha[0]}")

def avaliar_rpn(pilha, expressao):
    tokens = expressao.split()
    for token in tokens:
        if token.isdigit():
            pilha = empilhar(pilha, float(token))
        else:
            pilha = operar(pilha, token)
    return pilha, pilha[0]


pilha = inicializar()

while True:
    print("\n------------- MENU CALCULADORA HP12c ---------------")
    print("1 - Zerar pilhas")
    print("2 - Empilhar novo número")
    print("3 - Calcular operação")
    print("4 - Ver pilha")
    print("0 - Sair")
    print("\n----------------------------------------------------")


    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        pilha = inicializar()
        print("Pilha zerada!")
    elif opcao == "2":
        valor = float(input("Digite o número: "))
        pilha = empilhar(pilha, valor)
    elif opcao == "3":
        expressao = input("Digite a expressão RPN: ")
        pilha, resultado = avaliar_rpn(pilha, expressao)
        print(f"O resultado da expressão algébrica é: {resultado}")
    elif opcao == "4":
        mostrar_pilha(pilha)
    elif opcao == "0":
        print("Encerrando calculadora...")
        break
    else:
        print("Opção inválida, tente novamente.")