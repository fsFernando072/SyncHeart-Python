# ANÁLISE DOS DADOS COLETADOS

# 1) Estatísticas descritivas
summary(dados$cpu) # retorna um resumo dos dados, como o mínimo, máximo, média e mediana
sd(dados$ram) # retorna o desvio padrão dos dados (dispersão dos dados em torno da média)
quantile(dados$disco, probs = c(0.25, 0.75, 0.95)) # retorna os quantis dados (primeiro quarto, segundo quarto, etc)

# 2) Visualizações temporais
dados$horario <- as.POSIXct(dados$horario) # conversão do formato datahora

plot(dados$horario, dados$cpu, type = "l", # gráfico de linha que demonstra o uso de CPU
     xlab = "Data/Hora", ylab = "Uso de CPU (%)", # (em porcentagem) ao longo do tempo
     main = "Uso de CPU ao Longo do Tempo")

plot(dados$horario, dados$cpu, type = "l", col = "red", # gráfico de linha que junta o gráfico acima com
     ylim = c(0, 100), xlab = "Data/Hora", ylab = "Uso (%)") # o gráfico de linha do uso de RAM (em porcentagem)
lines(dados$horario, dados$ram, col = "blue")
legend("right", legend = c("CPU", "RAM"), 
       col = c("red", "blue"), lty = 1)

plot(dados$horario, dados$disco, type = "l", # gráfico de linha que demonstra o uso de disco
     xlab = "Data/Hora", ylab = "Uso de Disco (kB)", # (em kiloBytes)
     main = "Uso de Disco ao Longo do Tempo")

dados$disco_MB <- dados$disco / 1024

plot(dados$horario, dados$disco_MB, type = "l", # gráfico de linha que demonstra o uso de disco
     xlab = "Data/Hora", ylab = "Uso de Disco (MB)", # (em MegaBytes)
     main = "Uso de Disco ao Longo do Tempo")

# 3) Histograma do uso de CPU do marca-passo
hist(dados$cpu, main = "Histograma de uso de CPU",
     xlab = "Uso de CPU (%)")

# 3) Função para gerar relatório resumido
calcular_tempo_acima_limite <- function(valores, limite) { # função que calcula o tempo gasto
  sum(valores > limite, na.rm = TRUE) / length(na.omit(valores)) * 100 # acima de um determinado limite
}

gerar_relatorio <- function(dados) {
  cat("=== RELATÓRIO DE MONITORAMENTO ===\n\n")
  
  cat("Período analisado:", 
      format(min(dados$horario), "%Y-%m-%d"), "a",
      format(max(dados$horario), "%Y-%m-%d"), "\n\n")
  
  cat("ESTATÍSTICAS GERAIS:\n")
  cat("CPU - Média:", round(mean(dados$cpu, na.rm = TRUE), 1), "%\n")
  cat("RAM - Média:", round(mean(dados$ram, na.rm = TRUE), 1), "%\n")
  cat("Disco - Média:", round(mean(dados$disco, na.rm = TRUE), 1), "kB\n\n")
  
  cat("TEMPO ACIMA DE LIMITES CRÍTICOS:\n")
  cat("CPU > 25%:", round(calcular_tempo_acima_limite(dados$cpu, 25), 1), "%\n")
  cat("RAM > 55%:", round(calcular_tempo_acima_limite(dados$ram, 55), 1), "%\n")
}

gerar_relatorio(dados)