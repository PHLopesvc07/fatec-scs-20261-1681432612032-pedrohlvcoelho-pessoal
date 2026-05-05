from datetime import datetime, timedelta
import time
import threading
import os

# Importando os módulos com aliases para evitar conflitos de nomes
import setor_varejo as sv
import setor_juridico as sj
import setor_alimentos as sa
import setor_saude as ss

# --- ADAPTADORES CORRIGIDOS PARA O PADRÃO HUB ---

def adaptador_varejo(fila_lotes):
    pacotes = []
    if fila_lotes.esta_vazia():
        print("   ⚠️  Fila do Varejo está vazia!")
        return pacotes
        
    while not fila_lotes.esta_vazia():
        lote = fila_lotes.desenfileirar()
        prioridade = 3 if lote.prioridade == "Alta (Carga Fechada)" else 5
        pacotes.append({
            "id_original": f"VAR-LOTE-{id(lote)}",
            "setor_origem": "Varejo",
            "prioridade_calculada": prioridade,
            "conteudo": str(lote),
            "timestamp_criacao": getattr(lote, 'timestamp_consolidacao', datetime.now()),
            "timestamp_hub": datetime.now()
        })
    return pacotes

def adaptador_juridico(fila_auditada):
    pacotes = []
    if fila_auditada.esta_vazia():
        print("   ⚠️  Fila do Jurídico está vazia!")
        return pacotes
        
    while not fila_auditada.esta_vazia():
        cidadao = fila_auditada.desenfileirar()
        prioridade = 2 if cidadao.prioridade_legal else 5
        pacotes.append({
            "id_original": f"JUR-PROT-{cidadao.id_protocolo}",
            "setor_origem": "Jurídico",
            "prioridade_calculada": prioridade,
            "conteudo": str(cidadao),
            "timestamp_criacao": datetime.now(),
            "timestamp_hub": datetime.now()
        })
    return pacotes

def adaptador_alimentos(lista_fila_2):
    pacotes = []
    if not lista_fila_2:
        print("   ⚠️  Fila de Alimentos está vazia!")
        return pacotes
        
    itens_para_processar = lista_fila_2.copy()
    lista_fila_2.clear()
    
    for item in itens_para_processar:
        prioridade = item.get("prioridade", 2)
        pacotes.append({
            "id_original": f"ALI-SKU-{item['id_sku']}",
            "setor_origem": "Alimentos",
            "prioridade_calculada": prioridade,
            "conteudo": f"{item['nome_produto']} (Validade: {item['data_validade']})",
            "timestamp_criacao": datetime.now(),
            "timestamp_hub": datetime.now()
        })
    return pacotes

def adaptador_saude(lista_ordenada):
    pacotes = []
    if not lista_ordenada:
        print("   ⚠️  Fila de Saúde está vazia!")
        return pacotes
        
    pacientes_para_processar = lista_ordenada.copy()
    lista_ordenada.clear()
    
    for p in pacientes_para_processar:
        pacotes.append({
            "id_original": f"SAU-PAC-{id(p)}",
            "setor_origem": "Saúde",
            "prioridade_calculada": p.nivel_prioridade,
            "conteudo": f"{p.nome} | Sintoma: {p.sintoma_relatado}",
            "timestamp_criacao": getattr(p, 'timestamp_chegada', datetime.now()),
            "timestamp_hub": datetime.now()
        })
    return pacotes


# --- DESTINOS FINAIS (CONSUMIDORES) ---

class ConsumidorFinal:
    def __init__(self, nome, regra_entrega):
        self.nome = nome
        self.regra_entrega = regra_entrega
        self.itens_entregues = []
    
    def receber_item(self, pacote):
        self.itens_entregues.append(pacote)
        print(f"   ✅ [{self.nome}] Recebido: {pacote['id_original']}")

class TransportadoraExterna:
    def __init__(self):
        self.fila_transporte = []
    
    def aguardar_transporte(self, pacote):
        self.fila_transporte.append(pacote)
        print(f"   🚛 [TRANSPORTADORA] {pacote['id_original']} aguardando...")


# --- MOTOR DO HUB CENTRAL (SIMPLIFICADO) ---

class HubCentral:
    def __init__(self):
        self.triagem_central = []  # Lista simples (será ordenada com sort)
        self.setores = []
        self.tempo_inicio = datetime.now()
        self.estatisticas = {
            "total_coletado": 0,
            "total_despachado": 0,
            "gargalos": {}
        }
        
        # Destinos finais
        self.consumidores = {
            "Saúde": ConsumidorFinal("Hospital Central", "DESPACHO IMEDIATO"),
            "Alimentos": ConsumidorFinal("Centro de Distribuição Food", "DESPACHO EM SEGUNDO LUGAR"),
            "Emergência": ConsumidorFinal("SAMU - Serviço de Atendimento", "EMERGÊNCIA ABSOLUTA"),
            "Varejo": ConsumidorFinal("Centro Logístico Varejista", "AGUARDA TRANSPORTE"),
            "Jurídico": ConsumidorFinal("Cartório Digital", "AGUARDA TRANSPORTE")
        }
        
        self.transportadora = TransportadoraExterna()
        self.monitorando = False
    
    def registrar_setor(self, nome, fila_referencia, funcao_adaptadora):
        """Registra um setor no Hub"""
        self.setores.append((nome, fila_referencia, funcao_adaptadora))
        self.estatisticas["gargalos"][nome] = 0
    
    def ordenar_triagem(self):
        """Ordena a fila por prioridade (menor número primeiro)"""
        self.triagem_central.sort(key=lambda x: x["prioridade_calculada"])
    
    def coletar_round_robin(self):
        """Coleta itens de todos os setores em formato Round Robin"""
        print("\n>>> HUB: INICIANDO COLETA ROUND ROBIN...")
        print("="*50)
        time.sleep(1)
        
        for nome, fila, adaptador in self.setores:
            try:
                print(f"\n🔄 Setor: {nome}")
                time.sleep(0.8)
                
                pacotes = adaptador(fila)
                
                if not pacotes:
                    print(f"   ℹ️  Nenhum item para coletar")
                    continue
                
                # Adiciona na lista de triagem
                for p in pacotes:
                    self.triagem_central.append(p)
                    self.estatisticas["total_coletado"] += 1
                    print(f"   📦 {p['id_original']} (Prioridade: {p['prioridade_calculada']})")
                    time.sleep(0.2)
                
                print(f"   ✅ {len(pacotes)} itens coletados")
                
                if len(pacotes) > 5:
                    self.estatisticas["gargalos"][nome] += len(pacotes)
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        
        # Ordena a fila após coletar todos
        self.ordenar_triagem()
        
        print(f"\n📊 Total coletado: {self.estatisticas['total_coletado']}")
        print(f"📊 Fila ordenada por prioridade (1=urgente, 5=normal)")
        print("="*50)
        time.sleep(1)
    
    def rotear_despacho(self, pacote):
        """Decide o destino baseado em regras de negócio"""
        setor = pacote["setor_origem"]
        prioridade = pacote["prioridade_calculada"]
        
        # Regra 1: Saúde emergencial
        if setor == "Saúde" and prioridade == 1:
            return self.consumidores["Emergência"]
        
        # Regra 2: Alimentos críticos
        elif setor == "Alimentos" and prioridade == 1:
            return self.consumidores["Alimentos"]
        
        # Regra 3: Baixa prioridade vai pra transportadora
        elif setor in ["Varejo", "Jurídico"] and prioridade >= 5:
            return "TRANSPORTADORA"
        
        # Regra 4: Consumidor padrão do setor
        elif setor in self.consumidores:
            return self.consumidores[setor]
        
        else:
            return ConsumidorFinal("Processamento Geral", "PADRÃO")
    
    def despachar_final(self):
        """Despacha itens em ordem de prioridade"""
        print("\n" + "="*50)
        print("🚀 DESPACHO FINAL - ORDEM DE PRIORIDADE")
        print("="*50)
        time.sleep(1.5)
        
        if not self.triagem_central:
            print("⚠️  Fila vazia!")
            return
        
        total = len(self.triagem_central)
        
        for i, pacote in enumerate(self.triagem_central, 1):
            setor = pacote["setor_origem"]
            pri = pacote["prioridade_calculada"]
            
            print(f"\n─── Despacho {i}/{total} ───")
            time.sleep(0.8)
            
            # Tempo de vida
            timestamp = pacote.get("timestamp_criacao")
            if timestamp:
                tempo_vida = datetime.now() - timestamp
                print(f"⏱️  Tempo no sistema: {tempo_vida}")
            
            print(f"📋 ID: {pacote['id_original']}")
            print(f"🏭 Origem: {setor} | Prioridade: {pri}")
            
            # Roteamento
            destino = self.rotear_despacho(pacote)
            
            if destino == "TRANSPORTADORA":
                print(f"📦 Conteúdo: {pacote['conteudo']}")
                self.transportadora.aguardar_transporte(pacote)
            else:
                print(f"📦 Conteúdo: {pacote['conteudo']}")
                print(f"🎯 Destino: {destino.nome} ({destino.regra_entrega})")
                destino.receber_item(pacote)
            
            self.estatisticas["total_despachado"] += 1
            time.sleep(0.3)
        
        # Limpa a fila após despachar
        self.triagem_central.clear()
        
        print(f"\n✅ Despacho concluído: {total} itens")
        print("="*50)
        time.sleep(1)
    
    def painel_monitoramento(self):
        """Painel simples de monitoramento"""
        self.monitorando = True
        
        def monitorar():
            while self.monitorando:
                os.system('clear' if os.name == 'posix' else 'cls')
                
                print("="*50)
                print("🎛️  PAINEL DE MONITORAMENTO - HUB CENTRAL")
                print("="*50)
                print(f"⏰ Operação: {datetime.now() - self.tempo_inicio}")
                print(f"📊 Pendentes: {len(self.triagem_central)}")
                print(f"📥 Coletados: {self.estatisticas['total_coletado']}")
                print(f"📤 Despachados: {self.estatisticas['total_despachado']}")
                
                # Gargalo
                print(f"\n🔍 GARGALOS:")
                for nome, qtd in self.estatisticas["gargalos"].items():
                    if qtd > 0:
                        print(f"   {nome}: {qtd} itens")
                
                # Consumidores
                print(f"\n🏢 CONSUMIDORES:")
                for nome, cons in self.consumidores.items():
                    if cons.itens_entregues:
                        print(f"   {cons.nome}: {len(cons.itens_entregues)}")
                
                # Transportadora
                print(f"\n🚛 TRANSPORTADORA: {len(self.transportadora.fila_transporte)} itens")
                
                print("="*50)
                time.sleep(3)
        
        thread = threading.Thread(target=monitorar, daemon=True)
        thread.start()
    
    def parar_monitoramento(self):
        self.monitorando = False


# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    print("\n" + "="*50)
    print("   🚀 HUB CENTRAL DE DISTRIBUIÇÃO")
    print("="*50)
    time.sleep(1)
    
    # Inicializa Hub
    print("\n🔧 Inicializando...")
    hub = HubCentral()
    print("✅ Hub pronto!")
    time.sleep(0.5)
    
    # Registra setores
    print("\n📋 Registrando setores...")
    print("-"*30)
    
    try:
        hub.registrar_setor("Varejo", sv.fila2, adaptador_varejo)
        print(f"✅ Varejo ({len(sv.fila2)} itens)")
    except Exception as e:
        print(f"❌ Varejo: {e}")
    
    try:
        hub.registrar_setor("Jurídico", sj.fila2, adaptador_juridico)
        print(f"✅ Jurídico ({len(sj.fila2)} itens)")
    except Exception as e:
        print(f"❌ Jurídico: {e}")
    
    try:
        hub.registrar_setor("Alimentos", sa.fila_2, adaptador_alimentos)
        print(f"✅ Alimentos ({len(sa.fila_2)} itens)")
    except Exception as e:
        print(f"❌ Alimentos: {e}")
    
    try:
        hub.registrar_setor("Saúde", ss.fila_ordenada, adaptador_saude)
        print(f"✅ Saúde ({len(ss.fila_ordenada)} itens)")
    except Exception as e:
        print(f"❌ Saúde: {e}")
    
    print("-"*30)
    time.sleep(1)
    
    # Inicia monitor
    print("\n🎛️  Painel de monitoramento ativo!")
    hub.painel_monitoramento()
    time.sleep(2)
    
    # Coleta
    print("\n" + "="*50)
    print("   🔄 CICLO DE COLETA")
    print("="*50)
    time.sleep(1)
    
    hub.coletar_round_robin()
    
    print("\n⏳ Processando...")
    time.sleep(3)
    
    # Despacho
    print("\n" + "="*50)
    print("   📤 PROCESSO DE DESPACHO")
    print("="*50)
    time.sleep(1)
    
    hub.despachar_final()
    
    # Relatório final
    print("\n" + "="*50)
    print("📊 RELATÓRIO FINAL")
    print("="*50)
    time.sleep(2)
    
    print(f"\n📈 RESUMO:")
    print(f"   • Coletados: {hub.estatisticas['total_coletado']}")
    print(f"   • Despachados: {hub.estatisticas['total_despachado']}")
    print(f"   • Transportadora: {len(hub.transportadora.fila_transporte)}")
    print(f"   • Tempo total: {datetime.now() - hub.tempo_inicio}")
    
    time.sleep(2)
    
    # Finaliza
    print("\n🛑 Finalizando...")
    hub.parar_monitoramento()
    time.sleep(1)
    
    print("\n" + "="*50)
    print("   ✅ HUB FINALIZADO COM SUCESSO!")
    print("="*50)