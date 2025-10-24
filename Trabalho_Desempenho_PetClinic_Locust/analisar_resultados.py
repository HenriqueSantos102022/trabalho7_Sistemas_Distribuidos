import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Define os nomes de endpoint que queremos analisar individualmente
# (O 'name' que definimos no locustfile para o GET /owners/{id})
ENDPOINTS_DE_INTERESSE = [
    "/api/customer/owners",
    "/api/customer/owners/[id]",
    "/api/vet/vets",
    "/api/customer/owners" # O 'POST' tem o mesmo nome do 'GET'
]

def processar_resultados():
    """
    Lê todos os CSVs da pasta /results, calcula as médias 
    e retorna dois DataFrames: um agregado e um por endpoint.
    """
    arquivos_csv = glob.glob("results/*_stats.csv")
    
    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado em /results.")
        print("Certifique-se de que o script 'run_all_tests.sh' foi executado.")
        return None, None

    lista_resultados_agregados = []
    lista_resultados_endpoints = []

    for f in arquivos_csv:
        nome_arquivo = os.path.basename(f)
        
        # Define o cenário
        if "cenario_A" in nome_arquivo:
            cenario = "A (Leve)"
        elif "cenario_B" in nome_arquivo:
            cenario = "B (Moderado)"
        elif "cenario_C" in nome_arquivo:
            cenario = "C (Pico)"
        else:
            continue
            
        df_run = pd.read_csv(f)
        
        # --- 1. Processamento de Dados Agregados ---
        df_agregado = df_run[df_run["Name"] == "Aggregated"].iloc[0]
        
        total_reqs = df_agregado["Request Count"]
        total_fails = df_agregado["Failure Count"]
        success_perc = 100 * (total_reqs - total_fails) / total_reqs if total_reqs > 0 else 100
        
        lista_resultados_agregados.append({
            "Cenário": cenario,
            "Tempo Médio (ms)": df_agregado["Average Response Time"],
            "Tempo Máximo (ms)": df_agregado["Max Response Time"],
            "P90 (ms)": df_agregado["90%"], # Nova Métrica
            "Req/s": df_agregado["Requests/s"],
            "Total Requisições": total_reqs,
            "Total Falhas": total_fails, # Nova Métrica
            "% Sucesso": success_perc
        })
        
        # --- 2. Processamento de Dados por Endpoint ---
        df_endpoints = df_run[df_run["Name"].isin(ENDPOINTS_DE_INTERESSE)]
        
        for _, row in df_endpoints.iterrows():
            # Combina Método (GET/POST) com Nome da URL
            endpoint_name = f"{row['Type']} {row['Name']}"
            
            ep_reqs = row["Request Count"]
            ep_fails = row["Failure Count"]
            ep_success_perc = 100 * (ep_reqs - ep_fails) / ep_reqs if ep_reqs > 0 else 100
            
            lista_resultados_endpoints.append({
                "Cenário": cenario,
                "Endpoint": endpoint_name,
                "Tempo Médio (ms)": row["Average Response Time"],
                "% Sucesso": ep_success_perc
            })

    # Cria os DataFrames finais
    df_completo_agregado = pd.DataFrame(lista_resultados_agregados)
    df_completo_endpoints = pd.DataFrame(lista_resultados_endpoints)
    
    # Define a ordem correta dos cenários
    ordem_cenarios = ["A (Leve)", "B (Moderado)", "C (Pico)"]
    
    # Calcula a média dos 5 runs para cada cenário (Agregado)
    df_final_agregado = df_completo_agregado.groupby("Cenário").mean().reset_index()
    df_final_agregado = df_final_agregado.set_index("Cenário").reindex(ordem_cenarios).reset_index()

    # Calcula a média dos 5 runs para cada cenário (Endpoint)
    df_final_endpoints = df_completo_endpoints.groupby(["Cenário", "Endpoint"]).mean().reset_index()
    
    return df_final_agregado, df_final_endpoints

def salvar_graficos_agregados(df):
    """Gera os 4 gráficos Agregados (Gerais)."""
    if df is None: return
    print("Gerando gráficos Agregados (1 a 4)...")
    
    # --- Gráfico 1: Tempo de Resposta (Médio vs Máximo) ---
    df.plot(x="Cenário", y=["Tempo Médio (ms)", "Tempo Máximo (ms)"],
            kind="bar", figsize=(10, 6),
            title="Tempo de Resposta Médio e Máximo por Cenário (Agregado)")
    plt.ylabel("Tempo (ms)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("results/grafico_01_tempo_medio_max.png")

    # --- Gráfico 2: Requisições por Segundo (RPS) ---
    df.plot(x="Cenário", y="Req/s",
            kind="bar", figsize=(10, 6), color='blue',
            title="Requisições por Segundo (RPS) por Cenário (Agregado)",
            legend=False)
    plt.ylabel("Requisições/Segundo")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("results/grafico_02_req_por_segundo.png")

    # --- Gráfico 3: Porcentagem de Sucesso ---
    df.plot(x="Cenário", y="% Sucesso",
            kind="bar", figsize=(10, 6), color='green',
            title="Porcentagem de Sucesso por Cenário (Agregado)",
            legend=False)
    plt.ylabel("% de Sucesso")
    plt.ylim(0, 101)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("results/grafico_03_sucesso_perc.png")

    # --- Gráfico 4: Total de Requisições Atendidas ---
    df.plot(x="Cenário", y="Total Requisições",
            kind="bar", figsize=(10, 6), color='purple',
            title="Total de Requisições Atendidas por Cenário",
            legend=False)
    plt.ylabel("Nº de Requisições")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("results/grafico_total_reqs.png")
    print("Salvo: results/grafico_04_total_reqs.png")

    # --- GRÁFICO 5: Percentil 90 (P90) ---
    df.plot(x="Cenário", y="P90 (ms)",
            kind="bar", figsize=(10, 6), color='orange',
            title="Percentil 90 (P90) de Tempo de Resposta (Agregado)",
            legend=False)
    plt.ylabel("Tempo (ms)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("results/grafico_05_tempo_p90.png")

    # --- GRÁFICO 6: Contagem Total de Falhas ---
    df.plot(x="Cenário", y="Total Falhas",
            kind="bar", figsize=(10, 6), color='red',
            title="Contagem Total de Falhas por Cenário (Agregado)",
            legend=False)
    plt.ylabel("Nº de Falhas (Média das 5 runs)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("results/grafico_06_total_falhas.png")
    
    print("Gráficos 1 a 5 salvos.")
    plt.close('all')

def salvar_graficos_endpoints(df):
    """Gera os 2 gráficos por Endpoint."""
    if df is None: return
    print("Gerando gráficos por Endpoint (6 e 7)...")
    
    # Define a ordem correta dos cenários
    ordem_cenarios = ["A (Leve)", "B (Moderado)", "C (Pico)"]

    # --- GRÁFICO 7: Tempo Médio por Endpoint ---
    df_pivot_tempo = df.pivot(index='Endpoint', columns='Cenário', values='Tempo Médio (ms)')
    # Reordena as colunas
    df_pivot_tempo = df_pivot_tempo.reindex(columns=ordem_cenarios) 
    
    df_pivot_tempo.plot(kind="bar", figsize=(12, 7),
                        title="Tempo Médio de Resposta por Endpoint")
    plt.ylabel("Tempo (ms)")
    plt.xlabel("Endpoint")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("results/grafico_07_endpoint_tempo.png")

    # --- GRÁFICO 8: Taxa de Sucesso por Endpoint ---
    df_pivot_sucesso = df.pivot(index='Endpoint', columns='Cenário', values='% Sucesso')
    # Reordena as colunas
    df_pivot_sucesso = df_pivot_sucesso.reindex(columns=ordem_cenarios)
    
    df_pivot_sucesso.plot(kind="bar", figsize=(12, 7),
                          title="Taxa de Sucesso por Endpoint")
    plt.ylabel("% Sucesso")
    plt.xlabel("Endpoint")
    plt.ylim(0, 101)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("results/grafico_08_endpoint_sucesso.png")
    
    print("Gráficos 6 e 7 salvos.")
    plt.close('all')

def main():
    # 1. Processa os dados dos CSVs e calcula as médias
    df_agregado, df_endpoints = processar_resultados()
    
    if df_agregado is not None:
        # 2. Salva a tabela de resumo (Agregado)
        caminho_tabela_agregado = "results/tabela_resumo_agregado.csv"
        df_agregado.to_csv(caminho_tabela_agregado, index=False, float_format='%.2f')
        print(f"Tabela de resumo AGREGADO salva em: {caminho_tabela_agregado}")
        
        # Imprime a tabela Agregada no console
        print("\n--- Tabela de Resumo (AGREGADO - Média de 5 execuções) ---")
        print(df_agregado.to_string(index=False, float_format='%.2f'))
        print("-----------------------------------------------------------\n")
        
        # 3. Gera e salva os gráficos Agregados
        salvar_graficos_agregados(df_agregado)

    if df_endpoints is not None:
        # 4. Salva a tabela de resumo (Endpoint)
        caminho_tabela_endpoints = "results/tabela_resumo_endpoints.csv"
        df_endpoints.to_csv(caminho_tabela_endpoints, index=False, float_format='%.2f')
        print(f"Tabela de resumo por ENDPOINT salva em: {caminho_tabela_endpoints}")
        
        # 5. Gera e salva os gráficos por Endpoint
        salvar_graficos_endpoints(df_endpoints)

if __name__ == "__main__":
    plt.style.use('ggplot') # Define o estilo dos gráficos
    main()