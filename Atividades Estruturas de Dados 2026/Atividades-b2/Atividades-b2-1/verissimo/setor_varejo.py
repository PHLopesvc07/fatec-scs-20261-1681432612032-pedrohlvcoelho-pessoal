# ─────────────────────────────────────────────────────────
# EQUIPE 07 + EQUIPE 08 - Sistema Completo
# Setor Varejo (Moda e Grande Consumo)
# Checkout de Pedidos + Consolidação de Lotes
# ─────────────────────────────────────────────────────────

from datetime import datetime

# ==============================
# CLASSES DO CHECKOUT (Equipe 07)
# ==============================

class ItemVenda:
    def __init__(self, id_pedido: int, nome_item: str, quantidade_pecas: int):
        self.id_pedido = id_pedido
        self.nome_item = nome_item
        self.quantidade_pecas = quantidade_pecas
        self.timestamp_criacao = datetime.now()

    def __str__(self):
        return (f"ID: {self.id_pedido}, Item: {self.nome_item}, "
                f"Qtd: {self.quantidade_pecas} peças")


class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def enfileirar(self, dado):
        novo_no = No(dado)
        if self.fim is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no
        self.tamanho += 1

    def desenfileirar(self):
        if self.inicio is None:
            raise IndexError("Fila vazia.")
        dado = self.inicio.dado
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        self.tamanho -= 1
        return dado

    def esta_vazia(self) -> bool:
        return self.inicio is None

    def __len__(self):
        return self.tamanho

    def __iter__(self):
        """Permite iterar sobre a fila sem consumi-la"""
        atual = self.inicio
        while atual is not None:
            yield atual.dado
            atual = atual.proximo


# ==============================
# CONSOLIDAÇÃO DE LOTES (Equipe 08)
# ==============================

LIMITE_CARGA_FECHADA = 50


class LoteConsolidado:
    def __init__(self, pedidos: list):
        self.pedidos = pedidos
        self.total_pecas = sum(p.quantidade_pecas for p in pedidos)
        self.prioridade = "Alta (Carga Fechada)" if self.total_pecas > LIMITE_CARGA_FECHADA else "Normal"
        self.timestamp_consolidacao = datetime.now()

    def __str__(self):
        ids = [str(p.id_pedido) for p in self.pedidos]
        return (f"Lote [{', '.join(ids)}] | Total: {self.total_pecas} peças "
                f"| Prioridade: {self.prioridade}")


class ConsolidadorLotes:
    def __init__(self, fila_entrada: Fila, fila_saida: Fila):
        self.fila_entrada = fila_entrada
        self.fila_saida = fila_saida

    def processar(self):
        """
        Agrupa todos os pedidos da fila_entrada em lotes e envia para fila_saida.
        Lotes com mais de 50 peças recebem prioridade Alta (Carga Fechada).
        """
        acumulados = []
        total_acumulado = 0

        while not self.fila_entrada.esta_vazia():
            pedido = self.fila_entrada.desenfileirar()
            acumulados.append(pedido)
            total_acumulado += pedido.quantidade_pecas

            # Quando ultrapassar o limite, fecha o lote e começa um novo
            if total_acumulado > LIMITE_CARGA_FECHADA:
                lote = LoteConsolidado(acumulados[:])
                self.fila_saida.enfileirar(lote)
                print(f"Lote consolidado -> {lote}")
                acumulados = []
                total_acumulado = 0

        # Lote residual (itens que não atingiram o limite)
        if acumulados:
            lote = LoteConsolidado(acumulados[:])
            self.fila_saida.enfileirar(lote)
            print(f"Lote consolidado -> {lote}")


# ==============================
# PREPARAÇÃO DA FILA CLASSIFICADA PARA O HUB
# ==============================

def mostrar_fila_hub(fila_lotes: Fila):
    """
    APENAS MOSTRA os lotes que estão na fila, sem consumi-los.
    Esta função é apenas para debug/visualização.
    """
    print("\n=== FILA 2 — LOTES PRONTOS PARA O HUB ===")
    if fila_lotes.esta_vazia():
        print("Fila vazia!")
        return
    
    for lote in fila_lotes:
        prioridade_calculada = 3 if lote.prioridade == "Alta (Carga Fechada)" else 5
        print(f"  Lote ID: VAREJO-LOTE-{id(lote)} | "
              f"Peças: {lote.total_pecas} | "
              f"Prioridade: {lote.prioridade} | "
              f"Prioridade Hub: {prioridade_calculada}")


# ==============================
# TESTE DO SISTEMA
# ==============================

# IMPORTANTE: Estas filas serão acessadas pelo Hub
fila1 = Fila()  # Pedidos individuais (Fila 1 - Itens Avulsos)
fila2 = Fila()  # Lotes consolidados  (Fila 2 - Lotes Consolidados)

# Equipe 07: Checkout — geração de itens de venda
pedidos_teste = [
    ItemVenda(701, "Camiseta Polo",      12),
    ItemVenda(702, "Calça Jeans",        20),
    ItemVenda(703, "Tênis Casual",        8),
    ItemVenda(704, "Jaqueta de Couro",   35),
    ItemVenda(705, "Meia Esportiva",     50),
    ItemVenda(706, "Vestido Floral",     15),
    ItemVenda(707, "Shorts Tactel",      22),
    ItemVenda(708, "Blusa de Frio",      40),
    ItemVenda(709, "Bermuda Jeans",      10),
    ItemVenda(710, "Camisa Social",      18),
]

print("=== FILA 1 — PEDIDOS AVULSOS ===")
for pedido in pedidos_teste:
    fila1.enfileirar(pedido)
    print(f"  Enfileirado -> {pedido}")

# Equipe 08: Consolidação de Lotes
print("\n=== PROCESSAMENTO — CONSOLIDAÇÃO DE LOTES ===")
consolidador = ConsolidadorLotes(fila1, fila2)
consolidador.processar()

# CORREÇÃO: Apenas MOSTRAR os lotes, NÃO consumir a fila2
# A fila2 DEVE permanecer intacta para o Hub coletar!
mostrar_fila_hub(fila2)

print(f"\n✅ Total de lotes prontos para o Hub: {len(fila2)}")
print("⚠️  fila2 está preservada e pronta para coleta do Hub!")