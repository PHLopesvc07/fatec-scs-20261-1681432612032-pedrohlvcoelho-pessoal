#/-----------------------------------------------------------------------------------------/
#/*                         FATEC-São Caetano do Sul                                        */
#/*                         Estrutura de Dados                                              */
#/*                         Id da Atividade: B2-1                                           */
#/*             Objetivo: Manipular filas para criar uma ordem de prioridade para pacientes */
#/*            Autor: ERICK JOSHUA REVOLLO, GABRIEL XAVIER DE ALMEIDA                       */
#/*                          E MARCELO ENRIQUE KORIN                                        */
#/*                            Data:04/05/2026                                              */
#/-----------------------------------------------------------------------------------------/

from datetime import datetime, timedelta

class Paciente:
    def __init__(self, nome, sintoma_relatado, timestamp_chegada, idade, pcd, gestante):
        self.nome = nome
        self.sintoma_relatado = sintoma_relatado
        self.timestamp_chegada = timestamp_chegada
        self.idade = idade
        self.pcd = pcd
        self.gestante = gestante
        self.emergencia = False

    def __str__(self):
        return (
            f"Sintoma: {self.sintoma_relatado} | "
            f"Idade: {self.idade} | PcD: {self.pcd} | "
            f"Gestante: {self.gestante} | "
            f"Emergencia: {'Sim' if self.emergencia else 'Nao'} | "
            f"Chegada: {self.timestamp_chegada.strftime('%H:%M:%S')}"
        )

fila_bruta = []

"""
while True:
    nome = input("Nome: ")
    sintoma = input("Sintoma: ")
    idade = int(input("Idade: "))
    pcd = input("PcD (s/n): ").strip().lower()
    gestante = input("Gestante (s/n): ").strip().lower()

    timestamp = datetime.now()

    paciente = Paciente(nome, sintoma, timestamp, idade, pcd, gestante)
    fila_bruta.append(paciente)

    print("Paciente enfileirado!\n")

    continuar = input("Adicionar outro paciente? (s/n): ")
    if continuar.lower() != "s":
        break
"""

agora = datetime.now()

pacientes = [
    Paciente("Lucas", "Dor no peito", agora - timedelta(minutes=15), 45, "n", "n"),
    Paciente("Mariana", "Febre alta", agora - timedelta(minutes=14), 30, "n", "s"),
    Paciente("Carlos", "Falta de ar", agora - timedelta(minutes=13), 60, "s", "n"),
    Paciente("Ana", "Dor de cabeça", agora - timedelta(minutes=12), 22, "n", "n"),
    Paciente("João", "Tontura", agora - timedelta(minutes=11), 70, "n", "n"),
    Paciente("Fernanda", "Pressão alta", agora - timedelta(minutes=10), 55, "n", "n"),
    Paciente("Rafael", "Acidente leve", agora - timedelta(minutes=9), 28, "n", "n"),
    Paciente("Beatriz", "Contrações", agora - timedelta(minutes=8), 32, "n", "s"),
    Paciente("Eduardo", "Desmaio", agora - timedelta(minutes=7), 65, "n", "n"),
    Paciente("Juliana", "Alergia", agora - timedelta(minutes=6), 19, "n", "n"),
]

fila_bruta.extend(pacientes)

PALAVRAS_EMERGENCIA = ["dor no peito", "falta de ar", "inconsciente"]

def calcular_prioridade(paciente):
    sintoma = paciente.sintoma_relatado.lower()

    if "inconsciente" in sintoma:
        nivel = 1
    elif "dor no peito" in sintoma or "falta de ar" in sintoma:
        nivel = 2
    elif any(p in sintoma for p in PALAVRAS_EMERGENCIA):
        nivel = 3
    elif paciente.idade >= 60 or paciente.pcd == "s" or paciente.gestante == "s":
        nivel = 4
    else:
        nivel = 5

    bonus = 0 if (paciente.pcd == "s" or paciente.gestante == "s" or paciente.idade >= 60) else 1

    return (nivel, bonus, paciente.timestamp_chegada)


def classificar_e_ordenar(fila):
    for paciente in fila:
        nivel, _, _ = calcular_prioridade(paciente)
        paciente.nivel_prioridade = nivel

        sintoma = paciente.sintoma_relatado.lower()
        paciente.emergencia = any(p in sintoma for p in PALAVRAS_EMERGENCIA)

    return sorted(fila, key=calcular_prioridade)


fila_ordenada = classificar_e_ordenar(fila_bruta)