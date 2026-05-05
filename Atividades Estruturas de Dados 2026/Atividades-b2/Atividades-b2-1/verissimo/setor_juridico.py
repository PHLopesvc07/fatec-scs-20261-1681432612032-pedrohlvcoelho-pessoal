# ─────────────────────────────────────────────────────────
# EQUIPE 09 + EQUIPE 10 - Sistema Completo
# Cadastro de Solicitantes + Auditoria de Prioridade
# ─────────────────────────────────────────────────────────

# ==============================
# CLASSES DO CADASTRO (Equipe 09)
# ==============================

class Cidadao:
    def __init__(self, id_protocolo: int, nome: str, idade: int, pcd: bool):
        self.id_protocolo = id_protocolo
        self.nome = nome
        self.idade = idade
        self.pcd = pcd
        self.prioridade_legal = False

    def __str__(self):
        return (f"Prot: {self.id_protocolo}, Nome: {self.nome}, "
                f"Idade: {self.idade}, PCD: {self.pcd}")


class No:
    def __init__(self, cidadao: Cidadao):
        self.cidadao = cidadao
        self.proximo = None


class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def enfileirar(self, cidadao: Cidadao):
        novo_no = No(cidadao)

        if self.fim is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

        self.tamanho += 1

    def desenfileirar(self) -> Cidadao:
        if self.inicio is None:
            raise IndexError("Fila vazia.")

        cidadao = self.inicio.cidadao
        self.inicio = self.inicio.proximo

        if self.inicio is None:
            self.fim = None

        self.tamanho -= 1
        return cidadao

    def esta_vazia(self) -> bool:
        return self.inicio is None

    def __len__(self):
        return self.tamanho


# ==============================
# AUDITORIA DE PRIORIDADE (Equipe 10)
# ==============================

class AuditoriaPrioridade:

    def __init__(self, fila_entrada: Fila, fila_saida: Fila):
        self.fila_entrada = fila_entrada
        self.fila_saida = fila_saida

    def processar(self):

        while not self.fila_entrada.esta_vazia():

            cidadao = self.fila_entrada.desenfileirar()

            # Regra de prioridade legal
            if cidadao.idade >= 60 or cidadao.pcd:
                cidadao.prioridade_legal = True
            else:
                cidadao.prioridade_legal = False

            print(f"Auditado -> {cidadao} | Prioridade: {cidadao.prioridade_legal}")

            # envia para a fila 2
            self.fila_saida.enfileirar(cidadao)


# ==============================
# TESTE DO SISTEMA
# ==============================

fila1 = Fila()   # registros brutos
fila2 = Fila()   # classificados

# Simulação de cadastro
fila1.enfileirar(Cidadao(901, "Maria", 72, False))
fila1.enfileirar(Cidadao(902, "João", 45, False))
fila1.enfileirar(Cidadao(903, "Ana", 20, True))
fila1.enfileirar(Cidadao(904, "Guilherme", 18, True))
fila1.enfileirar(Cidadao(905, "Pedro", 23, False))
fila1.enfileirar(Cidadao(906, "Luíza", 15, False))

# Auditoria
auditoria = AuditoriaPrioridade(fila1, fila2)
auditoria.processar()