#!/bin/bash
echo "Iniciando a bateria de testes automatizada..."

# Garante que a pasta de resultados exista
mkdir -p results

# Define os cenários
# Formato: "nome_base usuarios spawn_rate tempo_execucao"
SCENARIOS=(
    "cenario_A 50 10 5m"
    "cenario_B 100 20 5m"
    "cenario_C 200 30 3m"
)

# Define o número de repetições por cenário
REPETICOES=5

# Loop principal de cenários
for scenario in "${SCENARIOS[@]}"; do
    # Desmembra os parâmetros
    read -r NOME_BASE USERS SPAWN_RATE RUNTIME <<< "$scenario"
    
    echo "-----------------------------------------------------"
    echo "Iniciando Cenário: $NOME_BASE ($USERS usuários, $RUNTIME)"
    echo "-----------------------------------------------------"

    # Loop de repetições
    for (( i=1; i<=$REPETICOES; i++ )); do
        echo "-> Rodada $i de $REPETICOES..."
        
        # Define o nome único do arquivo CSV
        CSV_PREFIX="results/${NOME_BASE}_run_${i}"

        # Executa o Locust
        locust -f locustfile.py \
               --host=http://localhost:8080 \
               --headless \
               --users $USERS \
               --spawn-rate $SPAWN_RATE \
               --run-time $RUNTIME \
               --csv=$CSV_PREFIX \
               --csv-full-history
        
        echo "-> Rodada $i concluída. CSV salvo em ${CSV_PREFIX}_stats.csv"
    done
done

echo "-----------------------------------------------------"
echo "Bateria de testes completa. Todos os CSVs estão em /results."
echo "-----------------------------------------------------"