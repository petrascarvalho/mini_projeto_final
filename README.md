# 📊 Mini Projeto — Visualização de Dados e Business Intelligence

**Curso:** SENAI/SC — Lab 365  
**Módulo:** M1S07  
**Professor:** Rodrigo Garcia Brunini  
**Base de Dados:** FreeSQL — Human Resources `HR`  
**Autor:** Petras Ruben Carvalho  

---

## 🎯 Objetivo do Projeto

Este repositório contém o desenvolvimento de um pipeline de análise de dados utilizando **SQL** e **Python**, a partir da base **Human Resources (HR)** disponível no ambiente FreeSQL.

O objetivo principal do projeto é estruturar dados brutos, realizar consultas SQL, exportar os resultados para CSV, aplicar técnicas de tratamento e limpeza dos dados, gerar métricas estatísticas e construir gráficos para apoiar a tomada de decisão.

---

## 🧭 Visão Geral do Pipeline

```text
Base HR no FreeSQL
        ↓
Consultas SQL
        ↓
Exportação para CSV
        ↓
Tratamento em Python
        ↓
Análise Estatística
        ↓
Visualização dos Dados
        ↓
Base Final Processada
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| **FreeSQL** | Ambiente utilizado para consulta da base HR |
| **SQL** | Extração, relacionamento, filtros e agrupamentos |
| **Python** | Tratamento, análise exploratória e visualização |
| **Pandas** | Manipulação e integração dos dados |
| **NumPy** | Cálculos numéricos e distribuição dos dados |
| **Matplotlib** | Criação dos gráficos |
| **CSV** | Integração entre SQL e Python |

---

## 📁 Estrutura do Projeto

```text
mini_projeto_final/
│
├── sql/
│   ├── query_01.sql
│   └── query_02.sql
│
├── csv_nao_processados/
│   ├── query_01.csv
│   └── query_02_completa.csv
│
├── processados/
│   └── final.csv
│
├── python/
│   └── query_01.py
│
└── README.md
```

---

## 🧩 Etapa 01 — Extração dos Dados com SQL

A primeira etapa do projeto foi realizada no **FreeSQL**, utilizando a base de dados **HR**.

Foram desenvolvidas duas consultas principais:

| Query | Objetivo |
|---|---|
| `query_01.sql` | Analisar a distribuição de salários por departamento e cargo |
| `query_02.sql` | Analisar funcionários por região, país, cidade, departamento e cargo |

---

## 🔗 Relacionamento entre as Tabelas

As consultas foram construídas a partir da tabela principal `HR.EMPLOYEES`, relacionando as demais tabelas por meio de `LEFT JOIN`.

```sql
HR.EMPLOYEES.DEPARTMENT_ID = HR.DEPARTMENTS.DEPARTMENT_ID
HR.EMPLOYEES.JOB_ID        = HR.JOBS.JOB_ID
HR.DEPARTMENTS.LOCATION_ID = HR.LOCATIONS.LOCATION_ID
HR.LOCATIONS.COUNTRY_ID    = HR.COUNTRIES.COUNTRY_ID
HR.COUNTRIES.REGION_ID     = HR.REGIONS.REGION_ID
```

### Tabelas utilizadas

- `HR.EMPLOYEES`
- `HR.DEPARTMENTS`
- `HR.JOBS`
- `HR.LOCATIONS`
- `HR.COUNTRIES`
- `HR.REGIONS`

---

## 📌 Query 01 — Salários por Departamento e Cargo

A `query_01.sql` foi desenvolvida para responder à seguinte pergunta de negócio:

> Como os salários estão distribuídos por departamento e cargo?

A consulta apresenta uma visão consolidada contendo:

- departamento;
- cargo;
- quantidade de funcionários;
- menor salário de referência;
- maior salário de referência.

```sql
SELECT
    d.DEPARTMENT_NAME AS departamento,
    j.JOB_TITLE AS cargo,
    COUNT(e.EMPLOYEE_ID) AS quantidade_funcionarios,
    MIN(j.MIN_SALARY) AS menor_salario,
    MAX(j.MAX_SALARY) AS maior_salario
FROM HR.EMPLOYEES e
LEFT JOIN HR.DEPARTMENTS d
    ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN HR.JOBS j
    ON e.JOB_ID = j.JOB_ID
GROUP BY
    d.DEPARTMENT_NAME,
    j.JOB_TITLE
ORDER BY
    d.DEPARTMENT_NAME,
    j.JOB_TITLE;
```

### 📈 Leitura Gerencial

Essa consulta permite avaliar a distribuição de cargos dentro dos departamentos e observar as faixas salariais previstas para cada função.

A análise pode apoiar decisões relacionadas à estrutura organizacional, concentração de funcionários por área e comparação de faixas salariais entre cargos.

---

## 🌎 Query 02 — Funcionários por Região

A `query_02.sql` foi criada para responder à seguinte pergunta de negócio:

> Como os funcionários estão distribuídos por região, considerando localização, departamento, cargo e salário?

A consulta utiliza uma **CTE** para organizar os dados antes da apresentação final.

```sql
WITH RESULTADO_FUNCIONARIOS AS (
    SELECT
        E.EMPLOYEE_ID AS ID_EMPREGADO,
        E.FIRST_NAME || ' ' || E.LAST_NAME AS NOME_FUNCIONARIO,
        R.REGION_NAME AS REGIAO,
        C.COUNTRY_NAME AS PAIS,
        L.CITY AS CIDADE,
        D.DEPARTMENT_NAME AS DEPARTAMENTO,
        J.JOB_TITLE AS CARGO,
        E.SALARY AS SALARIO
    FROM HR.EMPLOYEES E
    LEFT JOIN HR.DEPARTMENTS D ON E.DEPARTMENT_ID = D.DEPARTMENT_ID
    LEFT JOIN HR.JOBS J        ON E.JOB_ID = J.JOB_ID
    LEFT JOIN HR.LOCATIONS L   ON D.LOCATION_ID = L.LOCATION_ID
    LEFT JOIN HR.COUNTRIES C   ON L.COUNTRY_ID = C.COUNTRY_ID
    LEFT JOIN HR.REGIONS R     ON C.REGION_ID = R.REGION_ID
    WHERE
        E.SALARY > 1000
        AND E.SALARY < 3000
)
SELECT
    ID_EMPREGADO,
    NOME_FUNCIONARIO,
    REGIAO,
    PAIS,
    CIDADE,
    DEPARTAMENTO,
    CARGO,
    SALARIO,
    COUNT(ID_EMPREGADO)
    OVER(PARTITION BY REGIAO, PAIS, CIDADE, DEPARTAMENTO, CARGO) 
    AS QUANTIDADE_FUNCIONARIOS
FROM RESULTADO_FUNCIONARIOS
ORDER BY
    REGIAO,
    PAIS,
    CIDADE,
    DEPARTAMENTO,
    CARGO,
    NOME_FUNCIONARIO;
```

### ⚙️ Recursos Aplicados

- `LEFT JOIN`
- `WHERE`
- `ORDER BY`
- CTE com `WITH`
- Função de janela com `COUNT() OVER(PARTITION BY)`

### 📈 Leitura Gerencial

Essa consulta permite analisar a distribuição dos funcionários por região, país, cidade, departamento e cargo, mantendo o nível individual de cada funcionário.

A função de janela possibilita calcular a quantidade de funcionários por grupo sem perder o detalhamento dos registros.

---

## 📤 Etapa 02 — Exportação dos Resultados para CSV

Após a execução das consultas no FreeSQL, os resultados foram exportados para arquivos CSV.

| Arquivo | Origem | Finalidade |
|---|---|---|
| `query_01.csv` | `query_01.sql` | Complementar a análise salarial |
| `query_02_completa.csv` | `query_02.sql` | Base principal com dados detalhados dos funcionários |

A exportação para CSV foi necessária para permitir a continuidade da análise em Python.

---

## 🐍 Etapa 03 — Tratamento dos Dados em Python

Na etapa em Python, os arquivos CSV foram carregados, tratados e integrados.

Bibliotecas utilizadas:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

Principais processos realizados:

- carregamento dos arquivos CSV;
- inspeção inicial dos dados;
- padronização dos nomes das colunas;
- padronização dos campos `DEPARTAMENTO` e `CARGO`;
- integração das bases;
- tratamento de valores nulos;
- conversão das colunas numéricas;
- análise estatística dos salários;
- identificação de outliers;
- geração de gráficos;
- exportação da base final tratada.

---

## 🧹 Etapa 04 — Padronização e Limpeza dos Dados

Para evitar erros na manipulação e na junção dos datasets, os nomes das colunas foram padronizados.

```python
df1.columns = df1.columns.str.strip().str.upper()
df2.columns = df2.columns.str.strip().str.upper()
```

Também foram padronizadas as colunas utilizadas como chave de relacionamento:

```python
for coluna in ['DEPARTAMENTO', 'CARGO']:
    df1[coluna] = df1[coluna].astype(str).str.strip().str.upper()
    df2[coluna] = df2[coluna].astype(str).str.strip().str.upper()
```

Essa etapa garante maior consistência nos dados e evita problemas causados por espaços, letras minúsculas ou diferenças de escrita.

---

## 🔄 Etapa 05 — Integração das Bases

A base `query_02_completa.csv` foi utilizada como base principal, enquanto a `query_01.csv` foi usada para complementar os dados com as informações de menor e maior salário.

```python
df_final = pd.merge(
    df2,
    df3,
    how='left',
    on=['DEPARTAMENTO', 'CARGO']
)
```

O tipo de junção utilizado foi o **LEFT JOIN**, mantendo todos os registros da base principal e adicionando as informações complementares quando houvesse correspondência entre departamento e cargo.

---

## 🧾 Etapa 06 — Tratamento de Valores Nulos

Os valores ausentes foram tratados de acordo com o tipo da coluna.

| Tipo de coluna | Tratamento |
|---|---|
| Texto | Substituição por `SEM INFORMAÇÃO` |
| Numérica | Mantida como `NaN` para preservar os cálculos |

Essa decisão evita que colunas numéricas sejam convertidas em texto, garantindo que os cálculos estatísticos funcionem corretamente.

---

## 📊 Etapa 07 — Análise Estatística dos Salários

Foram calculadas as principais medidas estatísticas da coluna `SALARIO_ATUAL`.

| Métrica | Objetivo |
|---|---|
| Média | Identificar o salário médio |
| Mediana | Identificar o valor central da distribuição |
| Mínimo | Identificar o menor salário |
| Máximo | Identificar o maior salário |

Essas métricas fornecem uma visão geral da distribuição salarial dos funcionários analisados.

---

## 📉 Etapa 08 — Identificação de Outliers

A análise de outliers foi realizada pelo método **IQR**, conhecido como intervalo interquartil.

```python
Q1 = salarios.quantile(0.25)
Q3 = salarios.quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
```

Foram considerados possíveis outliers os salários abaixo do limite inferior ou acima do limite superior.

Essa etapa é importante para identificar valores que se distanciam do comportamento geral dos dados.

---

## 📊 Etapa 09 — Visualização dos Dados

Foram gerados dois gráficos principais para apoiar a análise exploratória.

### 📦 Boxplot dos Salários

Utilizado para visualizar:

- mediana;
- quartis;
- dispersão dos salários;
- possíveis outliers.

### 📊 Gráfico de Barras da Distribuição Salarial

Utilizado para analisar:

- concentração de funcionários por faixa salarial;
- distribuição dos salários;
- comparação com os limites do IQR.

---

## 💾 Etapa 10 — Exportação da Base Final

Após o tratamento e análise dos dados, foi gerado o arquivo final:

```text
processados/final.csv
```

Esse arquivo contém a base consolidada, tratada e pronta para novas análises, dashboards ou relatórios gerenciais.

---

## ✅ Resultados Obtidos

Ao final do projeto, foram alcançados os seguintes resultados:

- criação de consultas SQL na base HR;
- relacionamento entre múltiplas tabelas;
- exportação dos resultados para CSV;
- integração dos dados em Python;
- padronização e limpeza dos datasets;
- tratamento de valores ausentes;
- análise estatística dos salários;
- identificação de possíveis outliers;
- criação de gráficos exploratórios;
- geração da base final `final.csv`.

---

## 🧠 Aprendizados do Projeto

Este projeto permitiu aplicar, de forma prática, conceitos importantes de análise de dados e Business Intelligence, como:

- extração de dados com SQL;
- relacionamento entre tabelas;
- uso de CTE;
- uso de função de janela;
- preparação de dados para análise;
- limpeza e padronização de datasets;
- análise estatística;
- visualização de dados;
- construção de base final para suporte à decisão.

---

## 🏁 Conclusão

O mini projeto demonstrou um fluxo completo de análise de dados, iniciando pela extração das informações no FreeSQL e avançando para o tratamento, integração e análise exploratória em Python.

A etapa SQL permitiu estruturar os dados da base HR, relacionando funcionários, departamentos, cargos, localizações, países e regiões.

A etapa em Python possibilitou consolidar os arquivos CSV, padronizar os dados, tratar valores ausentes, calcular indicadores estatísticos e gerar gráficos para facilitar a interpretação dos salários.

O resultado final foi a criação de uma base consolidada chamada `final.csv`, pronta para ser utilizada em novas análises, dashboards e relatórios de Business Intelligence.
