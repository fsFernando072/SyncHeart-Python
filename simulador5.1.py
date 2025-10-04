# funções relacionadas a tempo tanto do mundo real quanto do processo.
import time
from datetime import datetime

# funções que permitem a geração de números randômicos.
import random

# funções para o monitoramento das peças de Hardware.
import psutil

# funções para manipular arquivos CSV.
import pandas

# ----- Variáveis Globais -----
# Usadas para melhorar a qualidade das informações de disco e bateria.
# As qtd armazenam cada vezes que ocorreu um monitoramento ou uma arritmia
# e as total armazenam um número aleatório correspondente ao disco ou a bateria
# para que os valores finais das mesmas sejam iguais durante toda a execução.
while True:

    qtdArritmia = 0
    qtdMonitoramento = 0
    totalArritmia = 0.0
    totalMonitoramento = 0.0
    inicio = time.time()
    tempoMaximo = 30 * 60
    qtdProcessos = 0
    dados = []
    tempoCsv = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    usuario = input("Escreva o código da máquina (marca-passo): ")

    while True:
        # Métricas passadas durante a execução.
        # Bateria comum de um marcapasso possui 1620J
        # Um fluxo comum de dados gasta cerca de 0,739J por dia (0,046%)
        # Com arritmias, o gasto vai para 1,48J (0,092%)

        disco = psutil.disk_usage("/").percent
    
        # A CPU comumente varia entre 1% a 5%, já quando tem arritmia pode variar de 10% a 30%
        cpu = psutil.cpu_percent(interval=0.1) / 3

        # Vezes 0.6 para se aproximar da média de 30 KB a 50 KB do uso de uma ram de 254 KB.
        # A ram costuma ter um consumo padrão de 5% a 15% normalmente, com arritmia passa a ser 15% a 40%
        ram = psutil.virtual_memory().percent * 0.6
    
        # Horário em que foram gerados os dados acima.
        # tempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        tempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Porcentagem atual da bateria
        bateria = 0.0 #%

        # Quantidade de processos simultâneos
        qtdProcessos = len(list(psutil.process_iter()))
    
        # Simula o tempo de espera entre batimentos cardíacos reais.
        # time.sleep(random.uniform(0.7, 1.1))
        time.sleep(9.9)
        
        # Coletando porcentagem da bateria
        bateria = psutil.sensors_battery()[0] # [0] indica o primeiro item retornado do comando, que é a porcentagem

        # Variável de detecção de arritmia
        arritmiaDetectada = False

        # 20% de chance de arritmia.
        if random.random() < 0.2:
            arritmiaDetectada = True # ativando variavel
            # Somando nas variáveis globais.
            totalArritmia += random.uniform(0.3, 0.5)
            qtdArritmia = 1
        
            # Alterações por conta da arritmia.
            cpu += random.uniform(9, 20)
            disco += (totalArritmia) + (totalMonitoramento * qtdMonitoramento)
            ram += 20
        
            # Tempo que a execução é interrompida para simular o estímulo no coração
            time.sleep(0.1) 
        else:
            # Somando nas variáveis globais
            totalMonitoramento += random.uniform(0.0625, 0.1170)
            qtdMonitoramento += 1
        
            # Alterações por conta do monitoramento.
            disco += (totalArritmia * qtdArritmia) + (totalMonitoramento * qtdMonitoramento)
        
        # Adicionando os dados no dicionário.
        dados.append({
            "horario": tempo,
            "arritmia": arritmiaDetectada,
            "cpu(%)": cpu,
            "ram(KB)": ram,
            "disco(KB)": disco,
            "bateria(%)": bateria,
            "qtd_processos": qtdProcessos,
            "usuario": usuario
        })

        # Print no terminal.
        if arritmiaDetectada:
            print(f"-- Tempo: {tempo} Arritmia detectada! --")
            arritmiaDetectada = False # desativando variável
        else:
            print(f"\n--- Tempo: {tempo} ---")
        print(f"""
CPU: {cpu:.1f}%
RAM: {ram:.1f} KB
Disco: {disco:.1f} KB
Bateria: {bateria}%
Qtd Processos: {qtdProcessos}
Usuário: {usuario}
""")
        # Alerta de threads se RAM > 40 ---
        if ram > 40:  
            procs_threads = []
            for proc in psutil.process_iter(['name']):
                try:
                    procs_threads.append((proc.info['name'], proc.num_threads()))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # ordena do maior para o menor número de threads
            top3 = sorted(procs_threads, key=lambda x: x[1], reverse=True)[:3]

            print(">> ALERTA DE RAM SOBRECARREGADA (RAM > 40%)\nTop 3 processos por número de threads:")
            for nome, qtd in top3:
                print(f"   {nome} - {qtd} threads")

        print("-----------------------------------\n")

        df = pandas.DataFrame(dados)
        df.to_csv(f"dados-{usuario}.csv", index=False, float_format="%.2f")
        
        if time.time() - inicio >= tempoMaximo:
            break
