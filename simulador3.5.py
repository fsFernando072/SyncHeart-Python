# funções relacionadas a tempo tanto do mundo real quanto do processo.
import time

# funções que permitem a geração de números randomicos.
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
    dados = []
    tempoCsv = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())

    while True:
        # Métricas passadas durante a execução.
        # Bateria comum de um marcapasso possui 1620J
        # Um fluxo comum de dados gasta cerca de 0,739J por dia (0,046%)
        # Com arritmias, o gasto vai para 1,48J (0,092%)

        disco = psutil.disk_usage("/").percent
    
        # A CPU comumente varia entre 1% a 5%, já quando tem arritmia pode variar de 10% a 30%
        cpu = psutil.cpu_percent(interval=1) / 3

        # Vezes 0.6 para se aproximar da média de 30 KB a 50 KB do uso de uma ram de 254 KB.
        # A ram costuma ter um consumo padrão de 5% a 15% normalmente, com arritimia passa a ser 15% a 40%
        ram = psutil.virtual_memory().percent * 0.6
    
        # Horário em que foram gerados os dados acima.
        tempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
        # Simula o tempo de espera entre batimentos cardíacos reais.
        time.sleep(random.uniform(0.8, 1.2))
    
        # 1% de chance de arritmia.
        if random.random() < 0.01:
            # Somando nas variáveis globais.
            totalArritmia += random.uniform(0.3, 0.5)
            qtdArritmia += 1
        
            # Alterações por conta da arritmia.
            cpu += random.uniform(9, 20)
            disco += (totalArritmia * qtdArritmia) + (totalMonitoramento * qtdMonitoramento)
            ram += 20
        
            # Print no terminal.
            print(f"-- Tempo: {tempo} Arritmia detectada! --")
            print(f"CPU: {cpu:.1f}% \nRAM: {ram:.1f} KB \nDisco: {disco:.1f} KB")
            print("-----------------------------------\n")
        
            # Tempo que a execução é interrompida para simular o estímulo no coração
            time.sleep(0.1)
        
            dados.append({
                "horario": tempo,
                "cpu": cpu,
                "ram": ram,
                "disco": disco,
            })
            
        else:
            # Somando nas variáveis globais
            totalMonitoramento += random.uniform(0.0625, 0.1170)
            qtdMonitoramento += 1
        
            # Alterações por conta do monitoramento.
            disco += (totalArritmia * qtdArritmia) + (totalMonitoramento * qtdMonitoramento)
        
            # Print no terminal.
            print(f"\n--- Tempo: {tempo}s ---")
            print(f"CPU: {cpu:.1f}% \nRAM: {ram:.1f} KB \nDisco: {disco:.1f} KB")
            print("-----------------------------------\n")
    
        df = pandas.DataFrame(dados)
        df.to_csv(f"dados-{tempoCsv}.csv", index=False, float_format="%.2f")
        
        if time.time() - inicio >= tempoMaximo:
            break