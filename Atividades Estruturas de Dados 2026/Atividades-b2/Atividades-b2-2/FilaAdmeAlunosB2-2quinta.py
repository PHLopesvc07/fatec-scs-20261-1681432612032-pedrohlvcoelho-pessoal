'''
*---------------------------------------------------------------*
*       Fatec São Caetano do Sul                                *
*       Atividade B2-2                                          *
*       Autor: Pedro Henrique Lopes Vilela Coelho               *
*        Objetivo: Gerenciar uma ordem de impressão seguindo    *
*       os conceitos de fila (FIFA)                             *
*                                                               *  
*       data: 30/04/2026                                        *
*---------------------------------------------------------------*
'''


class FilaImpressao: 
    def __init__(self):
        self.filaAdm = []
        self.filaAlunos = []
        self.filaGeral = []

    def addArq(self, user, nomeArq, paginas):
        documento = {"arquivo": nomeArq, "paginas": paginas}

        if user.lower() in ['adm', 'administrador', 'admin']:
            self.filaAdm.append(documento)
            print(f"Documento '{nomeArq}' adicionado à fila de ADM")
        elif user.lower() in ['aluno', 'alunos']:
            self.filaAlunos.append(documento)
            print(f"Documento '{nomeArq}' adicionado à fila de Alunos")
        else:
            print("ERRO: Tipo de usuário inválido.")

    def reorganizarFila(self):
        if not self.filaAdm and not self.filaAlunos:
            print("Filas vazias. Nada para reorganizar.")
            return

        if len(self.filaGeral) == 0:
            self.filaGeral.extend(self.filaAdm)
            self.filaGeral.extend(self.filaAlunos)
            self.filaAdm.clear()
            self.filaAlunos.clear()
            print("Fila Geral organizada (ADM primeiro)!")
        else:
            print("Ainda há itens na Fila Geral. Imprima-os antes de reorganizar.")

    def consumirFila(self):  
        if len(self.filaGeral) > 0:
            doc = self.filaGeral.pop(0)
            print(
                f"Imprimindo...\nArquivo: '{doc['arquivo']}' | Páginas: {doc['paginas']}")
        else:
            print("Fila Geral vazia. Reorganize antes de imprimir.")

    def exibirListas(self):
        print("\n--- STATUS DAS FILAS ---")
        self.mostraSubLista("Fila ADM", self.filaAdm)
        self.mostraSubLista("Fila Alunos", self.filaAlunos)
        self.mostraSubLista("Fila Geral", self.filaGeral)

    def mostraSubLista(self, nome, lista):
        if lista:  
            print(f"{nome}:")
            for doc in lista:
                print(f"  - {doc['arquivo']} ({doc['paginas']} págs)")
        else:
            print(f"{nome} está vazia")


sistema = FilaImpressao()
while True:
    print("\n===============================")
    print("   SISTEMA DE FILA DE IMPRESSÃO")
    print("===============================")
    print("1 - Adicionar arquivo")
    print("2 - Consumir fila")
    print("3 - Listar estado das filas")
    print("4 - Reorganizar fila")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == '1':
        user = input("Tipo (adm/aluno): ").strip()
        nomeArq = input("Nome do arquivo: ").strip()
        try:
            paginas = int(input("Páginas: "))
            sistema.addArq(user, nomeArq, paginas)
        except ValueError:
            print("ERRO: Quantidade inválida.")

    elif opcao == '2':
        sistema.consumirFila()

    elif opcao == '3':
        sistema.exibirListas()

    elif opcao == '4':
        sistema.reorganizarFila()

    elif opcao == '5': # Opção de teste para add arquivos :D
        sistema.addArq('adm', 'D1', 10)
        sistema.addArq('aluno', 'A1', 5)
        sistema.addArq('adm', 'D2', 15)
        sistema.addArq('aluno', 'A2', 2)
        sistema.addArq('adm', 'D3', 8)
        sistema.addArq('aluno', 'A3', 12)
        sistema.addArq('adm', 'D4', 20)
        sistema.addArq('aluno', 'A4', 3)
        
    elif opcao == '6':  # Opção de teste para add arquivos :D
        sistema.addArq('adm', 'D5', 25)
        sistema.addArq('aluno', 'A5', 18)
        
    elif opcao == '0':
        break
    
    