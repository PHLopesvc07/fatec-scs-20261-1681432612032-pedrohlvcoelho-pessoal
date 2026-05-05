from datetime import datetime, date, timedelta

fila_1 = []
fila_2 = []
log_descartes = []


def formatar_data(data_str):
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data.strftime("%d/%m/%Y")
    except ValueError:
        return None


def gerar_produto():
    print("\n=== Entrada de Estoque ===")

    while True:
        sku = input("SKU: ").strip()
        if sku.isdigit():
            sku = int(sku)
            break
        print("SKU inválido.")

    while True:
        nome = input("Produto: ").strip()
        if nome:
            break
        print("Nome inválido.")

    while True:
        data_str = input("Validade (DD/MM/AAAA): ").strip()
        data_formatada = formatar_data(data_str)

        if data_formatada:
            break
        print("Data inválida.")

    produto = {
        "id_sku": sku,
        "nome_produto": nome,
        "data_validade": data_formatada,
        "processado": False 
    }

    fila_1.append(produto)
    print("Produto adicionado à Fila 1.")

def gerar_produtos_teste():
    hoje = date.today()

    produtos = [
        {"id_sku": 2001, "nome_produto": "Leite", "data_validade": (hoje + timedelta(days=1)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2002, "nome_produto": "Pão", "data_validade": (hoje + timedelta(days=0)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2003, "nome_produto": "Arroz", "data_validade": (hoje + timedelta(days=15)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2004, "nome_produto": "Carne", "data_validade": (hoje - timedelta(days=2)).strftime("%d/%m/%Y"), "processado": False},  # vencido
        {"id_sku": 2005, "nome_produto": "Iogurte", "data_validade": (hoje + timedelta(days=2)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2006, "nome_produto": "Queijo", "data_validade": (hoje + timedelta(days=5)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2007, "nome_produto": "Frango", "data_validade": (hoje - timedelta(days=1)).strftime("%d/%m/%Y"), "processado": False},  # vencido
        {"id_sku": 2008, "nome_produto": "Manteiga", "data_validade": (hoje + timedelta(days=3)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2009, "nome_produto": "Ovos", "data_validade": (hoje + timedelta(days=1)).strftime("%d/%m/%Y"), "processado": False},
        {"id_sku": 2010, "nome_produto": "Suco", "data_validade": (hoje + timedelta(days=20)).strftime("%d/%m/%Y"), "processado": False},
    ]

    fila_1.extend(produtos)

def processar_produto():
    if not fila_1:
        print("Fila 1 vazia.")
        return

    produto = None
    index = None

    for i, item in enumerate(fila_1):
        if not item.get("processado"):
            produto = item
            index = i
            break

    if produto is None:
        print("Todos os produtos já foram processados.")
        return

    fila_1.pop(index)

    validade = datetime.strptime(
        produto["data_validade"], "%d/%m/%Y"
    ).date()

    dias = (validade - date.today()).days

    if dias < 0:
        log_descartes.append(produto)
        print("Produto vencido! Descartado (Perda).")
        return

    if dias <= 2:
        produto["critico"] = True
        produto["prioridade"] = 1
    else:
        produto["critico"] = False
        produto["prioridade"] = 2

    produto["dias_restantes"] = dias
    produto["processado"] = True

    fila_2.append(produto)

    fila_2.sort(key=lambda x: datetime.strptime(x["data_validade"], "%d/%m/%Y"))

    print("Produto enviado para a Fila 2.")


def mostrar_fila_1():
    if not fila_1:
        print("Fila 1 vazia.")
        return

    print("\n=== FILA 1 (ESTOQUE BRUTO) ===")
    for p in fila_1:
        print("SKU:", p["id_sku"], "| Produto:", p["nome_produto"], "| Validade:", p["data_validade"], "| Processado:", p["processado"])

def mostrar_fila_2():
    if not fila_2:
        print("Fila 2 vazia.")
        return

    print("\n=== FILA 2 (CLASSIFICADOS) ===")
    for p in fila_2:
        print("SKU:", p["id_sku"], "| Produto:", p["nome_produto"], "| Validade:", p["data_validade"], "| Dias restantes:", p["dias_restantes"], "| Prioridade:", "Alta" if p["critico"] else "Normal")

def mostrar_descartes():
    if not log_descartes:
        print("Nenhum descarte.")
        return

    print("\n=== DESCARTES (PERDAS) ===")
    for p in log_descartes:
        print("SKU:", p["id_sku"], "| Produto:", p["nome_produto"], "| Validade:", p["data_validade"])

def menu():
    while True:
        print("\n====== MENU ======")
        print("1 - Adicionar Produto")
        print("2 - Processar Produto")
        print("3 - Mostrar Fila 1")
        print("4 - Mostrar Fila 2")
        print("5 - Mostrar Descartes")
        print("6 - Sair")

        opcao = input("Opção: ")

        if opcao == "1":
            gerar_produto()

        elif opcao == "2":
            processar_produto()

        elif opcao == "3":
            mostrar_fila_1()

        elif opcao == "4":
            mostrar_fila_2()

        elif opcao == "5":
            mostrar_descartes()

        elif opcao == "6":
            break

        else:
            print("Opção inválida.")

gerar_produtos_teste()

while len(fila_1) > 0:
    processar_produto()