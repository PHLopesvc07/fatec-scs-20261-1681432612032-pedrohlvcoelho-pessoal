'''
*---------------------------------------------------------------*
*       Fatec São Caetano do Sul                                *
*       Atividade B2-3                                          *
*       Autor: Pedro Henrique Lopes Vilela Coelho               *
*       Objetivo: Raizes de Arvore                              * 
*                                                               *  
*       data: 11/05/2026                                        *
*---------------------------------------------------------------*
'''
class No:
    def __init__(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None

class ArvoreBST:
    def __init__(self, raiz=None):
        self.raiz = raiz

    def inserir(self, valor):
        if self.raiz is None:
            self.raiz = No(valor)
        else:
            self._inserir_recursivo(valor, self.raiz)

    def _inserir_recursivo(self, valor, no_atual):
        if valor < no_atual.valor:
            if no_atual.esq is None:
                no_atual.esq = No(valor)
            else:
                self._inserir_recursivo(valor, no_atual.esq)
        elif valor > no_atual.valor:
            if no_atual.dir is None:
                no_atual.dir = No(valor)
            else:
                self._inserir_recursivo(valor, no_atual.dir)

    def _busca_no(self, valor, no_atual):
        if no_atual is None or no_atual.valor == valor:
            return no_atual
        if valor < no_atual.valor:
            return self._busca_no(valor, no_atual.esq)
        return self._busca_no(valor, no_atual.dir)

    def imprimir_nos_internos(self):
        internos = []
        def _percorrer(no):
            if no:
                if no.esq or no.dir:
                    internos.append(str(no.valor))
                _percorrer(no.esq)
                _percorrer(no.dir)
        _percorrer(self.raiz)
        print("Nós Internos:", ", ".join(internos) if internos else "Nenhum")

    def imprimir_folhas(self):
        folhas = []
        def _percorrer(no):
            if no:
                if not no.esq and not no.dir:
                    folhas.append(str(no.valor))
                _percorrer(no.esq)
                _percorrer(no.dir)
        _percorrer(self.raiz)
        print("Nós Externos (Folhas):", ", ".join(folhas) if folhas else "Nenhum")

    def imprimir_niveis(self):
        if not self.raiz:
            print("Árvore vazia.")
            return
        fila = [(self.raiz, 0)]
        niveis = {}
        while fila:
            no, nivel = fila.pop(0)
            if nivel not in niveis:
                niveis[nivel] = []
            niveis[nivel].append(str(no.valor))
            if no.esq:
                fila.append((no.esq, nivel + 1))
            if no.dir:
                fila.append((no.dir, nivel + 1))
        
        print("Exibição por Níveis:")
        for nivel, valores in sorted(niveis.items()):
            print(f"  Nível {nivel}: {', '.join(valores)}")

    def calcular_altura(self, no):
        if no is None:
            return -1
        altura_esq = self.calcular_altura(no.esq)
        altura_dir = self.calcular_altura(no.dir)
        return max(altura_esq, altura_dir) + 1

    def calcular_profundidade(self, valor):
        profundidade = 0
        atual = self.raiz
        while atual:
            if atual.valor == valor:
                return profundidade
            elif valor < atual.valor:
                atual = atual.esq
            else:
                atual = atual.dir
            profundidade += 1
        return -1

    def imprimir_ancestrais(self, valor):
        ancestrais = []
        atual = self.raiz
        while atual and atual.valor != valor:
            ancestrais.append(str(atual.valor))
            if valor < atual.valor:
                atual = atual.esq
            else:
                atual = atual.dir
        
        if atual is None:
            print("Ancestrais: Nó não encontrado.")
        else:
            ancestrais.reverse()
            print("Ancestrais (do nó até a raiz):", " -> ".join(ancestrais) if ancestrais else "Nenhum (é a raiz)")

    def imprimir_descendentes(self, valor):
        alvo = self._busca_no(valor, self.raiz)
        descendentes = []
        def _percorrer(no):
            if no:
                descendentes.append(str(no.valor))
                _percorrer(no.esq)
                _percorrer(no.dir)
        
        if alvo:
            _percorrer(alvo.esq)
            _percorrer(alvo.dir)
            print("Descendentes:", ", ".join(descendentes) if descendentes else "Nenhum (é folha)")
        else:
            print("Descendentes: Nó não encontrado.")

    def analisar_arvore(self, valor_busca):
        if not self.raiz:
            print("Árvore vazia!")
            return

        print("=" * 50)
        print("A. DIAGNÓSTICO GERAL")
        print("=" * 50)
        print(f"Identificação da Raiz: {self.raiz.valor}")
        self.imprimir_nos_internos()
        self.imprimir_folhas()
        self.imprimir_niveis()

        print("=" * 50)
        print(f"B. DIAGNÓSTICO ESPECÍFICO (Busca: {valor_busca})")
        print("=" * 50)
        
        alvo = self._busca_no(valor_busca, self.raiz)
        if alvo:
            grau = 0
            if alvo.esq: grau += 1
            if alvo.dir: grau += 1
            print(f"Grau do Nó: {grau}")
            
            self.imprimir_ancestrais(valor_busca)
            self.imprimir_descendentes(valor_busca)
            
            print(f"Altura do Nó: {self.calcular_altura(alvo)}")
            print(f"Profundidade do Nó: {self.calcular_profundidade(valor_busca)}")
            print(f"Endereço de Memória: {id(alvo)}")
        else:
            print(f"O valor {valor_busca} não foi encontrado na árvore.")

def menu():
    arvore = ArvoreBST()
    
    while True:
        print("\nSISTEMA DE GESTÃO DE BST")
        print("1. Inserir Valor")
        print("2. Executar Diagnóstico")
        print("3. Resetar Árvore")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            try:
                nums = input("Digite o(s) valor(es) separados por espaço: ").split()
                for n in nums:
                    arvore.inserir(int(n))
                print("Valores processados.")
            except ValueError:
                print("Erro: Digite apenas números inteiros.")

        elif opcao == '2':
            try:
                v = int(input("Digite o valor para diagnóstico específico: "))
                arvore.analisar_arvore(v)
            except ValueError:
                print("Erro: Valor inválido.")

        elif opcao == '3':
            arvore = ArvoreBST()
            print("Árvore reiniciada.")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
