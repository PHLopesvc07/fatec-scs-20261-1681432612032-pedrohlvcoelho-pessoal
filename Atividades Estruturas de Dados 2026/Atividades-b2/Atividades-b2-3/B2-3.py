class No:
    def _init_(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None
class ArvoreBST:
    def init (self, raiz=None):
        self.raiz = raiz 
    #Funções de diagnóstico obrigatórias
    def analisar_arvore(self, valor_busca): pass
    def imprimir_nos_internos(self): pass
    def imprimir_Folhas (self): pass
    def imprimir_niveis(self): pass
    def calcular_altura(self, no): pass
    def imprimir_ancestrais (self, valor): pass
    def imprimir_descendentes(self, valor): pass
