# Avaliação de Desempenho do Spring PetClinic (Microservices) com Locust

🎥 [Assista ao vídeo de demonstração no YouTube](https://www.youtube.com/watch?v=slVGNqvesc4)

Este repositório contém os artefatos para um trabalho de avaliação de desempenho. O objetivo principal é medir e relatar o desempenho básico da aplicação **Spring PetClinic (versão microsserviços)**, utilizando a ferramenta de teste de carga **Locust**.

## 🎯 Aplicação-Alvo

A aplicação testada é o **Spring PetClinic - Microservices**. Esta arquitetura é composta por múltiplos serviços, incluindo: API Gateway, Customers, Vets, e Visits.

**Repositório Oficial:** [https://github.com/spring-petclinic/spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices)

## 🛠️ Ferramentas Utilizadas

**Docker & Docker Compose:** Para containerizar e executar a aplicação PetClinic.\
**Locust:** Ferramenta de teste de carga (escrita em Python) para simular o comportamento do usuário.\
**Python 3:** Para executar o Locust e os scripts de análise.\
**Bibliotecas Python:** `pandas` e `matplotlib` para análise e plotagem dos resultados.\
**Bash Script:** Para automatizar a execução de múltiplos cenários e repetições.\
**WSL 2 (Recomendado):** Para um ambiente Linux no Windows, facilitando a execução de scripts `.sh`.

## 📂 Estrutura do Repositório

```
.
├── locustfile.py           # Script principal do Locust (define as tarefas e o mix de carga)
├── run_all_tests.sh        # Script BASH para executar TODOS os cenários e repetições
├── analisar_resultados.py  # Script Python para ler os CSVs e gerar gráficos/tabelas
├── README.md               # Este arquivo
└── results/                # Pasta de destino para os CSVs brutos, tabelas de resumo e gráficos (.png)
```

## 🚀 Como Executar o Teste (Passo a Passo)

Siga estas etapas para configurar o ambiente e reproduzir a avaliação de desempenho.

### 1. Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:
* [Git](https://git-scm.com/downloads)
* [Docker Desktop](https://www.docker.com/products/docker-desktop) (com Docker Compose)
* [Python 3](https://www.python.org/downloads/)

### 2. Configuração do Ambiente

Recomenda-se usar **dois terminais** (ou duas janelas do VS Code) para este processo: um para o "Servidor" (PetClinic) e outro para o "Cliente" (Locust).

**Terminal 1: Subir a Aplicação (Spring PetClinic)**

1.  Clone o repositório oficial da aplicação (em um local separado do seu projeto de teste):
    ```bash
    git clone [https://github.com/spring-petclinic/spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices)
    cd spring-petclinic-microservices
    ```
2.  Inicie os contêineres:
    ```bash
    docker-compose up
    ```
3.  **Deixe este terminal rodando.** A aplicação estará disponível em `http://localhost:8080`.

**Terminal 2: Configurar o Projeto de Teste (Este Repositório)**

1.  Clone *este* repositório:
    ```bash

    git clone [https://github.com/HenriqueSantos102022/trabalho7_Sistemas_Distribuidos.git](https://github.com/HenriqueSantos102022/trabalho7_Sistemas_Distribuidos.git)
    cd trabalho7_Sistemas_Distribuidos
    ```
2.  (Opcional, mas recomendado) Crie e ative um ambiente virtual Python:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac/WSL
    # .\venv\Scripts\activate  # Windows (CMD/PowerShell)
    ```
3.  Instale as dependências do Locust e da análise:
    ```bash
    pip install locust pandas matplotlib
    ```
4.  Dê permissão de execução ao script principal (Linux/Mac/WSL):
    ```bash
    chmod +x run_all_tests.sh
    ```

### 3. Execução da Bateria de Testes

No **Terminal 2**, com a aplicação rodando no Terminal 1, execute o script de automação:

```bash
./run_all_tests.sh
```

Este script executará automaticamente todos os 3 cenários (A, B, C) com 5 repetições cada. O processo total levará aproximadamente **65 minutos**. Ele salvará 15 arquivos CSV na pasta `results/`.

### 4. Análise e Geração de Gráficos

Após a conclusão do `run_all_tests.sh`:

1.  Execute o script de análise para processar os dados:
    ```bash
    python3 analisar_resultados.py
    ```
2.  O script irá:
    * Imprimir tabelas de resumo diretamente no terminal.
    * Salvar as tabelas em `results/tabela_resumo_agregado.csv` e `results/tabela_resumo_endpoints.csv`.
    * Gerar e salvar todos os 7 gráficos (como `.png`) na pasta `results/`.

## 📈 Cenários de Teste

O plano de teste consiste em 3 cenários de carga, executados 5 vezes cada (modificado das 30 repetições originais para otimizar o tempo).

**Cenário A (Leve):** 50 usuários por 5 minutos.
**Cenário B (Moderado):** 100 usuários por 5 minutos.
**Cenário C (Pico):** 200 usuários por 3 minutos.

O `locustfile.py` executa 4 tarefas com o seguinte *mix* de carga:

`GET /owners` (lista donos): 40% 
`GET /owners/{id}` (detalhe do dono): 30% 
`GET /vets` (lista veterinários): 20% 
`POST /owners` (cadastro de dono): 10% 

## 📊 Resultados e Entregáveis

Os resultados finais gerados pelo script `analisar_resultados.py` são salvos na pasta `/results`. As métricas analisadas incluem:

Tempo médio de resposta
Tempo máximo de resposta
Percentil 90 (P90) de resposta
Requisições por segundo (req/s)
% de Sucesso e contagem de Erros

Os gráficos gerados incluem:
1.  Tempo de Resposta Médio e Máximo (Agregado)
2.  Requisições por Segundo (Agregado)
3.  Porcentagem de Sucesso (Agregado)
4.  Percentil 90 (P90) de Tempo de Resposta (Agregado)
5.  Contagem Total de Falhas (Agregado)
6.  Tempo Médio de Resposta por Endpoint

7.  Taxa de Sucesso por Endpoint
