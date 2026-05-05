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

'''
É a atividade dos numeros (se Y>X Y=Direita do nó X, se Z>X e Z<Y,
 a esquerda do nó Y estando numa profundidade maior por estar mais baixo
 e numa altura menor em relação a raiz)
Ex: profundidade(P)\ Altura(A)
                30                  | P:0 ,A:3
        15               40         | P:1 ,A:2
    7       18        34    None    | P:2 ,A:1
  3  9    16  22                    | P:3 ,A:0

neste caso a folha 22 está na profundidade 3 e altura 0, 

'''