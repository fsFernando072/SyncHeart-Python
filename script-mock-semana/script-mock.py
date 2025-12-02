import csv
import random
from datetime import datetime, timedelta

# --- Configurações Globais ---
uuid = "680fab1b-5333-4caa-970b-091a484dcf7d"
header = [
    "timestamp_utc", "uuid", "arritmia_detectada", "cpu_porcentagem",
    "ram_porcentagem", "disco_uso_kb", "bateria_porcentagem",
    "total_tarefas_ativas", "lista_tarefas_ativas"
]
tarefas_base = ["task_monitor_heartbeat", "task_data_logging"]
tarefas_extra = ["task_pacing_control", "task_battery_management"]

# --- Funções de Geração de Dados (inalteradas) ---
def gerar_ram(linha_idx, total_linhas):
    if linha_idx in random.sample(range(total_linhas), k=2):
        return round(random.uniform(86, 95), 2)  # crítico
    else:
        return round(random.uniform(70, 84), 2)  # normal/atenção

def gerar_cpu(linha_idx, total_linhas):
    if linha_idx in random.sample(range(total_linhas), k=2):
        return round(random.uniform(21, 30), 2)  # crítico
    else:
        return round(random.uniform(5, 19), 2)  # normal/atenção

def gerar_bateria(linha_idx, bateria_inicial=100, decaimento=0.01):
    valor = bateria_inicial - (linha_idx * decaimento)
    return max(round(valor, 2), 0)

def gerar_linha(base_time, linha_idx, total_linhas, bateria_inicial):
    timestamp = base_time.strftime("%Y-%m-%d %H:%M:%S")
    arritmia = random.choice([False] * 9 + [True])
    cpu = gerar_cpu(linha_idx, total_linhas)
    ram = gerar_ram(linha_idx, total_linhas)
    disco = round(173578407 + random.uniform(0, 1000), 4)
    bateria = gerar_bateria(linha_idx, bateria_inicial)
    
    tarefas = tarefas_base + tarefas_extra if arritmia else tarefas_base
    total_tarefas = len(tarefas)
    lista_tarefas = ",".join(tarefas)
    
    return [
        timestamp, uuid, arritmia, cpu, ram, disco, bateria, total_tarefas, lista_tarefas
    ]

# --- Funções de Geração de Arquivos Refatoradas ---

def gerar_csv_diario(data_inicio_periodo, n_linhas=360, bateria_inicial=100):
    """Gera um único arquivo CSV para um dia e período específicos."""
    
    # Define o nome do arquivo com base na data e hora de início (12h)
    timestamp_str = data_inicio_periodo.strftime("%Y-%m-%d_%Hh")
    output_file = f"{timestamp_str}_{uuid}.csv"
    
    # Intervalo de captura de 10 segundos
    step = timedelta(seconds=10)
    
    with open(output_file, "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for i in range(n_linhas):
            # O timestamp de cada linha é calculado a partir da data_inicio_periodo
            current_time = data_inicio_periodo + i * step
            linha = gerar_linha(current_time, i, n_linhas, bateria_inicial)
            writer.writerow(linha)

    print(f"Arquivo '{output_file}' gerado com {n_linhas} linhas (período de 1 hora a partir de 12h).")

def gerar_semana():
    """Gera 7 arquivos CSV, um para cada dia da semana, começando às 12h."""
    
    # Data de início solicitada: 8 de Dezembro de 2025, 12:00:00 (Segunda-feira)
    data_inicio_base = datetime(2025, 12, 1, 12, 0, 0)
    
    # Número de linhas para cobrir exatamente 1 hora em passos de 10s: (3600s / 10s)
    linhas_por_hora = 360 

    print(f"Iniciando a geração de 7 arquivos para a semana a partir de {data_inicio_base.strftime('%Y-%m-%d')}.")

    for dia in range(7):
        # Calcula a data de início para o dia específico (incrementa dias, mantem 12h)
        data_atual_12h = data_inicio_base + timedelta(days=dia)
        
        # Gera o CSV para esse dia. A bateria_inicial é sempre 100% para cada novo dia/arquivo.
        gerar_csv_diario(
            data_inicio_periodo=data_atual_12h,
            n_linhas=linhas_por_hora,
            bateria_inicial=100
        )
    
    print("\nGeração de todos os arquivos da semana concluída.")


if __name__ == "__main__":
    # Remove a chamada antiga e chama a nova função principal
    # gerar_csv(360) 
    gerar_semana()